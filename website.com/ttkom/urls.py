from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [

    # lookup user
    path("utilisateur/<int:pk>", views.DetailUser.as_view(), name="detail_user"),
    
    # password recovery
    path("reinitialiser_le_mot_de_pass/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("reinitialiser_le_mot_de_pass/valider/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reinitialiser/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reinitialiser/valider/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # edit account
    path("compte/", views.account, name="edit_account"),
    path("changer_le_mdp/", auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy("login"),
    ), name="password_change"),

    # register
    path("S\'inscrire/", views.register_view, name="register"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name='activate'),
    path("account_activation_sent/", views.account_activation_send, name='account_activation_sent'),

    # login
    path("connextion/", auth_views.LoginView.as_view(), name="login"),
    path("deconnection/", auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name="logout"),

    # post
    path('', views.index, name="home"),
    path('detail_du_post/<slug:pk>', views.post_detail_view, name="post_detail"),
    path("like/<int:pk>", views.like_view, name="like_post"),

]
