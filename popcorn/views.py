from django.shortcuts import render
from django.views import generic
from django.contrib.auth import logout
from .forms import RecipeForm  # , CategoryForm
from .models import Recipe


# Create your views here.
# class IndexView(generic.DetailView):
#     template_name = 'popcorn/index.html'

def index(request):
    return render(request, 'popcorn/index.html')


def recipe(request):
    return render(request, 'popcorn/recipe.html')


def recipes(request):
    return render(request, 'popcorn/recipes.html', {'recipes': Recipe.objects.all()})


class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'popcorn/recipe.html'


def edit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)

        if form.is_valid():
            # add redirection
            form.save()
            return render(request, 'popcorn/index.html')
    else:
        form = RecipeForm()
    return render(request, 'popcorn/recipe_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'popcorn/logout_success.html')

# def add_category(request):
#     lastimage= Category.objects.last()

#     imagefile= lastimage.imagefile if lastimage is not None else None


#     form = CategoryForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()


#     context= {'imagefile': imagefile,
#               'form': form
#               }

#     return render(request, 'popcorn/recipe_edit.html', {'form' : form})
