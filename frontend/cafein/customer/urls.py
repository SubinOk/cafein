from . import views
from django.urls import path
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