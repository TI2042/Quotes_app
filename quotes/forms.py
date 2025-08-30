from django import forms
from django.core.exceptions import ValidationError

from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]

    def clean(self):
        cleaned = super().clean()
        text = cleaned.get("text")
        source = cleaned.get("source")

        if text and source:
            qs = Quote.objects.filter(text=text, source=source)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Цитата уже существует!")

            source_qs = Quote.objects.filter(source=source)
            if self.instance.pk:
                source_qs = source_qs.exclude(pk=self.instance.pk)
            if source_qs.count() >= 3:
                raise ValidationError("Нельзя добавить больше 3 цитат из одного источника.")

        return cleaned
