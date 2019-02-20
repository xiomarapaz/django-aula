#encoding: utf-8

# This Python file uses the following encoding: utf-8
from django.contrib.auth.decorators import login_required
from aula.utils.decorators import group_required

#workflow
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render

#templates
from django.template import RequestContext

from aula.apps.assignatures.models import *
from aula.apps.usuaris.models import User2Professor, Accio
from aula.utils.tools import getImpersonateUser, getSoftColor
from aula.apps.horaris.models import *

#Imports del mòdul actual.
from forms import *
from reports import *
from aula import settings

#--- Gestió UFS ----------------------------------------------

@login_required
@group_required(['professors'])
def seleccionarAssignatura(request):
    #Selecciona assignatura per veure les UFS
    credentials = getImpersonateUser(request)
    (user, _ ) = credentials

    professor = User2Professor( user )

    if professor is None:
        HttpResponseRedirect( '/' )

    llistaAssignatures = Assignatura.objects.filter(horari__professor = professor.id).distinct()
    return render(request, "veureAssignatures.html",
              {'llistaAssignatures': llistaAssignatures})

@login_required
@group_required(['professors'])
def veureUnitatsFormatives(request, idAssignatura):
    llistaUFS = UF.objects.filter(assignatura_id=idAssignatura)
    return render(request,
              "veureUFS.html",
              {'llistaUFS': llistaUFS, "idAssignatura": idAssignatura})

@login_required
@group_required(['professors'])
def eliminarUnitatFormativa(request, idAssignatura, id):
    ufAEsborrar = UF.objects.get(pk = id)
    ufAEsborrar.delete()
    return HttpResponseRedirect('/assignatures/veureUnitatsFormatives/' + idAssignatura)

@login_required
@group_required(['professors'])
def modificarUnitatFormativa(request, idAssignatura, id):
    uf = UF.objects.get(assignatura = idAssignatura, id = id)

    if request.method == 'POST':
        formulari = NovaUFForm(request.POST)
        if formulari.is_valid():
            #Gravem a la BD.
            nom = formulari.cleaned_data['nom']
            data_inici = formulari.cleaned_data['data_inici']
            data_fi = formulari.cleaned_data['data_fi']
            horesTeoriques = formulari.cleaned_data['horesTeoriques']
            assignatura = Assignatura.objects.get(pk = idAssignatura)

            uf.nom = nom
            uf.dinici = data_inici
            uf.dfi = data_fi
            uf.assignatura = assignatura
            uf.horesTeoriques = horesTeoriques
            uf.save()

            return HttpResponseRedirect(
                '/assignatures/veureUnitatsFormatives/' + idAssignatura)
        else:
            return render(request,
                "form.html", {'form': formulari})
    else:
        formulari = NovaUFForm(initial={'nom':uf.nom,
                'data_inici':uf.dinici, 'data_fi':uf.dfi,
                'assignatura': uf.assignatura, 'horesTeoriques': uf.horesTeoriques})
        return render(request,
                "form.html", {'form': formulari})

@login_required
@group_required(['professors'])
def crearUnitatFormativa(request, idAssignatura):
    #Formulari amb dades associades.
    assignatura = Assignatura.objects.get(pk=idAssignatura)
    if request.method == 'POST':
        formulari = NovaUFForm(request.POST)
        if formulari.is_valid():
            #Gravem a la BD.
            nom = formulari.cleaned_data['nom']
            data_inici = formulari.cleaned_data['data_inici']
            data_fi = formulari.cleaned_data['data_fi']
            horesTeoriques = formulari.cleaned_data['horesTeoriques']
            assignatura = Assignatura.objects.get(pk = idAssignatura)
            uf = UF(nom = nom, dinici = data_inici, dfi = data_fi, \
             assignatura=assignatura, horesTeoriques = horesTeoriques)
            uf.save()

            return HttpResponseRedirect(
                '/assignatures/veureUnitatsFormatives/' + idAssignatura)
        else:
            #Formulari sense dades associades.
            return render(request, "form.html", {'form': formulari})
    else:
        formulari = NovaUFForm(initial={'data_inici':assignatura.curs.data_inici_curs,
            'data_fi':assignatura.curs.data_fi_curs})
        return render(request, "form.html", {'form': formulari})

