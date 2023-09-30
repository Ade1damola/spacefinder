from django.urls import path
from . import views

urlpatterns =[
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('register', views.registerPage, name="register"),

    path('update-user/', views.updateUser, name="update-user"),

    path('home', views.home, name="home"),
    path('', views.landingPage, name="landing-page"),
    path('space/', views.Space, name="space"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-space/', views.createSpace, name="create-space"),
]