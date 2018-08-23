#encoding utf-8

raise Exception("No executis, produeix noms duplicats")
'''
from extHoraris.models import Materia
import re

def canviarTitolMateria(materia):
    xreg = re.search('[0-9]+', materia.codi)
    numero = int(xreg.group(0))
    iniciNumero = xreg.start(0)
    fiNumero = xreg.end(0)
    codiIniciText = materia.codi[0:iniciNumero]
    codiFinalText = materia.codi[fiNumero:]
    if not (codiIniciText.upper() == "MP" or codiIniciText.upper() == "M"):
        #Tenim un problema informar.
        raise Exception("Ha fallat el codi:" + str(materia.codi))

    materia.codi = "M" + "{:0>2d}".format(numero) + codiFinalText
    print materia.codi
    materia.save()

materies = Materia.objects.all()
for materia in materies:
    try:
      canviarTitolMateria(materia)
    except Exception as e:
      print str(e)
'''
