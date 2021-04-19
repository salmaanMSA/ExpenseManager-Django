from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register',RegistrationView.as_view(),name="register"),
    path('login',LoginView.as_view(),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name="activate"),
    #path('request-reset-link',RequestPasswordResetEmail.as_view(),name="reset-password"),
    #path('set-new-password/<uidb64>/<token>',CompletePasswordReset.as_view(),name="reset-user-password"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "authentication/reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "authentication/password_reset_sent.html"), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "authentication/reset_password_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "authentication/password_reset_done.html"), name='password_reset_complete'),
    
]
