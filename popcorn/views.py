from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django.shortcuts import get_object_or_404

from .forms import RecipeForm, CommentForm
from .models import Recipe, Category

# Create your views here.
# class IndexView(generic.DetailView):
#     template_name = 'popcorn/main_page.html'

def index(request):
    return render(request, 'popcorn/main_page.html', {'recipes': Recipe.objects.all()})

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
        #Todo add nice page to say that you are not authorized 
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if slug is None: 
        if request.method =='POST':
            form = RecipeForm(request.POST, request.FILES)

            if form.is_valid():
                if form.instance.author is None:
                    form.instance.author = request.user
                # TODO: add redirection
                form.save()
                return render(request, 'popcorn/main_page.html')
        else:
            form = RecipeForm()
    else:
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.method =='POST':
            form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

            if form.is_valid():
                if form.instance.author is None:
                    form.instance.author = request.user
                # TODO: add redirection
                form.save()
                return render(request, 'popcorn/main_page.html')
        else:
            form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
            return render(request, 'popcorn/recipe_edit.html', {'form': form})

    return render(request, 'popcorn/recipe_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'popcorn/logout_success.html')

def vote_up(request, slug):
    review = Recipe.objects.get(slug=slug)
    user = request.user
    vote = review.votes.get(user.id)
    if vote is None:
        review.votes.up(user.id)
        return render(request, 'popcorn/main_page.html')
    past_action = vote.ACTION_FIELD[vote.action]
    if past_action == 'num_vote_up':
        review.votes.delete(user.id) 
    else:
        review.votes.up(user.id)
    return render(request, 'popcorn/main_page.html')

def vote_down(request, slug):
    review = Recipe.objects.get(slug=slug)
    user = request.user
    vote = review.votes.get(user.id)
    if vote is None:
        review.votes.down(user.id)
        return render(request, 'popcorn/main_page.html')
    past_action = vote.ACTION_FIELD[vote.action]
    if past_action == 'num_vote_down':
        review.votes.delete(user.id) 
    else:
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
