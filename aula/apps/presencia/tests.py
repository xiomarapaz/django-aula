#encoding: utf-8
import re
from django.test import TestCase, LiveServerTestCase
from django.test import Client
from aula.utils.testing.tests import TestUtils
from aula.apps.alumnes.models import Nivell, Curs, Grup
from aula.apps.horaris.models import DiaDeLaSetmana, FranjaHoraria, Horari
from aula.apps.assignatures.models import Assignatura, TipusDAssignatura, UF
from aula.apps.presencia.models import Impartir, ControlAssistencia
from django.conf import settings
from datetime import date, timedelta
from aula.apps.presencia.test.testDBCreator import TestDBCreator

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox import webelement

'''
class SimpleTest(TestCase):

    def setUp(self):
        tUtils = TestUtils()
        
        #Crear n alumnes.
        DAM = Nivell.objects.create(nom_nivell='DAM') #type: Nivell
        primerDAM = Curs.objects.create(nom_curs='1er', nivell=DAM) #type: Curs
        primerDAMA = Grup.objects.create(nom_grup='A', curs=primerDAM) #type: Grup
        self.nAlumnesGrup = 10
        alumnes = tUtils.generaAlumnesDinsUnGrup(primerDAMA, self.nAlumnesGrup)

        # Crear un profe.
        profe1=tUtils.crearProfessor('SrProgramador','patata')
        
        # Crear un horari
        tmpDS = DiaDeLaSetmana.objects.create(n_dia_uk=1,n_dia_ca=0,dia_2_lletres='DL',dia_de_la_setmana='dilluns', es_festiu=False)
        tmpFH1 = FranjaHoraria.objects.create(hora_inici = '9:00', hora_fi = '10:00')
        tmpFH2 = FranjaHoraria.objects.create(hora_inici = '10:00', hora_fi = '11:00')
        tmpFH3 = FranjaHoraria.objects.create(hora_inici = '11:00', hora_fi = '12:00')

        programacioDAM = Assignatura.objects.create(nom_assignatura='Programació', curs=primerDAM)
        entradaHorari1 = Horari.objects.create(
            assignatura=programacioDAM, 
            professor=profe1,
            grup=primerDAMA, 
            dia_de_la_setmana=tmpDS,
            hora=tmpFH1,
            nom_aula='3.04',
            es_actiu=True)

        tipusAssigDiscontinuada = TipusDAssignatura.objects.create(
            tipus_assignatura=settings.CUSTOM_UNITAT_FORMATIVA_DISCONTINUADA)

        sistemesDAM = Assignatura.objects.create(
            nom_assignatura='Sistemes', 
            curs=primerDAM,
            tipus_assignatura=tipusAssigDiscontinuada)

        entradaHorari2 = Horari.objects.create(
            assignatura=sistemesDAM, 
            professor=profe1,
            grup=primerDAMA, 
            dia_de_la_setmana=tmpDS,
            hora=tmpFH2,
            nom_aula='3.04',
            es_actiu=True)

        entradaHorari3 = Horari.objects.create(
            assignatura=sistemesDAM, 
            professor=profe1,
            grup=primerDAMA, 
            dia_de_la_setmana=tmpDS,
            hora=tmpFH3,
            nom_aula='3.04',
            es_actiu=True)

        self.sistemesDAM_UF1=UF.objects.create(nom='UF1', dinici=date.today(), dfi=date.today()+timedelta(days=14), 
            horesTeoriques=2, assignatura=sistemesDAM) 
        self.sistemesDAM_UF2=UF.objects.create(nom='UF2', dinici=date.today(), dfi=date.today()+timedelta(days=14), 
            horesTeoriques=2, assignatura=sistemesDAM) 

        #Crea controls d'assistencia
        self.estats = tUtils.generarEstatsControlAssistencia()

        #Aquí hauriem de crear unes quantes classes a impartir i provar que l'aplicació funciona correctament.
        diaActual = date.today() #type: date
        diaActualSetmana = diaActual.weekday()
        dillunsActual = diaActual - timedelta(diaActualSetmana)

        self.programacioDilluns = Impartir.objects.create(
            horari = entradaHorari1,
            professor_passa_llista = profe1,
            dia_impartir = dillunsActual) #type: Impartir

        tUtils.omplirAlumnesHora(alumnes, self.programacioDilluns)

        self.sistemesDilluns = Impartir.objects.create(
            horari = entradaHorari2,
            professor_passa_llista = profe1,
            dia_impartir = dillunsActual
        )     
        tUtils.omplirAlumnesHora(alumnes, self.sistemesDilluns)

        self.sistemesDillunsHora2 = Impartir.objects.create(
            horari = entradaHorari3,
            professor_passa_llista = profe1,
            dia_impartir = dillunsActual
        )     
        tUtils.omplirAlumnesHora(alumnes, self.sistemesDillunsHora2)

 
    def test_numeroAlumnesMostratsEsCorrecte(self):
        c = Client()
        response = c.post('http://localhost:8000/usuaris/login/', {'usuari':'SrProgramador', 'paraulaDePas':'patata'})
        response = c.get('http://localhost:8000/presencia/passaLlista/' + str(self.programacioDilluns.pk) + '/')
        nBotonsPresent = response.content.count("btn btn-default btnPresent")
        self.assertTrue(nBotonsPresent == self.nAlumnesGrup, "Error falten usuaris en el llistat")

    def test_passarLlistaModificaBD(self):
        c = Client()
        response = c.post('http://localhost:8000/usuaris/login/', {'usuari':'SrProgramador', 'paraulaDePas':'patata'})
        response = c.get('http://localhost:8000/presencia/passaLlista/' + str(self.programacioDilluns.pk) + '/')
        #Localitzar els CA's que cal enviar.
        estatsAEnviar=self.obtenirEstats(response.content)
        
        response = c.post('http://localhost:8000/presencia/passaLlista/' + str(self.programacioDilluns.pk) + '/', 
         estatsAEnviar)
        
        #Comprova que ha canviat l'estat.
        controlsAssistencia = ControlAssistencia.objects.filter(impartir=self.programacioDilluns, estat=self.estats['p'])
        self.assertTrue(len(controlsAssistencia) == self.nAlumnesGrup, 
            "Error el número de controls d'assisència marcats com a present hauria de ser " + str(self.nAlumnesGrup) + 
            "i és:" + str(len(controlsAssistencia)))

    def test_passarLlistaModificaBD_unitatsFormativesDiscontinuades(self):
        #Passar llista amb unitats formatives discontinuades, tenim en compte la UF.
        c = Client()
        response = c.post('http://localhost:8000/usuaris/login/', {'usuari':'SrProgramador', 'paraulaDePas':'patata'})
        response = c.get('http://localhost:8000/presencia/passaLlista/' + str(self.sistemesDilluns.pk) + '/')
        
        estatsAEnviar=self.obtenirEstats(response.content)
        ufsAEnviar=self.obtenirUFs(response.content)
        dadesPost = {} #type: List[int]
        dadesPost.update(estatsAEnviar)
        dadesPost.update(ufsAEnviar)

        response = c.post('http://localhost:8000/presencia/passaLlista/' + str(self.sistemesDilluns.pk) + '/', 
         dadesPost)

        #Comprova que ha canviat l'estat de la UF i l'estat de l'assistència.
        #TODO
        controlsAssistencia = ControlAssistencia.objects.filter(impartir=self.sistemesDilluns, 
            estat=self.estats['p'], uf=self.sistemesDAM_UF2)
        self.assertTrue(len(controlsAssistencia)== self.nAlumnesGrup)
    
    
    def test_passarLlistaUnitatsFormatives_passarLlistaHoraSeguentComprovarUFS(self):
        #Test per comprovar que passant llista a una hora la següent conserva les unitats formatives.
        c = Client()
        response = c.post('http://localhost:8000/usuaris/login/', {'usuari':'SrProgramador', 'paraulaDePas':'patata'})
        response = c.get('http://localhost:8000/presencia/passaLlista/' + str(self.sistemesDilluns.pk) + '/')
        
        estatsAEnviar=self.obtenirEstats(response.content)
        ufsAEnviar=self.obtenirUFs(response.content)
        dadesPost = {} #type: List[int]
        dadesPost.update(estatsAEnviar)
        dadesPost.update(ufsAEnviar)
    
        controlsAssitenciaIUfs = self.obtenirControlAssistenciaIUfs(response.content)

        c.post('http://localhost:8000/presencia/passaLlista/' + str(self.sistemesDilluns.pk) + '/', 
            dadesPost)

        #Comprovar que a la següent hora hi han marcades les uf's de la primera.
        response = c.get('http://localhost:8000/presencia/passaLlista/' + str(self.sistemesDillunsHora2.pk) + '/')
        controlsAssitenciaIUfsHora2 = self.obtenirControlAssistenciaIUfs(response.content)

        #comprovar que totes les UF's es marquen com a UF2 al seleccionar el botó de l'hora anterior.
        for codiControlAssistencia in controlsAssitenciaIUfsHora2.keys():
            self.assertIsNotNone(re.search('\$\(\'\#rad_id_{0}+-uf_{1}+'.format(codiControlAssistencia, '1'), response.content))
        
    def obtenirEstats(self, html):
        valorsAEnviar={}
        
        matches=re.findall('name="[0-9]+-estat"', html)
        for match in matches:
            coincidencia = str(match)[6:-1]
            valorsAEnviar[coincidencia] = self.estats['p'].pk
        return valorsAEnviar

    def obtenirIdEstats(self, estats):
        #type: Dict[str] -> List[str]
        tmp = []
        for estat in estats.keys():
            tmp.append(estat[:-6])
        return tmp

    def obtenirUFs(self, html):
        valorsAEnviar={}
        
        matches=re.findall('name="[0-9]+-uf"', html)
        for match in matches:
            coincidencia = str(match)[6:-1]
            valorsAEnviar[coincidencia] = self.sistemesDAM_UF2.pk
        return valorsAEnviar

    def obtenirControlAssistenciaIUfs(self, html):
        # type: (str)->Dict[List[int]]
        #Obtenir els codis del control d'assitència i les ufs.
        matches = re.findall('id="rad_id_([0-9]+)-uf_([0-9]+)', html)
        controlsIUFs = {} # type: Dict[List[int]] 
        for match in matches:
            if not controlsIUFs.has_key(match[0]):
                controlsIUFs[match[0]] = list(match[1])
            else:
                controlsIUFs[match[0]].append(match[1])
        return controlsIUFs
'''

