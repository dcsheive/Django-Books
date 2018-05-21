from django.db import models

# Create your models here.
from ..register.models import User

class ReviewManager(models.Manager):
    def addbook(self,data):
        errors = {}
        if len(data['title'])<5:
            errors['title'] = "Title must be at least 5 characters!"
        if len(data['authorlist']):
            if len(data['author'])>0 and len(data['authorlist'])>0:
                errors['author'] = "You may only choose one: select author or enter author!"
        if len(data['text'])<1:
            errors['review'] = "Please enter your review!"
        if len(data['author'])<1 and len(data['authorlist'])<1:
            errors['author'] = 'Choose an author!'
        if Author.objects.filter(name=data['author']):
            errors['author'] = "Author exists in list!"
        if Book.objects.filter(title=data['title']) and Book.objects.filter(author= data['author']):
            errors['title'] = "Book already exists in list!"
        return errors
    def addreview(self,data):
        errors ={}
        if len(data['text'])<1:
            errors['review'] = "Please enter your review!"
        return errors



class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(Author, related_name='books')
    objects = ReviewManager()

class Review(models.Model):
    stars = models.IntegerField(5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    objects = ReviewManager()