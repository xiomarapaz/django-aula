# This Python file uses the following encoding: utf-8

from django.http.response import *
import re
from xlutils.copy import copy
from xlutils.filter import process,XLRDReader,XLWTWriter
import xlrd, xlwt
from django.conf import settings

#Importació meva aplicació
from extHoraris.models import *

FILTRE_GRUP = 0
FILTRE_PROFE = 1
FILTRE_AULA = 2

ORDENAT_COLUMNES = 0
ORDENAT_FILES = 1

"""
    Valida que no hi hagi cap error, si n'hi ha algun llança una excepció.
"""
def validarFormulariHorari(request):
    if len(request.POST['codiMateria']) > 15:
        raise Exception(u"El codi de l'assignatura no pot superar els 15 caràcters.<br>.")
    if re.search('^MP[0-9]{2}(-{0,1}[A-Z|0-9|\s]+)?$',request.POST['codiMateria']) is None:
        raise Exception(u"Error el codi de la matèria ha de ser en majúscules" +
                ", sense espais i amb sigles per exemple: MP01-BD, MP01, MP02-LAB ...<br>.")

def imprimirHorariAula(idAula):
    fileToRead = settings.EXT_HORARIS_DIR + u'/horariPlantillaAula.xls'
    destFileName = u'/horariAula_' + idAula + u'.xls'
    fileToWrite = settings.MEDIA_ROOT  + destFileName
    rwb = xlrd.open_workbook(fileToRead, formatting_info=True)
    rsheet = rwb.sheet_by_index(0)

    wwb = copy(rwb)
    wsheet = wwb.get_sheet(0)
    #Volem el full en horitzontal
    wsheet.set_portrait(False)
    #wsheet.insert_bitmap(settings.EXT_HORARIS_DIR + u'/logo.bmp', 0, 5)
    wsheet.insert_bitmap(settings.EXT_HORARIS_DIR + u'/logo.bmp', 0, 5, x=0, y=10, scale_x=0.11, scale_y=0.11)

    taula = _crearTaulaHorari(idAula,FILTRE_AULA)
    for idxf, fil in enumerate(taula):
        for idxc, cela in enumerate(fil):
            tmpStr = u''
            #tmpStrAula = u''
            for classe in cela:
                entrada = classe
                """:type : EntradaHorari"""
                #print str(entrada.profe) + str(entrada.aula) + str(idxf) + str(idxc)
                if (tmpStr != ''):
                    tmpStr = tmpStr + "\n\n"
                    #tmpStrAula = tmpStrAula + "\r\n"
                tmpStr = tmpStr + unicode(entrada.grup) + " (" + unicode(entrada.grup.codiXtec) + ")" + \
                    " - " + unicode(entrada.materia) + "\n" + \
                         unicode(entrada.profe.nomComplert)

                #tmpStrAula = tmpStrAula + str(entrada.profe) + " - " + str(entrada.aula)
            _modificarValorCela(rsheet, wsheet, str(idxf) + ',' + str(idxc), tmpStr)
            #_setOutCell(wsheet, idxf + filesMargeSuperior, idxc*2 + 1 + columnesMargeEsquerre, tmpStrAula)

    #Escriure les franges horàries.
    franges = Franja.objects.all()
    for idx, franja in enumerate(franges):
        _modificarValorCela(rsheet, wsheet, 'hora' + str(idx), str(franja))

    #Escriure el nom de l'aula
    aula = Aula.objects.get(id=idAula)
    _modificarValorCela(rsheet, wsheet, 'aula', aula.nom)

    wwb.save(fileToWrite)

    return settings.MEDIA_URL + destFileName

