# This Python file uses the following encoding: utf-8
from aula.utils import tools
from aula.apps.alumnes.models import Alumne
from django.db.models.aggregates import Count
from django.db.models import Q
from itertools import chain
from aula.apps.presencia.models import ControlAssistencia
from aula.apps.alumnes.models import Grup

def alertaAssitenciaReport( data_inici, data_fi, nivell, tpc , ordenacio ):
    report = []

    
    taula = tools.classebuida()
    
    taula.titol = tools.classebuida()
    taula.titol.contingut = u'Ranking absència alumnes nivell {0}'.format( nivell )
    taula.capceleres = []
    
    capcelera = tools.classebuida()
    capcelera.amplade = 30
    capcelera.contingut = u'Alumne'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 15
    capcelera.contingut = u'hores absent no justificat'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 10
    capcelera.contingut = u'hores docència'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 20
    capcelera.contingut = u'%absència no justificada (absènc.no.justif./docència)'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 5
    capcelera.contingut = u'hores present'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 10
    capcelera.contingut = u'hores absènc. justif.'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 10
    capcelera.contingut = u'% assistència'
    taula.capceleres.append( capcelera )


    taula.fileres = []
    

#     q_nivell = Q( grup__curs__nivell = nivell )
#     q_data_inici = Q(  controlassistencia__impartir__dia_impartir__gte = data_inici  )
#     q_data_fi = Q(  controlassistencia__impartir__dia_impartir__lte = data_fi  )
#     q_filte = q_nivell & q_data_inici & q_data_fi
#     q_alumnes = Alumne.objects.filter( q_filte )
# 
#     q_p = q_alumnes.filter( controlassistencia__estat__codi_estat__in = ('P','R' ) ).order_by().distinct().annotate( x=Count('controlassistencia__estat') ).values_list( 'id', 'x' )
#     q_j = q_alumnes.filter( controlassistencia__estat__codi_estat = 'J' ).order_by().distinct().annotate( x=Count('controlassistencia__estat') ).order_by().distinct().values_list( 'id', 'x' )
#     q_f = q_alumnes.filter( controlassistencia__estat__codi_estat = 'F' ).order_by().distinct().annotate( x=Count('controlassistencia__estat') ).values_list( 'id', 'x' )

