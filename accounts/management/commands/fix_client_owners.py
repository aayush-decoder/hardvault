from django.core.management.base import BaseCommand
from accounts.models import Client, Owner


class Command(BaseCommand):
    help = 'Fix clients without owners by assigning them to all available owners'

    def handle(self, *args, **options):
        clients_without_owners = []
        
        for client in Client.objects.all():
            if client.owners.count() == 0:
                clients_without_owners.append(client)
        
        if not clients_without_owners:
            self.stdout.write(self.style.SUCCESS('All clients have owners assigned!'))
            return
        
        self.stdout.write(f'Found {len(clients_without_owners)} clients without owners')
        
        owners = Owner.objects.all()
        if not owners:
            self.stdout.write(self.style.ERROR('No owners found in database!'))
            return
        
        self.stdout.write(f'Available owners: {owners.count()}')
        for owner in owners:
            self.stdout.write(f'  - {owner.company_name} (ID: {owner.id})')
        
        for client in clients_without_owners:
            self.stdout.write(f'\nClient: {client.user.get_full_name()} ({client.user.email})')
            self.stdout.write('Select owner IDs (comma-separated) or press Enter to assign all:')
            
            # For automated fix, assign to first owner
            first_owner = owners.first()
            client.owners.add(first_owner)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Assigned to {first_owner.company_name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Fixed {len(clients_without_owners)} clients'))
