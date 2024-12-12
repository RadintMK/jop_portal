# main/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Notification
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=Application)
def create_application_notification(sender, instance, created, **kwargs):
    if created:
        # Уведомление для работодателя
        Notification.objects.create(
            user=instance.job.employer,
            message=f'New application received for {instance.job.title} from {instance.applicant.username}'
        )
        
        # Уведомление для соискателя
        Notification.objects.create(
            user=instance.applicant,
            message=f'Your application for {instance.job.title} has been submitted successfully'
        )
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)