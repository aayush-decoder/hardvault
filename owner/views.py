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
            
            # Get the client code from the data
            client_code = data.get('client_code')
            
            if not client_code:
                return JsonResponse({"status": "error", "message": "Client code is required."}, status=400)
            
            # Find the record by client_code and update it
            try:
                record = HardwareRecord.objects.get(client_code=client_code)
                
                # Update hardware fields
                record.product_id = data.get('device_product_id')
                record.model_name = data.get('device_model_name')
                record.ram_serial = data.get('ram_serial')
                record.ram_manufacturer = data.get('ram_manufacturer')
                record.ram_part_number = data.get('ram_part_number')
                record.disk_model = data.get('disk_model')
                record.disk_interface_type = data.get('disk_interface_type')
                record.disk_serial = data.get('disk_serial')
                
                record.save()
                
                print("Hardware data updated successfully for code:", client_code)
                return JsonResponse({"status": "success", "message": "Hardware data updated successfully."}, status=200)
                
            except HardwareRecord.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Invalid client code."}, status=404)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
