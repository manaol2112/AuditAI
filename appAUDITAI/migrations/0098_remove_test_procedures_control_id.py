# Generated by Django 5.0.6 on 2024-06-02 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appAUDITAI', '0097_test_procedures_control_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_procedures',
            name='CONTROL_ID',
        ),
    ]