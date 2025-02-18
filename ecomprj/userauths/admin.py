from django.contrib import admin
from userauths.models import User,Profile,ContactUs

class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','bio']
# class ProfileAdmin(admin.ModelAdmin):
#     list_display=['user']
class ContactUsAdmin(admin.ModelAdmin):
    list_display=['email','full_name','subject']


admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(ContactUs,ContactUsAdmin)



# Register your models here.
