from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from .models import User, Owner, OTP
import json


# ==================== OWNER VIEWS ====================

def owner_register(request):
    """Owner registration - requires admin approval"""
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
        
        # Create user (not approved yet)
        user = User.objects.create_user(
            username=email.split('@')[0] + str(User.objects.count()),
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_type='owner',
            is_approved=False,
            is_active=False  # Cannot login until approved
        )
        
        # Create owner profile
        Owner.objects.create(
            user=user,
            company_name=company_name
        )
        
        return render(request, 'accounts/owner_register_success.html', {
            'company_name': company_name
        })
    
    return render(request, 'accounts/owner_register.html')


# Client accounts removed - hardware form is public


def user_login(request):
    """Login page for owners and admins only"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Check if owner is approved
            if user.user_type == 'owner' and not user.is_approved:
                return render(request, 'accounts/login.html', {
                    'error': 'Your account is pending admin approval. Please wait for approval.'
                })
            
            login(request, user)
            
            # Redirect based on user type
            if user.user_type == 'admin':
                return redirect('/admin/')
            else:  # owner
                return redirect('owner-dashboard')
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
        return redirect('/admin/')
    
    owner = request.user.owner_profile
    
    # Get hardware records for this owner by company name
    from owner.models import HardwareRecord
    hardware_records = HardwareRecord.objects.filter(owner_name=owner.company_name)
    
    return render(request, "accounts/owner_dashboard.html", {
        "owner": owner,
        "hardware_records": hardware_records,
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
    """Send OTP via email - configure email backend in settings"""
    if otp_type == 'registration':
        subject = 'Your HardVault Registration Code'
        message = f'Your OTP code is: {otp_code}\n\nThis code will expire in 10 minutes.'
    else:
        subject = 'Your HardVault Password Reset Code'
        message = f'Your password reset code is: {otp_code}\n\nThis code will expire in 10 minutes.'
    
    try:
        # Use Django's email backend (configure in settings.py)
        from django.core.mail import send_mail
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print(f"✓ Email sent successfully to {email}")
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        # In development, print OTP to console
        print(f"OTP for {email}: {otp_code}")
