#encoding: utf-8

from aula.apps.alumnes.models import *
from datetime import date

DATA_INICI = date(2018, 8, 27)
DATA_FI = date(2018, 9, 30)

cursos = Curs.objects.all()
for curs in cursos:
    curs.data_inici_curs = DATA_INICI
    curs.data_fi_curs = DATA_FI
    curs.save()
