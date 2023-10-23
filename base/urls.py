from django.urls import path
from . import views

urlpatterns =[
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('register', views.registerPage, name="register"),

    path('update-user/', views.updateUser, name="update-user"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('newsletter_subscription', views.subscribe_to_newsletter, name="newsletter_subscription"),

    path('', views.home, name="home"),
    path('hostel/', views.hostel, name="hostel"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('confirm_pay/', views.confirm_pay, name="confirm_pay"),

    path('new_registration/', views.new_registration, name="new_registration"),
    path('signup/', views.signup, name="signup"),

    path('space/<str:pk>/', views.space, name="space"),
    path('create-space/', views.createSpace, name="create-space"),
    path('update-space/<str:pk>/', views.updateSpace, name="update-space"),
    path('delete-space/<str:pk>/', views.deleteSpace, name="delete-space"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

]