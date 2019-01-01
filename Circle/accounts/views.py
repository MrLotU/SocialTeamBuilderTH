from braces.views import PrefetchRelatedMixin
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, RedirectView, UpdateView

from .forms import UserCreateForm
from .models import UserProfile


class LoginView(FormView):
    """Logs a user in"""
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
    """Logs a user out"""
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class SignUpView(CreateView): # pylint: disable=too-many-ancestors
    """Creates a new user"""
    form_class = UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

class ProfileView(PrefetchRelatedMixin, DetailView): # pylint: disable=too-many-ancestors
    """Profile of a user"""
    model = UserProfile
    prefetch_related = ("user", "skills")
    template_name = "accounts/profile.html"

class ProfileEditView(LoginRequiredMixin, PrefetchRelatedMixin, UpdateView): # pylint: disable=too-many-ancestors
    """Update profile of a user"""
    model = UserProfile
    prefetch_related = ("user", "skills")
    fields = ("bio", "pfp", "skills")
    template_name = "accounts/profile_edit.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['pfp'].required = False
        form.fields['skills'].required = False
        return form