def imprimirHorariProfe(idProfe):
    fileToRead = settings.EXT_HORARIS_DIR + u'/horariPlantillaProfe.xls'
    destFileName = u'/horariProfe_' + idProfe + u'.xls'
    fileToWrite = settings.MEDIA_ROOT  + destFileName
    rwb = xlrd.open_workbook(fileToRead, formatting_info=True)
    rsheet = rwb.sheet_by_index(0)

    wwb = copy(rwb)
    wsheet = wwb.get_sheet(0)
    #Volem el full en horitzontal i altres propietats. El logo no es copia inserto manualment.
    wsheet.set_portrait(False)
    wsheet.insert_bitmap(settings.EXT_HORARIS_DIR + u'/logo.bmp', 0, 5, x=0, y=10, scale_x=0.11, scale_y=0.11)
    wsheet.set_left_margin(0.25)
    wsheet.set_right_margin(0.25)
    wsheet.set_top_margin(0.25)
    wsheet.set_bottom_margin(0.25)
    wsheet.set_header_str('')
    wsheet.set_footer_str('')

    taula = _crearTaulaHorari(idProfe,FILTRE_PROFE)
    for idxf, fil in enumerate(taula):
        for idxc, cela in enumerate(fil):
            tmpStr = u''
            tmpStrAula = u''
            for classe in cela:
                entrada = classe
                """:type : EntradaHorari"""
                #print str(entrada.profe) + str(entrada.aula) + str(idxf) + str(idxc)
                if (tmpStr != ''):
                    tmpStr = tmpStr + "\n\n"
                tmpStr = tmpStr + unicode(entrada.grup) + " (" + unicode(entrada.grup.codiXtec) + ")" + \
                        " - " + unicode(entrada.materia) + "\n" + \
                            unicode(entrada.aula)
            _modificarValorCela(rsheet, wsheet, str(idxf) + ',' + str(idxc), tmpStr)

    #Escriure les franges horàries.
    franges = Franja.objects.all()
    for idx, franja in enumerate(franges):
        _modificarValorCela(rsheet, wsheet, 'hora' + str(idx), unicode(franja))

    #Escriure el nom del profe.
    profe = Profe.objects.get(id=idProfe)
    _modificarValorCela(rsheet, wsheet, 'nom', unicode(profe.nomComplert))
    wwb.save(fileToWrite)

    return settings.MEDIA_URL + destFileName

def imprimirHorariGrup(idGrup):
    fileToRead = settings.EXT_HORARIS_DIR + u'/horariPlantillaGrup.xls'
    destFileName = u'/horariGrup_' + idGrup + u'.xls'
    fileToWrite = settings.MEDIA_ROOT  + destFileName
    rwb = xlrd.open_workbook(fileToRead, formatting_info=True)
    rsheet = rwb.sheet_by_index(0)

    wwb = copy(rwb)
    wwb, wwb_style = _copy2(rwb)

    wsheet = wwb.get_sheet(0)
    #Volem el full en horitzontal i altres propietats. El logo no es copia inserto manualment.
    wsheet.set_portrait(False)
    #wsheet.insert_bitmap(settings.EXT_HORARIS_DIR + u'/logo.bmp', 0, 5, x=5, y=5, scale_x=0.75, scale_y=0.75)
    wsheet.insert_bitmap(settings.EXT_HORARIS_DIR + u'/logo.bmp', 0, 5, x=0, y=0, scale_x=0.095, scale_y=0.095)
    wsheet.set_left_margin(0.25)
    wsheet.set_right_margin(0.25)
    wsheet.set_top_margin(0.25)
    wsheet.set_bottom_margin(0.25)
    wsheet.set_header_str('')
    wsheet.set_footer_str('')

    taula = _crearTaulaHorari(idGrup,FILTRE_GRUP, ORDENAT_COLUMNES)
    for idxc, col in enumerate(taula):
        valorAnterior = u''
        indexAnterior = None
        for idxf, cela in enumerate(col):
            tmpStr = u''
            for classe in cela:
                entrada = classe
                """:type : EntradaHorari"""
                if (tmpStr != u''):
                    tmpStr = tmpStr + u"\n\n"
                tmpStr = tmpStr + unicode(entrada.materia) + u" - " + unicode(entrada.aula) + u"\n" + \
                         unicode(entrada.profe.nomComplert)
            indexActual = _cercaExcel(rsheet, u'[' + unicode(idxf) + ',' + unicode(idxc) + ']')
            #print u'cerca cela: {0}, {1}, {2} ---> {3} '.format(idxf, idxc, unicode(indexActual), tmpStr)
            if tmpStr == valorAnterior and tmpStr != u'':
              #Fusiona cel·les, si tenen el mateix valor que l'anterior.
              if indexActual != None and indexAnterior != None:
                #print 'fusiona:{0} {1}, {2} {3}'.format(indexAnterior[0], indexAnterior[1], indexActual[0], indexActual[1])
                wsheet.merge(indexAnterior[0], indexActual[0], indexAnterior[1], indexActual[1])
                # Obtenir el mateix estil que la cel·la anterior. No ho fà i nosé perquè.
                celaO=_getOutCell(wsheet, indexActual[0], indexActual[1])
                celaD=_getOutCell(wsheet, indexAnterior[0], indexAnterior[1])
                saved_style = wwb_style[celaO.xf_idx]
                celaO.xf_idx = celaD.xf_idx
              else:
                print "ERROR", indexActual, indexAnterior
            else:
              #Assigna valors
              if indexActual != None:
                #print u'cell:{0}, {1}, {2}'.format(indexActual[0], indexActual[1], tmpStr)
                _setOutCell(wsheet, indexActual[0], indexActual[1], tmpStr)
              else:
                print "ERROR2", indexActual

            indexAnterior = indexActual
            valorAnterior = tmpStr

    #Escriure les franges horàries.
    franges = Franja.objects.all()
    for idx, franja in enumerate(franges):
        _modificarValorCela(rsheet, wsheet, 'hora' + str(idx), str(franja))

    #Escriure el grup.
    grup = Grup.objects.get(id=idGrup)
    _modificarValorCela(rsheet, wsheet, 'grup', str(grup.nom))

    wwb.save(fileToWrite)

    return settings.MEDIA_URL + destFileName


