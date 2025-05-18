from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Job, Application, Resume

class UserRegistrationForm(UserCreationForm):
    is_employer = forms.BooleanField(required=False, label='Работодатель')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company_name', 'bio', 'location', 'phone', 'website', 'profile_picture']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['employer', 'created_at']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }

class JobSearchForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ChoiceField(choices=[('', 'All')] + Job.CATEGORIES, required=False)
    experience_level = forms.ChoiceField(choices=[('', 'All')] + Job.EXPERIENCE_LEVELS, required=False)
    location = forms.CharField(required=False)
    is_remote = forms.BooleanField(required=False)
    min_salary = forms.DecimalField(required=False)