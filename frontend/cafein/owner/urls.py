from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'owner'
urlpatterns = [
    path('login/', views.ownerLogin, name='ownerLogin'),
    path('logout/', views.ownerLogout, name='ownerLogout'),
    path('home/', views.ownerHome, name='ownerHome'),
    path('findPassword/', views.findPassword, name='findPassword'),
    path('checkPassword/', views.checkPassword, name='checkPassword'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.ownerDelete, name='ownerDelete'), 
    path('update/', views.ownerUpdate, name='ownerUpdate'),
    path('change/', views.ownerChange, name='ownerChange'),
    path('manage/', views.ownerManage, name='ownerManage'),
    path('statistics/', views.ownerStatistics, name='ownerStatistics'),
]