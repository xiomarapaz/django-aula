#Generar el calendari de festius per tots els cursos iguals.
#Simplement cal crear els rangs de dies festius dins llFestius.
from aula.apps.horaris.models import Festiu
from aula.apps.alumnes.models import Curs
from aula.apps.horaris.models import FranjaHoraria

llFestius=(
    ('2018-10-12', '2018-10-12'),
    ('2018-10-29', '2018-10-29'),
    ('2018-11-1', '2018-11-2'),
    ('2018-12-6', '2018-12-8'),
    ('2018-12-24', '2019-01-7'),
    ('2019-03-1', '2019-03-4'),
    ('2019-04-15', '2019-04-22'),
    ('2019-05-01', '2019-05-01')
)
fInici=FranjaHoraria.objects.get(hora_inici='8:00', hora_fi='9:00')
fFi=FranjaHoraria.objects.get(hora_inici='20:05', hora_fi='21:00')
for curs in Curs.objects.all():
    for festiu in llFestius:
        f1=Festiu(curs=curs,
            data_inici_festiu=festiu[0], 
            data_fi_festiu=festiu[1],
            franja_horaria_inici=fInici,
            franja_horaria_fi=fFi )
        f1.save()
