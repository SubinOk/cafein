from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'main'
urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('login/', views.login, name='login'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]