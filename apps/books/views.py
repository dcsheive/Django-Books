from django.shortcuts import render, redirect
from .models import User,Book,Author,Review
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'reviews': Review.objects.all().order_by('-id')[:3],
        'books': Book.objects.all(),
        'range' : [1,2,3,4,5]
    }
    return render(request,'books/books.html', context)

def addbook(request):
    if request.method =="POST":
        errors = Review.objects.addbook(request.POST)
        request.session['title'] = request.POST['title']
        request.session['text'] = request.POST['text']
        request.session['author'] = request.POST['author']
        request.session['authorlist'] = request.POST['authorlist']
        request.session['stars'] = request.POST['stars']
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/books/add')
        else:
            if len(request.POST['author']):
                Author.objects.create(name=request.POST['author'])
                this_author = Author.objects.get(name=request.POST['author'])
            else: 
                this_author = Author.objects.get(name=request.POST['authorlist'])
            Book.objects.create(title=request.POST['title'], author=this_author)
            this_book = Book.objects.get(title=request.POST['title'])
            Review.objects.create(stars=request.POST['stars'], text=request.POST['text'],book= this_book, poster= User.objects.get(id=request.session['id']))
            keepid = request.session['id'] 
            keepname = request.session['fname']
            request.session.clear()
            request.session['id'] = keepid   
            request.session['fname'] = keepname
            return redirect('/books/')
    else:
        return redirect('/books/')
def book(request,number):
    context = {
        'book': Book.objects.get(id=number),
        'reviews' : reversed(Review.objects.filter(book=number)),
        'range' : [1,2,3,4,5]
    }
    return render(request, 'books/book.html', context)

def add(request):
    context = {
        'authors': Author.objects.all()
    }
    if 'title' not in request.session:
        request.session['title'] = ""
    if 'text' not in request.session:
        request.session['text'] = ""
    if 'author' not in request.session:
        request.session['author'] = ""
    if 'authorlist' not in request.session:
        request.session['authorlist'] = ""
    if 'stars' not in request.session:
        request.session['stars'] = 1

    return render(request, 'books/addbook.html', context)

def userbooks(request,number):
    context = {
        'user': User.objects.get(id=number),
        'reviews': Review.objects.filter(poster=number),
        'count': User.objects.get(id=number).reviews.count()
    }
    return render(request, 'books/user.html',context)

def addreview(request,number):
    if request.method =="POST":
        errors = Review.objects.addreview(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/books/'+number)
        else:
            Review.objects.create(stars=request.POST['stars'], text=request.POST['text'],book= Book.objects.get(id=number), poster= User.objects.get(id=request.session['id']))
            return redirect('/books/'+number)
    else:
        return redirect('/books/')

def delete(request, number):
    if request.method =="POST":
        Review.objects.get(id = request.POST['review_id']).delete()
        return redirect('/books/'+number)
    else:
        return redirect('/books/')