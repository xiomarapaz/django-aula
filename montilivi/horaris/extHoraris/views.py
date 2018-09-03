# This Python file uses the following encoding: utf-8

#Importació django.
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http.response import *
import traceback
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
import re
import csv

#Importació meva aplicació
from extHoraris.models import *
from extHoraris import horaris
from extHoraris.forms import *
from extHoraris import utils

BD = 'default'
OPCIO_MODIFICAR = 'Modificar'
OPCIO_AFEGIR = 'Afegir'

@login_required
def index(request):
    form = None
    if request.method == 'POST':
        form = loginForm(request.POST)
        if (form.is_valid()):
            try:
                #Crear el grup a la BD local extHoraris (Obté els grups de la BD principal).
                idGrup = request.POST['idGrup']
                modelGrup = Grup.objects.get(id=idGrup)

                return HttpResponseRedirect(urlresolvers.reverse('extHoraris__calendari',args=[str(idGrup)]))
            except Exception as e:
                form.addError(u'Error al afegir el grup dins la BD.' + e.message)
    else:
        form = loginForm()

    grups = Grup.objects.all().order_by('nom')

    return render(request, 
                'extHoraris/horaris_seleccionar.html',
                {'form': form,
                 'grups': grups,
                })

@login_required
def calendari(request, idGrup):
    #Guardem la variable que ens permetrà tornar d'un manteniment de profes.
    request.session['HorarisRetorn'] = idGrup
    return __mostrarCalendari__(request, idGrup)

@login_required
def afegirEntradaHorari(request):

    idGrup = request.POST['idGrup']
    try:
        horaris.validarFormulariHorari(request)

        modelMateria, created = Materia.objects.using(BD).get_or_create(codi=request.POST['codiMateria'])
        modelProfe = Profe.objects.using(BD).get(id=request.POST['idProfe'])
        modelAula = Aula.objects.using(BD).get(id=request.POST['idAula'])
        modelDia = Dia.objects.using(BD).get(id=request.POST['idDia'])
        modelFranja = Franja.objects.using(BD).get(id=request.POST['idFranja'])
        modelGrup = Grup.objects.using(BD).get(id=idGrup)

        modelEntradaH = EntradaHorari()
        modelEntradaH.materia = modelMateria
        modelEntradaH.profe = modelProfe
        modelEntradaH.grup = modelGrup
        modelEntradaH.aula = modelAula
        modelEntradaH.dia = modelDia
        modelEntradaH.franja = modelFranja
        modelEntradaH.save(using=BD)
        return __mostrarCalendari__(request, idGrup)

    except Exception as e:
        #raise
        #import pdb; pdb.set_trace()
        return __mostrarCalendari__(request, idGrup, message=unicode(e))

@login_required
def veureEntradaHorari(request, idEntrada):
    entradaHorari = EntradaHorari.objects.using(BD).get(id=idEntrada)

    return __mostrarCalendari__(request, entradaHorari.grup.id, opcio=OPCIO_MODIFICAR,
                         codiMateria=entradaHorari.materia.codi, idProfe=entradaHorari.profe.id,
                        idAula=entradaHorari.aula.id, idDia=entradaHorari.dia.id, idFranja=entradaHorari.franja.id,
                        idEntradaHorari=idEntrada)

@login_required
def mostraAfegirEntradaHorariPle(request, idGrup, pkDia, pkFranja):
    #Mostrar el calendari amb el dia i la hora seleccionades.
    return  __mostrarCalendari__(request, idGrup, opcio=OPCIO_AFEGIR, codiMateria='',
                             idAula=0, idDia=pkDia, idFranja=pkFranja, idEntradaHorari='', message='Entra el professor i l\'assignatura, fes click a afegir', isErrorMessage=False)

