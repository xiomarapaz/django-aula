#encoding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.forms import Form

from aula.apps.assignatures.models import UF
from aula.apps.presencia.utils import crearDiccionari
from aula.apps.presencia.models import ControlAssistencia, Impartir
from aula.apps.BI.utils import dades_dissociades
from aula.apps.BI.prediccio_assistencia import predictTreeModel
from aula.apps.presencia.utils import obtenir_hora_anterior
from forms import ControlAssistenciaForm, ControlAssistenciaUFForm

class PassarLlistaManager(object):
    '''
    Classe que gestiona el formulari de passar llista.
    És interessant per tal de reaprofitar codi en les dues formes de passar llista
    Convencional i per UF's.
    '''
    impartir=None

    def __init__(self, impartir):
        '''
        Crea l'objecte passar llista amb la instància d'impartir sobre la que treballem.
        :type impartir: Impartir
        '''
        self.impartir = impartir

    def crearFormulari(self, post, control_a):
        '''
        Crea el formulari per el tipus de passar llista que realitzem.
        :type post: dict diccionari post
        :type control_a: ControlAssistencia
        '''
        if not post:
            form = ControlAssistenciaForm(
                prefix=str(control_a.pk),
                instance=control_a)
        else:
            form = ControlAssistenciaForm(
                data=post,
                prefix=str(control_a.pk),
                instance=control_a)
        return form

    def render(self, request, variableDictionary ):
        return render(
            request,
            "passaLlista.html",
            variableDictionary
            )

class PassarLlistaUFsManager(PassarLlistaManager):
    '''
    Classe que gestiona el formulari de passar llista en el cas de les UF's.
    És similar al passar llista, simplement incorpora un selector per tal 
    que el professor indiqui la UF que realitza cada alumne.
    '''
    dictUfs={}
    ufs=None

    def __init__(self, impartir):
        '''
        Inicialitza totes les dades que necessita el gestor.
        '''
        PassarLlistaManager.__init__(self, impartir)
        self.ufs = UF.objects.filter(assignatura=self.impartir.horari.assignatura.id)
        self.dictUfs = crearDiccionari(self.ufs)

    def crearFormulari(self, post, control_a):
        '''
        Crea el formulari segons el tipus a inicialitzar
        :type post: dict diccionari post
        :type control_a: ControlAssistencia
        '''
        if not post:
            form = ControlAssistenciaUFForm(
                prefix=str(control_a.pk),
                instance=control_a,
                id_assignatura=self.impartir.horari.assignatura.id)
        else:
            form = ControlAssistenciaUFForm(
                post,
                prefix=str(control_a.pk),
                instance=control_a,
                id_assignatura=self.impartir.horari.assignatura.id)
        
        #Actualitza la UF seleccionada.
        control_anterior=obtenir_hora_anterior(form.instance)
        form.n_uf_seleccionada = -1
        if control_anterior != None:
            form.n_uf_seleccionada = self.dictUfs.get(control_anterior.uf_id, -1)
        return form

    def render(self, request, variableDictionary ):
        newVariableDictionary = variableDictionary
        newVariableDictionary["ufs"] = self.ufs
        return render(
            request,
            "passaLlistaAmbUFs.html",
            newVariableDictionary
            )