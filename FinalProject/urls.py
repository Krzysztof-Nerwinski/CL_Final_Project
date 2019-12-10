"""FinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from timer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/logout/', LogoutView, name='logout'),
    # path('accounts/password_change/', PasswordChangeView, name='password_change'),
    # path('accounts/password_change/done/', PasswordChangeDoneView, name='password_change_done'),
    # path('accounts/password_reset/', PasswordResetView, name='password_reset'),
    # path('accounts/password_reset/done/', PasswordResetDoneView, name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView, name='password_reset_confirm'),
    # path('accounts/reset/done/', PasswordResetCompleteView, name='password_reset_complete'),
    path('', include('timer.urls')),


]
