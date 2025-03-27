from django import forms

class TownForm(forms.Form):
    town_name = forms.CharField(label='Город', max_length=50)