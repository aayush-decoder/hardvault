# Hardware Collection System - Architecture Documentation

## Overview
This system allows shop owners to collect hardware information from their clients' computers using a general-purpose executable file and a unique client code system.

## System Flow

### 1. Client Registration Flow
```
User fills form → System generates code → Record created in DB → User gets code + exe download
```

**Steps:**
1. Client visits `/client/form/` and fills out:
   - Name
   - Email
   - Phone
   - Owner Name (optional, defaults to "Shop Owner")

2. System validates email is not duplicate

3. System generates unique client code:
   - Format: `[First 3 chars of email][6 random alphanumeric chars]`
   - Example: For email "john@example.com" → `JOH4K7M2P`

4. Database record created with:
   - Client information (name, email, phone)
   - Owner name
   - Client code (unique identifier)
   - Empty hardware fields (to be filled later)

5. User is shown:
   - Their unique client code (prominently displayed)
   - Download button for the general exe file
   - Instructions on how to use the program

### 2. Hardware Collection Flow
```
User runs exe → Enters code → Exe collects hardware info → Sends to server → Server updates DB record
```

**Steps:**
1. User downloads and runs `hardware_collector.exe`

2. Program prompts user to enter their client code

3. Program collects hardware information:
   - System Product ID
   - Model Name
   - RAM Serial, Manufacturer, Part Number
   - Disk Model, Interface Type, Serial

4. Program sends data to `/owner/data/api/` with:
   - Client code
   - All collected hardware information

5. Server validates client code and updates the matching database record

6. User receives success/error message

### 3. Data Retrieval Flow
```
User provides name + email → System fetches record → Returns all data
```

**Endpoint:** `/client/data/api`
- Still uses name + email for lookup (code is only for exe identification)
- Returns complete client and hardware information

## Database Schema

### HardwareRecord Model
```python
{
    # Client Information
    "client_name": CharField(max_length=100),
    "client_email": EmailField(),
    "client_phone": CharField(max_length=15),
    
    # Owner Information
    "owner_name": CharField(max_length=100),
    
    # Unique Identifier
    "client_code": CharField(max_length=20, unique=True),
    
    # System Information (filled by exe)
    "product_id": CharField(max_length=100, blank=True, null=True),
    "model_name": CharField(max_length=255, blank=True, null=True),
    
    # RAM Information (filled by exe)
    "ram_serial": CharField(max_length=100, blank=True, null=True),
    "ram_manufacturer": CharField(max_length=100, blank=True, null=True),
    "ram_part_number": CharField(max_length=100, blank=True, null=True),
    
    # Disk Information (filled by exe)
    "disk_model": CharField(max_length=255, blank=True, null=True),
    "disk_interface_type": CharField(max_length=100, blank=True, null=True),
    "disk_serial": CharField(max_length=100, blank=True, null=True)
}
```

## API Endpoints

### 1. Client Form Submission
**URL:** `/client/form/download`  
**Method:** GET  
**Parameters:**
- `name` (required)
- `email` (required)
- `phone` (required)
- `owner_name` (optional)

**Response:** HTML page with client code and download link

**Process:**
1. Validates email uniqueness
2. Generates client code
3. Creates database record
4. Returns download page with code

### 2. Hardware Data Submission
**URL:** `/owner/data/api/`  
**Method:** POST  
**Content-Type:** application/json

**Request Body:**
```json
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
```

**Response:**
```json
{
    "status": "success",
    "message": "Hardware data updated successfully."
}
```

**Error Responses:**
- 400: Missing client code
- 404: Invalid client code
- 400: Other errors

### 3. Client Data Retrieval
**URL:** `/client/data/api`  
**Method:** GET  
**Parameters:**
- `name` (required)
- `email` (required)

**Response:**
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

### 4. Exe File Download
**URL:** `/client/form/download-exe`  
**Method:** GET  
**Response:** Binary file (hardware_collector.exe)

## Key Changes from Previous System

### Before:
- Personalized exe file generated for each user
- Client info embedded in exe file
- Exe directly sent client info to server
- No code system

### After:
- Single general exe file for all users
- Client code system for identification
- User enters code when running exe
- Database record created before exe runs
- Hardware fields updated by exe (not created)

## Security Considerations

1. **Client Code:**
   - Not cryptographically secure (no uniqueness check)
   - Sufficient for basic identification
   - Consider adding uniqueness validation if needed

2. **API Endpoints:**
   - `/owner/data/api/` uses @csrf_exempt (required for exe)
   - Consider adding API key authentication
   - Rate limiting recommended

3. **Data Validation:**
   - Email uniqueness enforced
   - Client code validation on hardware submission
   - Consider adding input sanitization

## File Structure

```
project/
├── client/
│   ├── views.py          # Client-facing views
│   ├── urls.py           # Client URL routing
│   └── templates/
│       └── client/
│           ├── form.html      # Registration form
│           └── download.html  # Code display + download
├── owner/
│   ├── models.py         # HardwareRecord model
│   └── views.py          # Data receiving endpoint
├── static/
│   └── script_general.py # General exe source code
├── media/
│   └── downloads/
│       └── hardware_collector.exe  # Pre-built exe
└── docs/
    └── SYSTEM_ARCHITECTURE.md  # This file
```

## Building the General Exe

The general exe should be built once and stored in `media/downloads/`:

```bash
pyinstaller --name hardware_collector --onefile --distpath media/downloads static/script_general.py
```

Or it will be built automatically on first form submission.

## Future Enhancements

1. **Code Retrieval System:**
   - Allow users to retrieve lost codes via email
   - User menu to view their code

2. **Code Uniqueness:**
   - Add uniqueness check in code generation
   - Retry logic if duplicate generated

3. **Authentication:**
   - Add API key system for exe
   - Owner authentication for data access

4. **Notifications:**
   - Email code to user after registration
   - Notify owner when hardware data received

5. **Multi-device Support:**
   - Allow multiple hardware submissions per code
   - Track submission history
