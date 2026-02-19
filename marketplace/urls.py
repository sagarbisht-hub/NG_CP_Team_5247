from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_page, name='login'),
    path('send-login-otp/', views.send_login_otp, name='send_login_otp'),
    path('verify-login-otp/', views.verify_login_otp, name='verify_login_otp'),
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job-request/', views.create_job_form, name='create_job_form'),
    path('job-tracking/<int:job_id>/', views.job_tracking, name='job_tracking'),
    path('create-job/', views.create_job, name='create_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('help/', views.help_page, name='help'),
    path('logout/', views.logout_view, name='logout'),
]
