from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, JobForm, JobApplicationForm
from .models import Job, JobApplication, Profile

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
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('dashboard')  # Change this to your intended redirect
        else:
            messages.error(request, 'Registration failed. Please try again.')
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
def post_job(request):
    if request.user.role != 'employer':
        messages.error(request, "Only employers can post jobs.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to post the job. Please try again.')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})

# Job Listings View
def job_listings(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'jobs/job_listings.html', {'jobs': jobs})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role == 'student':
        # Students should see job details and apply option
        already_applied = JobApplication.objects.filter(job=job, student=request.user).exists()
        return render(request, 'jobs/job_detail_student.html', {
            'job': job, 
            'already_applied': already_applied
        })

    elif request.user.role == 'employer':
        # Employers should see job applications
        applications = JobApplication.objects.filter(job=job)
        return render(request, 'jobs/job_detail_employer.html', {
            'job': job,
            'applications': applications
        })

    else:
        # Redirect other roles
        return redirect('dashboard')

    
# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# Apply for job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user.role != 'student':
        return redirect('dashboard')

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

@login_required
def view_applications(request, job_id):
     job = get_object_or_404(Job, id=job_id, employer=request.user)
     applications = job.applications.all()
     return render(request, 'jobs/view_applications.html', {'job': job, 'applications': applications})

@login_required
def application_detail(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, job__employer=request.user)
    return render(request, 'jobs/application_detail.html', {'application': application})

@login_required
def student_dashboard(request):
    jobs = Job.objects.all()
    return render(request, 'dashboard/student_dashboard.html', {'jobs': jobs})
