# Generated by Django 5.2.1 on 2025-06-03 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=100)),
                ('model_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RAMModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(blank=True, max_length=100, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=100, null=True)),
                ('part_number', models.CharField(blank=True, max_length=100, null=True)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ram_modules', to='owner.systeminfo')),
            ],
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('interface_type', models.CharField(blank=True, max_length=100, null=True)),
                ('serial', models.CharField(blank=True, max_length=100, null=True)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disks', to='owner.systeminfo')),
            ],
        ),
    ]
