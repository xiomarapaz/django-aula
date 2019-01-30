# -*- coding: utf-8 -*-
# Faig l'autenticació basada en la idea:
# https://www.ibm.com/support/knowledgecenter/en/SSFKSJ_9.0.0/com.ibm.mq.sec.doc/q128720_.htm
# Es tracta de passar un token a l'usuari un cop s'hagi autenticat, així no exposo el password cada vegada.

from __future__ import unicode_literals
import json, traceback, datetime

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from . import utils
from aula.apps.presencia.models import Impartir, ControlAssistencia
from aula.apps.usuaris.models import User2Professor, Accio
from aula.apps.presencia.business_rules.impartir import impartir_despres_de_passar_llista
from aula.apps.horaris.models import FranjaHoraria, Horari



usuariTokens = {}

def ajuda(request):
    return HttpResponse('API Rest framework, per usar en Android i altres sistemes.')

def login(request, idUsuari):
    #type: (HttpRequest, str) -> HttpResponse
    '''
    Obtenir el body de la petició, generar un token, aquest token el rebrà l'usuari i podrà accedir a tota l'API a través seu, 
    així no exposem el password. 
    Guardarem el token en memòria i els que superin una hora des de que han estat creats'.
    '''
    try:
        usuari = User.objects.get(username=idUsuari)
    except ObjectDoesNotExist as ex:
        return HttpResponseNotFound('Usuari no localitzat')
        
    token = utils.gen_password(length=20)
    usuariTokens[usuari.pk] = token
    
    response = HttpResponse(token)
    response.set_cookie('token', token)
    return response
    

def getImpartirPerData(request, paramData, idUsuari):
    #type: (HttpRequest, str, str) -> HttpResponse
    '''
    Retorna tots els registres del model Impartir donada una data.
    El format d'ingŕes de la data és Y-M-D
    '''
    try:
        data = utils.convertirData(paramData)
        usuari = utils.obtenirUsuari(idUsuari)
        if not usuari:
            return HttpResponseNotFound('Usuari no localitzat')

        if not utils.tokenCorrecte(request, usuariTokens, usuari.pk):
            return HttpResponseServerError("Token no trobat")
        
        idProfe = usuari.pk
        #Sempre obtinc les classes a impartir dels profes que fan classe i els de guàrdia.
        classesAImpartirDelDia = Impartir.objects.filter(
            Q(horari__professor__id = idProfe, dia_impartir=data) |
            Q(professor_guardia_id = idProfe, dia_impartir=data))
        llistaClasseAImpartirHorari = []
        for classeAImpartir in classesAImpartirDelDia:
            horariSerialitzat = serializers.serialize('json', [classeAImpartir.horari.hora])[1:-1]
            classeAImpartirSerialitzada = serializers.serialize('json', [classeAImpartir])[1:-1]
            llistaClasseAImpartirHorari.append(
                {u'impartir': classeAImpartirSerialitzada,
                u'horari': horariSerialitzat,
                u'assignatura': classeAImpartir.horari.assignatura.nom_assignatura})
        dadesAEnviar = json.dumps(llistaClasseAImpartirHorari, ensure_ascii=False).encode('utf-8')
        print ("A enviar:", dadesAEnviar)
        return HttpResponse(dadesAEnviar)
    except:
        traceback.print_exc()
        return HttpResponseServerError('Error API')

def getControlAssistencia(request, idImpartir, idUsuari):
    '''
    Retorna una llista d'objectes JSON
    Cada objecte conté tres valors ca (controlAssistencia), alumne(Alumne) i estat(Codi estat hora anterior).
    '''
    try:
        usuari = utils.obtenirUsuari(idUsuari)
        if not usuari:
            return HttpResponseNotFound('Usuari no localitzat')

        if not utils.tokenCorrecte(request, usuariTokens, usuari.pk):
                return HttpResponseServerError("Token no trobat")
        
        assistencies = []
        cas = ControlAssistencia.objects.filter(
        impartir__id=idImpartir).order_by('alumne__cognoms')
        for ca in cas:
            #print "CA:", ca.impartir.horari.hora.hora_inici
            caIAlumneDict = {
                'ca':serializers.serialize('json', [ca])[1:-1],
                'estatHoraAnterior': utils.faltaHoraAnterior(ca, tipus_retorn = 'C')}
            assistencies.append(caIAlumneDict)

        dadesAEnviar = json.dumps(assistencies)
        return HttpResponse(dadesAEnviar)
    except:
        traceback.print_exc()
        return HttpResponseServerError('Error API')

@csrf_exempt
def putControlAssistencia(request, idImpartir, idUsuari):
    #type: (HttpRequest, str, str) -> HttpResponse
    # Passa llista d'una hora en concret, rebem un array de ControlAssistencia en JSON.
    try:
        usuari = utils.obtenirUsuari(idUsuari)
        if not usuari:
            return HttpResponseNotFound('Usuari no localitzat')

        if not utils.tokenCorrecte(request, usuariTokens, usuari.pk):
            return HttpResponseServerError("Token no trobat")
        
        impartir = Impartir.objects.get(pk=idImpartir)
        pertany_al_professor = usuari.pk in [impartir.horari.professor.pk, \
                                       impartir.professor_guardia.pk if impartir.professor_guardia else -1]
        if not (pertany_al_professor):
            return HttpResponseServerError('No tens permissos per passar llista')    

        #Retorna una llista de controls d'assistència.
        controlsAssistencia = list(serializers.deserialize('json', request.body))
        
        #Modifica només en cas que hi hagi elements a modificar.
        if len(controlsAssistencia) > 0:
            impartir.dia_passa_llista = datetime.datetime.now()
            impartir.professor_passa_llista = User2Professor(usuari)
            impartir.currentUser = usuari
            impartir.save()

            # LOGGING
            Accio.objects.create(
                tipus='PL',
                usuari=usuari,
                l4=False,
                impersonated_from=None,
                text=u"""Passar llista API presenciaRest: {0}.""".format(impartir)
            )

            #Modifica tots els controls d'assistència.
            retorn = ''
            for caDeserialitzat in controlsAssistencia:
                ca = caDeserialitzat.object

                # ca = ControlAssistencia.objects.filter(
                #     alumne=controlAssistencia.alumne,
                #     impartir=controlAssistencia.impartir)[0] #type: ControlAssistencia
                ca.currentUser = usuari
                ca.professor = User2Professor(usuari)
                ca.credentials = (usuari, False) #Usuari i L4.
                caDeserialitzat.save()
                impartir_despres_de_passar_llista(impartir)

                if (retorn != ''):
                    retorn += ', '
                retorn += str(ca.pk)
            msg = '{"ids": "' + str(retorn) + '"}'
            return HttpResponse(msg)
        else:
            return HttpResponseServerError('Cal passar informació en el body.')    
    except Exception as excpt:
        traceback.print_exc()
        import ipdb; ipdb.set_trace()
        return HttpResponseServerError('Error API')

def getFrangesHoraries(request, idUsuari):
    try:
        usuari = utils.obtenirUsuari(idUsuari)
        if not usuari:
            return HttpResponseNotFound('Usuari no localitzat')

        franges = FranjaHoraria.objects.all()
        return HttpResponse(serializers.serialize('json', franges))
    except Exception as excpt:
        traceback.print_exc()
        import ipdb; ipdb.set_trace()
        return HttpResponseServerError('Error API')

def test(request):
    alumne = {"nom":'ó'}
    dades = json.dumps(alumne, ensure_ascii=False).encode('utf-8')
    return HttpResponse(u'ó'.encode('utf-8') + dades)
