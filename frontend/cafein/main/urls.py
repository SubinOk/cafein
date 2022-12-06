from . import views
from django.urls import path, include

app_name = 'main'
print("text")
urlpatterns = [
    path('', views.login, name='login'),
    path('/ownerlogin/', include('owner.urls'))
]