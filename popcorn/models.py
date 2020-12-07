from django.contrib.auth.models import User as AuthUser
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from vote.models import VoteModel


# TODO: Add validators in different areas (images), but research them first
# TODO: Research https://django-simple-history.readthedocs.io for approval history

class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    newsletter_signup = models.BinaryField()
    blocked_on = models.DateTimeField()
    blocked_till = models.DateTimeField()
    blocked_by = models.ForeignKey("Moderator", on_delete=models.SET_NULL, null=True, related_name='blocked_users')
    deleted_on = models.DateTimeField()
    deleted_by = models.ForeignKey("Moderator", on_delete=models.SET_NULL, null=True, related_name='deleted_users')
    # MAYBE: avatar


class Moderator(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    granted_on = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField()


# class Vote(models.Model):
#     object_id = models.PositiveIntegerField()
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     value = models.BinaryField()
#     voted_on = models.DateTimeField(auto_now_add=True)
#     vote_target = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     target_id = GenericForeignKey('vote_target')


class Recipe(VoteModel, models.Model):
    class Difficulty(models.IntegerChoices):
        VERY_EASY = 1, ('Bardzo łatwa')
        EASY = 2, ('Łatwa')
        NORMAL = 3, ('Średnia')
        DIFFICULT = 4, ('Trudna')
        VERY_DIFFICULT = 5, ('Bardzo trudna')

    id = models.AutoField(primary_key=True)
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    icon = models.ImageField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authored_recipes', blank=True)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    preparation_time = models.PositiveIntegerField(blank=True, null=True)
    servings_count = models.PositiveIntegerField(blank=True, null=True)
    difficulty = models.IntegerField(choices=Difficulty.choices, default=Difficulty.NORMAL, blank=True, null=True)
    hidden_on = models.DateTimeField(null=True, blank=True)
    hidden_by = models.ForeignKey(Moderator, on_delete=models.SET_NULL, null=True, related_name='hidden_recipes',
                                  blank=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(Moderator, on_delete=models.SET_NULL, null=True, related_name='deleted_recipes',
                                   blank=True)

    # TODO: Fix relations in recipe
    # comments = GenericRelation('Comment')
    # votes = GenericRelation('Vote')

    # TODO: When WYSIWYG is picked add images

    def is_hidden(self):
        return self.hidden_on is not None

    def is_deleted(self):
        return self.deleted_on is not None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(self.name + " " + str(self.id), allow_unicode=False)
        super().save(*args, **kwargs)


class Comment(models.Model):
    object_id = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authored_comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField()
    deleted_by = models.ForeignKey(Moderator, on_delete=models.SET_NULL, null=True, related_name='comments_deleted')
    comment_parent = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    parent_id = GenericForeignKey('comment_parent')

    # TODO: Fix relations in comment
    # comments = GenericRelation('Comment')
    # votes = GenericRelation('Vote')

    def is_deleted(self):
        return self.deleted_on is not None


class Measurment(models.Model):
    full_name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=6)


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    count = models.PositiveIntegerField()
    measurment = models.ForeignKey(Measurment, on_delete=models.SET_NULL, null=True)
