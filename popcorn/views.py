from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings

from .forms import RecipeForm, CategoryForm
from .models import Recipe, Category


# Create your views here.
# class IndexView(generic.DetailView):
#     template_name = 'popcorn/main_page.html'

def index(request):
    return render(request, 'popcorn/main_page.html', {'recipes': Recipe.objects.all()})


def recipe(request):
    return render(request, 'popcorn/recipe.html')


class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'popcorn/recipe.html'


def edit_recipe(request):
    if not request.user.is_authenticated:
        #Todo add nice page to say that you are not authorized 
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            # add redirection
            form.save()
            return render(request, 'popcorn/main_page.html')
    else:
        form = RecipeForm()
    return render(request, 'popcorn/recipe_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'popcorn/logout_success.html')
