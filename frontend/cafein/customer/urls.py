from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'customer'
urlpatterns =[
    path('home/', views.customerHome, name='customerHome'),
    path('signup/', views.signup, name='signup'),
    path('<cafeName>/home', views.cafeHome, name='cafeHome'),
    path('review/', views.cafeReview, name='cafeReview'),
    path('<cafeName>/createReview', views.createReview, name='createReview'),
    path('<cafeName>/review/<int:reviewid>', views.cafeReviewDetail, name='cafeReviewDetail'),
    path('like/<cafeName>', views.cafeLike, name='cafeLike'),
    path('like/', views.index, name='cafeLikeList'),
    path('findCafe/', views.getCafeData, name='getCafeData'),
]

# urlpatterns = [
#     path('login/', views.ownerLogin, name='ownerLogin'),
#     path('logout/', views.ownerLogout, name='ownerLogout'),
#     path('home/', views.ownerHome, name='ownerHome'),
#     path('checkPassword/', views.checkPassword, name='checkPassword'),
#     path('signup/', views.signup, name='signup'),
#     path('delete/', views.ownerDelete, name='ownerDelete'), 
#     path('change/', views.ownerChange, name='ownerChange'),
#     path('manage/', views.ownerManage, name='ownerManage'),
#     path('statistics/', views.ownerStatistics, name='ownerStatistics'),
#     path('statistics/detail', views.ownerStatisticsDetail, name='ownerStatisticsDetail'),
# ]