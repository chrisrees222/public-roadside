from django.urls import path, include
from .views import homeView, UserProfile, register, user_login, user_logout, delete_profile, profile_settings, change_password, select_payment
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', homeView, name='home-page'),
    path('profile/', UserProfile.as_view(), name='user-profile' ),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('about/', view=views.about, name='about'),  
    path('recoverycompanies/', view=views.recoverycompanies, name='recoverycompanies'),  
    path('contactus/', view=views.contactus, name='contactus'), 
    path('companydetail/<int:pk>', views.ProfileDetailView.as_view(), name='company_details'),
      
    path("config/", views.stripe_config),
    path("create-checkout-session-thirty/", views.create_checkout_session_thirty),
    path("create-checkout-session-sixty/", views.create_checkout_session_sixty),
    path("create-checkout-session-ninety/", views.create_checkout_session_ninety),
    path("webhook", views.my_webhook_view),
    path("success/", views.success),
    path("cancel/", views.cancel), 
    path('select_payment/', select_payment, name='select_payment'),
     
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('profile_settings/', profile_settings, name='profile_settings'),
    path("change_password", views.change_password, name="change_password"), 
    path('captcha/', include('captcha.urls')),   
    
    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)