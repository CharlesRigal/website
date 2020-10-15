from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # static views
    path('', views.index, name="home"),
    path('detail_du_post/<slug:pk>', views.post_detail_view, name="post_detail"),
    path("like/<int:pk>", views.like_view, name="like_post"),
]
