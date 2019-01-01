from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, RedirectView, CreateView
from django.urls import reverse_lazy
from .forms import *

class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signin.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

class LogoutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Accounts index.")