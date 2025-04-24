from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends_page, name='friends_page'),
    path('send_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('confirm_request/<int:request_id>/', views.confirm_friend_request, name='confirm_friend_request'),
    path('reject_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
