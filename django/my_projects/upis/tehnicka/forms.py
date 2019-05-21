from django.forms import ModelForm
from .models import  Ucenik, Smjer, Predmet

# https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/#modelform
# Creating a form to add an article.
#>>> form = ArticleForm()
# Creating a form to change an existing article.
#>>> article = Article.objects.get(pk=1)
#>>> form = ArticleForm(instance=article)

class UcenikEditForm(ModelForm):
    class Meta:
        model=Ucenik
        fields=('ime', 'prezime', 'JMBG','smjer')
