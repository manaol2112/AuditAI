# Generated by Django 5.0.6 on 2024-05-22 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAUDITAI', '0078_auditfile_audit_id_alter_workpaper_upload_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditfile',
            name='DATE_SENT',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
