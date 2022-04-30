from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.homePage, name='home'),


    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='login/reset_password.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='login/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='login/reset.html'), name='password_reset_confirm'),
    path('reset_passowrd_complete', auth_views.PasswordResetCompleteView.as_view(template_name='login/reset_password_complete.html'), name='password_reset_complete'),

    path('ticket/', views.ticket, name='ticket'),
    path('buyTicket/', views.buyTicket, name='buyTicket'),
    path('ticketChecker/<str:pk>/', views.ticketChecker, name='ticketChecker'),
    path('ticketState/<str:pk>/', views.ticketState, name='ticketState'),

    path('map/', views.map, name='map'),
]
