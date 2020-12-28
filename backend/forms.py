from django import forms


class CoinNameForm(forms.Form):
    coin_name = forms.CharField(label="", required=False)

class LanguageEnForm(forms.Form):
    languageEN = forms.BooleanField(label="", required=False)

class LanguageRuForm(forms.Form):
    languageRU = forms.BooleanField(label="", required=False)
