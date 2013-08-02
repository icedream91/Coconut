from django.forms import ModelForm
from blog.models import ArticleComment
from blog.models import PageComment


class ArticleCommentForm(ModelForm):
    class Meta:
        model=ArticleComment
        exclude=('pub_time','article')


class PageCommentForm(ModelForm):
    class Meta:
        model=PageComment
        exclude=('pub_time','page')


