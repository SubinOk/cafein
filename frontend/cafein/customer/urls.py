from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'customer'
urlpatterns =[
    path('home/', views.customerHome, name='customerHome'),
    path('signup/', views.signup, name='signup'),
    path('<int:cafeId>/home', views.cafeHome, name='cafeHome'),
    path('review/', views.cafeReview, name='cafeReview'),
    path('<int:cafeId>/createReview', views.createReview, name='createReview'),
    path('<int:cafeId>/review/<int:reviewid>', views.cafeReviewDetail, name='cafeReviewDetail'),
    path('like/<int:cafeId>', views.cafeLike, name='cafeLike'),
    path('like/', views.index, name='cafeLikeList'),
    path('findCafe/', views.getCafeData, name='getCafeData'),
    path('<int:cafeId>/cafeReview/', views.cafeIdReview, name='cafeIdReview'),
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