#     dict_p, dict_j, dict_f = dict( q_p ), dict( q_j ), dict( q_f )


    q_alumnes = Alumne.objects.filter( grup__curs__nivell = nivell )    
    
    q_data_inici = Q( impartir__dia_impartir__gte = data_inici  )
    q_data_fi = Q( impartir__dia_impartir__lte = data_fi  )
    q_filtre = q_data_inici & q_data_fi
    q_controls = ControlAssistencia.objects.filter(  alumne__in = q_alumnes ).filter( q_filtre )
    
    q_p = q_controls.filter( estat__codi_estat__in = ('P','R' ) ).order_by().values_list( 'id','alumne__id' ).distinct()
    q_j = q_controls.filter( estat__codi_estat = 'J' ).order_by().values_list( 'id','alumne__id' ).distinct()
    q_f = q_controls.filter( estat__codi_estat = 'F' ).order_by().values_list( 'id','alumne__id' ).distinct()
    
    from itertools import groupby
    dict_p = {}
    data = sorted(q_p, key=lambda x: x[1])
    for k, g in groupby( data, lambda x: x[1] ):
        dict_p[k] = len( list(g) )
    
    dict_j = {}
    data = sorted(q_j, key=lambda x: x[1])
    for k, g in groupby( data, lambda x: x[1] ):
        dict_j[k] = len( list(g) )

    dict_f = {}
    data = sorted(q_f, key=lambda x: x[1])
    for k, g in groupby( data, lambda x: x[1] ):
        dict_f[k] = len( list(g) )
    
    #ajuntar dades diferents fonts
    alumnes = []
    for alumne in q_alumnes.select_related( 'grup', 'grup__curs' ).order_by().distinct():
        alumne.p = dict_p.get( alumne.id, 0)
        alumne.j = dict_j.get( alumne.id, 0)
        alumne.f = dict_f.get( alumne.id, 0)
        alumne.ca = alumne.p + alumne.j + alumne.f or 0.0
        alumne.tpc = ( float( alumne.f ) / float( alumne.ca ) ) * 100.0 if alumne.ca > 0 else 0
        alumne.tpc_assist =  ( float( alumne.p )  / float( alumne.ca ) ) * 100.0 if alumne.ca > 0 else 0
        alumnes.append(alumne)
    #----------------------
    #choices = ( ('a', u'Nom alumne',), ('ca', u'Curs i alumne',),('n',u'Per % Assistència',), ('cn',u'Per Curs i % Assistència',),
    order_a = lambda a: ( a.cognoms,  a.nom)
    order_ca = lambda a: ( a.grup.curs.nom_curs, a.grup.nom_grup, a.cognoms, a.nom )
    order_n = lambda a: ( -1 * a.tpc, -1 * a.f )
    order_cn = lambda a: ( a.grup.curs.nom_curs, a.grup.nom_grup  , -1 * a.tpc)
    order = order_ca if ordenacio == 'ca' else order_n if ordenacio == 'n' else order_cn if ordenacio == 'cn' else order_a
    
    
    for alumne in  sorted( [ a for a in alumnes if a.tpc > tpc ] , key=order  ):   
                
        filera = []
        
        #-nom--------------------------------------------
        camp = tools.classebuida()
        camp.enllac = '/tutoria/detallTutoriaAlumne/{0}/all'.format(alumne.pk )
        camp.contingut = unicode(alumne) + ' (' + unicode(alumne.grup) + ')'
        filera.append(camp)

        #-docència--------------------------------------------
        camp = tools.classebuida()
        camp.contingut = unicode(alumne.f) 
        filera.append(camp)

        #-present--------------------------------------------
        camp = tools.classebuida()
        camp.contingut = unicode(alumne.ca) 
        filera.append(camp)

        #-%--------------------------------------------
        camp = tools.classebuida()
        camp.contingut =u'{0:.2f}%'.format(alumne.tpc ) 
        filera.append(camp)
        
        #-absent--------------------------------------------
        camp = tools.classebuida()
        camp.contingut = unicode(alumne.p) 
        filera.append(camp)

        #-justif--------------------------------------------
        camp = tools.classebuida()
        camp.contingut = unicode(alumne.j) 
        filera.append(camp)

        #-assist--------------------------------------------
        camp = tools.classebuida()
        camp.contingut = u'{0:.2f}%'.format(alumne.tpc_assist) 
        filera.append(camp)



        taula.fileres.append( filera )

    report.append(taula)

    return report

def alertaAssitenciaEstadistiquesReport (data_inici, data_fi, percent, percentMinimATenirEnCompte=0):
    #Informe d'assistència del número d'alumnes que han superat el % de faltes. 
    #percent: En tant per 1. Ex: 0.8 no superen el 80% de faltes.
    #percentMinimATenirEnCompte: Si supera aquest % d'assistència no el tenim en compte a l'estadística.
    #Recorrer per tots els grups.
    estadistiques = []
    for grup in Grup.objects.all():
        estadistiques.append( \
            _processarGrupAlertaAssitenciaEstadistiques( \
                grup, data_inici, data_fi, percent, percentMinimATenirEnCompte))
    
    report = []
    taula = tools.classebuida()
    
    taula.capceleres = []
    lenCol = 1/5*100

    taula.titol = tools.classebuida()
    capcelera = tools.classebuida()
    capcelera.amplade = lenCol
    capcelera.contingut = u'Alumnes'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = lenCol
    capcelera.contingut = u'Num. Alumnes'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = lenCol
    capcelera.contingut = u'Assisteixen menys del ' + unicode(percent*100) + u'% de les hores'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = lenCol
    capcelera.contingut = u'Assisteixen menys del ' + \
        unicode(percentMinimATenirEnCompte*100) + u'% de les hores'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = lenCol
    capcelera.contingut = u'Assisteixen entre un {}% i un {}% de les hores'.format(
        unicode(percentMinimATenirEnCompte*100),
        unicode(percent*100))
    taula.capceleres.append( capcelera )

    taula.fileres = []
    
    for estadistica in estadistiques:
        filera = []
        camp = tools.classebuida()
        camp.contingut = u'{}'.format(estadistica['nomGrup']) 
        filera.append(camp)

        camp = tools.classebuida()
        camp.contingut = u'{}'.format(estadistica['nAlumnes']) 
        filera.append(camp)

        camp = tools.classebuida()
        camp.contingut = u'{}'.format(estadistica['noSuperenPercent']) 
        filera.append(camp)

        camp = tools.classebuida()
        camp.contingut = u'{}'.format(estadistica['noSuperenPercentMinim']) 
        filera.append(camp)

        camp = tools.classebuida()
        camp.contingut = u'{}'.format(estadistica['totalSenseCasosMinims']) 
        filera.append(camp)

        taula.fileres.append(filera)

    report.append(taula)
    return report


