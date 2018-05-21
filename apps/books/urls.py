from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^addbook', views.addbook),
    url(r'(?P<number>\d+)/delete', views.delete),
    url(r'(?P<number>\d+)/$', views.book), 
    url(r'(?P<number>\d+)/review', views.addreview), 
    url(r'user/(?P<number>\d+)', views.userbooks),

]
 