from django import forms
from tehnicka.models import Ucenik, Smjer,Predmet

class UcenikForm(forms.ModelForm):
    class Meta:
        model = Ucenik
        fields = ('ime', 'prezime','JMBG','smjer')

#class NameForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)\
