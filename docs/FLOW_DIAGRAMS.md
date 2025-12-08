# System Flow Diagrams

## 1. Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT REGISTRATION                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  User visits     │
                    │  /client/form/   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Fills form:     │
                    │  - Name          │
                    │  - Email         │
                    │  - Phone         │
                    │  - Owner Name    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Submit form     │
                    │  GET /download   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Check duplicate │
                    │  email?          │
                    └────────┬─────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                   YES               NO
                    │                 │
                    ▼                 ▼
            ┌──────────────┐  ┌──────────────────┐
            │ Show error   │  │ Generate code    │
            │ message      │  │ [EMAIL][:3]+[6]  │
            └──────────────┘  └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Create DB record │
                              │ with empty       │
                              │ hardware fields  │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Show download    │
                              │ page with CODE   │
                              └────────┬─────────┘
                                       │
┌──────────────────────────────────────┴─────────────────────────┐
│                      HARDWARE COLLECTION                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ User clicks      │
                    │ download button  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Download         │
                    │ hardware_        │
                    │ collector.exe    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User runs exe    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Exe prompts:     │
                    │ "Enter code:"    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User enters      │
                    │ their code       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Exe collects:    │
                    │ - System info    │
                    │ - RAM details    │
                    │ - Disk details   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ POST to          │
                    │ /owner/data/api/ │
                    │ with code + data │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Server validates │
                    │ code exists?     │
                    └────────┬─────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                   NO                YES
                    │                 │
                    ▼                 ▼
            ┌──────────────┐  ┌──────────────────┐
            │ Return 404   │  │ Update DB record │
            │ Invalid code │  │ with hardware    │
            └──────────────┘  │ details          │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Return success   │
                              │ message          │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ User sees        │
                              │ "Success!"       │
                              └──────────────────┘
```

## 2. Database Record Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECORD CREATION (Form Submit)                 │
├─────────────────────────────────────────────────────────────────┤
│  client_name:        "John Doe"                                 │
│  client_email:       "john@example.com"                         │
│  client_phone:       "1234567890"                               │
│  owner_name:         "Shop Owner"                               │
│  client_code:        "JOH4K7M2P"  ← Generated                   │
│  ─────────────────────────────────────────────────────────────  │
│  product_id:         NULL          ← Empty                      │
│  model_name:         NULL          ← Empty                      │
│  ram_serial:         NULL          ← Empty                      │
│  ram_manufacturer:   NULL          ← Empty                      │
│  ram_part_number:    NULL          ← Empty                      │
│  disk_model:         NULL          ← Empty                      │
│  disk_interface_type: NULL         ← Empty                      │
│  disk_serial:        NULL          ← Empty                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ User runs exe with code
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RECORD UPDATE (Exe Submission)                  │
├─────────────────────────────────────────────────────────────────┤
│  client_name:        "John Doe"                                 │
│  client_email:       "john@example.com"                         │
│  client_phone:       "1234567890"                               │
│  owner_name:         "Shop Owner"                               │
│  client_code:        "JOH4K7M2P"                                │
│  ─────────────────────────────────────────────────────────────  │
│  product_id:         "ABC123"      ← Updated                    │
│  model_name:         "Dell Inspiron" ← Updated                  │
│  ram_serial:         "12345"       ← Updated                    │
│  ram_manufacturer:   "Samsung"     ← Updated                    │
│  ram_part_number:    "M471A"       ← Updated                    │
│  disk_model:         "Samsung SSD" ← Updated                    │
│  disk_interface_type: "SATA"       ← Updated                    │
│  disk_serial:        "S3Z9NX"      ← Updated                    │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Code Generation Process

```
┌──────────────────────────────────────────────────────────────┐
│                    CODE GENERATION                            │
└──────────────────────────────────────────────────────────────┘

Input: email = "john@example.com"

Step 1: Extract first 3 characters
        ↓
        "joh"

Step 2: Convert to uppercase
        ↓
        "JOH"

Step 3: Generate 6 random alphanumeric characters
        ↓
        "4K7M2P"

