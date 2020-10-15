from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # post
    path('', views.index, name="home"),
    path('detail_du_post/<slug:pk>', views.post_detail_view, name="post_detail"),
    path("like/<int:pk>", views.like_view, name="like_post"),

    # login
    path("connextion/", auth_views.LoginView.as_view(), name="login"),
    path("deconnection/", auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name="logout"),
]
