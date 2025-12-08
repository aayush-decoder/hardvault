# User Guide - Hardware Collection System

## For Clients (End Users)

### How to Submit Your Hardware Information

#### Step 1: Register Your Information
1. Visit the registration form (provided by your shop owner)
2. Fill in the required information:
   - Your full name
   - Your email address
   - Your phone number
   - Shop owner's name (optional)
3. Click "Submit"

#### Step 2: Save Your Code
After submitting the form, you'll see a page with:
- **Your unique client code** (example: `JOH4K7M2P`)
- A download button for the hardware collector program

**IMPORTANT:** Write down or save your client code! You'll need it in the next step.

#### Step 3: Download the Program
1. Click the "Download Hardware Collector" button
2. Save the file to your computer
3. The file will be named `hardware_collector.exe`

#### Step 4: Run the Program
1. Double-click the downloaded `hardware_collector.exe` file
2. When prompted, enter your client code (from Step 2)
3. Press Enter
4. Wait for the program to collect your hardware information
5. You'll see a success message when complete

#### Step 5: Verify Your Information
1. Visit the data verification link (provided by your shop owner)
2. Enter your name and email
3. View your submitted hardware information

### What Information is Collected?

The program collects the following hardware information:
- Computer model and product ID
- RAM serial number, manufacturer, and part number
- Hard disk model, interface type, and serial number

**Privacy Note:** Only hardware information is collected. No personal files, browsing history, or passwords are accessed.

### Troubleshooting

#### "Client code is required" error
- Make sure you entered your code correctly
- Codes are case-sensitive
- Check for extra spaces

#### "Invalid client code" error
- Verify you're using the correct code from the registration page
- Make sure you completed the registration form first

#### "Error submitting data" message
- Check your internet connection
- Make sure the server is running
- Contact your shop owner for assistance

#### Can't find my code
- Currently, you need to save your code from the registration page
- Future versions will allow code retrieval via email
- Contact your shop owner if you lost your code

---

## For Shop Owners

### Setting Up the System

#### Initial Setup
1. Ensure Django project is running
2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Build the general exe (optional - will auto-build on first use):
   ```bash
   pyinstaller --name hardware_collector --onefile --distpath media/downloads static/script_general.py
   ```

#### Providing Access to Clients
1. Share the registration form URL: `http://yourserver.com/client/form/`
2. Instruct clients to follow the registration process
3. Provide support for any issues

### Managing Client Records

#### Viewing Records
Access the Django admin panel:
```
http://yourserver.com/admin/
```

Filter and search by:
- Client name
- Client email
- Client code
- Hardware details

#### Exporting Data
Use Django admin's export functionality or create custom views to export client hardware data.

### API Usage

#### Get Client Data
```bash
curl "http://yourserver.com/client/data/api?name=John%20Doe&email=john@example.com"
```

Response:
```json
{
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "client_phone": "1234567890",
    "owner_name": "Shop Owner",
    "product_id": "ABC123",
    "model_name": "Dell Inspiron",
    "ram_serial": "12345",
    "ram_manufacturer": "Samsung",
    "ram_part_number": "M471A",
    "disk_model": "Samsung SSD",
    "disk_interface_type": "SATA",
    "disk_serial": "S3Z9NX"
}
```

### Best Practices

1. **Code Management:**
   - Advise clients to save their codes immediately
   - Consider implementing email notifications with codes
   - Keep a backup of client codes

2. **Security:**
   - Use HTTPS in production
   - Implement rate limiting on API endpoints
   - Regular database backups

3. **Support:**
   - Provide clear instructions to clients
   - Have a support channel for issues
   - Monitor for failed submissions

4. **Maintenance:**
   - Regularly check for incomplete records (missing hardware data)
   - Follow up with clients who haven't submitted hardware info
   - Keep the exe file updated if you modify the script

### Common Administrative Tasks

#### Finding Clients Without Hardware Data
```python
from owner.models import HardwareRecord

incomplete = HardwareRecord.objects.filter(product_id__isnull=True)
for record in incomplete:
    print(f"{record.client_name} ({record.client_code}) - No hardware data")
```

#### Regenerating a Client Code
```python
from owner.models import HardwareRecord
import random
import string

def regenerate_code(email):
    record = HardwareRecord.objects.get(client_email=email)
    prefix = email[:3].upper()
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    record.client_code = prefix + random_part
    record.save()
    return record.client_code
```

#### Bulk Export to CSV
```python
import csv
from owner.models import HardwareRecord

with open('hardware_records.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Email', 'Phone', 'Code', 'Model', 'Product ID'])
    
    for record in HardwareRecord.objects.all():
        writer.writerow([
            record.client_name,
            record.client_email,
            record.client_phone,
            record.client_code,
            record.model_name,
            record.product_id
        ])
```

### Customization

#### Changing Code Format
Edit `client/views.py`:
```python
def generate_client_code(email):
    # Current: [3 chars email][6 random]
    # Example custom: [4 chars email][8 random]
    prefix = email[:4].upper()
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return prefix + random_part
```

#### Customizing the Download Page
Edit `templates/client/download.html` to match your branding.

#### Adding Email Notifications
Install django email backend and add to `client/views.py`:
```python
from django.core.mail import send_mail

# After creating record:
send_mail(
    'Your Hardware Collection Code',
    f'Your code is: {client_code}',
    'from@example.com',
    [email],
    fail_silently=False,
)
```

### Monitoring and Analytics

Track important metrics:
- Total registrations
- Completion rate (registered vs hardware submitted)
- Average time between registration and submission
- Most common hardware configurations

### Support Contact

For technical issues or questions about the system, contact your system administrator or refer to the technical documentation in `docs/SYSTEM_ARCHITECTURE.md`.
