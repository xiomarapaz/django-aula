# This Python file uses the following encoding: utf-8
from aula.utils import tools
from aula.apps.alumnes.models import Alumne
from aula.apps.presencia.models import ControlAssistencia, Impartir, EstatControlAssistencia
from models import *
from django.db.models import Q, Sum, Count

def faltesAssistenciaEntreDatesUFsRpt( 
    grup, assignatura, professor=None):
    ''' Informe de faltes per UF, si el paràmetre professor és None, entem en la vista de tutor i no filtrem per profe només per grup. '''
    ufs = UF.objects.filter(assignatura = assignatura).distinct()
    report = []
    nTaula = 0

    for uf in ufs: 
        dataFi = uf.dfi.replace(hour=23, minute=59, second=59)

        q_grup = Q(impartir__horari__grup = grup)
        q_assignatures = Q(impartir__horari__assignatura = assignatura)
        #q_primer_dia = Q(impartir__dia_impartir = dataDesDe ) & Q(impartir__horari__hora__hora_inici__gte = horaDesDe.hora_inici)
        q_hores = Q(impartir__dia_impartir__gte = uf.dinici ) & Q(impartir__dia_impartir__lte = dataFi)
        #q_darrer_dia = Q(impartir__dia_impartir = dataFinsA ) & Q(impartir__horari__hora__hora_fi__lte = horaFinsA.hora_fi)
        #q_hores = q_primer_dia | q_mig | q_darrer_dia

        if professor==None:
          controls = ControlAssistencia.objects.filter( q_grup & q_assignatures & q_hores )
        else:
          q_professor = Q(impartir__horari__professor = professor)
          controls = ControlAssistencia.objects.filter( q_grup & q_assignatures & q_hores & q_professor )          

        alumnes = Alumne.objects.filter( controlassistencia__pk__in = controls.values_list('pk', flat=True)
                                      ).distinct()
        
        #RESUM-------------------------------------------------------------------------------------------------
        taula = tools.classebuida()
        taula.codi = nTaula; nTaula+=1
        taula.tabTitle = uf.nom
            
        taula.titol = tools.classebuida()
        taula.titol.contingut = u'Resum assistència de {0} de {1} entre {2} {3}h i {4} {5}h'.format( 
                                        grup, 
                                        unicode(assignatura),
                                        uf.dinici.strftime( '%d/%m/%Y' ),
                                        uf.dinici.strftime( '%H:%M' ),
                                        dataFi.strftime( '%d/%m/%Y' ),
                                        dataFi.strftime( '%H:%M' )
                                    )
        taula.capceleres = []
        
        capcelera = tools.classebuida()
        capcelera.amplade = 120
        capcelera.contingut = u'Alumne'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'F. Justificades'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'F. Injustificades'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'H. Assistencia'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'H. Programades'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'%F. Justificades (sobre programades)'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'%F. Injustificades (sobre programades)'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'%F. Total (sobre programades)'
        taula.capceleres.append( capcelera )

        taula.fileres = []
        
        for alumne in  alumnes:

            filera = []
            #-Controls---------------------------------------
            ca = controls.filter( alumne = alumne, estat__codi_estat__isnull = False ).distinct().count()
            
            #-nom--------------------------------------------
            camp = tools.classebuida()
            camp.enllac = ''
            camp.contingut = unicode(alumne) + ' (' + unicode(alumne.grup) + ')'
            filera.append(camp)

            #-f. justificades --------------------------------------------
            fj = controls.filter( alumne = alumne, estat__codi_estat = 'J' ).distinct().count()
            camp = tools.classebuida()
            camp.contingut = unicode(fj) 
            filera.append(camp)

            #-f. injustificades --------------------------------------------
            fi = controls.filter( alumne = alumne, estat__codi_estat = 'F' ).distinct().count()
            camp = tools.classebuida()
            camp.contingut = unicode(fi) 
            filera.append(camp)

            #-h. presents--------------------------------------------
            filtre = Q(alumne = alumne) & (Q(estat__codi_estat='R') | Q(estat__codi_estat='P'))
            hp = controls.filter(filtre).distinct().count()
            camp = tools.classebuida()
            camp.contingut = unicode(hp) 
            filera.append(camp)

            #-hores planificades UF -----------------------------------------
            subq_grup = Q(horari__grup = grup)
            subq_assignatura = Q(horari__assignatura = assignatura)
            subq_hores = Q(dia_impartir__gte = uf.dinici ) & Q(dia_impartir__lte = uf.dfi)

            if professor==None:
              horesPlanificades = Impartir.objects.filter(subq_grup & subq_assignatura & subq_hores)
            else:
              subq_professor = Q(horari__professor = professor)
              horesPlanificades = Impartir.objects.filter(subq_grup & subq_assignatura & subq_professor & subq_hores)

            camp = tools.classebuida()
            camp.contingut = unicode(uf.horesTeoriques)
            filera.append(camp)

            #-% justificades sobre UF -----------------------------------------
            tpcUFJust = (1.0*fj) / (1.0*uf.horesTeoriques) if uf.horesTeoriques <> 0 else 'N/A'
            camp = tools.classebuida()
            camp.contingut = u'{0:.2f}%'.format(tpcUFJust*100) if isinstance(tpcUFJust, float) else 'N/A'
            filera.append(camp)

            #-% injustificades sobre UF -----------------------------------------
            tpcUFInjust = (1.0*fi) / (1.0*uf.horesTeoriques) if uf.horesTeoriques <> 0 else 'N/A'
            camp = tools.classebuida()
            camp.contingut = u'{0:.2f}%'.format(tpcUFInjust*100) if isinstance(tpcUFInjust, float) else 'N/A'
            filera.append(camp)

            #-% faltes totals sobre UF -----------------------------------------
            tcpUF = (1.0*(fi+fj)) / (1.0*uf.horesTeoriques) if uf.horesTeoriques <> 0 else 'N/A'
            camp = tools.classebuida()
            camp.contingut = u'{0:.2f}%'.format(tcpUF*100) if isinstance(tcpUF, float) else 'N/A'
            filera.append(camp)            

            taula.fileres.append( filera )

        report.append(taula)

    return report
    
