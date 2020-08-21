#-*- coding: utf-8 -*-
from django.urls import path
from . import views
from django.contrib import admin

app_name = 'mp3'

urlpatterns = [
	path('', views.index, name='home'),
	path('pass/', views.saveSong, name='save-song'),
]
