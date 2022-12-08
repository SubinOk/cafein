from . import views
from django.urls import path, include

app_name = 'owner'
urlpatterns = [
    path('login/', views.ownerLogin, name='ownerLogin'),
    path('findPassword/', views.findPassword, name='findPassword'),
    path('signup/', views.signup, name='signup'),

]