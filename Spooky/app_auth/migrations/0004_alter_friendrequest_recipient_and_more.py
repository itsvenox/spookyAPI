# Generated by Django 5.0.2 on 2024-03-07 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0003_alter_friendrequest_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to='app_auth.userprofile'),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='sent_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
