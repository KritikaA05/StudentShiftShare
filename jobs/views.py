from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import UserRegistrationForm, ProfileForm, JobForm, JobApplicationForm
from .models import Job, JobApplication, Profile

# Utility functions
def is_employer(user):
    return user.role == 'employer'

def is_student(user):
    return user.role == 'student'

# Home View
def home(request):
    return render(request, 'jobs/home.html')

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'jobs/register.html', {'form': form})

# Profile View
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Failed to update profile.')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'jobs/profile.html', {'form': form})

# Dashboard View
@login_required
def dashboard(request):
    return render(request, 'jobs/dashboard.html')

# Job Posting View
@login_required
@user_passes_test(is_employer, login_url='dashboard')
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_listings')
        else:
            messages.error(request, 'Failed to post the job.')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

# Job Listings View
def job_listings(request):
    job_list = Job.objects.all().order_by('-posted_at')
    paginator = Paginator(job_list, 10)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    return render(request, 'jobs/job_listings.html', {'jobs': jobs})

# Job Detail View
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user.role == 'student':
        already_applied = JobApplication.objects.filter(job=job, student=request.user).exists()
        return render(request, 'jobs/job_detail_student.html', {'job': job, 'already_applied': already_applied})
    elif request.user.role == 'employer':
        applications = JobApplication.objects.filter(job=job)
        return render(request, 'jobs/job_detail_employer.html', {'job': job, 'applications': applications})
    else:
        return redirect('dashboard')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# Apply for Job View
@login_required
@user_passes_test(is_student, login_url='dashboard')
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.student = request.user
            application.save()
            messages.success(request, "You successfully applied for the job!")
            return redirect('job_listings')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

# View Applications View
@login_required
@user_passes_test(is_employer, login_url='dashboard')
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.all()
    return render(request, 'jobs/view_applications.html', {'job': job, 'applications': applications})

# Application Detail View
@login_required
@user_passes_test(is_employer, login_url='dashboard')
def application_detail(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, job__employer=request.user)
    return render(request, 'jobs/application_detail.html', {'application': application})

# Static Pages
def about_us(request):
    return render(request, 'jobs/about_us.html')

def contact_us(request):
    return render(request, 'jobs/contact_us.html')

def terms_of_services(request):
    return render(request, 'jobs/terms_of_services.html')

def privacy_policy(request):
    return render(request, 'jobs/privacy_policy.html')
