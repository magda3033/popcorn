"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path

from . import views
from .forms import UserRegistrationForm

from django_registration.backends.activation.views import RegistrationView

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/add/', views.edit_recipe, name='add_recipe'),
    path('recipes/edit/<str:slug>', views.edit_recipe, name='edit_recipe'),
    path('recipes/view/<str:slug>', views.post_comment, name='recipe'),
    path('recipes/view/<str:slug>/up', views.vote_up, name='voteup'),
    path('recipes/view/<str:slug>/down', views.vote_down, name='votedown'),
    path('accounts/profile/', views.index),
    path('accounts/register/',
        RegistrationView.as_view(
            form_class=UserRegistrationForm
        ),
        name='django_registration_register',
    ),
    path('accounts/',
        include('django_registration.backends.activation.urls')
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
]
