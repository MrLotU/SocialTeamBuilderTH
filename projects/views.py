from braces.views import PrefetchRelatedMixin
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.forms import Textarea
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (DeleteView, DetailView, ListView,
                                  RedirectView, TemplateView)

from .constants import get_application_filters
from .forms import PositionFormSet, ProjectForm
from .models import Application, Position, Project


class DeleteProject(RedirectView):
    url = reverse_lazy('projects:index')

    def get(self, request, pk, *args, **kwargs):
        m = Project.objects.get(pk=pk)
        if not request.user.is_authenticated or not m.creator == request.user:
            return HttpResponseRedirect(reverse_lazy('projects:detail', kwargs={
                'pk': m.pk
            }))
        m.delete()
        return super().get(request, pk=pk, *args, **kwargs)


class HandleApplicationView(RedirectView):
    def get_redirect_url(self, pk, *args, **kwargs): 
        return reverse_lazy('projects:applications', kwargs={
            'pk': pk
        })

    def get(self, request, pk, app, s, *args, **kwargs): 
        project = Project.objects.get(pk=pk)
        if not request.user.is_authenticated or not project.creator == request.user:
            return HttpResponseRedirect(reverse_lazy('projects:detail', kwargs={
                'pk': pk
            }))
        res = super().get(request, *args, **kwargs, pk=pk, app=app, s=s)
        app = Application.objects.get(pk=app)
        if not s in [0, 1]:
            return res
        if s == 1:
            app.accepted = True
            app.position.filled = True
            app.position.save()
        else:
            app.denied = True
        app.save()
        return res

class ApplicationsView(TemplateView):
    template_name = "projects/applications.html"

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        if not request.user.is_authenticated or not project.creator == request.user:
            return HttpResponseRedirect(reverse_lazy('projects:detail', kwargs={
                'pk': kwargs['pk']
            }))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=kwargs['pk'])
        context['project'] = project
        context['projects'] = Project.objects.filter(creator=self.request.user)
        f = None
        try:
            f = int(self.request.GET.get('f', None))
        except (ValueError, TypeError):
            pass
        filters = [{'name': v, 'selected': i == f} for i, v in enumerate(get_application_filters())]
        if not f:
            filters[0]['selected'] = True
        context['filters'] = filters
        apps = Application.objects.filter(position__project__pk=kwargs['pk'])
        if f == 1:
            apps = apps.filter(position__filled=False, accepted=False, denied=False)
        elif f == 2:
            apps = Application.objects.filter(position__filled=True, accepted=True)
        elif f == 3:
            apps = Application.objects.filter(denied=True)
        context['applications'] = apps
        return context

class ProjectDetail(PrefetchRelatedMixin, DetailView):
    model = Project
    template_name = "projects/project.html"
    prefetch_related = ('positions',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        apped_positions = []
        for pos in obj.positions.all():
            for app in pos.applications.all():
                if app.user == self.request.user:
                    apped_positions.append(pos)
        context['apped_positions'] = apped_positions
        return context


class ProjectApply(RedirectView):
    def get_redirect_url(self, pk, *args, **kwargs): 
        return reverse_lazy('projects:detail', kwargs={
            'pk': pk
        })

    def get(self, request, pk, pos, *args, **kwargs): 
        if not request.user.is_authenticated:
            return redirect_to_login(reverse_lazy(
                'projects:detail', kwargs={
                    'pk': pk
                }
            ))
        Application.objects.create(
            user=request.user,
            position=Position.objects.get(pk=pos)
        )
        return super().get(request, pk=pk, pos=pos * args, **kwargs)


class CreateProject(TemplateView): 
    template_name = 'projects/project_new.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(reverse_lazy(
                'projects:new'
            ))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class Index(PrefetchRelatedMixin, ListView): 
    model = Project
    template_name = "projects/index.html"
    prefetch_related = ('positions',)

    def get_queryset(self):
        need = self.request.GET.get('n', None)
        search = self.request.GET.get('s', None)
        filter_filled = self.request.GET.get('f', None)
        if not need and not search:
            return super().get_queryset()
        base = self.model.objects
        if search:
            base = base.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if need:
            if filter_filled:
                base = base.filter(position__filled=False, position__slug=need).distinct()
            else:
                base = base.filter(position__slug=need).distinct()
        return base

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        _needs = list(
            Project.objects.all()
            .select_related('position')
            .values('position__slug', 'position__name')
        )
        blacklist = []

        def f(i): 
            if i['position__slug'] in blacklist:
                return False
            blacklist.append(i['position__slug'])
            return True
        needs = filter(f, _needs)
        need = self.request.GET.get('n', None)

        def c(n): 
            n['selected'] = n['position__slug'] == need
            return n
        needs = list(map(c, needs))
        context['needs'] = needs
        context['s'] = self.request.GET.get('s')
        context['n'] = self.request.GET.get('n')
        context['f'] = self.request.GET.get('f')
        context['no_need_selected'] = not need
        return context
