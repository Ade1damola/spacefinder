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
    path('hostel/', views.hostel, name="hostel"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('confirm_pay/', views.confirm_pay, name="confirm_pay"),

# THE VIEWS I CREATED
    path('new_registration/', views.new_registration, name="new_registration"),
    path('signup/', views.signup, name="signup"),
    path('log_in/', views.log_in, name="log_in"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('link_sent/', views.link_sent, name="link_sent"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('password_changed/', views.password_changed, name="password_changed"),
    path('email_code/', views.email_code, name="email_code"),
    path('change_email/', views.change_email, name="change_email"),
    path('auth_error/', views.authentication_error, name="authentication_error"),
    path('verification_complete/', views.verification_complete, name="verification_complete"),
    path('access_denied/', views.access_denied, name="access_denied"),

    path('space/<str:pk>/', views.space, name="space"),
    path('create-space/', views.createSpace, name="create-space"),
    path('update-space/<str:pk>/', views.updateSpace, name="update-space"),
    path('delete-space/<str:pk>/', views.deleteSpace, name="delete-space"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

]