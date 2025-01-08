from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import all views from the current app

urlpatterns = [
    # Home and Auth URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Custom logout view
    
    # Profile & Dashboard
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Job URLs
    path('post_job/', views.post_job, name='post_job'),
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),  # Job details
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),  # Apply for job
    path('jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),  # View applications for a job
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),  # View application details
]
