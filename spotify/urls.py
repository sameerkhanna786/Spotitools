from django.urls import path
from . import views
import requests

urlpatterns = [
    path('', views.home, name='spotify-home'),
    path('sign-in/', views.sign_in, name='spotify-login'),
	path('after-sign-in/', views.after_sign_in, name='after-sign-in'),
	path('form-filled/', views.form, name = 'spotify-form')
]