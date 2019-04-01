from django.forms import ModelForm, modelformset_factory, BaseFormSet
from .models import Project, Position

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['timeline', 'title', 'description', 'requirements']

class PosFormSet(BaseFormSet):
    def full_clean(self):
        super().full_clean()
        print(self._non_form_errors.as_data())
        for error in self._non_form_errors.as_data():
            if error.code == 'too_few_forms':
                error.message = 'Please add 1 or more positions'

PositionFormSet = modelformset_factory(
    Position,
    fields=('name', 'description', 'length'),
    min_num=1,
    validate_min=True,
    extra=0,
    formset=PosFormSet
)
