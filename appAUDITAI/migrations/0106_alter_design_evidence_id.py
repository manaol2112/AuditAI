# Generated by Django 5.0.6 on 2024-06-05 02:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAUDITAI', '0105_alter_design_evidence_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design_evidence',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
