from django.urls import path
from . import views
from .views import modelview
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('modelview', modelview, name='modelview'),
    path('generate_images', views.generate_images, name='generate_images'),
    path('login_view', views.login_view, name='login_view'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('signup', views.signup_view, name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
