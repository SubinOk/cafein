from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'main'
urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.singup, name ='signup'),
    path('search/', views.search, name ='search'),
    
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),

]

