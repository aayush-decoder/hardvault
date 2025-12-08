# Migration Guide - Old System to New Code-Based System

## Overview
This guide helps you migrate from the personalized exe system to the new code-based system.

## Database Migration Required

### Step 1: Add client_code field to existing model

Run these Django commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Update existing records (if any)

If you have existing records without client codes, run this script:

```python
# migration_script.py
from owner.models import HardwareRecord
import random
import string

def generate_code(email):
    prefix = email[:3].upper()
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return prefix + random_part

# Update all existing records
for record in HardwareRecord.objects.filter(client_code__isnull=True):
    record.client_code = generate_code(record.client_email)
    record.save()
    print(f"Updated {record.client_email} with code {record.client_code}")
```

Run it:
```bash
python manage.py shell < migration_script.py
```

## Code Changes Summary

### 1. Models (owner/models.py)
**Added:**
- `client_code` field (CharField, unique=True)

**Modified:**
- `product_id` and `model_name` now allow blank=True, null=True

### 2. Views (client/views.py)
**Removed:**
- `personalise_script()` function
- `build_exe()` function (old version)

**Added:**
- `generate_client_code()` function
- `build_general_exe()` function
- `download_exe()` function

**Modified:**
- `download_file()` now creates DB record and generates code
- `prepare_exe_file()` now shows code page instead of building exe

### 3. Views (owner/views.py)
**Modified:**
- `receive_data()` now expects `client_code` instead of client details
- Updates existing record instead of creating new one

### 4. URLs (client/urls.py)
**Added:**
- `/client/form/download-exe` endpoint for exe download

### 5. Static Files
**Added:**
- `static/script_general.py` - New general exe source

**Deprecated:**
- `static/script4.py` - Old personalized script (keep for reference)

### 6. Templates
**Added:**
- `templates/client/download.html` - Code display page

**Modified:**
- `templates/client/form.html` - Added owner_name field

## Testing the Migration

### Test 1: New Registration
1. Visit `/client/form/`
2. Fill in name, email, phone, owner name
3. Submit form
4. Verify:
   - Code is displayed
   - Download link works
   - Database record created with code

### Test 2: Hardware Collection
1. Download the exe file
2. Run it
3. Enter the code from Test 1
4. Verify:
   - Hardware data collected
   - Data sent to server
   - Database record updated

### Test 3: Data Retrieval
1. Visit `/client/data/api?name=TestName&email=test@example.com`
2. Verify:
   - Returns complete record
   - Includes hardware data

## Building the General Exe

### Option 1: Manual Build
```bash
# Navigate to project root
cd /path/to/project

# Build the exe
pyinstaller --name hardware_collector --onefile --distpath media/downloads static/script_general.py

# Clean up build files
rmdir /s /q build
rmdir /s /q __pycache__
del hardware_collector.spec
```

### Option 2: Automatic Build
The system will automatically build the exe on first form submission if it doesn't exist.

## Rollback Plan

If you need to rollback to the old system:

1. **Restore old views.py files:**
   ```bash
   git checkout HEAD~1 client/views.py owner/views.py
   ```

2. **Keep the client_code field** (it won't hurt anything)

3. **Restore old URLs:**
   ```bash
   git checkout HEAD~1 client/urls.py
   ```

4. **Use old script:**
   - Rename `script4.py` back to active use

## Common Issues

### Issue 1: "Client code is required" error
**Cause:** Exe is sending old format data  
**Solution:** Rebuild exe from `script_general.py`

### Issue 2: "Invalid client code" error
**Cause:** Code doesn't exist in database  
**Solution:** Verify code was created during registration

### Issue 3: Duplicate email error
**Cause:** Email already registered  
**Solution:** This is expected behavior, use different email

### Issue 4: Exe file not found
**Cause:** General exe not built yet  
**Solution:** Submit one form to trigger automatic build, or build manually

## Performance Considerations

### Old System:
- Built new exe for each user (~30 seconds per user)
- Large storage requirement (multiple exe files)
- PyInstaller overhead per request

### New System:
- One-time exe build
- Instant response after first build
- Minimal storage requirement
- Much faster user experience

## Security Notes

1. **Client codes are not secrets** - They're identifiers, not authentication tokens
2. **API is still open** - Consider adding authentication in production
3. **No code expiration** - Codes remain valid indefinitely
4. **No rate limiting** - Add if abuse is a concern

## Next Steps

After migration:

1. Test thoroughly with real users
2. Monitor for any issues
3. Consider implementing code retrieval system
4. Add email notifications for codes
5. Implement owner dashboard to view submissions
