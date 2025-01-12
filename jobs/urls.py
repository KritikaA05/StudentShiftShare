from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import all views from the current app

urlpatterns = [
    # Home and Auth URLs
     path('', views.home, name='home'),
     path('login/', views.login_view, name='login'),
     path('register/', views.register_view, name='register'),
     path('dashboard/', views.dashboard_view, name='dashboard'),
     path('profile/', views.profile, name='profile'),
     path('logout/', views.logout_view, name='logout'),  # Custom logout view
   
    
   
    
    # Job URLs
    path('post_job/', views.post_job, name='post_job'),
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),  # Job details
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),  # Apply for job
    path('jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),  # View applications for a job
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),  # View application details

   # Informational URLs
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_services/', views.terms_of_services, name='terms_of_services'),
]
