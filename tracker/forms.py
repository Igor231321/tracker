from django import forms

from tracker.models import Transaction
from decimal import Decimal


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "description", "category", "created_at", "status"]

    amount = forms.CharField()

    def clean_amount(self):
        data = self.cleaned_data["amount"]

        if isinstance(data, str) and "+" in data:
            data = data.replace(" ", "")
            numbers = data.split("+")

            try:
                total = sum(map(Decimal, numbers))
                return total
            except ValueError:
                raise forms.ValidationError("Невірний формат числа.")
        else:
            try:
                return Decimal(data)
            except (ValueError, TypeError):
                raise forms.ValidationError("Невірний формат числа.")
