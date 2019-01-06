from django.http import HttpResponse
from django.views.generic import ListView
from .models import Project, Need

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Projects index.")

class Index(ListView):
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
                if n.name == need:
                    n.selected = True
                return n

            needs = list(map(check_need, needs))
        
        context['needs'] = needs
        return context

