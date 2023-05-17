from django.urls import path
from .views import*
urlpatterns = [
    path('signup',user_signup,name='signup'),
    path('signin',signin,name='signin'),
    path('signout',signout,name='signout'),
    path('forgot',forgot_password,name='forgot'),
    path('otp_verification/<str:username>/',otp_verify,name='otp_verify'),
    path('password_change/<str:username>/',password_change,name='password_change'),
    # path('login_otp/<str:username>/',login_otp,name='login_otp')


]