@login_required
@group_required(['professors'])
def llistatAssistenciaUFs(request):
    credentials = getImpersonateUser(request)
    (user, _ ) = credentials

    professor = User2Professor( user )
    head=u'Llistat %assistència entre Dates'

    grupsProfessor = Grup.objects.filter( horari__professor = professor  ).order_by('curs').distinct()
    assignaturesProfessor = Assignatura.objects.filter(
                                        horari__professor = professor,
                                        horari__grup__isnull = False ).order_by('curs','nom_assignatura').distinct()
    if request.method == 'POST':
        form = faltesAssistenciaEntreDatesForm( \
            request.POST, assignatures = assignaturesProfessor, grups = grupsProfessor )

        if form.is_valid():
            #Comprovar el codi de l'assignatura,
            #Si es tracta del report convencional o bé amb UFs solapades.
            
            #Cal tenir en compte si comptabilitzem les hores d'altres professors.
            horesAltresProfes= form.cleaned_data['horesAltresProfes']
            if horesAltresProfes:
                professor = None
                
            assignatura = form.cleaned_data['assignatura'][0]
            if assignatura.tipus_assignatura.tipus_assignatura.lower() \
                == settings.CUSTOM_UNITAT_FORMATIVA_DISCONTINUADA:
                report = faltesAssistenciaEntreDatesUFsDiscontinuadesRpt(
                    grup = form.cleaned_data['grup'],
                    assignatura = form.cleaned_data['assignatura'][0])
            else:
                report = faltesAssistenciaEntreDatesUFsRpt(
                    grup = form.cleaned_data['grup'],
                    assignatura = form.cleaned_data['assignatura'][0],
                    professor = professor)

            return render(request,
                    'reportTabs.html',
                        {'report': report,
                         'head': 'Informació alumnes' ,
                        })
    else:
        form = faltesAssistenciaEntreDatesForm( \
            assignatures = assignaturesProfessor , grups = grupsProfessor)
    return render(request,
                'form.html',
                {'form': form,
                 #'infoForm': [],
                 'head': head})

@login_required
@group_required(['professors'])
def configurarNotificacions(request, idAssignatura):
  assignatura=Assignatura.objects.get(id=idAssignatura)
  missatge=u''
  if request.POST:
    #Modificar les dades a la BD.
    if request.POST['activarNotificacions'].lower() == 'no':
      assignatura.activar_notificacions = False
    else:
      assignatura.activar_notificacions = True
    assignatura.percent_primer_avis = request.POST['primeraNotificacio']
    assignatura.percent_segon_avis = request.POST['segonaNotificacio']
    assignatura.save()
    missatge=u'Dades modificades'

  return render(
              request,
              "configurarNotificacions.html",
              {"assignatura":assignatura, "usuari":request.user, "missatge":missatge,
                "primeraNotificacio":assignatura.percent_primer_avis, "segonaNotificacio":assignatura.percent_segon_avis,
                "activarNotificacions":assignatura.activar_notificacions})

@login_required
@group_required(['professors'])
def testLlistatAssistenciaUFsDiscontinuades(request):
    assignatura = Assignatura.objects.get(id=60)
    grup = Grup.objects.get(id=11)

    report = faltesAssistenciaEntreDatesUFsDiscontinuadesRpt(
        grup, assignatura)

    return render_to_response(
        request,
        'reportTabs.html',
        {'report': report,
         'head': 'Informació alumnes' ,
        })
    '''
    from django.http import HttpResponse
    response = HttpResponse()
    response.write(html)
    return response
    '''
