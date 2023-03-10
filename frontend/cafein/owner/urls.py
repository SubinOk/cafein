from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'owner'
urlpatterns = [
    path('home/', views.ownerHome, name='ownerHome'),
    path('checkPassword/', views.checkPassword, name='checkPassword'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.ownerDelete, name='ownerDelete'), 
    path('change/', views.ownerChange, name='ownerChange'),
    path('manage/', views.ownerManage, name='ownerManage'),
    path('statistics/', views.ownerStatistics, name='ownerStatistics'),
    path('coment/', views.ownerComent, name='ownerComent'),
    path('coment/<int:reviewid>/', views.ownerComentDetail, name='ownerComentDetail'),
    path('upload/', views.ownerCommentUpload, name='ownerCommentUpload'),
    path('menu/', views.ownerManageMenu, name='ownerManageMenu'),
    path('checkCafeData/', views.checkCafeData, name='checkCafeData '),
    path('cafeDataUpdata/', views.review_update, name='review_update '),
]