from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User,Profile


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username"})) 
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder":"email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"password"})) 
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"confirm password"})) 
    
    class Meta:
        model = User
        fields=['username', 'email']

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter full name'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter mobile number'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter bio'}))
    class Meta:
        model = Profile
        fields=['full_name','image','mobile','bio']