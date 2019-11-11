from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('signin/', views.sign_in, name='sign_in'),
    path('signup/', views.sign_up, name='sign_up'),
    path('signout/', views.sign_out, name='sign_out'),
    path('user_info/', views.user_info, name='user_info'),
    path('nickname_change/', views.nickname_change, name='nickname_change'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
]