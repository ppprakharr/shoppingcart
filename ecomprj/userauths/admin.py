from django.contrib import admin
from userauths.models import User,Profile

class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','bio']
# class ProfileAdmin(admin.ModelAdmin):
#     list_display=['user']


admin.site.register(User,UserAdmin)
admin.site.register(Profile)



# Register your models here.
