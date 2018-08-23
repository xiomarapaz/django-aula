from aula.apps.alumnes.models import *
from datetime import *

###############################################
# Crear grups a partir dels cursos.
###############################################

cursos = Curs.objects.all()
for curs in cursos:
    nomGrup = curs.nom_curs + 'A'
    nomGrup2 = curs.nom_curs + 'B'
    nomGrup3 = curs.nom_curs + 'C'
    
    #Crear un dos o tres grups.
    if curs.nom_curs == 'EMV1' or curs.nom_curs == 'EMV2':
        obj, created = Grup.objects.get_or_create(curs=curs, nom_grup=nomGrup, descripcio_grup=nomGrup)
        obj, created = Grup.objects.get_or_create(curs=curs, nom_grup=nomGrup2, descripcio_grup=nomGrup2)
        obj, created = Grup.objects.get_or_create(curs=curs, nom_grup=nomGrup3, descripcio_grup=nomGrup3)                
    elif curs.nom_curs == 'INS1' or curs.nom_curs == 'INS2' \
        or curs.nom_curs == 'ITC1' or curs.nom_curs == 'ODL1':
        obj, created = Grup.objects.get_or_create(curs=curs, nom_grup=nomGrup, descripcio_grup=nomGrup)
        obj, created = Grup.objects.get_or_create(curs=curs, nom_grup=nomGrup2, descripcio_grup=nomGrup2)        
    else:
        obj, created = Grup.objects.get_or_create(curs=curs, nom_grup=curs.nom_curs, descripcio_grup=curs.nom_curs)    

###############################################
# Inicialitzar totes les dates dels cursos
###############################################

cursos = Curs.objects.all()
for curs in cursos:
    curs.data_inici_curs = date(2015,9,14)
    curs.data_fi_curs = date(2016,5,30)
    curs.save()

