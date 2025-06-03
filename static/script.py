import requests
import platform
import json

data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "os": platform.system(),
    "os_version": platform.version(),
    "ram_gb": 8,
    "disk_serials": "ABC123",
    "ram_serials": "0000",
    "system_info": "Dell Inspiron 15"
}

try:
    response = requests.post("http://127.0.0.1:8000/owner/data/api/", json=data)
    print(response.status_code, response.text[:5000])
except Exception as e:
    print("Error submitting data:", str(e))
