#encoding: utf-8
from extHoraris import models

def comprovaProfesSolapats(grupId):
    # Enter amb el grupId.
    # Retorna un array on cada element és un subarray amb les entrades dels profes solapats.
    # Optimitzat si faig una sola consulta i treballo amb un array en memòria.
    entradesAmbProfeRepetit={}
    entradesHorariesGrup = models.EntradaHorari.objects.filter(grup__pk = grupId)
    totesEntradesHoraries = models.EntradaHorari.objects.values('profe_id', 'dia_id', 'franja_id') #type: QuerySet
    for entrada in entradesHorariesGrup:
        if totesEntradesHoraries.filter(profe_id=entrada.profe_id, dia_id=entrada.dia_id, franja_id=entrada.franja_id).count() > 1:
            epSolapats = models.EntradaHorari.objects.filter(profe_id=entrada.profe_id, dia_id=entrada.dia_id, franja_id=entrada.franja_id)
            entradesAmbProfeRepetit[entrada.pk] = epSolapats
    return entradesAmbProfeRepetit

def comprovaAulesSolapades(grupId):
    # Enter amb el grupId.
    # Retorna un array on cada element és un subarray amb les entrades de les aules solapades.
    # Optimitzat si faig una sola consulta i treballo amb un array en memòria.
    entradesAulaRepetides={}
    entradesHorariesGrup = models.EntradaHorari.objects.filter(grup__pk = grupId)
    totesEntradesHoraries = models.EntradaHorari.objects.values('aula_id', 'dia_id', 'franja_id') #type: QuerySet
    for entrada in entradesHorariesGrup:
        if totesEntradesHoraries.filter(aula_id=entrada.aula_id, dia_id=entrada.dia_id, franja_id=entrada.franja_id).count() > 1:
            epSolapats = models.EntradaHorari.objects.filter(aula_id=entrada.aula_id, dia_id=entrada.dia_id, franja_id=entrada.franja_id)
            entradesAulaRepetides[entrada.pk] = epSolapats
    return entradesAulaRepetides

'''
def comprovaProfesSolapats(grupId):
    # Enter amb el grupId.
    # Retorna un array on cada element és un subarray amb les entrades dels profes solapats.
    # Es pot optimitzar si faig una sola consulta i treballo amb un array en memòria.
    entradesAmbProfeRepetit={}
    entradesHorariesGrup = models.EntradaHorari.objects.filter(grup__pk = grupId)
    totesEntradesHoraries = models.EntradaHorari.objects.all() #type: QuerySet

    for entrada in entradesHorariesGrup:
        #if hiHan2Repetits(totesEntradesHoraries, profe, entrada.dia, entrada.franja):
        if totesEntradesHoraries.filter(profe_id=entrada.profe_id, dia_id=entrada.dia_id, franja_id=entrada.franja_id).count() > 1:
            epSolapats = totesEntradesHoraries.filter(profe_id=entrada.profe_id, dia_id=entrada.dia_id, franja_id=entrada.franja_id)
            entradesAmbProfeRepetit[entrada.pk] = epSolapats
    return entradesAmbProfeRepetit

def comprovaAulesSolapades(grupId):
    profesRepetits=[]
    aulesRepetides=[]
    entradesHoraries = models.EntradaHorari.objects.filter(grup__pk = grupId)
    for entrada in entradesHoraries:
        profe = entrada.profe
        if len(models.EntradaHorari.objects.filter(profe=profe, dia=entrada.dia, franja=entrada.franja)) > 1:
            profesRepetits.append(profe)
        aula = entrada.aula
        if len(models.EntradaHorari.objects.filter(aula=aula, dia=entrada.dia, franja=entrada.franja)) > 1:
            aulesRepetides.append(aula)
    return profesRepetits, aulesRepetides
'''