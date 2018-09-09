# This Python file uses the following encoding: utf-8
from aula.utils.widgets import DateTextImput

from django import forms as forms
import datetime
from django.utils.datetime_safe import datetime as datetime_safe
from aula.apps.alumnes.models import Alumne, Grup
from aula.apps.horaris.models import FranjaHoraria
from django.forms.widgets import Widget

def _franjaHorariaIniciONone():
    #Si no ho faig així peta en els tests, al crear els objectes.
    franges = FranjaHoraria.objects.all()
    if len(franges) == 0:
        return None
    else:
        return [ franges[0] ]

def _franjaHorariaFiONone():
    #Si no ho faig així peta en els tests, al crear els objectes.
    franges = FranjaHoraria.objects.reverse()

    if len(franges) == 0:
        return None
    else:
        return [ franges[0] ]

class elsMeusAlumnesTutoratsEntreDatesForm( forms.Form ):
    grup = forms.ChoiceField(   )
    dataDesDe =  forms.DateField(label=u'Data des de', 
                                       initial=datetime.date.today,
                                       required = False, 
                                       help_text=u'Rang de dates: primer dia.',  
                                       widget = DateTextImput() )

    dataFinsA =  forms.DateField(label=u'Data fins a', 
                                       initial=datetime.date.today,
                                       required = True, 
                                       help_text=u'Rang de dates: darrer dia.',  
                                       widget = DateTextImput() )



    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('grups', None)
        super(elsMeusAlumnesTutoratsEntreDatesForm,self).__init__(*args,**kwargs)
        self.fields['grup'].choices = self.queryset    
                

class justificaFaltesW1Form(forms.Form):
    alumne = forms.ModelChoiceField( queryset= Alumne.objects.none(), 
                                          required = False, 
                                          empty_label="(Justificador)",
                                          help_text=u"""Alumne al que vols justificar faltes.(Justificador per tot el grup)"""  )

    data = forms.DateField(label=u'Data faltes a justificar', 
                                       initial=datetime.date.today,
                                       required = True, 
                                       help_text=u'Data on hi ha les faltes a justificar.',  
                                       widget = DateTextImput() )

    pas = forms.IntegerField(  initial=1, widget = forms.HiddenInput() )

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset', None)
        super(justificaFaltesW1Form,self).__init__(*args,**kwargs)
        self.fields['alumne'].queryset = self.queryset        
        
class informeSetmanalForm(forms.Form):
    grup = forms.ModelChoiceField( queryset= Grup.objects.none(), 
                                          required = False, 
                                          empty_label="-- Tots els alumnes --",
                                          help_text=u"""Tria un grup per fer l'informe."""  )

    data = forms.DateField(label=u'Setmana informe:', 
                                       initial=datetime.date.today,
                                       required = True, 
                                       help_text=u'Data on hi ha les faltes a justificar.',  
                                       widget = DateTextImput() )

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset', None)
        super(informeSetmanalForm,self).__init__(*args,**kwargs)
        self.fields['grup'].queryset = self.queryset
        
class seguimentTutorialForm(forms.Form):
    pregunta_oberta  = forms.CharField(  )
    pregunta_select  = forms.ChoiceField(  widget = forms.RadioSelect  )

    def __init__(self, *args, **kwargs):
        self.pregunta = kwargs.pop('pregunta', None)
        self.resposta_anterior = kwargs.pop('resposta_anterior', None)
        self.alumne = kwargs.pop('alumne', None)
        self.tutor = kwargs.pop('tutor', None)    

        super(seguimentTutorialForm,self).__init__(*args,**kwargs)
        if self.pregunta.es_pregunta_oberta:
            del self.fields['pregunta_select']
            self.q_valida = 'pregunta_oberta'
            self.fields[self.q_valida].widget.attrs={'size':'40'} 
        else:
            del self.fields['pregunta_oberta']
            self.q_valida = 'pregunta_select'
            self.fields['pregunta_select'].choices= [ (x.strip(),x.strip(), ) for x in self.pregunta.possibles_respostes.split('|')]  #[('',u'---Tria---')] +
        self.fields[self.q_valida].initial=self.resposta_anterior.resposta.strip() if self.resposta_anterior else None
        self.fields[self.q_valida].label = u'{0}'.format( self.pregunta.pregunta)
        self.fields[self.q_valida].help_text = self.pregunta.ajuda_pregunta   
        self.fields[self.q_valida].required = True 
        if self.pregunta.pregunta == 'Tutor/a' and self.q_valida == 'pregunta_oberta' and not self.fields[self.q_valida].initial:
            self.fields[self.q_valida].initial = u"{0}".format( self.tutor )
        if self.pregunta.pregunta == 'Curs' and self.q_valida == 'pregunta_oberta' and not self.fields[self.q_valida].initial:
            self.fields[self.q_valida].initial = u"{0}".format( self.alumne.grup )
        