def _crearTaulaHorari(id, tipusFiltre=FILTRE_GRUP, tipusTaulaVisualitzacio=ORDENAT_FILES):
    """
    Genera la taula amb l'horari del grup en memòria.
    Retorna una taula de objectes tipus EntradaHorari

    :param idGrup: El grup a crear la taula.
    :param bd: la BD a utilitzar
    :return: Taula de objectes tipus EntradaHorari
    """

    dies = Dia.objects.all()
    franges = Franja.objects.all()

    if (tipusFiltre == FILTRE_GRUP):
        entradesHorari = EntradaHorari.objects.filter(grup__id=id).order_by('dia')
    elif (tipusFiltre == FILTRE_PROFE):
        entradesHorari = EntradaHorari.objects.filter(profe__id=id).order_by('dia')
    elif (tipusFiltre == FILTRE_AULA):
        entradesHorari = EntradaHorari.objects.filter(aula__id=id).order_by('dia')

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
        entradaHorari.color = '{0},{0},{0}'.format(str(entradaHorari.materia.id * 40 % 200))
        matriuDiaHora[entradaHorari.dia.id][entradaHorari.franja.id].append(entradaHorari)

    #Colocar les entrades de l'horari en la taula de visualització.
    taula = []

    if tipusTaulaVisualitzacio == ORDENAT_FILES:
      #Recorregut per files
      i = 0
      for franja in franges:
          fila = []
          j = 0
          for dia in dies:
              fila.append('')
              if (matriuDiaHora.get(dia.id,None) != None):
                  if (matriuDiaHora[dia.id].get(franja.id,None) != None):
                      fila[j] = matriuDiaHora[dia.id][franja.id]
              j = j + 1

          taula.append(fila)
          i = i + 1
    else:
      #Recorregut per columnes.
      i = 0
      for dia in dies:
        col = []
        j = 0
        for franja in franges:
          col.append('')
          if (matriuDiaHora.get(dia.id,None) != None):
            if (matriuDiaHora[dia.id].get(franja.id,None) != None):
              col[j] = matriuDiaHora[dia.id][franja.id]
          j += 1
        taula.append(col)
        i += 1

    return taula

def _getOutCell(outSheet, rowIndex, colIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row: return None

    cell = row._Row__cells.get(colIndex)
    return cell

def _setOutCell(outSheet, row, col, value):
    """ Change cell value without changing formatting. """
    newCell = None

    # HACK to retain cell style.
    previousCell = _getOutCell(outSheet, row, col)
    # END HACK, PART I

    outSheet.write(row, col, value)

    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, row, col)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
    # END HACK
    return newCell

def _cercaExcel(sheet, valor):
  resultat = None
  fi = False
  files = range(sheet.nrows)
  cols = range(sheet.ncols)
  r = 0
  while r < len(files) and not fi:
    c = 0
    while c < len(cols) and not fi:
        cell = sheet.cell(r, c)
        if cell.value == valor:
          resultat = (r, c)
          fi = True
        c += 1
    r +=1
  return resultat

def _modificarValorCela(rsheet, wsheet, valorACercar, valorASubstituir):
  resultat = _cercaExcel(rsheet, '[' + valorACercar + ']')
  if resultat != None:
    _setOutCell(wsheet, resultat[0], resultat[1], valorASubstituir)
  return resultat

#
# suggested patch by John Machin
# http://stackoverflow.com/a/5285650/2363712
#
def _copy2(wb):
    w = XLWTWriter()
    process(
        XLRDReader(wb,'unknown.xls'),
        w
        )
    return w.output[0][1], w.style_list
