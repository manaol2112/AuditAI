# Generated by Django 5.0.6 on 2024-05-22 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAUDITAI', '0074_workpaper_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='workpaper_upload',
            name='audit_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
