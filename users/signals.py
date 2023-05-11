from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile


@receiver(post_save, sender=User)
def user_create(sender, instance, created, **kwargs):
    print("user_create")
    if created:
        print("profile created")
        my_profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.first_name
        )

        # send_mail(
        #     "Welcome to Example",
        #     "You account was scucessfully created, great work",
        #     settings.EMAIL_HOST_USER,
        #     [my_profile.email],
        #     False
        # )


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass
    except Exception as e:
        # Handle other exceptions, such as database-related errors
        print(f"An error occurred while deleting the user: {str(e)}")


@receiver(post_save, sender=Profile)
def edit_profile(sender, instance, created, **kwargs):
    print("edit_profile")
    if created is False:
        print("edit_profile created")
        profile = instance
        user = profile.user
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.email = profile.email
        user.save()
