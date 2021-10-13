from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from product.views import ProductUpdateView
from . import views
from .views import SignInView, profile, AccountUpdateView, user_delete

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('myprofile/', profile, name='profile'),

    path('delete_account/<int:id>', user_delete, name='delete_account'),
    path('update_account/<int:pk>', AccountUpdateView.as_view(), name='update_account'),

    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),


]