# Generated by Django 5.0.6 on 2024-05-22 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAUDITAI', '0080_remove_auditfile_file_name_auditfile_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditfile',
            name='file_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
