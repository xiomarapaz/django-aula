# This Python file uses the following encoding: utf-8
import re
from aula.utils.widgets import DateTextImput
from django import forms as forms
from django.forms import ModelForm, RadioSelect
from django.forms.widgets import DateInput, TextInput
from aula.apps.horaris.models import FranjaHoraria, Horari
from aula.apps.presencia.models import ControlAssistencia  , EstatControlAssistencia
from aula.apps.usuaris.models import Professor
from django.utils.datetime_safe import datetime
from aula.apps.alumnes.models import Nivell, Grup
from aula.utils.widgets import bootStrapButtonSelect

class NovaUFForm(forms.Form):
  nom = forms.CharField(label=u'Nom UF',
        help_text=u'Codi de la UF, per exemple UF1. No pot contenir espais', max_length=25)
  horesTeoriques = forms.IntegerField(label=u'Hores teòriques')
  data_inici = forms.DateField(label=u'Data inici',
                            required = True,
                            help_text=u'Data inici de la UF',
                            widget = DateTextImput() )
  data_fi = forms.DateField(label=u'Data fi',
                            required = True,
                            help_text=u'Data fi de la UF',
                            widget = DateTextImput() )

  def clean_nom(self):
    data = self.cleaned_data['nom']
    p = re.compile('^[a-z|A-Z|0-9]+$')
    m = p.match(data)
    if not m:
        raise forms.ValidationError("El nom no pot contenir espais, ni caràcters extranys.")
    return data

class faltesAssistenciaEntreDatesForm(forms.Form):
  grup = forms.ModelChoiceField( queryset = None )
  assignatura = forms.ModelMultipleChoiceField( queryset = None )
  horesAltresProfes = forms.BooleanField(
    required=False, 
    label=u"Hores altres profes?",
    help_text=u'Vols comptar hores d\'un altre profe, que faci la mateixa matèria?', 
    initial=False)


  def __init__(self, *args, **kwargs):
      self.assignatures = kwargs.pop('assignatures', None)
      self.grups = kwargs.pop('grups', None)
      super(faltesAssistenciaEntreDatesForm,self).__init__(*args,**kwargs)
      self.fields['assignatura'].queryset = self.assignatures
      self.fields['grup'].queryset = self.grups
