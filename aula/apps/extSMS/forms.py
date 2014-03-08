from django import forms
import django
from django.db.models import TextField
from django.forms import ModelForm, TextInput
from aula.apps.extSMS.models import extSMS


class smsForm(ModelForm):
    class Meta:
        model = extSMS
        fields = ['incidencia', 'envia']

        widgets = {
            'incidencia': TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}),
        }
