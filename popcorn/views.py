import datetime

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.conf import settings
from django.shortcuts import get_object_or_404

from .forms import RecipeForm, CommentForm
from .models import Recipe


# Create your views here.
# class IndexView(generic.DetailView):
#     template_name = 'popcorn/main_page.html'

def index(request):
    return render(request, 'popcorn/main_page.html',
                  {'recipes': Recipe.objects.all(),
                   'lastweek': Recipe.objects.filter(created_on__gte=timezone.now() - datetime.timedelta(days=7))})


def recipe(request, slug):
    return render(request, 'popcorn/recipe.html')

class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'popcorn/recipe.html'


def edit_recipe(request):
    if not request.user.is_authenticated:
        # Todo add nice page to say that you are not authorized
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            if form.instance.author is None:
                form.instance.author = request.user
            # TODO: add redirection
            form.save()
            return render(request, 'popcorn/main_page.html')
    else:
        form = RecipeForm()
    return render(request, 'popcorn/recipe_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'popcorn/logout_success.html')


def vote_up(request, slug):
    review = Recipe.objects.get(slug=slug)
    user = request.user
    review.votes.up(user.id)
    return render(request, 'popcorn/main_page.html')


def vote_down(request, slug):
    review = Recipe.objects.get(slug=slug)
    user = request.user
    review.votes.down(user.id)
    return render(request, 'popcorn/main_page.html')


def post_comment(request, slug):

    template_name = 'popcorn/recipe.html'
    recipe = get_object_or_404(Recipe, slug=slug)
    #Todo add check for deleted comments
    #comments = recipe.comments.filter(active=True)
    comments = recipe.comments.all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        if not request.user.is_authenticated:
            #Todo add nice page to say that you are not authorized 
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.recipe = recipe
            if new_comment.author is None:
                new_comment.author = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        if not request.user.is_authenticated:
            comment_form = None
        else:
            comment_form = CommentForm()

    return render(request, template_name, {'recipe': recipe,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
