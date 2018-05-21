from django.db import models
from django.apps import apps


# Create your models here.
from ..register.models import User

class MessageManager(models.Manager):
      def message(self,data):
            errors= {}
            if len(data['messagebox'])<1:
                  errors["message"] = "Message cannot be empty!"
            return errors 

class CommentManager(models.Manager):
      def comment(self,data):
            errors= {}
            if len(data['commentbox'])<1:
                  errors["comment"] = "Comment cannot be empty!"
            return errors 


class Message(models.Model):
      text = models.TextField()
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      page = models.ForeignKey(User, related_name="pages")
      poster = models.ForeignKey(User, related_name="messages")
      objects = MessageManager()

class Comment(models.Model):
      text = models.TextField()
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      message = models.ForeignKey(Message, related_name='comments')
      poster = models.ForeignKey(User, related_name="comments")
      page = models.ForeignKey(User,on_delete=models.CASCADE, related_name="pages_comments")
      objects = CommentManager()
