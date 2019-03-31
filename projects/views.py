from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from .models import Project, Need
from django.forms import HiddenInput


class CreateProject(CreateView): # pylint: disable=too-many-ancestors
    model = Project
    template_name = 'projects/project_new.html'
    fields = ['needs_internal', 'timeline', 'title', 'description', 'requirements', 'creator']

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(reverse_lazy(
                'projects:new'
            ))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(reverse_lazy(
                'projects:new'
            ))
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['needs_internal'].required = False
        form.fields['needs_internal'].widget = HiddenInput()

        return form

    def form_valid(self, form):
        form.instance.creator = self.request.user
        print(form)

        return super().form_valid(form)

    # Regex = r'\d+ (month|day|week|year|hour)s?'

class Index(ListView): # pylint: disable=too-many-ancestors
    model = Project
    template_name = "projects/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        needs = Need.objects.all()
        need = self.request.GET.get('need', None)
        if not need:
            context['no_need_selected'] = True
        else:
            def check_need(n):
                n.selected = n.slug == need
                return n

            needs = list(map(check_need, needs))

        context['needs'] = needs
        context['projects'] = [
            {'title': 'Invoice delivery tool', 'formatted_needs': 'Rails Developer'},
            {'title': 'Twitter client', 'formatted_needs': 'Designer'}
        ]
        return context
