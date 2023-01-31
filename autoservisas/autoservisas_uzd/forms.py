from .models import UzsakymoAtsiliepimas, VartotojoProfilis, Uzsakymas
from django import forms
from django.contrib.auth.models import User


class UzsakymoAtsiliepimasForm(forms.ModelForm):
    class Meta:
        model = UzsakymoAtsiliepimas
        fields = {"turinys", "komentatorius"}
        widgets = {"uzsakymas": forms.HiddenInput(), "komentatorius": forms.HiddenInput}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class VartotojoProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = VartotojoProfilis
        fields = ["foto"]


class TerminoIvedimas(forms.DateInput):
    input_type = 'date'


class VartotojoUzsakymasCreateForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ["automobilis", "vartotojas", "atlikimo_terminas", "statusas"]
        widgets = {"vartotojas": forms.HiddenInput(), "atlikimo_terminas": TerminoIvedimas()}
