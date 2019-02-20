import csv
from datetime import datetime

primeraLinia=True
comptador=10
with open('/home/administrador/Baixades/cas.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if primeraLinia:
            primeraLinia=False
        else:
            if len(row)>3:
                noms = unicode(row[1],'latin-1').split(",")
                dataNeixement=datetime.strptime(row[2], "%d/%m/%Y")
                print 'python manage.py createAlumn ' + str(comptador) + ' "' + noms[1].strip() + '" "' + noms[0] + '" ' + dataNeixement.strftime("%d-%m-%Y") + ' "CAS1"'
                comptador+=1
