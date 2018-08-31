#encoding: utf-8
from typing import List, Generic, TypeVar
from selenium import webdriver
from django.test import TransactionTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from extHoraris import models
from extHoraris import utils as utilitats
import datetime
import utils
from django.contrib.auth.models import User
from extHoraris.tests_helper import PaginaLogin, SeleccioGrup, AfegirHorari
from selenium.webdriver.firefox.webelement import FirefoxWebElement
import sys
import ipdb
import traceback

class SimpleTest(TransactionTestCase):
    #Carrego una fixture.
    fixtures = ['testProfesClasseAMateixaHora.json']

    def setUp(self):
        self.profeAmbHoresSolapades="jpere@prova.cat"

    def test_ComprovaProfesSolapats(self):
        #Donat una hora concreta, cal comprovar que el profe no estigui fent classe d'una altre cosa a la mateixa hora.
        #En aquest cas es produeix aquest fet, el test ho ha de detectar.
        entrada = models.EntradaHorari.objects.filter(profe__nomUsuari=self.profeAmbHoresSolapades)[0] #type: models.EntradaHorari
        classesProfeMateixaHora = models.EntradaHorari.objects.filter(profe=entrada.profe, dia=entrada.dia, franja=entrada.franja)      
        self.assertEqual(len(classesProfeMateixaHora), 2)

    def test_TempsSeleccio(self):
        #Comprovar les hores que es solapen d'un grup, n'hi ha una.
        t1 = datetime.datetime.now()
        nHoresSolapades = utilitats.comprovaProfesSolapats(models.Grup.objects.get(nom='ADI1').pk)
        t2 = datetime.datetime.now()
        self.assertEqual(len(nHoresSolapades), 1)
        print ("debug:", t2 - t1)

class TestsIntegracio(StaticLiveServerTestCase):
    #Carrego una fixture.
    fixtures = ['testProfesClasseAMateixaHora.json']

    def test_afegirDuesHoresSolpadesIComprova(self):
        #Test que afegeix dues hores solapades en horaris diferents i comprova que apareguin a l'apartat visual de solapaments.
        try:
            #User.objects.create_user('horaris','horaris@gmail.com','horaris')
            driver = webdriver.Firefox()
            pag = PaginaLogin(driver, self.live_server_url)
            pag.dologin()
        
            grups = models.Grup.objectes().all()
            grup1 = grups[0] #type: models.Grup
            grup2 = grups[1] #type: models.Grup

            pag = AfegirHorari(driver, self.live_server_url, str(grup1.pk))
            opcions = pag.obtenirElementsSelect("idProfe")
            nomProfe = opcions[2].text
            pag.seleccionarElement(opcions[2])
            opcions = pag.obtenirElementsSelect("idAula")
            pag.seleccionarElement(opcions[0])
            opcions = pag.obtenirElementsSelect("idDia")
            pag.seleccionarElement(opcions[0])
            opcions = pag.obtenirElementsSelect("idFranja")
            pag.seleccionarElement(opcions[0])
            pag.inserirText("codiMateria", "MP01-1")
            pag.enviar()

            pag = AfegirHorari(driver, self.live_server_url, str(grup2.pk))
            opcions = pag.obtenirElementsSelect("idProfe")
            pag.seleccionarElement(opcions[2])
            opcions = pag.obtenirElementsSelect("idAula")
            pag.seleccionarElement(opcions[0])
            opcions = pag.obtenirElementsSelect("idDia")
            pag.seleccionarElement(opcions[0])
            opcions = pag.obtenirElementsSelect("idFranja")
            pag.seleccionarElement(opcions[0])
            pag.inserirText("codiMateria", "MP01-2")
            pag.enviar()

            pag.driver.implicitly_wait(10)
            
            elem=driver.find_element_by_xpath('//div[@class="form-signin"]')
            elements=elem.find_elements_by_tag_name("li")
            ok = False
            for elem in elements: #type: FirefoxWebElement
                repetit = elem.text #type: str
                if (nomProfe in repetit and grup1.nom in repetit and grup2.nom in repetit):
                    ok = True
                    break
            self.assertTrue(ok, "Error no s'ha trobat el profe repetit")
            
        except:
            #traceback.print_tb(sys.exc_info()[2])
            traceback.print_exc()
            ipdb.post_mortem(sys.exc_info()[2])

    def test_seleccionaGrup(self):
        try:
            #User.objects.create_user('horaris','horaris@gmail.com','horaris')
            driver = webdriver.Firefox()
            pag = PaginaLogin(driver, self.live_server_url)
            pag.dologin()
        
            pag = SeleccioGrup(driver, self.live_server_url)
            grups = pag.getGroups() #type: List[FirefoxWebElement]
            #Seleccionar el primer grup.
            assert (len(grups)>0)
            primerGrup = grups[0]
            primerGrupText = primerGrup.text
            pag.clickOpcio(primerGrup)
            pag.submit()
            #Esperem el wait per consultar si hem passat a la següent pàgina.
            driver.implicitly_wait(10)

            html = driver.page_source #type: str
            self.assertTrue(html.find(primerGrupText)!=-1 and  html.find("Nova entrada horari")!=-1)
        except:
            #traceback.print_tb(sys.exc_info()[2])
            traceback.print_exc()
            ipdb.post_mortem(sys.exc_info()[2])

    def test_crearHoraClasseIComprovarAlaBD(self):
        #Crear hores de classe i comprovar que s'han creat correctament a la BD.
        try:
            driver = webdriver.Firefox()
            pag = PaginaLogin(driver, self.live_server_url)
            pag.dologin()

            grups = models.Grup.objectes().all()
            primerGrup = grups[0] #type: models.Grup
            pag = AfegirHorari(driver, self.live_server_url, unicode(primerGrup.pk))
            opcions = pag.obtenirElementsSelect("idProfe")
            idProfe, nomProfe = pag.obtenirIdNomSelect(opcions[0])
            pag.seleccionarElement(opcions[0])
            opcions = pag.obtenirElementsSelect("idAula")
            idAula, nomAula = pag.obtenirIdNomSelect(opcions[0])
            pag.seleccionarElement(opcions[0])
            opcions = pag.obtenirElementsSelect("idDia")
            idDia, nomDia = pag.obtenirIdNomSelect(opcions[0])
            pag.seleccionarElement(opcions[0])
            opcions = pag.obtenirElementsSelect("idFranja")
            idFranja, nomFranja = pag.obtenirIdNomSelect(opcions[0])
            pag.seleccionarElement(opcions[0])
            codiMateria = "MP01-PROVA"
            pag.inserirText("codiMateria", codiMateria)
            pag.enviar()

            driver.implicitly_wait(10)

            objecte = models.EntradaHorari.objectes().get(profe_id=idProfe, aula_id=idAula, dia_id=idDia, franja_id=idFranja, materia__codi=codiMateria)
            self.assertIsNotNone(objecte)
        except:
            traceback.print_exc()
            ipdb.post_mortem(sys.exc_info()[2])
        