Step 4: Concatenate
        ↓
        "JOH" + "4K7M2P"
        ↓
        "JOH4K7M2P"

Output: client_code = "JOH4K7M2P"

┌──────────────────────────────────────────────────────────────┐
│  More Examples:                                               │
│  ─────────────────────────────────────────────────────────── │
│  alice@test.com     → ALI8X3Q9Z                              │
│  bob@company.org    → BOB2N5K7M                              │
│  sarah@email.net    → SAR9P1W4T                              │
│  m@short.com        → M__6H2Y8K  (if email < 3 chars)        │
└──────────────────────────────────────────────────────────────┘
```

## 4. API Request/Response Flow

### Registration API

```
┌─────────────────────────────────────────────────────────────┐
│  REQUEST: GET /client/form/download                          │
├─────────────────────────────────────────────────────────────┤
│  Parameters:                                                 │
│    name=John%20Doe                                          │
│    email=john@example.com                                   │
│    phone=1234567890                                         │
│    owner_name=Shop%20Owner                                  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  RESPONSE: HTML Page                                         │
├─────────────────────────────────────────────────────────────┤
│  Status: 200 OK                                             │
│  Content: download.html with:                               │
│    - Client Code: JOH4K7M2P                                 │
│    - Download Button                                        │
│    - Instructions                                           │
└─────────────────────────────────────────────────────────────┘
```

### Hardware Submission API

```
┌─────────────────────────────────────────────────────────────┐
│  REQUEST: POST /owner/data/api/                              │
├─────────────────────────────────────────────────────────────┤
│  Content-Type: application/json                             │
│  Body:                                                       │
│  {                                                           │
│    "client_code": "JOH4K7M2P",                              │
│    "device_product_id": "ABC123",                           │
│    "device_model_name": "Dell Inspiron",                    │
│    "ram_serial": "12345",                                   │
│    "ram_manufacturer": "Samsung",                           │
│    "ram_part_number": "M471A",                              │
│    "disk_model": "Samsung SSD",                             │
│    "disk_interface_type": "SATA",                           │
│    "disk_serial": "S3Z9NX"                                  │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  RESPONSE: Success                                           │
├─────────────────────────────────────────────────────────────┤
│  Status: 200 OK                                             │
│  Body:                                                       │
│  {                                                           │
│    "status": "success",                                     │
│    "message": "Hardware data updated successfully."         │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

### Data Retrieval API

```
┌─────────────────────────────────────────────────────────────┐
│  REQUEST: GET /client/data/api                               │
├─────────────────────────────────────────────────────────────┤
│  Parameters:                                                 │
│    name=John%20Doe                                          │
│    email=john@example.com                                   │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  RESPONSE: Complete Record                                   │
├─────────────────────────────────────────────────────────────┤
│  Status: 200 OK                                             │
│  Body:                                                       │
│  {                                                           │
│    "client_name": "John Doe",                               │
│    "client_email": "john@example.com",                      │
│    "client_phone": "1234567890",                            │
│    "owner_name": "Shop Owner",                              │
│    "product_id": "ABC123",                                  │
│    "model_name": "Dell Inspiron",                           │
│    "ram_serial": "12345",                                   │
│    "ram_manufacturer": "Samsung",                           │
│    "ram_part_number": "M471A",                              │
│    "disk_model": "Samsung SSD",                             │
│    "disk_interface_type": "SATA",                           │
│    "disk_serial": "S3Z9NX"                                  │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

## 5. Error Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    ERROR SCENARIOS                           │
└─────────────────────────────────────────────────────────────┘

Scenario 1: Duplicate Email
────────────────────────────
User submits form → Email exists in DB → Show error on form page

Scenario 2: Invalid Code (Exe)
───────────────────────────────
Exe sends code → Code not in DB → Return 404 "Invalid client code"

Scenario 3: Missing Code (Exe)
───────────────────────────────
Exe sends data → No code field → Return 400 "Client code is required"

Scenario 4: Exe File Not Found
───────────────────────────────
User clicks download → File missing → Auto-build exe OR show 404

Scenario 5: Client Not Found (Data API)
────────────────────────────────────────
GET data/api → No match → Return 404 "No matching client found"

┌─────────────────────────────────────────────────────────────┐
│  Error Response Format:                                      │
│  ─────────────────────────────────────────────────────────  │
│  {                                                           │
│    "status": "error",                                       │
│    "message": "Description of error"                        │
│  }                                                           │
│                                                              │
│  OR                                                          │
│                                                              │
│  {                                                           │
│    "error": "Description of error"                          │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

## 6. Component Interaction Diagram

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│              │         │              │         │              │
│   Browser    │◄───────►│    Django    │◄───────►│   Database   │
│   (Client)   │         │   Server     │         │  (SQLite/    │
│              │         │              │         │   Postgres)  │
└──────┬───────┘         └──────┬───────┘         └──────────────┘
       │                        │
       │                        │
       │  1. GET /form/         │
       │───────────────────────►│
       │                        │
       │  2. HTML form          │
       │◄───────────────────────│
       │                        │
       │  3. Submit form        │
       │───────────────────────►│
       │                        │  4. Create record
       │                        │─────────────────►
       │                        │
       │                        │  5. Record created
       │                        │◄─────────────────
       │                        │
       │  6. Download page      │
       │     with code          │
       │◄───────────────────────│
       │                        │
       │  7. Download exe       │
       │───────────────────────►│
       │                        │
       │  8. Exe file           │
       │◄───────────────────────│
       │                        │
       ▼                        │
┌──────────────┐                │
│              │                │
│  Exe File    │                │
│  (Client PC) │                │
│              │                │
└──────┬───────┘                │
       │                        │
       │  9. POST hardware data │
       │───────────────────────►│
       │     with code          │
       │                        │  10. Update record
       │                        │─────────────────►
       │                        │
       │                        │  11. Updated
       │                        │◄─────────────────
       │                        │
       │  12. Success response  │
       │◄───────────────────────│
       │                        │
```

## 7. File System Structure

```
project/
│
├── client/
│   ├── views.py ──────────────► Registration & Download Logic
│   ├── urls.py ───────────────► URL Routing
│   └── templates/
│       └── client/
│           ├── form.html ─────► Registration Form
│           └── download.html ─► Code Display Page
│
├── owner/
│   ├── models.py ─────────────► HardwareRecord Model
│   └── views.py ──────────────► Data Receiving Logic
│
├── static/
│   ├── script4.py ────────────► OLD: Personalized script
│   └── script_general.py ─────► NEW: General script
│
├── media/
│   └── downloads/
│       └── hardware_collector.exe ─► Pre-built exe
│
└── docs/
    ├── README.md ─────────────► Documentation overview
    ├── SYSTEM_ARCHITECTURE.md ► Technical details
    ├── MIGRATION_GUIDE.md ────► Migration steps
    ├── USER_GUIDE.md ─────────► User instructions
    ├── QUICK_REFERENCE.md ────► Quick lookup
    ├── CHANGES_SUMMARY.md ────► What changed
    └── FLOW_DIAGRAMS.md ──────► This file
```

## 8. State Transition Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  RECORD STATE TRANSITIONS                    │
└─────────────────────────────────────────────────────────────┘

    [START]
       │
       │ User submits form
       ▼
┌──────────────┐
│  REGISTERED  │  ← Record created with code
│              │    Hardware fields = NULL
└──────┬───────┘
       │
       │ User runs exe with code
       ▼
┌──────────────┐
│   COMPLETE   │  ← Hardware fields populated
│              │    All data present
└──────────────┘

States:
─────────────────────────────────────────────────────────────
REGISTERED:  client_code exists, hardware fields NULL
COMPLETE:    client_code exists, hardware fields populated

Transitions:
─────────────────────────────────────────────────────────────
Form Submit  → REGISTERED
Exe Submit   → COMPLETE (if code valid)
```
