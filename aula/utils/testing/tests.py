#encoding: utf-8
# Utilitats compartides per fer testing.

from aula.apps.usuaris.models import Professor, Group
from aula.apps.alumnes.models import Grup, Alumne
from aula.apps.presencia.models import EstatControlAssistencia, Impartir, ControlAssistencia
from typing import List, Dict, Union
from datetime import date

import random

class TestUtils():

    def crearProfessor(self, nomUsuari, passwordUsuari):
    # type:(str, str) -> Professor
        grupProfessors, _ = Group.objects.get_or_create(name='professors')
        grupProfessionals, _ = Group.objects.get_or_create(name='professional')
        profe1 = Professor.objects.create(username=nomUsuari, password=passwordUsuari) #type: Professor
        profe1.groups.add(grupProfessors)
        profe1.groups.add(grupProfessionals)
        profe1.set_password(passwordUsuari)
        profe1.save()
        
        return profe1

    def generaAlumnesDinsUnGrup(self, grupAlumnes, nAlumnesAGenerar):
        #type:(Grup,int) -> List[Grup]
        noms = ['Xevi','Joan','Pere','Lluís','Brandom','Maria','Lola','Azucena']
        cognoms = ['Serra','Vazquez','García','Moreno','Vila','Vilamitjana']
        alumnesGenerats = [] #type: List[Grup]
        
        for i in range(0,nAlumnesAGenerar):
            alumne = Alumne.objects.create(ralc=100, grup=grupAlumnes, 
                nom=noms[random.randint(0,noms.__len__()-1)], 
                cognoms=cognoms[random.randint(0,cognoms.__len__()-1)], 
                tutors_volen_rebre_correu=False,
                data_neixement=date(1990,7,7) #english date.
                ) 
            alumnesGenerats.append(alumne)
        return alumnesGenerats
        
    def generarEstatsControlAssistencia(self):
        #type: ()->Dict[str, EstatControlAssistencia]
        estats = {} #type: Dict[str, EstatControlAssistencia]
        estats['p'] = EstatControlAssistencia.objects.create( codi_estat = 'P', nom_estat='Present' )
        estats['f'] = EstatControlAssistencia.objects.create( codi_estat = 'F', nom_estat='Falta' )
        estats['r'] = EstatControlAssistencia.objects.create( codi_estat = 'R', nom_estat='Retard' )
        estats['j'] = EstatControlAssistencia.objects.create( codi_estat = 'J', nom_estat='Justificada' )
        return estats

    def omplirAlumnesHora(self,alumnes, horaAImpartir):
        #type: (List[Alumne], Impartir)->Any
        for alumne in alumnes:
            ControlAssistencia.objects.create(
                alumne = alumne,
                impartir = horaAImpartir)