class FaltesAssistenciaEntreDatesForm(forms.Form):
    assignatura = forms.ModelMultipleChoiceField( queryset = None )
    grup = forms.ModelMultipleChoiceField( queryset = None )
    dataDesDe = forms.DateField(help_text=u'Data on començar a comptar',
                                       initial= datetime_safe.today(),
                                       required = True,
                                       widget = DateTextImput() )                                       
    horaDesDe = forms.ModelChoiceField( queryset = FranjaHoraria.objects.none())
    dataFinsA = forms.DateField(help_text=u'Data on finalitzar',
                                       initial= datetime_safe.today(),
                                       required = True,
                                       widget = DateTextImput() )
    horaFinsA = forms.ModelChoiceField( queryset = FranjaHoraria.objects.none())

    def __init__(self, *args, **kwargs):
        self.assignatures = kwargs.pop('assignatures', None)
        self.grups = kwargs.pop('grups', None)
        super(FaltesAssistenciaEntreDatesForm,self).__init__(*args,**kwargs)
        self.fields['assignatura'].queryset = self.assignatures
        self.fields['grup'].queryset = self.grups
        self.fields['horaDesDe'].queryset = FranjaHoraria.objects.all()
        self.fields['horaDesDe'].initial = _franjaHorariaIniciONone()
        self.fields['horaFinsA'].queryset = FranjaHoraria.objects.all()
        self.fields['horaFinsA'].initial = _franjaHorariaFiONone()


class FaltesAssistenciaEntreDatesUFsForm(forms.Form):
  assignatura = forms.ModelMultipleChoiceField( queryset = None )
  grup = forms.ModelMultipleChoiceField( queryset = None )

  def __init__(self, *args, **kwargs):
      self.assignatures = kwargs.pop('assignatures', None)
      self.grups = kwargs.pop('grups', None)
      super(FaltesAssistenciaEntreDatesUFsForm,self).__init__(*args,**kwargs)
      self.fields['assignatura'].queryset = self.assignatures
      self.fields['grup'].queryset = self.grups

class SeguimentTreureAlumneGrupForm(forms.Form):
    grup = forms.ModelChoiceField( queryset= Grup.objects.none(),
                                    to_field_name = 'pk',
                                    required = True,
                                    empty_label="(Selecciona el grup)",
                                    help_text=u"""Seleccioa el grup classe d'on vols treure l'alumne."""  )

    data = forms.DateField(label=u'Data a partir de la qual vols treure l\'alumne dels llistats.',
                                       initial=datetime.date.today,
                                       required = True,
                                       help_text=u'Cal que la data sigui superior o igual al dia actual.',
                                       widget = DateTextImput() )

    def __init__(self, *args, **kwargs):
        #Li passem la llista de grups en forma de querySet.
        #Exemple:
        #querySetGrups = Grup.objects.filter(...)
        querySetGrups = kwargs.pop('querySetGrups', None)
        super(SeguimentTreureAlumneGrupForm,self).__init__(*args,**kwargs)
        if (querySetGrups != None):
            self.fields['grup'].queryset = querySetGrups

class SeguimentTreureAlumneGrupForm2(forms.Form):
    #Selecciona alumne del grup.
    alumne = forms.ModelChoiceField( queryset= Alumne.objects.none(),
                                    required = True,
                                    empty_label="(Selecciona l'alumne a donar de baixa)",
                                    help_text=u"""Selecciona l'alumne a donar de baixa."""  )

    def __init__(self, *args, **kwargs):
        #Li passem la llista de grups en forma de querySet.
        #Exemple:
        #querySetGrups = Grup.objects.filter(...)
        qs = kwargs.pop('querySetAlumnes', None)
        super(SeguimentTreureAlumneGrupForm2,self).__init__(*args,**kwargs)
        if (qs != None):
            self.fields['alumne'].queryset = qs

