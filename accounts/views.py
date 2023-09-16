from django.shortcuts import render,redirect
from.forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registration successfull')
            print(f"user is: {user.last_name}")

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }      
    return render(request,'register.html',context)


def login(request):
    if request.method =='POST':
        email=request.POST['email']
        password=request.POST['password']

        user = auth.authenticate(email=email,password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
    return render(request,'login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out.')
    return redirect('login')