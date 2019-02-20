#encoding: utf-8
import datetime
from django.db.models import Q
from django.test import TestCase
from django.db.models.query import QuerySet
from aula.apps.assignatures.models import Assignatura
from aula.apps.alumnes.models import Alumne, Grup, Curs, Nivell
from aula.apps.presencia.models import ControlAssistencia, EstatControlAssistencia, Impartir
from aula.apps.horaris.models import FranjaHoraria, Horari, DiaDeLaSetmana
from aula.apps.usuaris.models import User, Group, Professor
from aula.utils.testing.tests import TestUtils
import others

class SimpleTest(TestCase):
    
    def setUp(self):
        #Crea dos dies de passar llista.
        #Passa llista dos dies en profes diferents.

        tu = TestUtils()
        #Crear n alumnes.
        DAM = Nivell.objects.create(nom_nivell='DAM') #type: Nivell
        primerDAM = Curs.objects.create(nom_curs='1er', nivell=DAM) #type: Curs
        primerDAMA = Grup.objects.create(nom_grup='A', curs=primerDAM) #type: Grup
        self.codiGrup = primerDAMA.pk
        self.nAlumnesGrup = 10
        self.alumnes = tu.generaAlumnesDinsUnGrup(primerDAMA, self.nAlumnesGrup)
        
        ug = Group()
        ug.name = "professors"
        ug.save()

        uProfessor = Professor(username='xevi', first_name='T', last_name='P')
        uProfessor.email = "xeviterr@gmail.com"
        uProfessor.is_staff = False
        uProfessor.is_active = False
        uProfessor.save()
        uProfessor.groups.add(ug)
        uProfessor.save()

        assignatura = Assignatura()
        assignatura.codi_assignatura = "ISO"
        assignatura.save()

        dataActual = datetime.datetime.now()
        dataActual.weekday()
        self.dataAEliminarAlumne = dataActual

        diaSet = DiaDeLaSetmana()
        diaSet.n_dia_uk = dataActual.isoweekday()
        diaSet.n_dia_ca = dataActual.weekday()
        diaSet.dia_2_lletres = tu.diesSetmana2Lletres[dataActual.weekday()]
        diaSet.dia_de_la_setmana = tu.diesSetmana[dataActual.weekday()]
        diaSet.es_festiu = False
        diaSet.save()

        fh = FranjaHoraria()
        fh.hora_inici = datetime.time(hour=8, minute=0, second=0)
        fh.hora_fi = datetime.time(hour=9, minute=0, second=0)
        fh.nom_franja = 'PrimerHoraMati'
        fh.save()

        horari = Horari()
        horari.assignatura = assignatura
        horari.professor = uProfessor
        horari.grup = primerDAMA
        horari.dia_de_la_setmana = diaSet
        horari.hora = fh
        horari.nom_aula = "3.04"
        horari.es_actiu = True
        horari.estat_sincronitzacio = "MAN"
        horari.save()

        #Crea controls d'assistencia
        self.estats = tu.generarEstatsControlAssistencia()
        self.estatFalta = self.estats['f']
        self.estatPresent = self.estats['p']

        estatsAAssignar = [
            self.estatPresent, None, 
            self.estatPresent, None, self.estatFalta, self.estatFalta]

        llistaImpartir = []
        dies=[-2, -1, 0, 1, 2, 3]
        for i in range(0,6):
            novaData = dataActual + datetime.timedelta(days=7*dies[i])
            imp = Impartir()
            imp.horari = horari 
            imp.dia_impartir = novaData #datetime.datetime(day=novaData.day, month=dataActual.month, year=dataActual.year)
            imp.pot_no_tenir_alumnes = False
            imp.save()
            llistaImpartir.append(imp)

            ca = ControlAssistencia()
            ca.alumne = self.alumnes[0]
            ca.estat = estatsAAssignar[i]
            ca.impartir = imp
            ca.professor = uProfessor
            ca.save()
        pass

        '''
        #Hores d'avui i dies següents
        ca = ControlAssistencia()
        ca.alumne = self.alumnes[0]
        ca.estat = self.estatPresent
        ca.impartir = imp
        ca.professor = uProfessor
        ca.save()

        ca = ControlAssistencia()
        ca.alumne = al
        ca.estat = None
        ca.impartir = imp3
        ca.professor = uProfessor
        ca.save()

        ca = ControlAssistencia()
        ca.alumne = al
        ca.estat = None
        ca.impartir = imp4
        ca.professor = uProfessor
        ca.save()

        #Hores anteriors
        ca = ControlAssistencia()
        ca.alumne = al
        ca.estat = ecaf
        ca.impartir = imp5
        ca.professor = uProfessor
        ca.save()

        ca = ControlAssistencia()
        ca.alumne = al
        ca.estat = None
        ca.impartir = imp6
        ca.professor = uProfessor
        ca.save()
        '''

    def test_treure_alumnes_de_tots_els_grups(self):
        """
        Test en que es comprova que al donar de baixa (no oficial) un alumne. Aquest s'elimina de tots els grups        

        Ens donen un codi d'alumne i un grup i una data a partir de la qual ha de desaparèixer l'alumne.
             - La data donada ha de ser superior a l'actual

        Obtenir els controls d'assistència on:
            - Seleccionar de impartir els codis que coincideixen amb dels horaris del grup.
            - Per cada hora a impartir:
                - Eliminar del control d'assistència el registres de l'alumne, a l'hora d'impartir donada. El dia d'impartir
                ha de ser superior a la data donada ( i la data donada ha de ser superior a l'actual).

        Cal enviar un correu al finalitzar.
        """
        #Eliminació de l'alumne de les llistes.
        nAlumnes = others.treureAlumnesLlistaClasse(self.alumnes[0].pk, self.codiGrup, self.dataAEliminarAlumne)
        
        #Comprovació després d'eliminar.
        horesAImpartir = others.horesAImpartirGrup(
            self.codiGrup, self.dataAEliminarAlumne, datetime.datetime.now()) #type: QuerySet

        #Comprova que s'han eliminat i no queden dades.
        #Per tant només han de quedar estats presents i les faltes.
        for _horaImpartir in horesAImpartir:
            horaImpartir = _horaImpartir  #type: Impartir
            cas = ControlAssistencia.objects.filter(impartir = horaImpartir)
            for ca in cas: # type: ControlAssistencia
                self.assertTrue (ca.estat == self.estatPresent or ca.estat == self.estatFalta)

        #Falta comprovar que no ha borrat la hora amb falta anterior a la data i una falta que teníem.
        self.assertTrue(ControlAssistencia.objects.filter(estat__codi_estat='F').count()==2)
        #Hores present n'hi ha de quedar una.
        self.assertTrue(ControlAssistencia.objects.filter(estat__codi_estat='P').count()==2)
        #Una hora anterior.
        self.assertTrue(ControlAssistencia.objects.filter(estat__codi_estat=None).count()==1)
