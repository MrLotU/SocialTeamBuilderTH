from django.contrib.auth.models import User
from django.db.models import (CASCADE, BooleanField, CharField, ForeignKey,
                              Manager, Model, TextField)
from django.db.utils import IntegrityError


class Project(Model):
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
    slug = CharField(max_length=255)

    @property
    def filledBy(self):
        return self.applications.get(accepted=True)

    def __init__(self, *args, **kwargs):
        try:
            kwargs['slug'] = kwargs['name'].lower().replace(' ', '_')
        except:
            pass
        super().__init__(*args, **kwargs)

class Application(Model):
    position = ForeignKey(Position, on_delete=CASCADE, related_name="applications")
    user = ForeignKey(User, on_delete=CASCADE, related_name="applications")
    accepted = BooleanField(default=False)
    denied = BooleanField(default=False)

    @property
    def status(self):
        if self.accepted:
            return 'Accepted'
        if self.denied:
            return 'Denied'
        return 'Awaiting judgement'
