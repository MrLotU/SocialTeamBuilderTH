from urllib.parse import quote_plus

from braces.views import PrefetchRelatedMixin
from django.contrib.auth.views import redirect_to_login
from django.forms import HiddenInput, Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView)

from .forms import PositionFormSet, ProjectForm
from .models import Need, Project


class DeleteProject(DeleteView):
    model = Project
    success_url = reverse_lazy('projects:index')

class ProjectDetail(PrefetchRelatedMixin, DetailView):
    model = Project
    template_name = "projects/project.html"
    prefetch_related = ('positions',)

class CreateProject(TemplateView): # pylint: disable=too-many-ancestors
    # model = Project
    template_name = 'projects/project_new.html'
    # fields = ['needs_internal', 'timeline', 'title', 'description', 'requirements', 'creator']

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(reverse_lazy(
                'projects:new'
            ))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.POST:
            form = ProjectForm(self.request.POST)
            formset = PositionFormSet(self.request.POST, prefix='formset')
        else:
            form = ProjectForm()
            formset = PositionFormSet(prefix='formset')            
        form.fields['timeline'].widget = Textarea()
        form.fields['requirements'].widget = Textarea()
        context['form'] = form
        context['posForm'] = formset
        return context


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(reverse_lazy(
                'projects:new'
            ))

        form = ProjectForm(request.POST)
        formset = PositionFormSet(request.POST, prefix='formset')

        if form.is_valid() and formset.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            for form in formset:
                if form.is_valid():
                    p = form.save(commit=False)
                    p.project = project
                    p.slug = p.name.lower().replace(' ', '_')
                    p.save()
                else:
                    return super().get(request, *args, **kwargs)
            return HttpResponseRedirect(reverse_lazy(
                'projects:detail',
                kwargs={
                    'pk': project.pk
                }
            ))

        return super().get(request, *args, **kwargs)
    #     return super().post(request, *args, **kwargs)

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields['needs_internal'].required = False
    #     form.fields['needs_internal'].widget = HiddenInput()

    #     return form

    # def form_valid(self, form):
    #     form.instance.creator = self.request.user
    #     print(form)

    #     return super().form_valid(form)

    # Regex = r'\d+ (month|day|week|year|hour)s?'

class Index(PrefetchRelatedMixin, ListView): # pylint: disable=too-many-ancestors
    model = Project
    template_name = "projects/index.html"
    prefetch_related = ('positions',)

    def get_queryset(self):
        need = self.request.GET.get('n', None)
        if not need:
            return super().get_queryset()
        return self.model.objects.filter(position__slug=need).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        _needs = list(
            Project.objects.all()
            .select_related('position')
            .values('position__slug', 'position__name')
        )
        blacklist = []
        def f(i): # pylint: disable=invalid-name
            if i['position__slug'] in blacklist:
                return False
            blacklist.append(i['position__slug'])
            return True
        needs = filter(f, _needs)
        need = self.request.GET.get('n', None)
        def c(n): # pylint: disable=invalid-name
            n['selected'] = n['position__slug'] == need
            return n
        needs = list(map(c, needs))
        context['needs'] = needs
        context['no_need_selected'] = not need
        return context
