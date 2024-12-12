# main/admin.py
from django.contrib import admin
from .models import UserProfile, Job, Application, Resume, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_employer', 'company_name', 'location']
    list_filter = ['is_employer']
    search_fields = ['user__username', 'company_name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'category', 'location', 'created_at', 'is_active']
    list_filter = ['category', 'experience_level', 'is_remote', 'is_active']
    search_fields = ['title', 'description', 'employer__username']
    date_hierarchy = 'created_at'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['job__title', 'applicant__username']
    date_hierarchy = 'created_at'

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'uploaded_at']
    search_fields = ['user__username']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_read', 'created_at']
    list_filter = ['is_read']
    search_fields = ['user__username', 'message']