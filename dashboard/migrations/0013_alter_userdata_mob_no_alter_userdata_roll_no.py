# Generated by Django 4.1.2 on 2022-11-30 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_userdata_universities_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='mob_no',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='roll_no',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
