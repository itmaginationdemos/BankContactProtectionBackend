# Generated by Django 4.0.1 on 2022-03-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationrequest',
            name='valid',
            field=models.BooleanField(default=True),
        ),
    ]