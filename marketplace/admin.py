from django.contrib import admin
from .models import Worker, Job

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['user', 'skills', 'rating', 'job_count', 'reliability_score']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'user', 'worker', 'price', 'created_at']
    list_filter = ['status', 'category', 'urgency']
