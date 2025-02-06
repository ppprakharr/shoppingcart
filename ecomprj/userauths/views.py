from django.shortcuts import redirect, render
from userauths.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User
# User = settings.AUTH_USER_MODEL


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, you are succesfully logged in")
            new_user = authenticate(username=form.cleaned_data['email'],password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('core:index')
    else:
        print('user cannot be created')
        form = UserRegistrationForm()

    
    context={
        'form':form
    }
    return render(request,'userauths/sign-up.html',context) 


# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"Hey You are already logged in")
        return redirect('core:index')
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request,email=email, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, "You are logged in")
                return redirect("core:index")
            else:
                messages.warning(request, "Incorrect password")
        except: 
            messages.warning(request, f"User with {email} does not exist")
        
    context ={

    }
    return render(request,'userauths/sign-in.html',context)

def logout_view(request):
    logout(request)
    messages.success(request, f"You are succesfully logged out")
    return redirect('userauths:sign-in')

        
