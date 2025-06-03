from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
from .models import HardwareRecord


# Create your views here.
def login(request):
    return HttpResponse('owner side')


@csrf_exempt 
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Example fields expected from .exe script
            # nname = data.get('name')
            # email = data.get('email')
            # phone = data.get('phone')
            # os_info = data.get('os')
            # ram_gb = data.get('ram_gb')
            # disk_serials = data.get('disk_serials')
            # ram_serials = data.get('ram_serials')
            # system_info = data.get('system_info')

            print(save_hardware_data(data))

            print("Received data:", data) 

            return JsonResponse({"status": "success", "message": "Data received."}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)









@csrf_exempt
def save_hardware_data(data):
    try:

        record = HardwareRecord.objects.create(
            client_name = data.get('client_name'),
            client_email = data.get('client_email'),
            client_phone = data.get('client_phone'),
            owner_name = data.get('owner_name'),
            product_id = data.get('device_product_id'),
            model_name = data.get('device_model_name'),
            ram_serial = data.get('ram_serial'),
            ram_manufacturer = data.get('ram_manufacturer'),
            ram_part_number = data.get('ram_part_number'),
            disk_model = data.get('disk_model'),
            disk_interface_type = data.get('disk_interface_type'),
            disk_serial = data.get('disk_serial'),
        )
        print("success")
        return JsonResponse({"message": "Hardware info saved successfully"}, status=201)
    except Exception as e:
        print("error: ", e)
        return JsonResponse({"error": str(e)}, status=400)
