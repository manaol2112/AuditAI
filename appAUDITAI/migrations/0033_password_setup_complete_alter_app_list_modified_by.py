# Generated by Django 5.0.4 on 2024-04-22 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAUDITAI', '0032_app_list_setup_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='password',
            name='SETUP_COMPLETE',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='app_list',
            name='MODIFIED_BY',
            field=models.CharField(default=False, max_length=50, null=True),
        ),
    ]
