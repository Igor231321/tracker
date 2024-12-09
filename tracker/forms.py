from django import forms

from tracker.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "description", "category", "operation"]
