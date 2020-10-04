from django import forms
from store.models import Tecnico
from django.forms import ModelForm


class TecnicoForm(ModelForm):
    class Meta:
        model = Tecnico
        fields = '__all__'
