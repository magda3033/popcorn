import datetime
import json

from django.contrib.auth import logout
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views import generic
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from .forms import RecipeForm, CommentForm
from .models import Recipe, Category


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

class CategoriesView(generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'popcorn/categories.html'

def edit_recipe(request, slug = None):
    #TODO: Automatically attach time category
    if not request.user.is_authenticated:
        # Todo add nice page to say that you are not authorized
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if slug is None: 
        if request.method =='POST':
            form = RecipeForm(request.POST, request.FILES)

            if form.is_valid():
                if form.instance.author is None:
                    form.instance.author = request.user
                form.save()
                return HttpResponseRedirect(reverse("recipe", kwargs={'slug': form.instance.slug}))
        else:
            form = RecipeForm()
    else:
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.method =='POST':
            form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

            if form.is_valid():
                if form.instance.author is None:
                    form.instance.author = request.user
                form.save()
                return HttpResponseRedirect(reverse("recipe", kwargs={'slug': form.instance.slug}))
        else:
            form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
            return render(request, 'popcorn/recipe_edit.html', {'form': form})

    return render(request, 'popcorn/recipe_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'popcorn/logout_success.html')

ACTIONS = {'up': 0, 'down': 1, 0: 'up', 1: 'down'}
NONE_ACTION = 'default'

def get_vote_status(recipe, user):

    vote = recipe.votes.get(user.id)
    if vote:
        return ACTIONS[vote.action]
    return NONE_ACTION

def vote_recipe(request, slug):

    recipe = Recipe.objects.get(slug=slug)
    user = request.user

    if not user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    vote = recipe.votes.get(user.id)
    body = json.loads(request.body)
    action_string = body['action']
    action_result = action_string
    action_value = ACTIONS[action_string]

    if vote is not None and vote.action == action_value:
        action_result = NONE_ACTION
        recipe.votes.delete(user.id)
    else:
        recipe.votes.vote(user.id, action_value)

    recipe = Recipe.objects.get(slug=slug)
    return JsonResponse({'action': action_result, 'count': recipe.vote_score})

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
            return HttpResponseRedirect(reverse("recipe", kwargs={'slug':slug}))
    else:
        if not request.user.is_authenticated:
            comment_form = None
        else:
            comment_form = CommentForm()

    return render(request, template_name, {'recipe': recipe,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'vote_status': get_vote_status(recipe, request.user)})
