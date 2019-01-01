from django.urls import path

from .views import LoginView, LogoutView, SignUpView, ProfileView, ProfileEditView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<slug:slug>/', ProfileView.as_view(), name='profile'),
    path('profile/<slug:slug>/edit/', ProfileEditView.as_view(), name='profile_edit')
]
