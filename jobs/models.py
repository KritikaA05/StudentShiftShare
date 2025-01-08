from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Custom User Model
class User(AbstractUser):
    STUDENT = 'student'
    EMPLOYER = 'employer'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (EMPLOYER, 'Employer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Job Model
class Job(models.Model):
    JOB_TYPES = [
        ('Part-Time', 'Part-Time'),
        ('Full-Time', 'Full-Time'),
        ('Internship', 'Internship'),
    ]
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, null=True, blank=True)
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

# Job Application Model
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"

# Shift Model
class Shift(models.Model):
    job_title = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

    def __str__(self):
        return f"{self.job_title} on {self.date} from {self.start_time} to {self.end_time}"

# Shift Collaboration Model
class ShiftCollaboration(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='shift_collaborations')
    student1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shift_student1')
    student2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shift_student2')
    agreed_at = models.DateTimeField(default=now)

    def clean(self):
        if self.student1 == self.student2:
            raise ValidationError("Students must be different.")

    def __str__(self):
        return f'{self.student1.username} & {self.student2.username} - {self.job.title}'

# Review Model
class Review(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    description = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'Review by {self.user.username} - {self.rating} Stars'

# Signals for Profile Auto-Creation
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
