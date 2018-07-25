#encoding:utf-8
from models import Impartir

def obtenir_hora_anterior(element):
    #A partir de les dades d'un control d'assistència obtenim
    #informació de la hora anterior.
    import datetime
    from aula.apps.presencia.models import ControlAssistencia

    horaInici = element.impartir.horari.hora.hora_inici
    dataHoraInici = datetime.datetime.combine(element.impartir.dia_impartir, horaInici)
    unaHora40abans = dataHoraInici + datetime.timedelta(seconds=-100*60)
    controls_anteriors = ControlAssistencia.objects.filter(
                     alumne = element.alumne,
                     impartir__horari__hora__hora_inici__lt = element.impartir.horari.hora.hora_inici,
                     impartir__horari__hora__hora_inici__gt = unaHora40abans,
                     impartir__dia_impartir = element.impartir.dia_impartir)
    res = None
    if len(controls_anteriors) >= 1:
        res = controls_anteriors[0]
    return res
    
def cercaUF(ufs, uf_id):
    #Determinar el número d'uf dins l'array (queryset) de ufs.
    #Torna posició dins array o -1
    n = 0
    for uf in ufs:
        #print uf
        if uf.id == uf_id:
            return n
        n+=1
    return -1

def crearDiccionari(ufs):
    #Crea un diccionari a partir del queyset de ufs
    #Guarem la posició que ocupa la UF dins el queryset.
    dic = {}
    n = 0
    for uf in ufs:
        dic[uf.id] = n
        n += 1
    return dic

def crearGuardia(profeASubstituir, franges, dataAImpartir, profeDeGuardia):
    '''
    Crea una hora de guàrdia.
    :type profeASubstituir: Professor
    :type profeDeGuardia: Professor
    franges: una o més instàncies de Franja
    dataAImpartir: la data en que impartim el curs.
    '''
    Impartir.objects.filter( dia_impartir = dataAImpartir,
                             horari__professor = profeASubstituir,
                             horari__hora__in = franges
        ).update( professor_guardia = profeDeGuardia  )
