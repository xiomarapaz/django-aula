#encoding: utf-8
from aula.utils.testing.tests import TestUtils
from aula.apps.alumnes.models import Nivell, Curs, Grup
from aula.apps.horaris.models import DiaDeLaSetmana, FranjaHoraria, Horari
from aula.apps.assignatures.models import Assignatura, TipusDAssignatura, UF
from aula.apps.presencia.models import Impartir, ControlAssistencia
from django.conf import settings
from datetime import date, timedelta

class TestDBCreator(object):
    '''
    Crea una BD de mostra per testejar el mòdul de presència.
    '''
    alumnes = None #type: QuerySet

    def __init__(self):
        
        tUtils = TestUtils()
        
        #Crear n alumnes.
        DAM = Nivell.objects.create(nom_nivell='DAM') #type: Nivell
        primerDAM = Curs.objects.create(nom_curs='1er', nivell=DAM) #type: Curs
        primerDAMA = Grup.objects.create(nom_grup='A', curs=primerDAM) #type: Grup
        self.nAlumnesGrup = 10
        alumnes = tUtils.generaAlumnesDinsUnGrup(primerDAMA, self.nAlumnesGrup)
        self.alumnes = alumnes
        # Crear un profe.
        profe1=tUtils.crearProfessor('SrProgramador','patata')
        
        # Crear un horari, 
        # compte, cal crear hores que ja hagin passat, per tal de fer el test.

        dataDiaActual = date.today() #type: date
        dataDiaAnterior = dataDiaActual - timedelta(1)
        dataDosDiesAnteriors = dataDiaActual - timedelta(2)
        diaAnterior = dataDiaAnterior.weekday()
        diaAnteriorUK = dataDiaAnterior.isoweekday()
        dosDiesAbans = dataDosDiesAnteriors.weekday()
        dosDiesAbansUK = dataDosDiesAnteriors.isoweekday()
        
        diesSetmana = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"]
        diesSetmana2Lletres = ["DL", "DM", "DI", "DJ", "DV", "DS", "DU"]
        
        tmpDS = DiaDeLaSetmana.objects.create(n_dia_uk=diaAnteriorUK,n_dia_ca=diaAnterior,
            dia_2_lletres=diesSetmana2Lletres[diaAnterior],dia_de_la_setmana=diesSetmana[diaAnterior], es_festiu=False)
        tmpDSSeguent = DiaDeLaSetmana.objects.create(n_dia_uk=dosDiesAbansUK,n_dia_ca=dosDiesAbans,
            dia_2_lletres=diesSetmana2Lletres[dosDiesAbans],dia_de_la_setmana=diesSetmana[dosDiesAbans], es_festiu=False)
        tmpFH1 = FranjaHoraria.objects.create(hora_inici = '9:00', hora_fi = '10:00')
        tmpFH2 = FranjaHoraria.objects.create(hora_inici = '10:00', hora_fi = '11:00')
        tmpFH3 = FranjaHoraria.objects.create(hora_inici = '11:00', hora_fi = '12:00')

        tipusAssigDiscontinuada = TipusDAssignatura.objects.create(
            tipus_assignatura=settings.CUSTOM_UNITAT_FORMATIVA_DISCONTINUADA)

        tipusAssigUF = TipusDAssignatura.objects.create(
            tipus_assignatura='Unitat Formativa'
        )

        programacioDAM = Assignatura.objects.create(
            nom_assignatura='Programació', curs=primerDAM,
            tipus_assignatura = tipusAssigUF
        )
        
        entradaHorari1 = Horari.objects.create(
            assignatura=programacioDAM, 
            professor=profe1,
            grup=primerDAMA, 
            dia_de_la_setmana=tmpDS,
            hora=tmpFH1,
            nom_aula='3.04',
            es_actiu=True)

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

        entradaHorari1_1 = Horari.objects.create(
            assignatura=programacioDAM, 
            professor=profe1,
            grup=primerDAMA, 
            dia_de_la_setmana=tmpDSSeguent,
            hora=tmpFH1,
            nom_aula='3.04',
            es_actiu=True)

        self.sistemesDAM_UF1=UF.objects.create(nom='UF1', dinici=date.today(), dfi=date.today()+timedelta(days=14), 
            horesTeoriques=2, assignatura=sistemesDAM) 
        self.sistemesDAM_UF2=UF.objects.create(nom='UF2', dinici=date.today(), dfi=date.today()+timedelta(days=14), 
            horesTeoriques=2, assignatura=sistemesDAM) 

        #Crea controls d'assistencia
        self.estats = tUtils.generarEstatsControlAssistencia()

        #Aquí hauriem de crear unes quantes classes a impartir i provar que l'aplicació funciona correctament.
        
        self.programacioDilluns = Impartir.objects.create(
            horari = entradaHorari1,
            professor_passa_llista = profe1,
            dia_impartir = dataDiaAnterior) #type: Impartir

        tUtils.omplirAlumnesHora(alumnes, self.programacioDilluns)

        self.sistemesDilluns = Impartir.objects.create(
            horari = entradaHorari2,
            professor_passa_llista = profe1,
            dia_impartir = dataDiaAnterior
        )     
        tUtils.omplirAlumnesHora(alumnes, self.sistemesDilluns)

        self.sistemesDillunsHora2 = Impartir.objects.create(
            horari = entradaHorari3,
            professor_passa_llista = profe1,
            dia_impartir = dataDiaAnterior
        )     
        tUtils.omplirAlumnesHora(alumnes, self.sistemesDillunsHora2)

        self.programacioDillunsHoraBuidaAlumnes = Impartir.objects.create(
            horari = entradaHorari1_1,
            professor_passa_llista = profe1,
            dia_impartir = dataDosDiesAnteriors
        )