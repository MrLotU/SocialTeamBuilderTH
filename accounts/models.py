from django.contrib.auth.models import User
from django.db.models import (CASCADE, CharField, ImageField, ManyToManyField,
                              Model, OneToOneField, SlugField, TextField, ForeignKey)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.core.mail import send_mail

def upload_dest(instance, filename):
    """Generates the destination to upload a pfp to"""
    return 'profile_pictures/{}/{}'.format(instance.user.id, filename)

class UserProfile(Model):
    """Profile for a user"""
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile')
    slug = SlugField(unique=True, allow_unicode=True, default='')
    bio = TextField(default="")
    pfp = ImageField(upload_to=upload_dest)
    skills_internal = TextField(default="")

    @property
    def skills(self):
        if self.skills_internal == '':
            return []
        return self.skills_internal.split(',')

    def get_absolute_url(self):
        return reverse_lazy("accounts:profile", kwargs={'slug': self.user.username})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a UserProfile when a User is created"""
    if created:
        UserProfile.objects.create(user=instance, slug=instance.username).save()

        send_mail(
            'Welcome!',
            f'Hi {instance.username}!\nThanks for signing up for a Circle account. We\'re glad to have you on board!\n\nKind regards,\nThe Circle team', # pylint: disable=line-too-long
            'welcome@circle.com',
            [instance.email],
            fail_silently=False
        )