@login_required
def modificarEntradaHorari(request):
    #Modificar o eliminar segons sigui el cas.
    try:
        horaris.validarFormulariHorari(request)

        idGrup = request.POST['idGrup']
        idEntradaHorari = request.POST['idEntradaHorari']
        opcio = request.POST['botoSubmit']
        entradaHorari = EntradaHorari.objects.using(BD).get(id=idEntradaHorari)

        modelMateria, created = Materia.objects.using(BD).get_or_create(codi=request.POST['codiMateria'])
        modelProfe = Profe.objects.using(BD).get(id=request.POST['idProfe'])
        modelAula = Aula.objects.using(BD).get(id=request.POST['idAula'])
        modelDia = Dia.objects.using(BD).get(id=request.POST['idDia'])
        modelFranja = Franja.objects.using(BD).get(id=request.POST['idFranja'])

        entradaHorari.materia = modelMateria
        entradaHorari.profe = modelProfe
        entradaHorari.aula = modelAula
        entradaHorari.dia = modelDia
        entradaHorari.franja = modelFranja
        entradaHorari.save(using=BD)

        return HttpResponseRedirect(urlresolvers.reverse('extHoraris__calendari',args=[str(idGrup)]))
    except Exception as e:
        return render_to_response(
                'extHoraris/resultat.html',
                {'head': u'Error al modificar entrada horari.' ,
                 'msgs': { 'errors': [u'Segurament l\'entrada ja existeix. Torna enrere i comprova-ho.', e.message.encode('utf-8')], 'warnings':  [], 'infos':  [] } },
                context_instance=RequestContext(request))

@login_required
def eliminarEntradaHorari(request, idEntrada):
    entrada = EntradaHorari.objects.using(BD).get(id=idEntrada)
    idGrup = entrada.grup.id
    entrada.delete()
    return HttpResponseRedirect( urlresolvers.reverse('extHoraris__calendari',args=[str(idGrup)]))

@login_required
def imprimirHorariGrup(request, idGrup):
    return render(request,
                'extHoraris/horaris_descarregar.html',
                {'url': horaris.imprimirHorariGrup(idGrup), 'idGrup': request.session.get('HorarisRetorn') })

@login_required
def imprimirHorariProfe(request, idProfe):
    return render(request,
                'extHoraris/horaris_descarregar.html',
                {'url': horaris.imprimirHorariProfe(idProfe), 'idGrup': request.session.get('HorarisRetorn') })

def imprimirHorariAula(request, idAula):
    return render(request,
                'extHoraris/horaris_descarregar.html',
                {'url': horaris.imprimirHorariAula(idAula), 'idGrup': request.session.get('HorarisRetorn') })

@login_required
def imprimirHorariAules(request):
    error = ''
    if request.method == 'POST':
        try:
            idAula = request.POST['id']
            return HttpResponseRedirect(urlresolvers.reverse('extHoraris__imprimirHorariAula',args=[idAula]))
        except Exception as e:
            error = u'Error al seleccionar una aula.' + e.message

    entrades = EntradaHorari.objects.all().order_by('aula')
    aules = []
    ultimaAula = ''
    for entrada in entrades:
        if entrada.aula != ultimaAula:
            aules.append(entrada.aula)
        ultimaAula = entrada.aula

    return render(request,
            'extHoraris/horaris_aula_seleccionar.html',
                {'aules': aules,
                 'idGrup': request.session.get('HorarisRetorn'),
                 'error': error})

@login_required
def imprimirHorariProfes(request):
    error = ''
    if request.method == 'POST':
        try:
            idProfe = request.POST['id']
            return HttpResponseRedirect(urlresolvers.reverse('extHoraris__imprimirHorariProfe',args=[idProfe]))
        except Exception as e:
            error = u'Error al seleccionar un professor.' + e.message

    profes = Profe.objects.all().order_by('nomUsuari')

    return render(
            request,
            'extHoraris/horaris_professor_seleccionar.html',
            {'profes': profes,
                'idGrup': request.session.get('HorarisRetorn'),
                'error': error})


