from braces.views import PrefetchRelatedMixin
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.forms import HiddenInput
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView,
                                  RedirectView, UpdateView)

from .forms import UserCreateForm
from .models import UserProfile


class LoginView(FormView):
    """Logs a user in"""
    form_class = AuthenticationForm
    template_name = "accounts/signin.html"

    def get_success_url(self):
        """Gets the URL to redirect to after a successful login"""
        # Check if we have a next url as Query parameter
        next_url = self.request.GET.get('next', None)
        if next_url:
            # Return the next URL
            return "{}".format(next_url)
        # Default: Redirect to home
        return reverse_lazy('projects:index')

    def get_form(self, form_class=None):
        """Get the form"""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        """Check if the form is valid"""
        # Login the user
        login(self.request, form.get_user())
        return super().form_valid(form)

class LogoutView(RedirectView):
    """Logs a user out"""
    url = reverse_lazy("projects:index")

    def get(self, request, *args, **kwargs):
        # Logout the user
        logout(request)
        return super().get(request, *args, **kwargs)

class SignUpView(CreateView):
    """Creates a new user"""
    form_class = UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

class ProfileView(PrefetchRelatedMixin, DetailView):
    """Profile of a user"""
    model = UserProfile
    prefetch_related = ("user",)
    template_name = "accounts/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        past_apps = self.request.user.applications.filter(accepted=True)
        context['past_apps'] = past_apps
        return context

    def get(self, request, *args, **kwargs):
        """Get the profile"""
        # If we pass in `/me/` as profile, see if we get a user back,
        # If not, redirect to login
        if self.kwargs[self.get_slug_field()] == "me":
            try:
                self.get_object()
            except self.model.DoesNotExist:
                return redirect_to_login(reverse_lazy(
                    "accounts:profile",
                    kwargs={"slug": "me"}
                ))
        return super().get(request, *args, **kwargs)


    def get_object(self, queryset=None):
        """Get object"""
        if not queryset:
            queryset = self.get_queryset()
        # If we pass in `/me` as profile,
        # Use the username of the current user instead
        slug = self.kwargs[self.get_slug_field()]
        if slug == "me":
            slug = self.request.user.username
        return queryset.get(slug=slug)

class ProfileEditView(LoginRequiredMixin, PrefetchRelatedMixin, UpdateView):
    """Update profile of a user"""
    model = UserProfile
    prefetch_related = ("user",)
    fields = ("bio", "pfp", "skills_internal")
    template_name = "accounts/profile_edit.html"

    def get_form(self, form_class=None):
        """Get form"""
        form = super().get_form(form_class)
        # Set some form overwrites
        form.fields['pfp'].required = False
        form.fields['skills_internal'].required = False
        form.fields['skills_internal'].widget = HiddenInput()
        return form

    def get(self, request, *args, **kwargs):
        auth_user = request.user
        profile = self.get_object()
        # Make sure we can only edit our own profile.
        # If we try to edit someone elses profile,
        # Redirect to their normal profile page
        if not auth_user == profile.user:
            return HttpResponseRedirect(reverse_lazy(
                'accounts:profile',
                kwargs={"slug": profile.slug}
            ))
        return super().get(request, *args, **kwargs)
