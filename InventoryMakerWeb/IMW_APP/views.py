

from django.shortcuts import render, redirect
from .models import inventory, items
from django.contrib.auth.models import User , auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=email.split("@")[0], email=email, password=password)
                user.save()
                return redirect('login')
        else: 
            messages.info(request, 'Passwords are not equal.')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['email'].split("@")[0]
        password = request.POST['password']
        user = auth.authenticate(username=username ,password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('index')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def settings(request):
    return render(request, 'settings.html')

@login_required
def data(request):
    ivts = inventory.objects.filter(user=request.user)
    if request.method == 'POST':
        new_ivt = inventory(title = request.POST['title'],
        user = User.objects.get(id=request.user.id))
        new_ivt.save()
        return redirect('data')

    return render(request, 'data.html', {'ivts': ivts})

def UpdateIvt(request, IvtPk):
    ivt = inventory.objects.get(id=IvtPk)
    if request.user.id == ivt.user_id:
        ivt.delete()
    return redirect('data')

def UpdateItm(request, IvtPk, ItmPk):
    ivt = inventory.objects.get(id=IvtPk)
    itm = items.objects.get(id=ItmPk)
    itm.delete()
    print(ivt,IvtPk,ivt.title)
    return redirect('SeeInventory',ivt=ivt.title)

def SeeInventory(request, ivt):
    ivt = inventory.objects.get(title=ivt, user = User.objects.get(id=request.user.id))
    itms = items.objects.filter(ivt=ivt)
    if request.method == 'POST':
        new_itm = items(ivt=ivt,name=request.POST['name'],description='this is an item')
        new_itm.save()
    return render(request, 'inventory.html', {'ivt': ivt,'itms':itms})
    

def SeeItem(request, ivt, itm):
    return render(request, 'login.html')




