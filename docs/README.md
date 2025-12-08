# Hardware Collection System Documentation

## Overview
This system allows shop owners to collect hardware information from clients using a code-based identification system with a general-purpose executable file.

## Documentation Files

### 1. [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)
**For:** Developers and System Administrators

Comprehensive technical documentation covering:
- System flow and architecture
- Database schema
- API endpoints and specifications
- Security considerations
- File structure
- Key changes from previous system

### 2. [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
**For:** Developers migrating from the old system

Step-by-step guide for:
- Database migrations
- Code changes summary
- Testing procedures
- Building the general exe
- Rollback procedures
- Common issues and solutions

### 3. [USER_GUIDE.md](USER_GUIDE.md)
**For:** End users and Shop owners

User-friendly instructions for:
- Client registration process
- Running the hardware collector
- Troubleshooting common issues
- Shop owner administrative tasks
- API usage examples
- Customization options

## Quick Start

### For Developers
1. Read [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) if migrating from old system
2. Review [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for technical details
3. Run database migrations
4. Build or let system auto-build the general exe

### For Shop Owners
1. Read [USER_GUIDE.md](USER_GUIDE.md) - Shop Owners section
2. Set up the system following initial setup instructions
3. Share registration form URL with clients
4. Provide support using troubleshooting guide

### For End Users
1. Read [USER_GUIDE.md](USER_GUIDE.md) - Clients section
2. Follow the 5-step process to submit hardware information

## System Requirements

### Server Requirements
- Python 3.8+
- Django 3.2+
- Database (SQLite/PostgreSQL/MySQL)

### Client Requirements (for exe)
- Windows OS
- Internet connection
- Administrator privileges (for hardware access)

### Build Requirements (for exe generation)
- PyInstaller
- Python WMI library
- Requests library

## Key Features

✅ **Single General Exe** - One exe file for all users  
✅ **Code-Based System** - Unique codes for client identification  
✅ **Automatic Hardware Collection** - Collects system, RAM, and disk info  
✅ **Database Integration** - Stores all client and hardware data  
✅ **User-Friendly** - Simple 5-step process for clients  
✅ **API Access** - RESTful API for data retrieval  

## System Flow Summary

```
Registration → Code Generation → Exe Download → Hardware Collection → Data Storage
```

1. Client fills registration form
2. System generates unique code (e.g., `JOH4K7M2P`)
3. Client downloads general exe file
4. Client runs exe and enters their code
5. Exe collects hardware info and sends to server
6. Server updates database record with hardware data

## Code Format

Client codes follow this format:
```
[First 3 characters of email][6 random alphanumeric characters]
```

Example:
- Email: `john@example.com`
- Code: `JOH4K7M2P`

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/client/form/` | GET | Display registration form |
| `/client/form/download` | GET | Submit form and get code |
| `/client/form/download-exe` | GET | Download exe file |
| `/client/data/api` | GET | Retrieve client data |
| `/owner/data/api/` | POST | Submit hardware data |

## Support and Contribution

### Reporting Issues
- Document the issue with steps to reproduce
- Include error messages and logs
- Specify environment (OS, Python version, etc.)

### Contributing
- Follow existing code style
- Update documentation for any changes
- Test thoroughly before submitting

### Contact
For questions or support, contact your system administrator.

## Version History

### Version 2.0 (Current)
- Implemented code-based system
- Single general exe for all users
- Improved user experience
- Better database structure

### Version 1.0 (Legacy)
- Personalized exe per user
- Direct client info embedding
- Slower generation process

## License

[Add your license information here]

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- PyInstaller Documentation: https://pyinstaller.org/
- Python WMI Documentation: https://pypi.org/project/WMI/

---

**Last Updated:** December 2025  
**Maintained By:** [Your Name/Team]
