from braces.views import PrefetchRelatedMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from .models import Project, Need
from django.forms import HiddenInput, Textarea
from .forms import ProjectForm, PositionFormSet

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        print(context)
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
        return context
