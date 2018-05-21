from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [ 
    url(r'^$', views.index), 
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^signin', views.signin),
    url(r'^reg', views.reg),
 
] 