from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(upload_to='image')
    full_name = models.CharField(max_length=100,null=True, blank=True)
    bio=models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=10)
    verified=models.BooleanField(default=False)

    def __str__(self):
       return self.user.username
        
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    # user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=200,default='lorem@gmail.com')
    phone=models.CharField(max_length=30,null=True,blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name_plural='Contact Us'
    
    def __str__(self):
        try:
            return self.full_name
        except:
            return self.user.username

# Create your models here.
