from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import *
from .forms import *

def home(request):
    recent_jobs = Job.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'recent_jobs': recent_jobs})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_employer = form.cleaned_data.get('is_employer')
            
            # Используем get_or_create для безопасного создания профиля
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'is_employer': is_employer}
            )

            if not created:
                profile.is_employer = is_employer
                profile.save()

            messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')

            return redirect('login')
    else:
        form = UserRegistrationForm()
        
    context = {'form': form}
    return render(request, 'register.html', context)

def jobs_list(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.filter(is_active=True)

    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        experience_level = form.cleaned_data.get('experience_level')
        location = form.cleaned_data.get('location')
        is_remote = form.cleaned_data.get('is_remote')
        min_salary = form.cleaned_data.get('min_salary')

        if search:
            jobs = jobs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        if category:
            jobs = jobs.filter(category=category)
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)
        if location:
            jobs = jobs.filter(location__icontains=location)
        if is_remote:
            jobs = jobs.filter(is_remote=True)
        if min_salary:
            jobs = jobs.filter(salary_min__gte=min_salary)

    return render(request, 'jobs_list.html', {
        'jobs': jobs,
        'form': form
    })

# main/views.py
@login_required
def profile(request):
    # Получаем или создаем профиль пользователя
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен успешно!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile
    }

    if user_profile.is_employer:
        context['jobs'] = Job.objects.filter(employer=request.user)
        context['applications'] = Application.objects.filter(job__employer=request.user)
    else:
        context['applications'] = Application.objects.filter(applicant=request.user)
        try:
            context['resume'] = Resume.objects.get(user=request.user)
        except Resume.DoesNotExist:
            context['resume'] = None

    return render(request, 'profile.html', context)

@login_required
def create_job(request):
    if not request.user.userprofile.is_employer:
        messages.error(request, 'Только работодатели могут публиковать вакансии!')
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Вакансия опубликована успешно!')
            return redirect('profile')
    else:
        form = JobForm()

    return render(request, 'create_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.user.userprofile.is_employer:
        messages.error(request, 'Работодатели не могут подавать заявки на вакансии!')
        return redirect('jobs_list')
        
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'Вы уже подали заявку на эту вакансию!')
        return redirect('jobs_list')

    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        resume = None

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.resume = resume
            application.save()
            messages.success(request, 'Заявка отправлена успешно!')
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'apply_job.html', {
        'form': form, 
        'job': job,
        'resume': resume
    })

@login_required
def upload_resume(request):
    resume_instance = Resume.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume_instance)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'Ваше резюме успешно обновлено.' if resume_instance else 'Ваше резюме успешно загружено.')
            return redirect('profile')
    else:
        form = ResumeForm(instance=resume_instance)

    return render(request, 'upload_resume.html', {'form': form})


@login_required
def notifications(request):
    notifications = request.user.notification_set.all().order_by('-created_at')
    # Отмечаем все уведомления как прочитанные
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.application_set.all()
    return render(request, 'view_applications.html', {'job': job, 'applications': applications})



def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user.userprofile)
    
    if job.employer.user != request.user:
        messages.error(request, 'У вас нет прав для удаления этой вакансии.')
        return redirect('profile')
    
    job.delete()
    messages.success(request, 'Вакансия успешно удалена!')
    return redirect('profile')