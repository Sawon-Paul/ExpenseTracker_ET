from django.urls import path
from .views import register_page, login_page, dashboard_page, logout_view,change_password,update_profile_page,home_view,contact_view,contactus_page,setting_page,delete_account_page, SendOTP, RegisterView, LoginView, DeleteAccountView

urlpatterns = [
    path('register/', register_page, name='register'),
    path('', home_view, name='home'),
    path('contact_us/',contactus_page,name='contact_us'),
    path('contact/', contact_view, name='contact'),
    path('login/', login_page, name='login'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('logout/', logout_view, name='logout'),  # Logout path
    path('setting/',setting_page,name='setting'),
    path('send-otp/', SendOTP.as_view(), name='send-otp'),
    path('register-api/', RegisterView.as_view(), name='register_api'),
    path('login-api/', LoginView.as_view(), name='login_api'),
    path('delete_account/', delete_account_page, name='delete_account'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account_api'),
    path('change-password/', change_password, name='change_password'),
    path('update_profile/', update_profile_page, name='update_profile_page'),
]