#encoding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from urllib import quote

from django.test import TestCase
from django.contrib.auth.models import User, Group
from datetime import date, timedelta
from django.test import Client
from django.http.response import HttpResponse
from django.conf import settings

from aula.apps.alumnes.models import Alumne, Grup, Curs, Nivell
from aula.apps.usuaris.models import Professor
from aula.apps.horaris.models import Horari, DiaDeLaSetmana, FranjaHoraria
from aula.apps.assignatures.models import Assignatura
from aula.apps.presencia.models import Impartir, ControlAssistencia, EstatControlAssistencia


class PresenciaSetmanalTestCase(TestCase):
    primerESOA = None
    alumne=None
    impartirDilluns=None
    urlBase = 'http://localhost:8000/'

    def setUp(self):
        #Crear n alumnes.
        ESO = Nivell.objects.create(nom_nivell='ESO') #type: Nivell
        primerESO = Curs.objects.create(nom_curs='1er', nivell=ESO) #type: Curs
        self.primerESOA = Grup.objects.create(nom_grup='A', curs=primerESO) #type: Grup
        alumne = Alumne.objects.create(ralc=100, grup=self.primerESOA, 
            nom='Xevi', cognoms='Petit', tutors_volen_rebre_correu=False) #type: Alumne
        self.alumne = alumne
        alumne2 = Alumne.objects.create(ralc=100, grup=self.primerESOA, 
            nom='Joan', cognoms='Serra', tutors_volen_rebre_correu=False) #type: Alumne
        # Crear un profe.
        grupProfessors, _ = Group.objects.get_or_create(name='professors')
        grupProfessionals, _ = Group.objects.get_or_create(name='professional')
        profe1 = Professor.objects.create(username='SrCastanya', password='patata') #type: Professor
        profe1.groups.add(grupProfessors)
        profe1.groups.add(grupProfessionals)
        profe1.set_password('patata')
        profe1.save()

        profe2 = Professor.objects.create(username='SrIntrus', password='patata') #type: Professor
        profe2.groups.add(grupProfessors)
        profe2.groups.add(grupProfessionals)
        profe2.set_password('patata')
        profe2.save()

        # Crear un horari
        tmpDS = DiaDeLaSetmana.objects.create(n_dia_uk=1,n_dia_ca=0,dia_2_lletres='DL',dia_de_la_setmana='dilluns', es_festiu=False)
        tmpFH = FranjaHoraria.objects.create(hora_inici = '9:00', hora_fi = '10:00')

        matresPrimerESO = Assignatura.objects.create(nom_assignatura='Mates', curs=primerESO)
        horari = Horari.objects.create(
            assignatura=matresPrimerESO, 
            professor=profe1,
            grup=self.primerESOA, 
            dia_de_la_setmana=tmpDS,
            hora=tmpFH,
            nom_aula='x',
            es_actiu=True)

        #Aquí hauriem de crear unes quantes classes a impartir i provar que l'aplicació funciona correctament.
        diaActual = date.today() #type: date
        diaActualSetmana = diaActual.weekday()
        dillunsActual = diaActual - timedelta(diaActualSetmana)

        impartirDilluns = Impartir.objects.create(
            horari = horari,
            professor_passa_llista = profe1,
            dia_impartir = dillunsActual
        )     
        self.impartirDilluns =impartirDilluns

        estatPresent = EstatControlAssistencia.objects.create( codi_estat = 'P', nom_estat='Present' )
        EstatControlAssistencia.objects.create( codi_estat = 'F', nom_estat='Falta' )
        EstatControlAssistencia.objects.create( codi_estat = 'R', nom_estat='Retard' )
        EstatControlAssistencia.objects.create( codi_estat = 'J', nom_estat='Justificada' )

        ControlAssistencia.objects.create(
            alumne = alumne,
            estat = estatPresent,
            impartir = impartirDilluns)

        ControlAssistencia.objects.create(
            alumne = alumne2,
            impartir = impartirDilluns)

    def test_alumne_creat(self):
        """Animals that can speak are correctly identified"""
        alumne = Alumne.objects.get(nom="Xevi")
        self.assertEqual(alumne.cognoms, 'Petit')
        
    def test_client(self):
        c=Client()
        response = c.post('http://localhost:8000/usuaris/login/', {'usuari':'SrCastanya', 'paraulaDePas':'patata'})
        response2 = c.get('http://127.0.0.1:8000/presenciaSetmanal/' + str(self.primerESOA.pk) + '/')
        f = open('prova.html','w')
        f.write(response2.content)
        f.close()
        self.assertNotEqual(response2.content,'')

    def _testComprovaCanviEstat(self, client, estatInicial, estatCanviat):
        url = self.urlBase + 'presenciaSetmanal/modificaEstatControlAssistencia/{2}/{0}/{1}'.format(
            self.alumne.pk, self.impartirDilluns.pk, quote(estatInicial))
        response = client.get(url) #type: HttpResponse
        self.assertIn(estatCanviat, response.content)

    def test_client_modificar_control_assistencia(self):
        settings.CUSTOM_NOMES_TUTOR_POT_JUSTIFICAR = True
        c=Client()
        response = c.post(self.urlBase + 'usuaris/login/', {'usuari':'SrCastanya', 'paraulaDePas':'patata'})
        self._testComprovaCanviEstat(c,'P','F')
        self._testComprovaCanviEstat(c,'F','R')
        self._testComprovaCanviEstat(c,'R',' ')
        self._testComprovaCanviEstat(c,' ','P')

    def test_client_modificar_control_assistencia_justifica_tothom(self):
        settings.CUSTOM_NOMES_TUTOR_POT_JUSTIFICAR = False
        c=Client()
        response = c.post(self.urlBase + 'usuaris/login/', {'usuari':'SrCastanya', 'paraulaDePas':'patata'})
        self._testComprovaCanviEstat(c,'P','F')
        self._testComprovaCanviEstat(c,'F','R')
        self._testComprovaCanviEstat(c,'R','J')
        self._testComprovaCanviEstat(c,'J',' ')
    
    def test_client_nopuc_modificar_assistencia_altri(self):
        c=Client()
        response = c.post(self.urlBase + 'usuaris/login/', {'usuari':'SrIntrus', 'paraulaDePas':'patata'})
        #Ha de donar error doncs l'usuari no pot modificar.
        #with self.assertRaises(AssertionError):
        #    self._testComprovaCanviEstat(c,'P','F')
        try:
            self._testComprovaCanviEstat(c,'P','F')
            self.fail("Error no s'ha generat excepció.")
        except AssertionError as identifier:
            pass #Tot bé.
            
        