def _processarGrupAlertaAssitenciaEstadistiques(
    grup, data_inici, data_fi, percent, percentMinimATenirEnCompte=0):
    #Funció que calcula les estadístiques generals d'un grup.
    #Passem un model grup:Grup.
    if not (percent >= 0 and percent <= 1):
        raise Exception(u"percent cal que estigui entre 0 i 1, ara és:{}" \
            .format(percent))

    if not (percentMinimATenirEnCompte >= 0 and percentMinimATenirEnCompte <= 1):
        raise Exception(u"percentMinimATenirEnCompte cal que estigui entre 0 i 1, ara és:{}" \
            .format(percentMinimATenirEnCompte))

    if not (percentMinimATenirEnCompte < percent):
        raise Exception(u"No pot ser que el percentatge mínim superi al màxim")

    casPresencia = ControlAssistencia.objects.filter(impartir__horari__grup__pk=grup.pk) \
        .filter(estat__codi_estat__isnull=False) \
        .filter(estat__codi_estat__in = ['P','R']) \
        .filter(impartir__dia_impartir__lte=data_fi) \
        .filter(impartir__dia_impartir__gte=data_inici) \
        .values('alumne') \
        .annotate(Count('id')) #type: ControlAssistencia
    
    cas = ControlAssistencia.objects.filter(impartir__horari__grup__pk=grup.pk) \
        .filter(estat__codi_estat__isnull=False) \
        .filter(impartir__dia_impartir__lte=data_fi) \
        .filter(impartir__dia_impartir__gte=data_inici) \
        .values('alumne') \
        .annotate(Count('id')) #type: ControlAssistencia

    #Posar els alumnes en un diccionari d'alumnes.
    #format per el codi de l'alumne i com a valor una tupla (horesPresent,horesTotals)
    dictAlumnes = {}
    for c in casPresencia:
        idAlumne = c['alumne']
        if idAlumne in dictAlumnes.keys():
            dictAlumnes[idAlumne] = (c['id__count'],dictAlumnes[idAlumne][1])
        else:
            dictAlumnes[idAlumne] = (c['id__count'],0)
    
    for c in cas:
        idAlumne = c['alumne']
        if idAlumne in dictAlumnes.keys():
            dictAlumnes[idAlumne] = (dictAlumnes[idAlumne][0],c['id__count'])
        else:
            dictAlumnes[idAlumne] = (0,c['id__count'])

    noSuperenPercentMinim = 0
    noSuperenElPercentatge = 0
    for key in dictAlumnes.keys():
        if float(dictAlumnes[key][1]) < float(dictAlumnes[key][0]):
            raise Exception(u"Un alumne té més hores totals que assistències" + unicode(dictAlumnes[key]))

        percentAssistencia = float(dictAlumnes[key][0]) / float(dictAlumnes[key][1])
        
        if percentAssistencia < percent:
            noSuperenElPercentatge += 1
            print u"No supera:", Alumne.objects.get(pk=key), \
            "Hores present:", float(dictAlumnes[key][0]), \
            "NTotal:" , float(dictAlumnes[key][1]), u"\n"
        if percentAssistencia < percentMinimATenirEnCompte:
            noSuperenPercentMinim += 1
            #print u"Possible baixa:", Alumne.objects.get(pk=key), key, 
            #"Hores present:", float(dictAlumnes[key][0]),
            #"NTotal:" , float(dictAlumnes[key][1]),
    
    return {'nomGrup':grup.nom_grup, 'nAlumnes':len(dictAlumnes), 
        'noSuperenPercent':noSuperenElPercentatge, 
        'noSuperenPercentMinim': noSuperenPercentMinim,
        'totalSenseCasosMinims': noSuperenElPercentatge - noSuperenPercentMinim}
