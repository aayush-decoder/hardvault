from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.http import FileResponse
import os
from django.conf import settings
import subprocess
import shutil

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



def download_file(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        email = request.GET.get('email')
        phone = request.GET.get('phone')

        exists = HardwareRecord.objects.filter(client_email=email).exists()

        if exists:
            return render(request, "client/form.html", {'request': request, 'duplicate_email': True})

        users_data = {
            "name": name,
            "email": email,
            "phone": phone
        }

        
        return prepare_exe_file(users_data)


    return HttpResponse("LOL")





def personalise_script(users_data):
    static_path = os.path.join(settings.BASE_DIR, 'static', 'script4.py')
    output_path = os.path.join(settings.MEDIA_ROOT, 'downloads', 'fscript.py')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(static_path, 'r', encoding='utf-8') as f:
            content = f.read()

        updated_content = content.replace("$NAME", users_data["name"])
        updated_content = updated_content.replace("$EMAIL", users_data["email"])
        updated_content = updated_content.replace("$PHONE", users_data["phone"])
        updated_content = updated_content.replace("$OWNER_NAME", "Shop Owner's name")
        print("userss data ", users_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return output_path

    except Exception as e:
        return f"Error: {str(e)}"






def build_exe(users_data):
    script_path = personalise_script(users_data)
    output_dir = os.path.join(settings.MEDIA_ROOT, 'downloads', 'dist')
    os.makedirs(output_dir, exist_ok=True)

    # Run PyInstaller to build the executable
    subprocess.run([
        'pyinstaller',
        '--name', 'script',
        '--onefile',
        '--distpath', output_dir,
        '--workpath', os.path.join(output_dir, 'build'),
        '--specpath', os.path.join(output_dir, 'spec'),
        script_path
    ], check=True)

    # Clean up the extra build files
    shutil.rmtree(os.path.join(output_dir, 'build'), ignore_errors=True)
    shutil.rmtree(os.path.join(output_dir, 'spec'), ignore_errors=True)
    build_name = 'script.exe'

    return os.path.join(output_dir, build_name)





def prepare_exe_file(users_data):
    # file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', 'script.exe')
    file_path = build_exe(users_data)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='script.exe')
