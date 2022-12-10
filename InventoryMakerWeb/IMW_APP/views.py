

from django.shortcuts import render, redirect
from .models import inventory, items
from django.contrib.auth.models import User , auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
            else:
                user = User.objects.create_user(username=email.split("@")[0], email=email, password=password1)
                user.save()
                return redirect('login')
        else: 
            messages.info(request, 'Passwords are not equal.')
    else:
        form = LoginForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['email'].split("@")[0]
        password1 = request.POST['password1']
        user = auth.authenticate(username=username ,password=password1)
        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('index')

def settings(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('noise')
            print(request.POST['email'])
            print(request.POST['password1'])
            print(request.POST['password2'])
    else:
        form = LoginForm()
    return render(request, 'settings.html', {'form': form})

@login_required
def data(request):
    ivts = inventory.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ItmForm(request.POST)
        new_ivt = inventory(name = request.POST['name'],
        user = User.objects.get(id=request.user.id))
        new_ivt.save()
    else:
        form = IvtForm()
    return render(request, 'data.html', {'form': form, 'ivts': ivts})

def SeeInventory(request, ivt):
    ivt = inventory.objects.get(name=ivt, user = User.objects.get(id=request.user.id))
    itms = items.objects.filter(ivt=ivt)
    if request.method == 'POST':
        form = IvtForm(request.POST)
        new_itm = items(ivt=ivt,name=request.POST['name'],description='this is an item')
        new_itm.save()
    else:
        form = IvtForm()
    return render(request, 'inventory.html', {'form': form, 'ivt': ivt,'itms':itms})
    
def SeeItem(request, ivt, itm):
    return render(request, 'login.html')

def UpdateIvt(request, IvtPk):
    ivt = inventory.objects.get(id=IvtPk)
    if request.user.id == ivt.user_id:
        ivt.delete()
    return redirect('data')

def UpdateItm(request, IvtPk, ItmPk):
    ivt = inventory.objects.get(id=IvtPk)
    itm = items.objects.get(id=ItmPk)
    itm.delete()
    print(ivt,IvtPk,ivt.name)
    return redirect('SeeInventory',ivt=ivt.name)






