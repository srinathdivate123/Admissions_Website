# Generated by Django 4.1.3 on 2022-11-24 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_userdata_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]