from django import forms
import django
from django.forms import ModelForm, TextInput, RadioSelect

from aula.apps.extSMS.models import extSMS



class smsForm(ModelForm):

    class Meta:
        model = extSMS
        fields = ['falta', 'estat']

        widgets = {
            'falta': TextInput(attrs={'class': 'disabled form-control', 'readonly': 'readonly'}),
            'estat': RadioSelect()
        }
