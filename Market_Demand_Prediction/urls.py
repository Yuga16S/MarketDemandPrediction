"""
URL configuration for Market_Demand_Prediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views2
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from marketdemandpredictionapp import views
from marketdemandpredictionapp.views import RegisterView, forgot_password, ProfileView, BannerView, GuestView, \
    get_crop_description

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('predict/', views.predict, name='predict'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-reset/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('', BannerView.as_view(), name='banner'),
    path('guest/', GuestView.as_view(), name='guest'),
    path('get_crop_description/', views.get_crop_description, name='get_crop_description'),
]
