from django.db.models import Model, CharField

class Project(Model):
    pass

class Need(Model):
    name = CharField(max_length=255)

    selected = False
