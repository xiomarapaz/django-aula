# This Python file uses the following encoding: utf-8
from django import forms
from django.forms.forms import NON_FIELD_ERRORS

class loginForm(forms.Form):
    idGrup = forms.Select()

    def addError(self, msg):
        self._errors.setdefault(NON_FIELD_ERRORS, []).append(msg)

class UploadFileForm(forms.Form):
    file = forms.FileField(required=False, help_text="Dades de l'usuari en format CSV, separar per coma.<br> Login_usuari, Nom complert")