class MySeleniumTests(LiveServerTestCase):

    def setUp(self):
        self.db = TestDBCreator()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(5)
    
    def tearDown(self):
        self.selenium.close()

    def test_treureAlumnes(self):
        self.loginUsuari()

        self.selenium.get(self.live_server_url + '/presencia/afegeixAlumnesLlista/' + 
            str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')
        #Comprovar quants alumnes hi ha seleccionats en aquesta hora. No n'hi hauria d'haver cap.
        cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
        self.assertTrue(len(cas)==0)

        #Seleccionar dos usuaris.
        for i in xrange(0,2):
            js = """ x = document.evaluate('//input[@type=\\\'checkbox\\\' and @value="""+str(self.db.alumnes[i].pk)+"""]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null );
                    x.singleNodeValue.click();
                """
            self.selenium.execute_script(js)
        #import ipdb; ipdb.set_trace()
        self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()
        
        #Comprovar alumnes en aquesta hora, n'hi hauria d'haver-hi dos.
        cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
        self.assertTrue(len(cas)==2)

        self.selenium.get(self.live_server_url + '/presencia/treuAlumnesLlista/' + 
            str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')

        #Seleccionar dos usuaris.
        js = """ x = document.evaluate('//input[@type=\\\'checkbox\\\' and @value="""+str(self.db.alumnes[0].pk)+"""]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null );
                x.singleNodeValue.click();
            """
        self.selenium.execute_script(js)
        self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()
        
        #Queda només un usuari.
        cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
        self.assertTrue(len(cas)==1)
    
    def test_selenium_passaLlistaPerUFs(self):
        self.loginUsuari()
        self.passaLlista()
        
        cas=ControlAssistencia.objects.filter(impartir_id=self.db.sistemesDilluns.pk)
        for ca in cas: #type: ControlAssistencia
            self.assertTrue(ca.estat.codi_estat == 'P' or ca.uf.nom=='UF1')

    def test_afegirAlumnes(self):
        self.loginUsuari()

        self.selenium.get(self.live_server_url + '/presencia/afegeixAlumnesLlista/' + 
            str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')
        #Comprovar quants alumnes hi ha seleccionats en aquesta hora. No n'hi hauria d'haver cap.
        cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
        self.assertTrue(len(cas)==0)

        #Seleccionar uns quants usuaris.
        self.selenium.execute_script('''
            cbox = document.getElementsByTagName("input");
                for (i=0;i<cbox.length;i++){
                    if (cbox[i].type == "checkbox") {
                    console.log("hola:" + cbox[i].type); 
                    cbox[i].click()
                }
            }
        ''')
        botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
        botons[0].click()
        
        #Comprovar alumnes en aquesta hora, hi haurien de ser tots.
        cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
        self.assertTrue(len(cas)==self.db.nAlumnesGrup)

    def test_passaLlista(self):
        #Passar llista convencional.
        self.loginUsuari()
        
        self.selenium.get(self.live_server_url + '/presencia/passaLlista/' + str(self.db.programacioDilluns.pk) + '/')
        #Obtenir tots els controls d'assistenica de l'hora marcada
        cas=ControlAssistencia.objects.filter(impartir_id=self.db.programacioDilluns.pk)
        #Seleccionar controls amb un script, no sé perque no funciona de la forma habitual.
        self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_0"); x.click()'.format(cas[0].pk))
        for i in range(1, len(cas)):
            self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_1"); x.click()'.format(cas[i].pk))
        
        botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
        botons[0].click()
        #Comprovar que tots els controls han quedat marcats. (He posat faltes a tots)
        cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDilluns.pk)
        self.assertTrue(cas[0].estat.codi_estat=='P')
        for i in range(1, len(cas)):
            self.assertTrue(cas[i].estat.codi_estat=='F')

    def test_passaLlistaPerUFsHoraSeguent(self):
        #Passo llista a l'hora següent, hauria de guardar la configuració correctament.
        self.loginUsuari()
        self.passaLlista()
        
        #Passo llista exàctament igual que l'hora anterior.
        self.selenium.get(self.live_server_url + '/presencia/passaLlista/' + str(self.db.sistemesDillunsHora2.pk) + '/')
        boto = self.selenium.find_element_by_id("ufsHoraAnterior")
        boto.click()
        boto = self.selenium.find_element_by_id("horaAnterior")
        boto.click()
        botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
        botons[0].click()

        #Comprovar resultats.
        cas=ControlAssistencia.objects.filter(impartir_id=self.db.sistemesDillunsHora2.pk)
        for ca in cas: #type: ControlAssistencia
            self.assertTrue(ca.estat.codi_estat == 'P' and ca.uf.nom=='UF1')

    def loginUsuari(self):
        self.selenium.get( self.live_server_url + '/usuaris/login/')
        #localitza usuari i paraulaDePas
        inputUser = self.selenium.find_element_by_name("usuari")
        inputUser.clear()
        inputUser.send_keys('SrProgramador')
        inputParaulaDePas = self.selenium.find_element_by_name("paraulaDePas")
        inputParaulaDePas.clear()
        inputParaulaDePas.send_keys('patata')
        botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
        boto = botons[0]
        boto.click()

    def passaLlista(self):
        self.selenium.get(self.live_server_url + '/presencia/passaLlista/' + str(self.db.sistemesDilluns.pk) + '/')
        #Obtenir tots els controls d'assistenica de l'hora marcada
        cas=ControlAssistencia.objects.filter(impartir_id=self.db.sistemesDilluns.pk)
        #Seleccionar controls amb un script, no sé perque no funciona de la forma habitual.
        for ca in cas:
            self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_0"); x.click()'.format(ca.pk))
            self.selenium.execute_script('x=document.getElementById("label_id_{}-uf_0"); x.click()'.format(ca.pk))
            
        botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
        botons[0].click()

        

