# This Python file uses the following encoding: utf-8
from aula.utils import tools
from aula.apps.alumnes.models import Alumne
from aula.apps.presencia.models import ControlAssistencia
from django.db.models import Q

def faltesAssistenciaEntreDatesProfessorRpt(
                    grup ,
                    assignatura ,
                    dataDesDe ,
                    horaDesDe ,
                    dataFinsA ,
                    horaFinsA ):

    q_grup = Q(impartir__horari__grup = grup)

    q_assignatura = Q(impartir__horari__assignatura = assignatura)

    q_primer_dia = Q(impartir__dia_impartir = dataDesDe ) & Q(impartir__horari__hora__hora_inici__gte = horaDesDe.hora_inici)
    q_mig = Q(impartir__dia_impartir__gt = dataDesDe ) & Q(impartir__dia_impartir__lt = dataFinsA)
    q_darrer_dia = Q(impartir__dia_impartir = dataFinsA ) & Q(impartir__horari__hora__hora_fi__lte = horaFinsA.hora_fi)
    q_hores = q_primer_dia | q_mig | q_darrer_dia

    controls = ControlAssistencia.objects.filter( q_grup & q_assignatura & q_hores )

    alumnes = Alumne.objects.filter( controlassistencia__pk__in = controls.values_list('pk', flat=True)
                                      ).distinct()
    #print "-----------------------------" + str(controls.query)

    report = []

    nTaula = 0

    #RESUM-------------------------------------------------------------------------------------------------
    taula = tools.classebuida()
    taula.codi = nTaula; nTaula+=1
    taula.tabTitle = 'Resum'

    taula.titol = tools.classebuida()
    taula.titol.contingut = u'Resum assistència de {0} de {1} entre {2} {3}h i {4} {5}h'.format(
                                    grup,
                                    assignatura,
                                    dataDesDe.strftime( '%d/%m/%Y' )  ,
                                    horaDesDe.hora_inici.strftime( '%H:%M' ),
                                    dataFinsA.strftime( '%d/%m/%Y' )  ,
                                    horaFinsA.hora_fi.strftime( '%H:%M' )
                                     )
    taula.capceleres = []

    capcelera = tools.classebuida()
    capcelera.amplade = 120
    capcelera.contingut = u'Alumne'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 70
    capcelera.contingut = u'hores absent no justificat'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 70
    capcelera.contingut = u'hores docència'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 100
    capcelera.contingut = u'%absència no justificada (absènc.no.justif./docència)'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 70
    capcelera.contingut = u'hores present'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 70
    capcelera.contingut = u'hores absènc. justif.'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 70
    capcelera.contingut = u'hores retard'
    taula.capceleres.append( capcelera )

    taula.fileres = []

    for alumne in  alumnes:

        filera = []

        #-nom--------------------------------------------
        camp = tools.classebuida()
        camp.enllac = ''
        camp.contingut = unicode(alumne) + ' (' + unicode(alumne.grup) + ')'
        filera.append(camp)

        #-faltes--------------------------------------------
        f = controls.filter( alumne = alumne, estat__codi_estat = 'F' ).distinct().count()
        camp = tools.classebuida()
        camp.contingut = unicode(f)
        filera.append(camp)

        #-controls--------------------------------------------
        ca = controls.filter( alumne = alumne, estat__codi_estat__isnull = False ).distinct().count()
        camp = tools.classebuida()
        camp.contingut = unicode(ca)
        filera.append(camp)

        #-%--------------------------------------------
        tpc = (1.0*f) / (1.0*ca) if ca <> 0 else 'N/A'
        camp = tools.classebuida()
        camp.contingut =u'{0:.2f}%'.format(tpc * 100) if isinstance( tpc, float ) else 'N/A'
        filera.append(camp)

        #-present--------------------------------------------
        p = controls.filter( alumne = alumne, estat__codi_estat = 'P' ).distinct().count()
        camp = tools.classebuida()
        camp.contingut = unicode(p)
        filera.append(camp)

        #-justif--------------------------------------------
        j = controls.filter( alumne = alumne, estat__codi_estat = 'J' ).distinct().count()
        camp = tools.classebuida()
        camp.contingut = unicode(j)
        filera.append(camp)

        #-retard--------------------------------------------
        j = controls.filter( alumne = alumne, estat__codi_estat = 'R' ).distinct().count()
        camp = tools.classebuida()
        camp.contingut = unicode(j)
        filera.append(camp)



        taula.fileres.append( filera )

    report.append(taula)


    #DETALL-------------------------------------------------------------------------------------------------
    taula = tools.classebuida()
    taula.codi = nTaula; nTaula+=1
    taula.tabTitle = 'Detall'

    taula.titol = tools.classebuida()
    taula.titol.contingut = u'Detall assistència de {0} de {1} entre {2} {3}h i {4} {5}h'.format(
                                    grup,
                                    assignatura,
                                    dataDesDe.strftime( '%d/%m/%Y' )  ,
                                    horaDesDe.hora_inici.strftime( '%H:%M' ),
                                    dataFinsA.strftime( '%d/%m/%Y' )  ,
                                    horaFinsA.hora_fi.strftime( '%H:%M' )
                                     )
    taula.capceleres = []

    capcelera = tools.classebuida()
    capcelera.amplade = 120
    capcelera.contingut = u'Alumne'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 400
    capcelera.contingut = u'hores absent no justificat'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 400
    capcelera.contingut = u'hores absènc. justif.'
    taula.capceleres.append( capcelera )


    taula.fileres = []


    for alumne in  alumnes:

        filera = []

        #-nom--------------------------------------------
        camp = tools.classebuida()
        camp.enllac = ''
        camp.contingut = unicode(alumne) + ' (' + unicode(alumne.grup) + ')'
        filera.append(camp)

        #-faltes--------------------------------------------
        f = controls.filter( alumne = alumne, estat__codi_estat = 'F' ).distinct().select_related('impartir','impartir__horari__hora', 'impartir__horari__assignatura')

        camp = tools.classebuida()
        camp.contingut = unicode(
                           u' | '.join(
                                 [ u'{0} {1} {2}'.format(x.impartir.dia_impartir.strftime( '%d/%m/%Y' )  , x.impartir.horari.hora, x.impartir.horari.assignatura)
                                   for x in f ]
                                     )
                                 )
        filera.append(camp)

        #-justif--------------------------------------------
        j = controls.filter( alumne = alumne, estat__codi_estat = 'J' ).distinct()
        camp = tools.classebuida()
        contingut = [ u'{0} {1} {2}'.format(x.impartir.dia_impartir.strftime( '%d/%m/%Y' )  , x.impartir.horari.hora, x.impartir.horari.assignatura)
                                   for x in j ]
        camp.multipleContingut =  [ ( c, None,) for c in contingut ]


        filera.append(camp)



        taula.fileres.append( filera )

    report.append(taula)

    return report