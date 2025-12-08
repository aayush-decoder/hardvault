"""
Test script to verify owner-client relationships
Run with: python manage.py shell < test_relationships.py
"""

from accounts.models import User, Owner, Client
from owner.models import HardwareRecord

print("\n" + "="*60)
print("TESTING OWNER-CLIENT RELATIONSHIPS")
print("="*60)

# Check all owners
print("\n1. ALL OWNERS:")
owners = Owner.objects.all()
for owner in owners:
    print(f"   - {owner.company_name} (ID: {owner.id}, User: {owner.user.email})")
    clients = owner.clients.all()
    print(f"     Clients: {clients.count()}")
    for client in clients:
        print(f"       * {client.user.get_full_name()} ({client.user.email})")

# Check all clients
print("\n2. ALL CLIENTS:")
clients = Client.objects.all()
for client in clients:
    print(f"   - {client.user.get_full_name()} ({client.user.email})")
    owners = client.owners.all()
    print(f"     Owners: {owners.count()}")
    for owner in owners:
        print(f"       * {owner.company_name}")

# Check hardware records
print("\n3. HARDWARE RECORDS:")
records = HardwareRecord.objects.all()
for record in records:
    print(f"   - {record.client_name} ({record.client_email})")
    print(f"     Owner: {record.owner_name}")
    print(f"     Code: {record.client_code}")
    print(f"     User: {record.user}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60 + "\n")
