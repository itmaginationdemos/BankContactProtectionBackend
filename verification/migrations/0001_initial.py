# Generated by Django 4.0.1 on 2022-03-03 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('timeout', models.DateTimeField()),
                ('requester_verification_code', models.CharField(max_length=255)),
                ('given_verification_code', models.CharField(max_length=255)),
                ('given', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verificationGivens', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verificationRequests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
