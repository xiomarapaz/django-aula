#encoding: utf-8

#Eliminar les franges horaries
from aula.apps.horaris.models import FranjaHoraria
FranjaHoraria.objects.all().delete()


#Carregar la fixture.
from subprocess import call
resultat = call('python ../../manage.py loaddata frangesHoraries.json', shell= True)
if resultat==0:
    print ("tot correcte")
else:
    print ("alguna cosa ha fallat!")