from django import forms
from django.contrib.humanize.templatetags.humanize import intcomma

from jars.models import Jar, JarOperation


class JarCreateForm(forms.ModelForm):
    class Meta:
        model = Jar
        fields = ["title", "goal"]


class JarOperationCreateForm(forms.ModelForm):
    class Meta:
        model = JarOperation
        fields = ["amount"]

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        jar = self.initial.get('jar')

        if jar is None:
            raise forms.ValidationError("Банка не була знайдена")

        if amount + jar.balance > jar.goal:
            raise forms.ValidationError(f"Максимальна сума поповнення банки: {intcomma(round(jar.remaining_amount()))}")
        return amount
