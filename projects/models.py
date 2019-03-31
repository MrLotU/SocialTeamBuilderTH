from django.db.models import Model, CharField, Manager, BooleanField, TextField, ForeignKey, CASCADE
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

class Project(Model):
    needs_internal = TextField(default="")
    timeline = CharField(max_length=255)
    title = CharField(max_length=255)
    description = TextField(default="")
    requirements = TextField(default="")

    creator = ForeignKey(User, CASCADE, related_name='created_projects')

class Position(Model):
    project = ForeignKey(Project, CASCADE, related_name='positions', related_query_name='position')
    name = CharField(max_length=255)
    description = TextField(default="")
    filled = BooleanField(default=False)
    length = CharField(max_length=255)

class NeedManager(Manager):
    def get_or_create(self, *args, **kwargs):
        print(args, kwargs)
        try:
            return super().get_or_create(*args, **kwargs)
        except IntegrityError:
            slug = kwargs['name'].lower().replace(' ', '_')
            return (super().get(slug=slug), False)

class Need(Model):
    name = CharField(max_length=255)
    slug = CharField(max_length=255, unique=True)

    objects = NeedManager()

    def __init__(self, *args, **kwargs):
        try:
            kwargs['slug'] = kwargs['name'].lower().replace(' ', '_')
        except:
            pass
        super().__init__(*args, **kwargs)

    selected = False
