from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image')
    full_name = models.CharField(max_length=100,null=True, blank=True)
    bio=models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=10)
    verified=models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

# Create your models here.
