from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),

    # Email Verification
    path('email-verification/<str:uidb64>/<str:token>', views.email_verification, name='email_verification'),
    path('email-verification-success/', views.email_verification_success, name='email_verification_success'),
    path('email-verification-sent/', views.email_verification_sent, name='email_verification_sent'),
    path('email-verification-failed/', views.email_verification_failed, name='email_verification_failed'),


    # Login/logout/dashboard
    path('login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='user_logout'),

    # Track order
    path('track-orders/', views.track_orders, name="track_orders"),
    path('manage-shipping/', views.manage_shipping, name="manage_shipping"),
    path('profile-update/', views.profile_update, name="profile_update"),
    path('profile-delete/', views.profile_delete, name="profile_delete"),


    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/password_reset/password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset/password_reset_complete.html"), name='password_reset_complete'),


    # Manage Shipping
    path('manage-shipping/', views.manage_shipping, name='manage_shipping'),


    # Track Order
    path('track-orders/', views.track_orders, name='track_orders'),


]






##### if user does not activate account, form should be deleted.