# Generated by Django 4.2.20 on 2025-04-06 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('CUSTOMER', 'Customer'), ('MODERATOR', 'Moderator'), ('ADMIN', 'Admin'), ('COMPANY', 'Company')], default='CUSTOMER', max_length=20, verbose_name='роль'),
        ),
    ]
