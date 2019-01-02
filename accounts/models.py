from django.contrib.auth.models import User
from django.db.models import (CASCADE, CharField, ImageField, ManyToManyField,
                              Model, OneToOneField, SlugField, TextField)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy

# from projects.models import Project

class Skill(Model):
    """Skill a User can have"""
    name = CharField(max_length=255)

class UserProfile(Model):
    """Profile for a user"""
    user = OneToOneField(User, on_delete=CASCADE)
    slug = SlugField(unique=True, allow_unicode=True, default='')
    bio = TextField(default="")
    pfp = ImageField()
    skills = ManyToManyField(Skill)
    # projects= ManyToManyField(Project)

    def get_absolute_url(self):
        return reverse_lazy("accounts:profile", kwargs={'slug': self.user.username})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a UserProfile when a User is created"""
    if created:
        UserProfile.objects.create(user=instance, slug=instance.username).save()