# Quick Reference Guide

## Code Generation Formula
```python
client_code = email[:3].upper() + random(6_alphanumeric_chars)
# Example: john@example.com → JOH4K7M2P
```

## Database Fields

### Created at Registration
- `client_name`
- `client_email`
- `client_phone`
- `owner_name`
- `client_code` (auto-generated)

### Filled by Exe
- `product_id`
- `model_name`
- `ram_serial`
- `ram_manufacturer`
- `ram_part_number`
- `disk_model`
- `disk_interface_type`
- `disk_serial`

## API Quick Reference

### Submit Registration
```
GET /client/form/download?name=John&email=john@example.com&phone=123456&owner_name=Shop
→ Returns HTML page with code and download link
```

### Download Exe
```
GET /client/form/download-exe
→ Returns hardware_collector.exe file
```

### Submit Hardware Data (from exe)
```
POST /owner/data/api/
Content-Type: application/json

{
    "client_code": "JOH4K7M2P",
    "device_product_id": "ABC123",
    "device_model_name": "Dell Inspiron",
    "ram_serial": "12345",
    "ram_manufacturer": "Samsung",
    "ram_part_number": "M471A",
    "disk_model": "Samsung SSD",
    "disk_interface_type": "SATA",
    "disk_serial": "S3Z9NX"
}

→ Returns {"status": "success", "message": "Hardware data updated successfully."}
```

### Retrieve Client Data
```
GET /client/data/api?name=John%20Doe&email=john@example.com
→ Returns complete client and hardware data as JSON
```

## File Locations

```
client/views.py              # Client-facing logic
owner/views.py               # Data receiving logic
owner/models.py              # HardwareRecord model
client/urls.py               # URL routing
static/script_general.py     # Exe source code
templates/client/form.html   # Registration form
templates/client/download.html  # Code display page
media/downloads/hardware_collector.exe  # Pre-built exe
```

## Common Commands

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Build General Exe
```bash
pyinstaller --name hardware_collector --onefile --distpath media/downloads static/script_general.py
```

### Run Development Server
```bash
python manage.py runserver
```

### Access Admin Panel
```
http://127.0.0.1:8000/admin/
```

## Django Shell Snippets

### View All Records
```python
from owner.models import HardwareRecord
HardwareRecord.objects.all()
```

### Find Record by Code
```python
record = HardwareRecord.objects.get(client_code="JOH4K7M2P")
```

### Find Incomplete Records
```python
incomplete = HardwareRecord.objects.filter(product_id__isnull=True)
```

### Generate New Code
```python
import random, string
email = "test@example.com"
code = email[:3].upper() + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Client code is required" | Missing code in POST data | Ensure exe sends client_code |
| "Invalid client code" | Code not in database | Verify registration completed |
| "This email is already registered" | Duplicate email | Use different email |
| "Exe file not found" | General exe not built | Build manually or submit one form |

## Testing Checklist

- [ ] Registration form loads
- [ ] Form submission creates DB record
- [ ] Code is displayed after submission
- [ ] Download link works
- [ ] Exe file downloads
- [ ] Exe prompts for code
- [ ] Exe collects hardware data
- [ ] Data is sent to server
- [ ] DB record is updated
- [ ] Data API returns complete info

## Security Notes

⚠️ **CSRF Exempt:** `/owner/data/api/` uses @csrf_exempt for exe compatibility  
⚠️ **No Authentication:** API endpoints are open (add auth in production)  
⚠️ **Code Not Secret:** Codes are identifiers, not security tokens  
⚠️ **HTTPS Required:** Use HTTPS in production for data security  

## Performance Tips

- Pre-build the general exe (don't rely on auto-build)
- Use database indexing on `client_code` and `client_email`
- Implement caching for frequently accessed data
- Add rate limiting to prevent abuse
- Monitor for failed submissions

## Backup Strategy

1. **Database:** Regular automated backups
2. **Exe File:** Keep in version control or backup storage
3. **Client Codes:** Export periodically to CSV
4. **Configuration:** Keep settings in version control

## Monitoring Points

- Registration success rate
- Hardware submission success rate
- Average time between registration and submission
- Failed API calls
- Duplicate email attempts
- Incomplete records (no hardware data)
