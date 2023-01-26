from .models import UzsakymoAtsiliepimas
from django import forms


class UzsakymoAtsiliepimasForm(forms.ModelForm):
    class Meta:
        model = UzsakymoAtsiliepimas
        fields = {"turinys", "komentatorius"}
        widgets = {"uzsakymas": forms.HiddenInput(), "komentatorius": forms.HiddenInput}
