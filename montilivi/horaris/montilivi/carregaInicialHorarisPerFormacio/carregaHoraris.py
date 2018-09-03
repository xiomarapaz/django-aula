#Genera horaris per fer formació. 
#50 profes. Cada profe fa un dies a la setmana en cursos diferents.

for i in range(1,51):
  print ("INSERT INTO `extHoraris_profe`(`nomUsuari`, `nomComplert`) VALUES ('profe{0}','Sr Professor {0}');".format(i))

from extHoraris import models
aules=models.Aula.objects.all()
dies=models.Dia.objects.all()
franges=models.Franja.objects.all()
grups=models.Grup.objects.all()


for i in range(1,51):
  models.Aula.objects.create(nom='{0:03}'.format(i))

for i in range(1,51):
    models.Materia.objects.create(codi='MP{0:02}'.format(i))

materies = models.Materia.objects.all()

nAula = 0
nProfe = 0
nMateria=0
for nGrup in range(0,10):
  for nDia in range(0,5):
    for nFranja in range(0,3):
      models.EntradaHorari.objects.create(aula=aules[nAula], dia=dies[nDia],franja=franges[nFranja], grup=grups[nGrup], materia=materies[nMateria],profe=profes[nProfe])
    nAula+=1
    nProfe+=1
    nMateria+=1


