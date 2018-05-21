from django.shortcuts import render, redirect
from datetime import datetime
from .models import Message, Comment, User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'users': User.objects.all(),
        'current': User.objects.get(id = request.session['id'])
    }
    return render(request,'user/users.html', context)

def createuser(request):
    if request.method == "POST":
        errors = User.objects.reg(request.POST)
        email = request.POST['email']
        first = request.POST['first_name']
        last = request.POST['last_name']
        passw= request.POST['password']
        level= request.POST['user_level']
        if email or first or last:
            request.session['email'] = email
            request.session['first_name'] = first
            request.session['last_name'] = last
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/users/create')
        else:
            pw_hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt())  
            a = User(first_name=first, last_name = last, email = email, password = pw_hash, user_level = level)
            a.save()
            return redirect('/users/')
    else:
        return redirect('/users/create')
def create(request):
    if 'id' not in request.session:
        return redirect('/')
    if User.objects.get(id=request.session['id']).user_level < 1:
        return redirect('/')
    return render(request,'user/usercreate.html')

def user(request, number):
    context = {
        'user': User.objects.get(id=number),
        'mymessages': reversed(Message.objects.filter(page= number)),
        'comments': Comment.objects.filter(page= number)
    }
    return render(request,'user/user.html', context)

def edit(request, number):
    if 'id' not in request.session:
        return redirect('/')
    if request.session['id'] != int(number): 
        if User.objects.get(id=request.session['id']).user_level < 1: 
            return redirect('/users/'+number)
    context = {
        'user': User.objects.get(id=number),
        'current': User.objects.get(id = request.session['id'])
    }
    return render(request,'user/useredit.html', context)

def update(request, number):
    errors = User.objects.update(request.POST, number)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/users/'+number+'/edit')
    if request.method == "POST":
        b = User.objects.get(id=number)
        b.first_name=request.POST['first_name']
        b.last_name=request.POST['last_name']
        b.email=request.POST['email']
        b.description = request.POST['description']
        b.updated_at = datetime.now()
        b.save()
        return redirect('/users/'+number)
    else:
        return redirect('/')

def makeadmin(request,number):
    if request.method == "POST":
        b = User.objects.get(id=number)
        b.user_level = request.POST['user_level']
        b.save()
        return redirect('/users/'+number)
    else:
        return redirect('/')
    

def updatepassword(request, number):
    errors = User.objects.updatepassword(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/users/create')
    if request.method == "POST":
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())  
        b = User.objects.get(id=number)
        b.password=pw_hash
        b.updated_at = datetime.now()
        b.save()
        return redirect('/users/'+number)
    else:
        return redirect('/')
def delete(request, number):
    b = User.objects.get(id=number)
    b.delete()
    request.session.clear()
    return redirect('/')


def message(request, number):
    if request.method == 'POST':
        errors = Message.objects.message(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/users/'+number)
        else:
            Message.objects.create(text=request.POST['messagebox'],poster=User.objects.get(id=request.session['id']), page = User.objects.get(id=number))
        return redirect('/users/'+number)
    else:
        return redirect('/users/'+number)

def deletemessage(request, number):
    Message.objects.get(id=int(request.POST['message_id'])).delete()
    return redirect('/users/'+number)


def comment(request, number):
    if request.method == 'POST':
        errors = Comment.objects.comment(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/users/'+number)
        else:
            Comment.objects.create(text=request.POST['commentbox'],poster=User.objects.get(id=request.session['id']), message = Message.objects.get(id=request.POST['message_id']), page = User.objects.get(id=number))
        return redirect('/users/'+number)
    else :
        return redirect('/users/'+number)

def deletecomment(request,number):
    Comment.objects.get(id=int(request.POST['comment_id'])).delete()
    return redirect('/users/'+number)