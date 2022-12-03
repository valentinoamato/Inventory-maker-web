

from django.shortcuts import render, redirect
from .models import inventory, items
from django.contrib.auth.models import User , auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
            messages.info(request, 'Password are not equal.')
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
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def data(request):
    print(request.user)
    print(User.objects.get(id=request.user.id))
    print(type(User.objects.get(id=request.user.id)))
    print(type(request.user))
    ivt = inventory.objects.filter(user=request.user)
    if request.method == 'POST':
        new_ivt = inventory(title = request.POST['title'],
        user = User.objects.get(id=request.user.id))
        new_ivt.save()
        return redirect('/data')

    return render(request, 'data.html', {'ivts': ivt})

def delete(request, pk):
    ivt = inventory.objects.get(id=pk)
    ivt.delete()
    return redirect('/data')