def faltesAssistenciaEntreDatesUFsDiscontinuadesRpt(
    grup, assignatura):
    '''
        Llistat de les UFs que no es fan entre dues dates.
        Son les que fan a automoció perque no tenen lloc als tallers.
        Cada alumne pot fer una UF diferent en un moment diferent.

        Per tots els membres del grup, entre data i data, 
        comprovar quantes hores pertanyen a la UF1 o a la UF2
    '''
    
    estatFalta = EstatControlAssistencia.objects.filter(codi_estat='F')[0]
    estatPresent = EstatControlAssistencia.objects.filter(codi_estat='P')[0]
    estatRetard = EstatControlAssistencia.objects.filter(codi_estat='R')[0]
    estatJustificada = EstatControlAssistencia.objects.filter(codi_estat='J')[0]

    
    #Obtenir la data més gran d'inici i fi de les UF's
    ufs = UF.objects.filter(Q(assignatura_id = assignatura.id))
    if len(ufs) == 0:
        raise Exception("No es pot treballar sense UF\'s")

    #Diccionari amb informació de cada UF, per mostrar més fàcilment.
    infoFaltes = {}

    dataInici = ufs[0].dinici
    dataFi = ufs[0].dfi
    for uf in ufs:
        if uf.dinici < dataInici:
            dataInici = uf.dinici
        if uf.dfi > dataFi:
            dataFi = uf.dfi
        #Assignar estructura per guardar informació de les UFS
        infoFaltes[uf.id] = []

    q_grup = Q(impartir__horari__grup = grup.id) #DAM1
    q_assignatures = Q(impartir__horari__assignatura = assignatura.id) #M1
    q_hores = Q(impartir__dia_impartir__gte = dataInici) &  \
            Q(impartir__dia_impartir__lte = dataFi)
    controls = ControlAssistencia.objects.filter( q_grup & q_assignatures & q_hores )
    alumnes = Alumne.objects.filter( controlassistencia__pk__in = 
        controls.values_list('pk', flat=True)).distinct()

    for alumne in alumnes:
        q_alumne = Q(alumne_id = alumne.pk)
        for uf in ufs:
            q_uf = Q(uf_id = uf)    
            controlsAlumne = ControlAssistencia.objects.filter( \
                q_grup & q_assignatures & q_hores & q_alumne & q_uf )
            nPresent = controlsAlumne.filter(estat_id=estatPresent.id).aggregate(Count("estat"))['estat__count']
            if not nPresent:
                nPresent = 0
            nFaltes = controlsAlumne.filter(estat_id=estatFalta.id).aggregate(Count("estat"))['estat__count']
            if not nFaltes:
                nFaltes = 0
            nJustificades = controlsAlumne.filter(estat_id=estatJustificada.id).aggregate(Count("estat"))['estat__count']
            if not nJustificades:
                nJustificades = 0
            #Seleccionar els controls que son faltes, justificades i presència.            
            print nPresent, nFaltes, nJustificades
            if len(controlsAlumne) > 0:
                infoFaltes[uf.id].append([controlsAlumne[0].alumne, nJustificades, 
                nFaltes, nPresent, uf.horesTeoriques, 
                str.format('{0:.2f}', nJustificades/float(uf.horesTeoriques)),
                str.format('{0:.2f}', nFaltes/float(uf.horesTeoriques)),
                str.format('{0:.2f}', (nFaltes + nJustificades)/float(uf.horesTeoriques))])

    #----------------------------------------------
    #Fem el report amb informació de infoFaltes.
    #----------------------------------------------

    report = []
    nTaula = 0

    for uf in ufs:
        taula = tools.classebuida()
        taula.codi = nTaula; nTaula += 1
        taula.tabTitle = uf.nom
            
        taula.titol = tools.classebuida()
        taula.titol.contingut = u'Resum assistència **UF Discontinuada**, de {0} de {1} entre {2} {3}h i {4} {5}h'.format( 
                                        grup.nom_grup, 
                                        assignatura.nom_assignatura ,
                                        dataInici.strftime( '%d/%m/%Y' ),
                                        dataFi.strftime( '%H:%M' ),
                                        dataFi.strftime( '%d/%m/%Y' ),
                                        dataFi.strftime( '%H:%M' )
                                    )
        taula.capceleres = []
        
        capcelera = tools.classebuida()
        capcelera.amplade = 120
        capcelera.contingut = u'Alumne'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'F. Justificades'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'F. Injustificades'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'H. Assistencia'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'H. Programades'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'%F. Justificades (sobre programades)'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'%F. Injustificades (sobre programades)'
        taula.capceleres.append( capcelera )

        capcelera = tools.classebuida()
        capcelera.amplade = 70
        capcelera.contingut = u'%F. Total (sobre programades)'
        taula.capceleres.append( capcelera )

        taula.fileres = []
            
        for fila in infoFaltes[uf.id]:
            filera = []
            for columna in fila:
                camp = tools.classebuida()
                camp.enllac = ''
                camp.contingut = columna
                filera.append(camp)

            taula.fileres.append(filera)
        report.append(taula)
    return report