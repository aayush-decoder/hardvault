from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.http import FileResponse
import os
from django.conf import settings
import subprocess
import shutil
import random
import string

from owner.models import HardwareRecord




# Create your views here.
def login(request):
    return HttpResponse("client side")

def form(request):
    return render(request, "client/form.html", {'request': request})



def fetch_data(request):
    if request.method == "GET":
        name = request.GET.get('name')
        email = request.GET.get('email')

        try:
            record = HardwareRecord.objects.get(client_name=name, client_email=email)

            data = {
                "client_name": record.client_name,
                "client_email": record.client_email,
                "client_phone": record.client_phone,

                "owner_name": record.owner_name,

                "product_id": record.product_id,
                "model_name": record.model_name,

                "ram_serial": record.ram_serial,
                "ram_manufacturer": record.ram_manufacturer,
                "ram_part_number": record.ram_part_number,

                "disk_model": record.disk_model,
                "disk_interface_type": record.disk_interface_type,
                "disk_serial": record.disk_serial,
            }

            return JsonResponse(data)
        except HardwareRecord.DoesNotExist:
            return JsonResponse({"error": "No matching client found."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=400)



def generate_client_code(email):
    """Generate a unique code: first 3 chars of email + 6 random alphanumeric chars"""
    prefix = email[:3].upper()
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return prefix + random_part


def download_file(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        email = request.GET.get('email')
        phone = request.GET.get('phone')
        owner_name = request.GET.get('owner_name', 'Shop Owner')  # Default owner name

        exists = HardwareRecord.objects.filter(client_email=email).exists()

        if exists:
            return render(request, "client/form.html", {'request': request, 'duplicate_email': True})

        # Generate unique code
        client_code = generate_client_code(email)

        # Create record in database with empty hardware fields
        HardwareRecord.objects.create(
            client_name=name,
            client_email=email,
            client_phone=phone,
            owner_name=owner_name,
            client_code=client_code
        )

        # Prepare the general exe file and show code to user
        return prepare_exe_file(request, client_code)

    return HttpResponse("LOL")





def prepare_exe_file(request, client_code):
    """Serve the pre-built general exe file and display the code to user"""
    # Path to the general exe file (should be pre-built and stored)
    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', 'hardware_collector.exe')
    
    # Check if general exe exists, if not, we need to build it once
    if not os.path.exists(file_path):
        # Build the general exe once (without personalization)
        file_path = build_general_exe()
    
    # Render a page showing the code and download link
    return render(request, 'client/download.html', {
        'client_code': client_code,
        'download_url': '/client/form/download-exe'
    })


def build_general_exe():
    """Build the general exe file once (without user-specific data)"""
    static_path = os.path.join(settings.BASE_DIR, 'static', 'script_general.py')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
    os.makedirs(output_dir, exist_ok=True)

    # Run PyInstaller to build the executable
    subprocess.run([
        'pyinstaller',
        '--name', 'hardware_collector',
        '--onefile',
        '--distpath', output_dir,
        '--workpath', os.path.join(output_dir, 'build'),
        '--specpath', os.path.join(output_dir, 'spec'),
        static_path
    ], check=True)

    # Clean up the extra build files
    shutil.rmtree(os.path.join(output_dir, 'build'), ignore_errors=True)
    shutil.rmtree(os.path.join(output_dir, 'spec'), ignore_errors=True)

    return os.path.join(output_dir, 'hardware_collector.exe')


def download_exe(request):
    """Endpoint to actually download the exe file"""
    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', 'hardware_collector.exe')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='hardware_collector.exe')
    return HttpResponse("Exe file not found", status=404)
