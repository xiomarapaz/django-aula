# This Python file uses the following encoding: utf-8

import os
import sys
from django.conf import settings

from aula.apps.avaluacioQualitativa.models import AvaluacioQualitativa
from aula.apps.sortides.models import NotificaSortida
from aula.apps.sortides.utils_sortides import notifica_sortides

def notifica():
    from aula.apps.alumnes.models import Alumne
    from django.db import transaction
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.models import Q
    from datetime import timedelta
    from django.utils.datetime_safe import datetime
    from aula.apps.presencia.models import EstatControlAssistencia
    from aula.apps.presencia.models import ControlAssistencia
    from django.core.mail import send_mail
    from aula.apps.usuaris.models import Accio

    num_correus_no_enviats=0
        
    urlDjangoAula = settings.URL_DJANGO_AULA
    textTutorial = settings.CUSTOM_PORTAL_FAMILIES_TUTORIAL
    
    #with transaction.autocommit():  #deprecated on 1.8. Now is the default behaviuor.

    # TODO x App
    #
    # treure fa_2_setmanes
    # llista alumnes q_no_informat_adreca deprecated: tenen adreça informada o tenen token
        
    #actualitzo notificacions sortides:
    notifica_sortides()

    #Notificacions        
    ara = datetime.now()
    
    # fa_2_setmanes = ara - timedelta(  days = 14 )
    presencies_notificar = EstatControlAssistencia.objects.filter( codi_estat__in = ['F','R','J']  )
    q_no_es_baixa = Q(data_baixa__gte = ara ) | Q(data_baixa__isnull = True )
    # q_no_informat_adreca = Q( correu_relacio_familia_pare = '' ) & Q( correu_relacio_familia_mare = '' )
    
    llista_alumnes = ( Alumne
                      .objects
                      .filter(q_no_es_baixa)
                      #.exclude( q_no_informat_adreca )
                      .values_list('pk', flat=True)
                     )

    avui = datetime.now().date()
    qualitatives_en_curs = [ q for q in AvaluacioQualitativa.objects.all()
                               if ( bool(q.data_obrir_portal_families) and
                                    bool( q.data_tancar_tancar_portal_families ) and
                                    q.data_obrir_portal_families <= avui <= q.data_tancar_tancar_portal_families
                                   )
                           ]


    for alumne_id in llista_alumnes:
        try:
            alumne = Alumne.objects.get( pk = alumne_id )

            adreca_mail_informada = bool( alumne.correu_relacio_familia_pare or alumne.correu_relacio_familia_mare ) 
            app_instalada = alumne.qr_portal_set.exists()

            fa_n_dies = ara - timedelta(  days = alumne.periodicitat_faltes )
            noves_sortides = NotificaSortida.objects.filter( alumne = alumne, relacio_familia_notificada__isnull = True  )
            noves_incidencies = alumne.incidencia_set.filter( relacio_familia_notificada__isnull = True  )
            noves_expulsions = alumne.expulsio_set.exclude( estat = 'ES').filter(    relacio_familia_notificada__isnull = True  )
            noves_sancions = alumne.sancio_set.filter( impres=True, relacio_familia_notificada__isnull = True  )
            noves_faltes_assistencia = ControlAssistencia.objects.filter( alumne = alumne, 
                                                                          # impartir__dia_impartir__gte = fa_2_setmanes,
                                                                          relacio_familia_notificada__isnull = True,
                                                                          estat__pk__in = presencies_notificar )
            noves_respostes_qualitativa = ( alumne
                                            .respostaavaluacioqualitativa_set
                                            .filter( qualitativa__in = qualitatives_en_curs )
                                            .filter( relacio_familia_notificada__isnull = True )
                                            )

            #comprovo si hi ha novetats de presencia i incidències
            fa_dies_que_no_notifiquem = alumne.relacio_familia_darrera_notificacio is None or \
                                        alumne.relacio_familia_darrera_notificacio < fa_n_dies
            hiHaNovetatsPresencia =  alumne.periodicitat_faltes > 0 and \
                                     fa_dies_que_no_notifiquem and \
                                     noves_faltes_assistencia.exists()
            hiHaNovetatsQualitativa = noves_respostes_qualitativa.exists()
            hiHaNovetatsSortides = noves_sortides.exists()
            hiHaNovetatsIncidencies = ( alumne.periodicitat_incidencies and
                                       ( noves_incidencies.exists() or noves_expulsions.exists() or noves_sancions.exists() )
                                      )
            hiHaNovetats =  (
                             hiHaNovetatsQualitativa or
                             hiHaNovetatsPresencia or
                             hiHaNovetatsSortides or
                             hiHaNovetatsIncidencies
                             )      


            #print u'Avaluant a {0}'.format( alumne )
            enviatOK = False
            if hiHaNovetats and adreca_mail_informada:
                #enviar correu i marcar novetats com a notificades:
                assumpte = u"{0} - Notificacions al Djau de {1}".format(alumne.nom, settings.NOM_CENTRE )
                missatge = [u"Benvolgut/da,",
                            u"",
                            u"Us comuniquem que teniu noves notificacions del vostre fill/a {0} a l'aplicació Djau del centre {1}".format(alumne.nom, urlDjangoAula),
                            u"",
                            u"Recordeu que el vostre nom d'usuari és: {0}".format( alumne.get_user_associat().username ),
                            u"",
                            u"Per qualsevol dubte que tingueu al respecte poseu-vos en contacte amb el tutor/a del vostre fill/a.",
                            u"",
                            u"Cordialment,",
                            u"",
                            settings.NOM_CENTRE,
                            u"",
                            u"{0}".format( textTutorial ),
                            ]
                
                try:                        
                    fromuser = settings.DEFAULT_FROM_EMAIL
                    if settings.DEBUG:
                        print u'Enviant missatge a {0}'.format( alumne )
                    send_mail(assumpte, 
                              u'\n'.join( missatge ), 
                              fromuser,
                              alumne.get_correus_relacio_familia(), 
                              fail_silently=False)
                    enviatOK = True
                except:
                    enviatOK = False
                    #Enviar msg a admins, ull! podem inundar de missatges si fallen tots els alumnes.
                    num_correus_no_enviats += 1


            #actualitzo QR's
            if hiHaNovetats:
                n_tokens = alumne.qr_portal_set.update( novetats_detectades_moment = ara  )

            enviatOK = enviatOK or bool(n_tokens)  # s'ha enviat per algun dels mitjants

            if enviatOK:                    
                noves_sortides.update( relacio_familia_notificada = ara )
                noves_incidencies.update( relacio_familia_notificada = ara )
                noves_expulsions.update( relacio_familia_notificada = ara )
                noves_sancions.update( relacio_familia_notificada = ara )
                noves_faltes_assistencia.update( relacio_familia_notificada = ara )
                noves_respostes_qualitativa.update( relacio_familia_notificada = ara )
                #if hiHaNovetatsPresencia:
                alumne.relacio_familia_darrera_notificacio = ara
                alumne.save()

                #LOGGING
                Accio.objects.create( 
                        tipus = 'NF',
                        usuari = alumne.get_user_associat(),
                        l4 = False,
                        impersonated_from = None,
                        text = u"""Notifica Relació Famílies a {0}.""".format( alumne )
                    )   
                                
        except ObjectDoesNotExist:
            pass
    
    # si hi ha correus que han fallat informar a l'admin

    if num_correus_no_enviats > 0:
        raise Exception(u"No s'han pogut enviar {} missatges a famílies.".format(num_correus_no_enviats))

