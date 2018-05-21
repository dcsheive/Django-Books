from django.shortcuts import render, redirect
from .models import User
import bcrypt
import re
from django.contrib import messages
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    
    return render(request, "register/home.html")
def signin(request):
    
    return render(request, "register/login.html")
def reg(request):
    if 'first_name' not in request.session:
        request.session['first_name'] = ""
    if 'last_name' not in request.session:
        request.session['last_name'] = ""
    if 'email' not in request.session:
        request.session['email'] = ""
    return render(request, "register/register.html")

def register(request):
    
    if request.method == "POST":
        errors = User.objects.reg(request.POST)
        email = request.POST['email']
        first = request.POST['first_name']
        last = request.POST['last_name']
        passw= request.POST['password']
        if email or first or last:
            request.session['email'] = email
            request.session['first_name'] = first
            request.session['last_name'] = last
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/reg')
        else:
            if len(User.objects.all()):
                level = 0
            else:
                level = 1
            pw_hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt())  
            a = User(first_name=first, last_name = last, email = email, password = pw_hash, user_level = level, description= "I'm a new user :)")
            a.save()
            request.session.clear()
            request.session['id'] = User.objects.get(email=email).id
            request.session['fname'] = User.objects.get(id=request.session['id']).first_name
            return redirect('/users/')
    else:
        return redirect('/reg')

def login(request):
    if request.method == "POST":
        errors = User.objects.log(request.POST)
        email = request.POST['email']
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/signin')
        else:
            request.session['id'] = User.objects.get(email=email).id
            request.session['fname'] = User.objects.get(id=request.session['id']).first_name
            return redirect('/users/')
    else:
        return redirect('/signin')
    



def home(request):
    if 'id' not in request.session:
        return redirect('/')
    return render(request, "register/home.html")

def logout(request):
    request.session.clear()
    return redirect('/')
