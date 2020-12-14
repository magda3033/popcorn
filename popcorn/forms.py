from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Recipe
from .models import Comment



# Adding css to django class
# https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
# https://docs.djangoproject.com/en/2.2/topics/forms/#working-with-form-templates
# https://www.youtube.com/watch?v=6-XXvUENY_8

class RecipeForm(forms.ModelForm):
    # name = forms.CharField()
    # difficulty = forms.ChoiceField()
    # recipe = SummernoteTextFormField()

    class Meta:
        OPTIONS = (
            ("AUT", "Austria"),
            ("DEU", "Germany"),
            ("NLD", "Neitherlands"),
        )
        model = Recipe
        fields = [
            'name',
            'difficulty',
            'preparation_time',
            'servings_count',
            # 'categories',
            # 'icon',
            'content',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'servings_count': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'servings_count': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'},choices=OPTIONS),
            # 'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'},choices=OPTIONS),
            'content': SummernoteWidget(),
        }
        labels = {
            'name': 'Nazwa przepisu',
            'difficulty': 'Trudność',
            'preparation_time': 'Czas przygotowania (w minutach)',
            'servings_count': 'Ilość porcji',
            # 'categories': 'Kategorie',
            # 'icon': 'Miniaturka',
            'content': '',
        }

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}