from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^getuser$', views.getuser),
    url(r'^create$', views.create),
    url(r'^createuser', views.createuser),
    url(r'(?P<number>\d+)/$', views.user), 
    url(r'(?P<number>\d+)/edit$', views.edit),
    url(r'(?P<number>\d+)/update$', views.update),
    url(r'(?P<number>\d+)/updatepassword$', views.updatepassword),
    url(r'(?P<number>\d+)/delete$', views.delete),
    url(r'(?P<number>\d+)/message$', views.message),
    url(r'(?P<number>\d+)/comment$', views.comment),
    url(r'(?P<number>\d+)/deletemessage', views.deletemessage),
    url(r'(?P<number>\d+)/deletecomment', views.deletecomment),
    url(r'(?P<number>\d+)/makeadmin', views.makeadmin),
    url(r'(?P<number>\d+)/follow$', views.follow),
    url(r'(?P<number>\d+)/followers', views.followers),
    url(r'(?P<number>\d+)/followings', views.followings),
    url(r'^dashboard', views.dashboard), 
]