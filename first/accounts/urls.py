from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from .import views
from  django.contrib.auth.views import login

urlpatterns = [
    path(r'',views.home),
    path(r'login/',login,{'template_name':'accounts/login.html'})
    path(r'ask/',views.answer),
]
