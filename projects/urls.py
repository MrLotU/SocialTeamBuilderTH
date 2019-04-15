"""Circle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import Index, CreateProject, ProjectDetail, ProjectApply, DeleteProject, ApplicationsView, HandleApplicationView

app_name = 'projects'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('new', CreateProject.as_view(), name='new'),
    path('project/<int:pk>/', ProjectDetail.as_view(), name='detail'),
    path('project/<int:pk>/apply/<int:pos>/', ProjectApply.as_view(), name='apply'),
    path('project/<int:pk>/delete', DeleteProject.as_view(), name='delete'),
    path('project/<int:pk>/applications', ApplicationsView.as_view(), name='applications'),
    path('project/<int:pk>/applications/<int:app>/<int:s>', HandleApplicationView.as_view(), name='handle_app')
]
