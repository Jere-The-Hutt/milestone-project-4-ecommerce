from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile fields.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    phone = models.CharField(
        max_length=20,
        blank=True
        )
    bio = models.TextField(
        blank=True,
        max_length=500
        )
    company = models.CharField(
        max_length=100,
        blank=True
        )
    website = models.URLField(blank=True)
    profile_image = models.ImageField(
        upload_to='profiles/%Y/%m/%d/',
        blank=True
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable string representation of the user profile."""
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


# Automatically create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a UserProfile when a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to automatically save the associated
    UserProfile when the User is saved.
    """
    instance.profile.save()