@login_required
def imprimirCsv(request):

    response = None

    if request.user.is_superuser:
        import csv

        #Obtenir el model
        entrades = EntradaHorari.objects.all()
        entradesFusionades = []

        #Fem la fusio horaris que corresponguin.
        for entrada in entrades:
            if entrada.grup.fusio == True:
                entradaFusionada = {
                        'materia' : entrada.materia,
                        'profe' : entrada.profe,
                        'grup' : entrada.grup.nomFusio,
                        'aula' : entrada.aula,
                        'dia' : entrada.dia.id,
                        'franja' : entrada.franja.id }
                if __elProfeJaTreballaALaMateixaHora__(entradesFusionades, entradaFusionada) == False:
                    entradesFusionades.append(entradaFusionada)
                else:
                    print "detectat profe que treballa a la mateixa hora:" + unicode(entradaFusionada)

            else:
                entradaFusionada = {
                        'materia' : entrada.materia,
                        'profe' : entrada.profe,
                        'grup' : entrada.grup,
                        'aula' : entrada.aula,
                        'dia' : entrada.dia.id,
                        'franja' : entrada.franja.id }
                entradesFusionades.append(entradaFusionada)


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=horaris.csv'

        #Escriure directament al CSV.
        writer = csv.writer(response)
        for e in entradesFusionades:
            #print [e.profe,e.grup,'M','CICLES',e.grup,'A',e.aula,'x',e.dia,e.dia.id,e.franja.id]
            writer.writerow([e['materia'],e['profe'],e['grup'],'M','CICLES',e['grup'],'A',e['aula'],'x',e['dia'],e['franja']])
    else:
        response = HttpResponse("No tens permisos per obtenir el llistat cal ser superusuari")

    return response

@login_required
def carregarCsvProfes(request):
    msg = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #import ipdb
        #ipdb.set_trace()
        #print request.FILES
        if form.is_valid():
            if len(request.FILES)>0:
                path = __salvarFitxer(request.FILES['file'])
                nProfesCreats, nProfesActualitzats =__importarFitxerUsuaris(path)
                msg = ''
                if nProfesCreats ==0 and nProfesActualitzats==0:
                    msg=u'Cap profe creat ni actualitzat, comprova el fitxer.'
                else:
                    if nProfesCreats > 0:
                        msg+=u'Creats:' + str(nProfesCreats) + '\n'
                    if nProfesActualitzats > 0:
                        msg+=u'Actualitzats:' + str(nProfesActualitzats) + '\n'
                
    else:
        form = UploadFileForm()
    return render(
            request,
            'extHoraris/upload.html',
            {'form': form, 'msg': msg})

def __elProfeJaTreballaALaMateixaHora__(entradesFusionades, novaEntrada):
    '''
        Cal comprovar que no hi hagin profes que ja treballin en la hora que anem a fusionar.
    '''
    elProfeJaTreballaALaMateixaHora = False
    i = 0
    while (not elProfeJaTreballaALaMateixaHora and i < len(entradesFusionades)):
        if entradesFusionades[i]['profe'] == novaEntrada['profe'] and \
           entradesFusionades[i]['dia'] == novaEntrada['dia'] and \
           entradesFusionades[i]['franja'] == novaEntrada['franja']:
            elProfeJaTreballaALaMateixaHora = True
        i = i +1
    return elProfeJaTreballaALaMateixaHora

