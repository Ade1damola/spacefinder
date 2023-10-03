from django.urls import path
from . import views

urlpatterns =[
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('register', views.registerPage, name="register"),

    path('update-user/', views.updateUser, name="update-user"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('newsletter-subscription', views.subscribe_to_newsletter, name="subscribe_to_newsletter"),

    path('', views.home, name="home"),

    path('space/<str:pk>/', views.space, name="space"),
    path('create-space/', views.createSpace, name="create-space"),
    path('update-space/<str:pk>/', views.updateSpace, name="update-space"),
    path('delete-space/<str:pk>/', views.deleteSpace, name="delete-space"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

]