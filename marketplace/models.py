from django.db import models
from django.contrib.auth.models import User

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=500)
    rating = models.FloatField(default=0.0)
    job_count = models.IntegerField(default=0)
    completed_jobs = models.IntegerField(default=0)
    reliability_score = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    is_new = models.BooleanField(default=True)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avatar = models.CharField(max_length=200, default='https://picsum.photos/100')
    technical_rating = models.FloatField(default=0.0)
    response_time = models.IntegerField(default=0)  # in minutes
    specialization = models.CharField(max_length=200, default='General')
    
    def __str__(self):
        return self.user.username

class Job(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    client_rating = models.FloatField(null=True, blank=True)
    ai_match_score = models.FloatField(default=0.0)
    estimated_duration = models.IntegerField(default=0)  # in hours
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bookings = models.IntegerField(default=0)
    average_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preferred_location = models.CharField(max_length=100, default='')
    loyalty_points = models.IntegerField(default=0)
    member_since = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Client Profile"
