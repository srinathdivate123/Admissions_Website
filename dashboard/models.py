from django.db import models
from django.contrib.auth.models import User
class UserData (models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, default='')
    email = models.CharField(max_length=50,default='')
    count = models.IntegerField(default=0)
    markscard = models.CharField(max_length=50)
    radio = models.CharField(max_length=10, default='')
    first_name = models.CharField(max_length=50, default='')
    middle_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    father_name = models.CharField(max_length=50, default='')
    mother_name = models.CharField(max_length=50, default='')
    roll_no = models.CharField(max_length=50,default=0)
    birth_date = models.CharField(max_length=50, default='')
    mob_no = models.CharField(max_length=50,default=0)
    course = models.CharField(max_length=50, default='')
    submitted = models.BooleanField(default=False)
    Cambridge_verified = models.BooleanField(default=False)
    Harward_verified = models.BooleanField(default=False)
    MIT_verified = models.BooleanField(default=False)
    Oxford_verified = models.BooleanField(default=False)
    Stanford_verified = models.BooleanField(default=False)
    UCLA_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.email