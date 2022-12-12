from . import views
from django.urls import path, include

app_name = 'owner'
urlpatterns = [
    path('login/', views.ownerLogin, name='ownerLogin'),
    path('logout/', views.ownerLogout, name='ownerLogout'),
    path('home/', views.ownerHome, name='ownerHome'),
    path('checkPassword/', views.checkPassword, name='checkPassword'),
    path('findPassword/', views.findPassword, name='findPassword'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.ownerDelete, name='ownerDelete'),
]