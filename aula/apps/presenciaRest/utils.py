# -*- coding: utf-8 -*-
import os
from datetime import date
import datetime
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest
from typing import List
from django.core import serializers

from aula.apps.presencia.models import ControlAssistencia



def add_secs_to_time(timeval, secs_to_add):
    dummy_date = datetime.date(1, 1, 1)
    full_datetime = datetime.datetime.combine(dummy_date, timeval)
    added_datetime = full_datetime + datetime.timedelta(seconds=secs_to_add)
    return added_datetime.time()

def PresenciaQuerySetGetCode(qs):
    #type: (QuerySet)-> None ; QuerySet de tipus assistència
    '''
    Passar un conjunt d'assistencies, determina si en alguna hi ha un present o retard.
    Si és així, vol dir que tenim un assistència durant aquest període.
    '''
    assistenciaCode = 'N'
    if qs is not None and qs.filter( estat__isnull = False  ).exists():
        if qs.filter( estat__codi_estat__in = ['P','R'] ):
            assistenciaCode = 'P'
        elif qs.filter( estat__codi_estat__in = ['J'] ):
            assistenciaCode = 'J'
        else:
            assistenciaCode = 'F'
    return assistenciaCode

def PresenciaQuerySet( qs ):
    #type: (QuerySet); QuerySet de tipus assistència
    if qs is not None and qs.filter( estat__isnull = False  ).exists():
        if qs.filter( estat__codi_estat__in = ['P','R'] ):
            esFaltaAnterior = 'Present'
        else:
            esFaltaAnterior = 'Absent'
    else:
        esFaltaAnterior = 'NA'
    return esFaltaAnterior

def gen_password(length=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"):
    random_bytes = os.urandom(length)
    len_charset = len(charset)
    indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
    return "".join([charset[index] for index in indices])

def convertirData(stringData):
    "Passem una data en format Y-M-D, comprova si és correcte i retorna una llista amb 3 enters."
    camps = stringData.split('-')
    return date(int(camps[0]),int(camps[1]), int(camps[2]))

def faltaHoraAnterior(ca, tipus_retorn = 'W'):
    #type: (ControlAssitencia, str)
    '''
    Comprova el codi de l'hora anterior, 2 Modes de retorn ('C', 'W'):
    Torna: Present, Absent o bé NA. (Mode paraula original='W')
    Torna: P o R -> P, F->F, J->J o N (Mode codi='C')

    @type ca: ControlAssistencia | Control assistencia actual.
    @type retorna: Indica si cal tornar un codi o bé una paraula ('C', 'W'), per defecte W=paraula.
    '''
    unaHora40abans = add_secs_to_time(ca.impartir.horari.hora.hora_inici, -100*60)
    controls_anteriors = ControlAssistencia.objects.filter(
                                                         alumne = ca.alumne,
                                                         impartir__horari__hora__hora_inici__lt = ca.impartir.horari.hora.hora_inici,
                                                         impartir__horari__hora__hora_inici__gt = unaHora40abans,
                                                         impartir__dia_impartir = ca.impartir.dia_impartir  )
    if tipus_retorn == 'W':
        esFaltaHoraAnterior = PresenciaQuerySet( controls_anteriors )
    else:
        esFaltaHoraAnterior = PresenciaQuerySetGetCode( controls_anteriors )
    return esFaltaHoraAnterior

def obtenirUsuari(nomUsuari):
    try:
        return User.objects.get(username=nomUsuari) # type: Usuari
    except ObjectDoesNotExist as ex:
        return None

def tokenCorrecte(request, usuariTokens, pkUsuari):
    #type: (HttpRequest, List, str) -> None
    print (usuariTokens,pkUsuari)
    if not pkUsuari in usuariTokens:
        return False
    print (usuariTokens,pkUsuari, request.COOKIES)
    if 'token' in request.COOKIES:
        if request.COOKIES.get('token') == usuariTokens[pkUsuari]:
            return True
    return False

def deserialitzarUnElement(objecteSerialitzat):
    return serializers.deserialize('json', u'[' + objecteSerialitzat + u']').next()

def serialitzarUnElement(objecte):
    #type: (Object)->string
    return serializers.serialize('json', [objecte])[1:-1], 