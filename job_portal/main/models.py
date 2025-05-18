from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Резюме пользователя {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employer = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    resume = models.OneToOneField(Resume, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
    
    def can_be_deleted_by(self, user):
        return self.user == user

class Job(models.Model):
    CATEGORIES = [
        ('IT', 'Информационные технологии'),
        ('SALES', 'Продажи'),
        ('MARKETING', 'Маркетинг'),
        ('FINANCE', 'Финансы'),
        ('HR', 'Кадры'),
        ('OTHER', 'Другое'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('ENTRY', 'Стартовая'),
        ('JUNIOR', 'Юниор'),
        ('MID', 'Средний'),
        ('SENIOR', 'Сеньор'),
        ('LEAD', 'Лид'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    experience_level = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_LEVELS,
        default='ENTRY' 
    )
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, default='Удаленно')
    is_remote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def can_be_deleted_by(self, user):
        return self.employer.user == user

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'В ожидании'),
        ('REVIEWED', 'Рассмотрена'),
        ('ACCEPTED', 'Принята'),
        ('REJECTED', 'Отклонена'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заявка на {self.job.title} от {self.applicant.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.message[:50]}"