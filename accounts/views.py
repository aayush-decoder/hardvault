from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from .models import User, Owner, Client, OTP
import json


# ==================== OWNER VIEWS ====================

def owner_register(request):
    """Owner registration page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        phone = request.POST.get('phone')
        
        # Check if user exists
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/owner_register.html', {'error': 'Email already registered'})
        
        # Generate and send OTP
        otp = OTP.objects.create(email=email, otp_type='registration')
        send_otp_email(email, otp.otp_code, 'registration')
        
        # Store data in session
        request.session['registration_data'] = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'company_name': company_name,
            'phone': phone,
            'user_type': 'owner'
        }
        
        return redirect('verify-otp')
    
    return render(request, 'accounts/owner_register.html')


def client_register(request):
    """Client registration page"""
    invitation_code = request.GET.get('invite')
    selected_owner = None
    
    if invitation_code:
        try:
            selected_owner = Owner.objects.get(invitation_code=invitation_code)
        except Owner.DoesNotExist:
            pass
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        owner_ids = request.POST.getlist('owners')
        
        # Debug: Print owner_ids
        print(f"DEBUG: Received owner_ids: {owner_ids}, type: {type(owner_ids)}")
        
        # Check if user exists
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/client_register.html', {
                'error': 'Email already registered',
                'owners': Owner.objects.all(),
                'selected_owner': selected_owner
            })
        
        # Generate and send OTP
        otp = OTP.objects.create(email=email, otp_type='registration')
        send_otp_email(email, otp.otp_code, 'registration')
        
        # Store data in session
        request.session['registration_data'] = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'owner_ids': owner_ids,
            'user_type': 'client'
        }
        
        return redirect('verify-otp')
    
    owners = Owner.objects.all()
    return render(request, 'accounts/client_register.html', {
        'owners': owners,
        'selected_owner': selected_owner
    })


def verify_otp(request):
    """OTP verification page"""
    if 'registration_data' not in request.session:
        return redirect('client-register')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        reg_data = request.session['registration_data']
        email = reg_data['email']
        
        # Verify OTP
        try:
            otp = OTP.objects.get(
                email=email,
                otp_code=otp_code,
                otp_type='registration',
                is_verified=False
            )
            
            if not otp.is_valid():
                return render(request, 'accounts/verify_otp.html', {
                    'error': 'OTP expired. Please register again.',
                    'email': email
                })
            
            # Mark OTP as verified
            otp.is_verified = True
            otp.save()
            
            # Create user
            user = User.objects.create_user(
                username=email.split('@')[0] + str(User.objects.count()),
                email=email,
                password=reg_data['password'],
                first_name=reg_data['first_name'],
                last_name=reg_data['last_name'],
                phone=reg_data.get('phone'),
                user_type=reg_data['user_type']
            )
            
            # Create profile based on user type
            if reg_data['user_type'] == 'owner':
                Owner.objects.create(
                    user=user,
                    company_name=reg_data['company_name']
                )
            else:  # client
                client = Client.objects.create(user=user)
                if reg_data.get('owner_ids'):
                    # Debug
                    print(f"DEBUG verify_otp: owner_ids from session: {reg_data['owner_ids']}")
                    
                    # Convert string IDs to integers
                    owner_ids = []
                    for oid in reg_data['owner_ids']:
                        if isinstance(oid, str) and oid.strip().isdigit():
                            owner_ids.append(int(oid.strip()))
                        elif isinstance(oid, int):
                            owner_ids.append(oid)
                    
                    print(f"DEBUG verify_otp: Converted owner_ids: {owner_ids}")
                    
                    if owner_ids:
                        owners = Owner.objects.filter(id__in=owner_ids)
                        print(f"DEBUG verify_otp: Found {owners.count()} owners")
                        client.owners.set(owners)
                        print(f"DEBUG verify_otp: Client now has {client.owners.count()} owners")
            
            # Clear session
            del request.session['registration_data']
            
            # Login user
            login(request, user)
            
            # Redirect based on user type
            if user.user_type == 'owner':
                return redirect('owner-dashboard')
            else:
                return redirect('client-dashboard')
        
        except OTP.DoesNotExist:
            return render(request, 'accounts/verify_otp.html', {
                'error': 'Invalid OTP',
                'email': email
            })
    
    email = request.session['registration_data']['email']
    return render(request, 'accounts/verify_otp.html', {'email': email})


def user_login(request):
    """Login page for both owners and clients"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user type
            if user.user_type == 'owner':
                return redirect('owner-dashboard')
            else:
                return redirect('client-dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid email or password'
            })
    
    return render(request, 'accounts/login.html')


def user_logout(request):
    """Logout user"""
    logout(request)
    return redirect('login')


