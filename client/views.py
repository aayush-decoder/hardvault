from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.http import FileResponse
import os
from django.conf import settings



# Create your views here.
def login(request):
    return HttpResponse("client side")

def form(request):
    return render(request, "client/form.html", {'request': request})

def download_file(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        email = request.GET.get('email')
        phone = request.GET.get('phone')

        personalise_script()
        
        return prepare_exe_file()


    return HttpResponse("LOL")





def personalise_script():
    static_path = os.path.join(settings.BASE_DIR, 'static', 'script4.py')
    output_path = os.path.join(settings.MEDIA_ROOT, 'downloads', 'fscript.py')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(static_path, 'r', encoding='utf-8') as f:
            content = f.read()

        updated_content = content.replace("Dummy", "Aayush")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return f"File saved at: {output_path}"

    except Exception as e:
        return f"Error: {str(e)}"




def prepare_exe_file():
    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', 'fscript.py')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='fscript.py')
