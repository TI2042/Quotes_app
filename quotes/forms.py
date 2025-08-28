from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]

    def clean(self):
        cleaned = super().clean()
        if Quote.objects.filter(text=cleaned.get("text")).exists():
            raise forms.ValidationError("Цитата уже существует!")
        if Quote.objects.filter(source=cleaned.get("source")).count() >= 3:
            raise forms.ValidationError("У источника уже 3 цитаты!")
        return cleaned
