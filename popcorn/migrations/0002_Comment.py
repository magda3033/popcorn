# Generated by Django 3.1.2 on 2020-12-14 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('popcorn', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='object_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='popcorn.recipe'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='deleted_on',
            field=models.DateTimeField(null=True),
        ),
    ]
