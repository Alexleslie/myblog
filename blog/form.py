from django import forms


class SearchForm(forms.Form):
    body = forms.TextInput()


class MessageForm(forms.Form):
    body = forms.TextInput()