def forgot_password(request):
    """Forgot password - send OTP"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate and send OTP
            otp = OTP.objects.create(email=email, otp_type='password_reset', user=user)
            send_otp_email(email, otp.otp_code, 'password_reset')
            
            request.session['reset_email'] = email
            return redirect('verify-reset-otp')
        
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {
                'error': 'Email not found'
            })
    
    return render(request, 'accounts/forgot_password.html')


def verify_reset_otp(request):
    """Verify OTP for password reset"""
    if 'reset_email' not in request.session:
        return redirect('forgot-password')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        email = request.session['reset_email']
        
        try:
            otp = OTP.objects.get(
                email=email,
                otp_code=otp_code,
                otp_type='password_reset',
                is_verified=False
            )
            
            if not otp.is_valid():
                return render(request, 'accounts/verify_reset_otp.html', {
                    'error': 'OTP expired. Please try again.',
                    'email': email
                })
            
            # Mark OTP as verified
            otp.is_verified = True
            otp.save()
            
            return redirect('reset-password')
        
        except OTP.DoesNotExist:
            return render(request, 'accounts/verify_reset_otp.html', {
                'error': 'Invalid OTP',
                'email': email
            })
    
    email = request.session['reset_email']
    return render(request, 'accounts/verify_reset_otp.html', {'email': email})


def reset_password(request):
    """Reset password after OTP verification"""
    if 'reset_email' not in request.session:
        return redirect('forgot-password')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            return render(request, 'accounts/reset_password.html', {
                'error': 'Passwords do not match'
            })
        
        email = request.session['reset_email']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        
        del request.session['reset_email']
        
        return render(request, 'accounts/reset_password.html', {
            'success': True
        })
    
    return render(request, 'accounts/reset_password.html')


# ==================== DASHBOARD VIEWS ====================

@login_required
def owner_dashboard(request):
    """Owner dashboard"""
    if request.user.user_type != 'owner':
        return redirect('client-dashboard')
    
    owner = request.user.owner_profile
    clients = owner.clients.all()
    
    # Get hardware records for owner's clients
    from owner.models import HardwareRecord
    client_emails = [client.user.email for client in clients]
    hardware_records = HardwareRecord.objects.filter(client_email__in=client_emails)

    emails = list(hardware_records.values_list("client_email", flat=True))
    
    return render(request, "accounts/owner_dashboard.html", {
    "owner": owner,
    "clients": clients,
    "hardware_records": hardware_records,
    "emails": emails,
})



@login_required
def client_dashboard(request):
    """Client dashboard"""
    if request.user.user_type != 'client':
        return redirect('owner-dashboard')
    
    client = request.user.client_profile
    
    # Get hardware records for this client
    from owner.models import HardwareRecord
    hardware_records = HardwareRecord.objects.filter(client_email=request.user.email)
    
    return render(request, 'accounts/client_dashboard.html', {
        'client': client,
        'hardware_records': hardware_records
    })


# ==================== API VIEWS ====================

def search_owners(request):
    """API to search owners by name or company"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'owners': []})
    
    owners = Owner.objects.filter(
        Q(company_name__icontains=query) | 
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query)
    )[:10]
    
    results = [{
        'id': owner.id,
        'company_name': owner.company_name,
        'owner_name': owner.user.get_full_name()
    } for owner in owners]
    
    return JsonResponse({'owners': results})


def resend_otp(request):
    """Resend OTP"""
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        otp_type = data.get('otp_type', 'registration')
        
        # Invalidate old OTPs
        OTP.objects.filter(email=email, otp_type=otp_type, is_verified=False).update(is_verified=True)
        
        # Create new OTP
        otp = OTP.objects.create(email=email, otp_type=otp_type)
        send_otp_email(email, otp.otp_code, otp_type)
        
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ==================== HELPER FUNCTIONS ====================

def send_otp_email(email, otp_code, otp_type):
    """Send OTP via email with HTML template using smtplib"""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    if otp_type == 'registration':
        subject = '🔒 Your HardVault Registration Code'
        title = 'Welcome to HardVault!'
        message = 'Thank you for registering. Use the code below to verify your account.'
    else:
        subject = '🔑 Your HardVault Password Reset Code'
        title = 'Password Reset Request'
        message = 'You requested to reset your password. Use the code below to continue.'
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = email
    
    # Plain text version
    text_content = f'{title}\n\n{message}\n\nYour OTP: {otp_code}\n\nThis code will expire in 10 minutes.\n\nIf you didn\'t request this, please ignore this email.'
    
    # HTML version with green/orange theme
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 50%, #fff3e0 100%); padding: 40px 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 40px rgba(76, 175, 80, 0.2);">
            <div style="background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); padding: 40px 30px; text-align: center;">
                <h1 style="margin: 0; color: white; font-size: 32px;">🔒 HardVault</h1>
                <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">{title}</p>
            </div>
            <div style="padding: 40px 30px;">
                <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">{message}</p>
                <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border: 3px solid #4caf50; padding: 30px; border-radius: 15px; text-align: center; margin: 30px 0;">
                    <p style="margin: 0 0 10px 0; color: #2e7d32; font-size: 14px; font-weight: 600; text-transform: uppercase;">Your Verification Code</p>
                    <div style="font-size: 48px; font-weight: bold; color: #1b5e20; letter-spacing: 8px; font-family: 'Courier New', monospace; margin: 10px 0;">{otp_code}</div>
                    <p style="margin: 10px 0 0 0; color: #2e7d32; font-size: 13px;">⏰ Expires in 10 minutes</p>
                </div>
                <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; border-radius: 5px; margin: 30px 0;">
                    <p style="margin: 0; color: #e65100; font-size: 14px;"><strong>⚠️ Security Notice:</strong> If you didn't request this code, please ignore this email. Your account is safe.</p>
                </div>
            </div>
            <div style="background: #f8fdf8; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                <p style="margin: 0 0 10px 0; color: #546e7a; font-size: 14px;">This email was sent by HardVault</p>
                <p style="margin: 0; color: #90a4ae; font-size: 12px;">Secure Hardware Information Management</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Attach parts
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    msg.attach(part1)
    msg.attach(part2)
    
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✓ Email sent successfully to {email}")
    except Exception as e:
        print(f"✗ Error sending email: {e}")
