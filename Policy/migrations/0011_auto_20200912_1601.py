# Generated by Django 3.1.1 on 2020-09-12 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Policy', '0010_auto_20200912_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businesspartner',
            old_name='bp_Type_id',
            new_name='bp_Type',
        ),
        migrations.RenameField(
            model_name='businesspartner',
            old_name='role_id',
            new_name='role',
        ),
    ]