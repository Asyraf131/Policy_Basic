# Generated by Django 3.1.1 on 2020-09-10 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Policy', '0003_auto_20200910_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='insurance',
            field=models.ForeignKey(limit_choices_to={'role_id': 3}, on_delete=django.db.models.deletion.CASCADE, related_name='insurance_id', to='Policy.businesspartner'),
        ),
    ]