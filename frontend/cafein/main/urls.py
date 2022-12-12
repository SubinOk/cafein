from . import views
from django.urls import path, include

app_name = 'main'
urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('login/', views.login, name='login'),
]