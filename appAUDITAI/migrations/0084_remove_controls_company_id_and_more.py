# Generated by Django 5.0.6 on 2024-05-23 22:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAUDITAI', '0083_remove_workpaper_upload_workpaper_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controls',
            name='COMPANY_ID',
        ),
        migrations.RemoveField(
            model_name='controls',
            name='CONTROL_ID',
        ),
        migrations.AddField(
            model_name='controls',
            name='CONTROL_TYPE',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.RemoveField(
            model_name='controls',
            name='APP_NAME',
        ),
        migrations.AlterField(
            model_name='controls',
            name='CONTROL_DESCRIPTION',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='controls',
            name='CONTROL_NAME',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.CreateModel(
            name='RISKDETAILS',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('RISK_DESCRIPTION', models.CharField(blank=True, max_length=1000, null=True)),
                ('RISK_STATUS', models.CharField(blank=True, max_length=256, null=True)),
                ('RISK_AREA', models.CharField(blank=True, max_length=256, null=True)),
                ('RISK_RATING', models.CharField(blank=True, max_length=256, null=True)),
                ('RISK_RATIONALE', models.CharField(blank=True, max_length=256, null=True)),
                ('APP_NAME', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appAUDITAI.app_list')),
            ],
            options={
                'db_table': 'RISKDETAILS',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='controls',
            name='RISK_NAME',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appAUDITAI.riskdetails'),
        ),
        migrations.CreateModel(
            name='RISKGENERAL',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('RISK_NAME', models.CharField(blank=True, max_length=256, null=True)),
                ('RISK_RATING', models.CharField(blank=True, max_length=256, null=True)),
                ('RISK_RATIONALE', models.CharField(blank=True, max_length=1000, null=True)),
                ('RISK_TYPE', models.CharField(blank=True, max_length=256, null=True)),
                ('APP_NAME', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appAUDITAI.app_list')),
            ],
            options={
                'db_table': 'RISKGENERAL',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='riskdetails',
            name='RISK_NAME',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appAUDITAI.riskgeneral'),
        ),
        migrations.AddField(
            model_name='controls',
            name='APP_NAME',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appAUDITAI.app_list'),
        ),
    ]