# Generated by Django 3.0.6 on 2020-06-21 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='fcm_token',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='students',
            name='fcm_token',
            field=models.TextField(default=''),
        ),
    ]
