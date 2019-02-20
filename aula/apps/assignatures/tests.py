#encoding: utf-8

from django.test import TestCase, LiveServerTestCase
from aula.apps.assignatures.testDBCreator import TestDBCreator
from aula.utils.testing.seleniumTests import SeleniumTests
from aula.apps.presencia.models import ControlAssistencia, Impartir, EstatControlAssistencia
from aula.apps.assignatures.models import UF, Assignatura

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from datetime import datetime

from typing import List
from django.conf import settings
from aula.utils.testing.tests import TestUtils
from aula.apps.presencia.management.commands.avisarUFs import Command
from django.core.mail.message import EmailMultiAlternatives
from django.core import mail

class MySeleniumTests(LiveServerTestCase):
    #Testeig de Correus.
    #Testeig de passar llista amb UF's i comprovar que els llistat surtin correctament.
    #Test integració final, amb el cas tipic d'entrada d'UF's d'un usuari.

    def setUp(self):
        settings.CUSTOM_NOMES_TUTOR_POT_JUSTIFICAR = False
        settings.DEBUG = True
        #self.selenium.implicitly_wait(5)
    
    def tearDown(self):
        pass        

    def test_comprovarcioEnviarMailsAUnPercentatgeDeFaltesXUFDiscontinuada(self):
        #Crear una situació en que dos usuaris tingui un % de faltes superior al 20 per cent i altre no i comprovar que ho notifica correctament.
        try:
            self.db = TestDBCreator()
            assignatura = Assignatura.objects.get(codi_assignatura='PROG') #type: Assignatura
            assignatura.activar_notificacions = True
            assignatura.tipus_assignatura = self.db.tipusAssigUFDiscontinuada
            assignatura.percent_primer_avis = 24
            assignatura.percent_segon_avis = 49
            assignatura.save()

            diesOrdenats = list(self.db.dies)
            
            #Hores a impartir programació, son 6, farem 3 i 3 per uf.
            uf1 = UF.objects.create(nom = "UF1_Programacio", dinici = diesOrdenats[0], dfi = diesOrdenats[4], \
                assignatura=self.db.programacioDAM, horesTeoriques = 3)

            uf2 = UF.objects.create(nom = "UF2_Programacio", dinici = diesOrdenats[0], dfi = diesOrdenats[4], \
                assignatura=self.db.programacioDAM, horesTeoriques = 3)

            
            #Seleccionar dos alumnes aleatòriament.
            import random
            self.assertTrue(self.db.alumnes > 1, "No hi han prous alumnes, per seleccionar-ne dos a l'atzar")
            nAleatori = random.randint(0, len(self.db.alumnes)-1)
            nAleatori2 = random.randint(0, len(self.db.alumnes)-1)
            if nAleatori == nAleatori2:
                if nAleatori2 < len(self.db.alumnes)-1:
                    nAleatori2 += 1
                else:
                    nAleatori2 -= 1

            alumneAmbFaltes1 = self.db.alumnes[nAleatori]
            alumneAmbFaltes2 = self.db.alumnes[nAleatori2]

            #Per cada alumne assignar 3 hores uf1 i 3 de uf2.
            patroUFs = [uf1,uf2,uf1,uf2,uf1,uf2]
            patroAssistencia = ['P','P','P','F','F','P']
            alumne = alumneAmbFaltes1
            nVolta=0
            for horaImpartir in self.db.impartirHores:
                ca = ControlAssistencia.objects.get(alumne=alumne, impartir=horaImpartir) #type: ControlAssistencia
                ca.estat=EstatControlAssistencia.objects.get(codi_estat=patroAssistencia[nVolta])
                ca.uf = patroUFs[nVolta]
                ca.professor = self.db.profe1
                ca.save()
                nVolta+=1

            patroUFs =  [uf1,uf1,uf1,uf2,uf2,uf2]
            patroAssistencia = ['P','P','P','F','F','F']
            alumne = alumneAmbFaltes2
            nVolta=0
            for horaImpartir in self.db.impartirHores:
                ca = ControlAssistencia.objects.get(alumne=alumne, impartir=horaImpartir) #type: ControlAssistencia
                ca.estat=EstatControlAssistencia.objects.get(codi_estat=patroAssistencia[nVolta])
                ca.uf = patroUFs[nVolta]
                ca.professor = self.db.profe1
                ca.save()
                nVolta+=1

            #Enviar mails.
            c = Command()
            c.handle()
            
            #Comprovar que el correu s'ha enviat (registre fals de Django)
            self.assertTrue(len(mail.outbox)==1)
            #Comprovar que les dades dels correus s'han generat correctament.
            dadesMail = c.dadesEnviadesAUltimaTramesa[0]
            for reg in dadesMail.dadesAEnviar:
                self.assertTrue(
                    (reg[0] == alumneAmbFaltes1 and reg[3]>=33 and reg[3]<=33.5) or
                    (reg[0] == alumneAmbFaltes2 and reg[3]==100 and reg[1] == uf2))
        except:
            TestUtils.llancaPostMortem()

    def test_comprovarcioEnviarMailsAUnPercentatgeDeFaltes(self):
        #Crear una situació en que dos usuaris tingui un % de faltes superior al 20 per cent i altre no i comprovar que ho notifica correctament.
        try:
            self.db = TestDBCreator()
            assignatura = Assignatura.objects.get(codi_assignatura='PROG') #type: Assignatura
            assignatura.activar_notificacions = True
            assignatura.percent_primer_avis = 24
            assignatura.percent_segon_avis = 49
            assignatura.save()

            assignatura = Assignatura.objects.get(codi_assignatura='SISTEMES') #type: Assignatura
            assignatura.activar_notificacions = True
            assignatura.percent_primer_avis = 24
            assignatura.percent_segon_avis = 49
            assignatura.save()

            diesOrdenats = list(self.db.dies)
            diesOrdenats.reverse()
            
            #Hores a impartir programació
            uf = UF.objects.create(nom = "UF1_Programacio", dinici = diesOrdenats[1], dfi = diesOrdenats[0], \
                assignatura=self.db.programacioDAM, horesTeoriques = 4)
            horesImpartirDeLaUF = []
            for impartir in self.db.impartirHores:
                if (impartir.dia_impartir >= diesOrdenats[1] and impartir.dia_impartir <= diesOrdenats[0]):
                    horesImpartirDeLaUF.append(impartir)

            alumneAmbFaltes1 = self.db.alumnes[0]
            alumneAmbFaltes2 = self.db.alumnes[1]

            nVolta = 0
            for horaImpartir in horesImpartirDeLaUF:
                #Alumne 1 només té una falta de 4.
                codi_estat = 'P'
                if nVolta == 0:
                    codi_estat = 'F'
                
                ca = ControlAssistencia.objects.get(alumne=alumneAmbFaltes1, impartir=horaImpartir) #type: ControlAssistencia
                ca.estat=EstatControlAssistencia.objects.get(codi_estat=codi_estat)
                ca.professor = self.db.profe1
                ca.save()

                #Alumne 2 té dues faltes de 4.
                codi_estat = 'P'
                if nVolta < 2:
                    codi_estat = 'F'
                
                ca = ControlAssistencia.objects.get(alumne=alumneAmbFaltes2, impartir=horaImpartir) #type: ControlAssistencia
                ca.estat=EstatControlAssistencia.objects.get(codi_estat=codi_estat)
                ca.professor = self.db.profe1
                ca.save()
                nVolta+=1

            #Hores a impartir sistemes.
            uf = UF.objects.create(nom = "UF1_Sistemes", dinici = diesOrdenats[2], dfi = diesOrdenats[0], \
                assignatura=self.db.sistemesDAM, horesTeoriques = 6)
            horesImpartirDeLaUF = []
            for impartir in self.db.impartirHoresSistemes:
                if (impartir.dia_impartir >= diesOrdenats[2] and impartir.dia_impartir <= diesOrdenats[0]):
                    horesImpartirDeLaUF.append(impartir)

            nVolta = 0
            for horaImpartir in horesImpartirDeLaUF:
                #Alumne 1 només té dues faltes de 6.
                codi_estat = 'P'
                if nVolta >= 0 and nVolta <=1:
                    codi_estat = 'F'
                
                ca = ControlAssistencia.objects.get(alumne=alumneAmbFaltes1, impartir=horaImpartir) #type: ControlAssistencia
                ca.estat=EstatControlAssistencia.objects.get(codi_estat=codi_estat)
                ca.professor = self.db.profe2
                ca.save()

                #Alumne 2 té tres faltes de 6.
                codi_estat = 'P'
                if nVolta >= 0 and nVolta <=2:
                    codi_estat = 'F'
                
                ca = ControlAssistencia.objects.get(alumne=alumneAmbFaltes2, impartir=horaImpartir) #type: ControlAssistencia
                ca.estat=EstatControlAssistencia.objects.get(codi_estat=codi_estat)
                ca.professor = self.db.profe2
                ca.save()
                nVolta+=1

            #Enviar mails.
            c = Command()
            c.handle()
            self.assertTrue(len(mail.outbox)==2)
            
            #comprova el destinatari del correu i el % de faltes.
            for i in range(0,len(mail.outbox)):
                m=mail.outbox[i] #type: EmailMultiAlternatives
                if self.db.mailProgramador in m.to:
                    dadesMail = c.dadesEnviadesAUltimaTramesa[i] #Dades del correu i que s'ha enviat.
                    for reg in dadesMail.dadesAEnviar:
                        #Comprovar que si es tracta de l'alumne1 té un 50% i si és l'alumne2 té un 24% de faltes.
                        self.assertTrue(
                            (reg[0] == alumneAmbFaltes2 and reg[3] == 50) or
                            (reg[0] == alumneAmbFaltes1 and reg[3] == 25))
                
                elif self.db.mailSistemes in m.to:
                    dadesMail = c.dadesEnviadesAUltimaTramesa[i] #Dades del correu enviat.
                    for reg in dadesMail.dadesAEnviar:
                        #Comprovar que si es tracta de l'alumne1 té un 50% i si és l'alumne2 té un 33% de faltes.
                        self.assertTrue(
                            (reg[0] == alumneAmbFaltes2 and reg[3] == 50) or
                            (reg[0] == alumneAmbFaltes1 and reg[3] >= 33 and reg[3] < 33.5))
                else:
                    raise Exception("El correu no va adreçat a ningú conegut.")
        except:
            TestUtils.llancaPostMortem()
            
    def test_comprovacioHoresUFs(self):
        #Crea les UF's, passa llista via codi i comprova que el llistat sigui correcte amb selenium.
        try:
            self.db = TestDBCreator()
            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            self.selenium = WebDriver(options=options)
            st = SeleniumTests(self.live_server_url, self.selenium)
            diesOrdenats = list(self.db.dies)
            diesOrdenats.reverse()
            uf = UF.objects.create(nom = "UF1", dinici = diesOrdenats[1], dfi = diesOrdenats[0], \
                assignatura=self.db.programacioDAM, horesTeoriques = 4)
            uf = UF.objects.create(nom = "UF2", dinici = diesOrdenats[4], dfi = diesOrdenats[2], \
                assignatura=self.db.programacioDAM, horesTeoriques = 2)
            
            for impartir in self.db.impartirHores:
                nAlumne = 0
                for alumne in self.db.alumnes:
                    #Els primers alumnes els hi posem falta, justificada i retard.
                    ca = ControlAssistencia.objects.get(impartir_id=impartir.pk, alumne_id=alumne.pk)
                    ca.currentUser = self.db.profe1
                    ca.professor = self.db.profe1
                    ca.credentials = ( self.db.profe1, True) #Usuari i L4.
                    estat = 'P'
                    if nAlumne==0:
                        estat='F'
                    elif nAlumne == 1:
                        estat='J'
                    elif nAlumne == 2:
                        estat='R'
                    ca.estat = EstatControlAssistencia.objects.get(codi_estat=estat)
                    ca.save()
                    nAlumne+=1

                impartir.dia_passa_llista = datetime.now()
                impartir.professor_passa_llista = self.db.profe1
                impartir.currentUser = self.db.profe1
                impartir.save()

            st = SeleniumTests(self.live_server_url, self.selenium)
            st.loginUsuari('SrProgramador', 'patata')

            self.selenium.get(self.live_server_url + '/assignatures/llistatAssistenciaEntreDates/')
            comboGrup = Select(self.selenium.find_element_by_name("grup"))
            opcio = comboGrup.options[1] #type: FirefoxWebElement
            comboGrup.select_by_value(opcio.get_attribute("value"))

            comboGrup = Select(self.selenium.find_element_by_name("assignatura"))
            opcio = comboGrup.options[0] #type: FirefoxWebElement
            comboGrup.select_by_value(opcio.get_attribute("value"))
            
            self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

            #Comprovar que el llistat és correcte.
            faltesJustificades, faltesInjustificades, hAssistencia, hProgramades = self.obtenirFaltesAlumne(self.db.alumnes[0])
            self.assertTrue(hAssistencia==0) #Tot és falta.
            self.assertTrue(hProgramades==4)
            self.assertTrue(faltesInjustificades == 4)
            self.assertTrue(faltesJustificades == 0)

            faltesJustificades, faltesInjustificades, hAssistencia, hProgramades = self.obtenirFaltesAlumne(self.db.alumnes[1])
            self.assertTrue(hAssistencia==0) #Tot és justificat.
            self.assertTrue(hProgramades==4)
            self.assertTrue(faltesInjustificades == 0)
            self.assertTrue(faltesJustificades == 4)

            alumne = self.db.alumnes[2]
            faltesJustificades, faltesInjustificades, hAssistencia, hProgramades = self.obtenirFaltesAlumne(alumne)
            self.assertTrue(hAssistencia==4) #Tot és retard.
            self.assertTrue(hProgramades==4)
            self.assertTrue(faltesInjustificades == 0)
            self.assertTrue(faltesJustificades == 0)
            alumne.controlassistencia_set.filter(estat__codi_estat='R')

            faltesJustificades, faltesInjustificades, hAssistencia, hProgramades = self.obtenirFaltesAlumne(self.db.alumnes[3])
            self.assertTrue(hAssistencia==4) #Tot és falta.
            self.assertTrue(hProgramades==4)
            self.assertTrue(faltesInjustificades == 0)
            self.assertTrue(faltesJustificades == 0)
        except:
            TestUtils.llancaPostMortem()
        finally:
            self.selenium.close()

    def test_integracio(self):
        try:
            self.db = TestDBCreator()
            #Fa el recorregut complert, crear UFs, passar llista, comprovar que els llistats apareguin correctament, tot a cop de Selenium.
            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            self.selenium = WebDriver(options=options)
            st = SeleniumTests(self.live_server_url, self.selenium)
            st.loginUsuari('SrProgramador', 'patata')
            
            #Comprovar que no existeix cap unitat formativa, crear tres unitats.
            self.selenium.get(self.live_server_url + '/assignatures/veureUnitatsFormatives/{}/'.format(self.db.programacioDAM.pk))
            self.assertFalse("Eliminar" in self.selenium.page_source)
            
            #Passar llista
            self.crearUnitatFormativa("uf1", "4", self.db.dies[3], self.db.dies[4])
            self.crearUnitatFormativa("uf2", "2", self.db.dies[0], self.db.dies[2])
            self.passarLlistaAPresentExcepteTresPrimers(self.db.impartirHores)

            #Comprovar estadístiques llistat.
            self.selenium.get(self.live_server_url + '/assignatures/llistatAssistenciaEntreDates/')
            comboGrup = Select(self.selenium.find_element_by_name("grup"))
            opcio = comboGrup.options[1] #type: FirefoxWebElement
            comboGrup.select_by_value(opcio.get_attribute("value"))

            comboGrup = Select(self.selenium.find_element_by_name("assignatura"))
            opcio = comboGrup.options[0] #type: FirefoxWebElement
            comboGrup.select_by_value(opcio.get_attribute("value"))
            
            self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()
            
            #Comprovar que el llistat és correcte.
            faltesJustificades, faltesInjustificades, hAssistencia, hProgramades = self.obtenirFaltesAlumne(self.db.alumnes[0])
            self.assertTrue(hAssistencia==0) #Tot és falta.
            self.assertTrue(hProgramades==4)
            self.assertTrue(faltesInjustificades == 4)
            self.assertTrue(faltesJustificades == 0)

            faltesJustificades, faltesInjustificades, hAssistencia, hProgramades = self.obtenirFaltesAlumne(self.db.alumnes[1])
            self.assertTrue(hAssistencia==4) #Tot és retard.
            self.assertTrue(hProgramades==4)
            self.assertTrue(faltesInjustificades == 0)
            self.assertTrue(faltesJustificades == 0)

            faltesJustificades, faltesInjustificades, hAssistencia, hProgramades = self.obtenirFaltesAlumne(self.db.alumnes[2])
            self.assertTrue(hAssistencia==0) #Tot és justificada.
            self.assertTrue(hProgramades==4)
            self.assertTrue(faltesInjustificades == 0)
            self.assertTrue(faltesJustificades == 4)
            self.selenium.close()
        except:
            TestUtils.llancaPostMortem()

    def obtenirFaltesAlumne(self, alumne):
        #type: (Alumne)->List[int]
        nomAlumne = alumne.cognoms + ", " + alumne.nom
        tdAlumne = self.selenium.find_element_by_xpath(u"//TD[contains(text(),'" + nomAlumne + "')]") #type: FirefoxWebElement
        trAlumne=tdAlumne.find_element_by_xpath('./..')
        tds=trAlumne.find_elements_by_tag_name('td') #type: List[FirefoxWebElement]
        faltesJustificades = int(tds[1].text)
        faltesInjustificades = int(tds[2].text)
        hAssistencia = int(tds[3].text)
        hProgramades = int(tds[4].text)
        return faltesJustificades, faltesInjustificades, hAssistencia, hProgramades

    def crearUnitatFormativa(self, nomUf, horesTeoriques, dataInici, dataFi):
        #type: (str, str, datetime, datetime)->None
        self.selenium.get(self.live_server_url + '/assignatures/crearUnitatFormativa/{}/'.format(self.db.programacioDAM.pk))
        camp = self.selenium.find_element_by_id("id_nom")
        camp.send_keys(nomUf)
        
        camp = self.selenium.find_element_by_id("id_horesTeoriques")
        camp.send_keys(horesTeoriques)

        camp = self.selenium.find_element_by_id("id_data_inici")
        camp.clear()
        camp.send_keys(dataInici.strftime('%d/%m/%Y'))

        camp = self.selenium.find_element_by_id("id_data_fi")
        camp.clear()
        camp.send_keys(dataFi.strftime('%d/%m/%Y'))
        
        self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

    def passarLlistaAPresentExcepteTresPrimers(self, hores):
        #type: (List[Impartir])->Any
        
        for horaImpartir in hores: #type: Impartir
            #Passar llista tots a present.
            self.selenium.get(self.live_server_url + '/presencia/passaLlista/' + str(horaImpartir.pk) + '/')
            cas=ControlAssistencia.objects.filter(impartir_id= horaImpartir.pk)
            for ca in cas:
                self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_0"); x.click()'.format(ca.pk))
            self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_1"); x.click()'.format(cas[0].pk)) #F
            self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_2"); x.click()'.format(cas[1].pk)) #R
            self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_3"); x.click()'.format(cas[2].pk)) #J
            self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()
        

    
