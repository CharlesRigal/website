from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # static views
    path("", views.index, name="home"),
]
