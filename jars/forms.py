from django import forms

from jars.models import Jar, JarOperation


class JarCreateForm(forms.ModelForm):
    class Meta:
        model = Jar
        fields = ["title", "goal"]


class JarOperationCreateForm(forms.ModelForm):
    class Meta:
        model = JarOperation
        fields = ["amount"]
