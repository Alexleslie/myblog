from django import forms


class SearchForm(forms.Form):
    body = forms.TimeField()
