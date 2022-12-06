from . import views
from django.urls import path, include

app_name = 'owner'
urlpatterns = [
    path('login/', views.ownerlogin, name='ownerlogin'),
]