def __mostrarCalendari__(request, idGrup, opcio=OPCIO_AFEGIR, codiMateria='', idProfe=0,
                         idAula=0, idDia=0, idFranja=0, idEntradaHorari='', message='', isErrorMessage=True):
    grup = Grup.objects.using(BD).get(id=idGrup)
    dies = Dia.objects.using(BD).all()
    franges = Franja.objects.using(BD).all()
    profes = Profe.objects.using(BD).all().order_by('nomUsuari')
    materies = Materia.objects.using(BD).all()
    aules = Aula.objects.using(BD).all().order_by('nom')
    entradesHorari = EntradaHorari.objects.using(BD).filter(grup__id=idGrup).order_by('dia')

    horarisProfeSolapats = utils.comprovaProfesSolapats(idGrup)
    horarisAulesSolapades = utils.comprovaAulesSolapades(idGrup)
    
    #Crear matriu per ordenar les entrades de l'horari.
    matriuDiaHora = {}
    diaAnterior = 0
    for entradaHorari in entradesHorari:
        if (entradaHorari.dia != diaAnterior):
            matriuDiaHora[entradaHorari.dia.id] = {}
            diaAnterior = entradaHorari.dia
        if not matriuDiaHora[entradaHorari.dia.id].has_key(entradaHorari.franja.id):
            matriuDiaHora[entradaHorari.dia.id][entradaHorari.franja.id] = []
        #Afegim el color a sac dins l'entrada de l'horari, visca no tenir tipus.
        if entradaHorari.pk in horarisProfeSolapats.keys():
            #Es profe solapat pintem de vermell.
            entradaHorari.color = '255,0,0'
            e1 = horarisProfeSolapats[entradaHorari.pk][0] #type: EntradaHorari
            e2 = horarisProfeSolapats[entradaHorari.pk][1] #type: EntradaHorari
            entradaHorari.msg = "Solapament entre PROFES: " + str(e1.grup) + " i " + str(e2.grup)
        elif entradaHorari.pk in horarisAulesSolapades.keys():
            entradaHorari.color = '230,0,0'
            e1 = horarisAulesSolapades[entradaHorari.pk][0] #type: EntradaHorari
            e2 = horarisAulesSolapades[entradaHorari.pk][1] #type: EntradaHorari
            entradaHorari.msg = "Solapament entre AULES: " + str(e1.grup) + " i " + str(e2.grup)
        else:
            entradaHorari.color = '{0},125,{0}'.format(str(entradaHorari.materia.id * 40 % 200))
            entradaHorari.msg = ''
        matriuDiaHora[entradaHorari.dia.id][entradaHorari.franja.id].append(entradaHorari)

    #Colocar les entrades de l'horari en la taula de visualització.
    # Taula que conté el dia i la hora de cada entrada.
    taulaDiaHora = []  # type: List[List[utils.DiaFranja]]
    taula = []
    i = 0
    fila = []
    for franja in franges:
        filaDiaHora = []
        fila = []

        j = 0
        for dia in dies:
            filaDiaHora.append(utils.DiaFranja(dia.pk, franja.pk))
            fila.append('')
            if (matriuDiaHora.get(dia.id,None) != None):
                if (matriuDiaHora[dia.id].get(franja.id,None) != None):
                    fila[j] = matriuDiaHora[dia.id][franja.id]
            j = j + 1

        taulaDiaHora.append(filaDiaHora)
        taula.append(fila)
        i = i + 1

    #Indiquem si es tracta de modificació o afegit.
    opcioModificar = True;
    funcioControlador = urlresolvers.reverse('extHoraris__modificarEntradaHorari',args=[])

    if opcio == OPCIO_AFEGIR:
        opcioModificar = False
        funcioControlador = urlresolvers.reverse('extHoraris__afegirEntradaHorari',args=[])

    esAdministrador = False
    if request.user.is_superuser:
        esAdministrador = True

    return render(
        request,
        'extHoraris/horaris.html',
        {
            'nomGrup': grup.nom,
            'materies': materies,
            'profes': profes,
            'dies': dies,
            'franges': franges,
            'aules': aules,
            'taulaDiaHora': taulaDiaHora,
            'taula': taula,
            'idGrup': idGrup,
            'idEntradaHorari': idEntradaHorari,
            'opcioModificar': opcioModificar,
            'funcioControlador': funcioControlador,
            'codiMateria': request.POST.get('codiMateria', codiMateria),
            'idAula': int(request.POST.get('idAula', idAula)),
            'idProfe': int(request.POST.get('idProfe', idProfe)),
            'idDia': int(request.POST.get('idDia', idDia)),
            'idFranja': int(request.POST.get('idFranja', idFranja)),
            'message': message,
            'isErrorMessage': isErrorMessage,
            'esAdministrador': esAdministrador,
            'horarisProfeSolapats': horarisProfeSolapats,
            'horarisAulesSolapades': horarisAulesSolapades, 
        })

def __salvarFitxer(f):
    #Salvar el fitxer
    path = settings.TMP_DIR + '/usuaris.csv'
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return path

def __importarFitxerUsuaris(path):
    """
    Carrega el fitxer d'usuaris a la BD.
    Si hi han usuaris creats actualitza.
    """
    profesCreats=0
    profesActualitzats=0

    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            profeExistent = Profe.objects.filter(nomUsuari=row[0])
            if len(profeExistent) > 0:
                #Actualitza
                p = profeExistent[0]
                p.nomComplert = row[1]
                p.save()
                profesActualitzats+=1
            else:
                p = Profe(nomUsuari=row[0], nomComplert=row[1])
                p.save()
                profesCreats+=1
    return profesCreats, profesActualitzats
