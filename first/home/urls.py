from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from home import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
]
