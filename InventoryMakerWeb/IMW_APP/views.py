

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

@login_required
def data(request):
    ivts = inventory.objects.filter(user=request.user)

    if request.method == 'POST':
        names = list(map(inventory.GetName,ivts))
        ids = list(map(inventory.GetId,ivts))

        if 'create' in request.POST:
            if not request.POST['name']:
                messages.info(request, 'You must insert a name!')

            elif request.POST['name']  in names:
                messages.info(request, 'The name inserted is already in use.')

            else:
                new_ivt = inventory(name = request.POST['name'],
                user = User.objects.get(id=request.user.id))
                if request.POST['description']:
                    new_ivt.description = request.POST['description']
                new_ivt.save()
        
        elif 'mod' in request.POST:
            mod = 0
            if  not int(request.POST.get('list',False)) in ids:
                messages.info(request, 'You must select an inventory to modify.')
            else:
                modIvt = inventory.objects.get(
                id = request.POST['list'],
                user = User.objects.get(id=request.user.id))

                if request.POST['name'] and request.POST['name'] not in names:
                    modIvt.name = request.POST['name']
                    mod = 1
                if request.POST['description']:
                    modIvt.description = request.POST['description']
                    mod = 1
                if not mod:
                    messages.info(request, 'You must insert at least one new value.')
                else:
                    modIvt.save()

        elif 'del' in request.POST:
            if not int(request.POST.get('list',False)) in ids:
                messages.info(request, 'You must select an inventory to delete.')
            else:
                ivt = inventory.objects.get(id=request.POST['list'],
                user = User.objects.get(id=request.user.id))
                ivt.delete()

        return redirect('data')

    return render(request, 'data.html', { 'ivts': ivts})
    

@login_required
def SeeInventory(request, ivt):
    ivt = inventory.objects.get(name=ivt, user = User.objects.get(id=request.user.id))
    itms = items.objects.filter(ivt=ivt)


    if request.method == 'POST':
        names = list(map(items.GetName,itms))
        ids = list(map(items.GetId,itms))

        if 'create' in request.POST:
            if not request.POST['name']:
                messages.info(request, 'You must insert a name!')
            elif request.POST['name'] in names:
                messages.info(request, 'The name inserted is already in use.')
            else:
                new_ivt = items(name = request.POST['name'],
                ivt = ivt)

                if request.POST['quantity']:
                    new_ivt.quantity = request.POST['quantity']

                if request.POST['unity']:
                    new_ivt.unity = request.POST['unity']

                if request.POST['description']:
                    new_ivt.description = request.POST['description']
                new_ivt.save()
        
        elif 'mod' in request.POST:
            mod = 0
            if not int(request.POST.get('list',False)) in ids:
                messages.info(request, 'You must select an inventory to modify.')
            else:
                modIvt = items.objects.get(
                id = request.POST['list'],
                ivt = ivt)
                if request.POST['name'] and request.POST['name'] not in names:
                    modIvt.name = request.POST['name']
                    mod = 1

                if request.POST['quantity']:
                    modIvt.quantity = request.POST['quantity']
                    mod = 1

                if request.POST['unity']:
                    modIvt.unity = request.POST['unity']
                    mod = 1

                if request.POST['description']:
                    modIvt.description = request.POST['description']
                    mod = 1

                if mod == 1:
                    modIvt.save()
                else:
                    messages.info(request, 'You must insert at least one new value.')

        elif 'del' in request.POST:
            if not int(request.POST.get('list',False)) in ids:
                messages.info(request, 'You must select an item to be deleted.')
            else:
                itm = items.objects.get(id=request.POST['list'],ivt=ivt)
                itm.delete()

        return redirect('SeeInventory',ivt.name)

    return render(request, 'inventory.html', {'ivt': ivt,'itms':itms})







