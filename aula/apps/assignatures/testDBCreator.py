#encoding: utf-8
from aula.utils.testing.tests import TestUtils
from aula.apps.alumnes.models import Nivell, Curs, Grup
from aula.apps.horaris.models import DiaDeLaSetmana, FranjaHoraria, Horari
from aula.apps.assignatures.models import Assignatura, TipusDAssignatura, UF
from aula.apps.presencia.models import Impartir, ControlAssistencia
from aula import settings
from datetime import date, timedelta
from typing import List

class TestDBCreator(object):
    '''
    Crea una BD de mostra per testejar el mòdul d'assignatures.
    '''
    alumnes = None #type: QuerySet

    def __init__(self):
        #Crear un parell d'assignatures.
        #Crear uf's per cada assignatura.
        #Simular un alumne absentista que necessita ser avisat.
        tUtils = TestUtils()
        
        #Crear n alumnes.
        DAM = Nivell.objects.create(nom_nivell='DAM') #type: Nivell
        primerDAM = Curs.objects.create(nom_curs='1DAM', nivell=DAM) #type: Curs
        primerDAMA = Grup.objects.create(nom_grup='1DAM_GRUP_A', curs=primerDAM) #type: Grup
        
        self.nAlumnesGrup = 20
        alumnes = tUtils.generaAlumnesDinsUnGrup(primerDAMA, self.nAlumnesGrup)
        self.alumnes = alumnes
        # Crear un profe.
        self.nomProgramador = 'SrProgramador'
        self.passwordProgramador = 'patata'
        self.mailProgramador = "programador@servidor.com"
        profe1=tUtils.crearProfessor(self.nomProgramador, self.passwordProgramador, self.mailProgramador)
        self.profe1 = profe1

        #Crear profe sistemes
        self.nomSistemes = 'SrSistemes'
        self.passwordSistemes = 'patata'
        self.mailSistemes = "sistemes@servidor.com"
        profe2=tUtils.crearProfessor(self.nomSistemes, self.passwordSistemes, "sistemes@servidor.com")
        self.profe2 = profe2
        
        # Genero tots els dies laboralbes de la setmana 0-5 (5 és el dia actual)
        # compte, cal crear hores que ja hagin passat, per tal de fer el test.
        dies = [] #type: List[date]
        diesALaBD = [] #type: List[DiaDeLaSetmana]
        for i in range(0,7):
            dataActual = date.today() - timedelta(6-i) #type: date
            if dataActual.weekday() not in (5, 6): #Cap de setmana no gràfices.
                dies.append(dataActual)
                diesALaBD.append(
                    DiaDeLaSetmana.objects.create(n_dia_uk=dataActual.isoweekday(),n_dia_ca=dataActual.weekday(),
                        dia_2_lletres=TestUtils.diesSetmana2Lletres[dataActual.weekday()],dia_de_la_setmana=TestUtils.diesSetmana[dataActual.weekday()], es_festiu=False))
        self.dies = dies
        self.diesALaBD = diesALaBD
        franges = tUtils.generarFrangesHoraries()
        
        tipusAssigUF = TipusDAssignatura.objects.create(
            tipus_assignatura='Unitat Formativa'
        )

        self.tipusAssigUFDiscontinuada = TipusDAssignatura.objects.create(
            tipus_assignatura=settings.CUSTOM_UNITAT_FORMATIVA_DISCONTINUADA
        )

        programacioDAM = Assignatura.objects.create(
            nom_assignatura='Programació', curs=primerDAM,
            tipus_assignatura = tipusAssigUF, codi_assignatura='PROG') #type: Assignatura
        self.programacioDAM = programacioDAM 

        sistemesDAM = Assignatura.objects.create(
            nom_assignatura='Sistemes', curs=primerDAM,
            tipus_assignatura = tipusAssigUF, codi_assignatura='SISTEMES') #type: Assignatura
        self.sistemesDAM = sistemesDAM

        horesProgramacio = []
        for nDia in range(4, 1, -1):
            for nHora in range(0, 2):
                horesProgramacio.append(
                    Horari.objects.create(
                        assignatura=programacioDAM, 
                        professor=profe1,
                        grup=primerDAMA, 
                        dia_de_la_setmana=diesALaBD[4],
                        hora=franges[0], #de 9 a 10
                        nom_aula='3.04',
                        es_actiu=True))

        horesSistemes = []
        for nDia in range(0, 4):
            for nHora in range(3, 5):
                h = Horari.objects.create(assignatura=sistemesDAM, 
                    professor=profe2,
                    grup=primerDAMA, 
                    dia_de_la_setmana = diesALaBD[nDia],
                    hora = franges[nHora],
                    nom_aula='3.05',
                    es_actiu=True)
                horesSistemes.append(h)
                
        #Crea controls d'assistencia
        self.estats = tUtils.generarEstatsControlAssistencia()

        #Aquí hauriem de crear unes quantes classes a impartir i provar que l'aplicació funciona correctament.
        self.impartirHores = [] #type: List[Impartir]
        self.impartirHoresSistemes = [] #type: List[Impartir]

        self.impartirHores.append(
            Impartir.objects.create(
                horari = horesProgramacio[0],
                professor_passa_llista = profe1,
                dia_impartir = dies[4]))
        tUtils.omplirAlumnesHora(alumnes, self.impartirHores[-1])
        self.programacioDia6Hora1 = self.impartirHores[-1]

        self.impartirHores.append(
            Impartir.objects.create(
                horari = horesProgramacio[1],
                professor_passa_llista = profe1,
                dia_impartir = dies[4]))
        tUtils.omplirAlumnesHora(alumnes, self.impartirHores[-1])
        self.programacioDia6Hora2 = self.impartirHores[-1]

        self.impartirHores.append(
            Impartir.objects.create(
                horari = horesProgramacio[2],
                professor_passa_llista = profe1,
                dia_impartir = dies[3]))
        tUtils.omplirAlumnesHora(alumnes, self.impartirHores[-1])
        self.programacioDia5Hora1 = self.impartirHores[-1]

        self.impartirHores.append(
            Impartir.objects.create(
                horari = horesProgramacio[3],
                professor_passa_llista = profe1,
                dia_impartir = dies[3]))
        tUtils.omplirAlumnesHora(alumnes, self.impartirHores[-1])
        self.programacioDia5Hora2 = self.impartirHores[-1]

        self.impartirHores.append(
            Impartir.objects.create(
                horari = horesProgramacio[4],
                professor_passa_llista = profe1,
                dia_impartir = dies[2]))
        tUtils.omplirAlumnesHora(alumnes, self.impartirHores[-1])
        self.programacioDia4Hora1 = self.impartirHores[-1]
        
        self.impartirHores.append(
            Impartir.objects.create(
                horari = horesProgramacio[5],
                professor_passa_llista = profe1,
                dia_impartir = dies[2]))
        tUtils.omplirAlumnesHora(alumnes, self.impartirHores[-1])
        self.programacioDia4Hora2 = self.impartirHores[-1]

        #Hores sistemes.
        for nDia in range(0, 3):
            for nHora in range(0,5):
                self.impartirHoresSistemes.append(
                    Impartir.objects.create(
                        horari = horesSistemes[nHora],
                        professor_passa_llista = profe2,
                        dia_impartir = dies[nDia]))
                tUtils.omplirAlumnesHora(alumnes, self.impartirHoresSistemes[-1])