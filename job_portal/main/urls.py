from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('profile/', views.profile, name='profile'),
    path('create-job/', views.create_job, name='create_job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('notifications/', views.notifications, name='notifications'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
]