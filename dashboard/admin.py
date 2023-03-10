from django.contrib import admin
from . models import UserData
class userdata(admin.ModelAdmin):
    list_display = ('email','submitted', 'course', 'count','markscard','radio','first_name','middle_name','last_name','father_name','mother_name','roll_no','birth_date','mob_no','Cambridge_verified','Harward_verified','MIT_verified','Oxford_verified','Stanford_verified','UCLA_verified')
admin.site.register(UserData, userdata)