#encoding: utf-8

#Programa en Python que unirà els grups de SAGA i els alumnes de SAGA, en el moment en que no està fixada la matrícula.
#./docs/installacio/IMPORTAR A DJAU sense curs actualitzat.docx

import csv
from csv import Dialect, QUOTE_MINIMAL

class MyDialect(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL

#TODO: Comprovar que fitxer1 i fitxer2 tinguin la mateixa llargada.

dictAlumneGrup={}
errors=[] #Llista alumnes amb error.

with open('/home/administrador/Descargas/grups.csv', 'rb') as fGrups:
    csv_reader_grups = csv.reader(fGrups, dialect=MyDialect)

    for grup in csv_reader_grups:
        print (grup, len(grup))
        if len(grup) == 3:
            nomAlumneSEspais = grup[1].replace(' ', '')
            dictAlumneGrup[nomAlumneSEspais] = grup[2]

with open('/home/administrador/Descargas/alumnesBo.csv', 'wb') as fAlumnesBo:
    with open('/home/administrador/Descargas/alumnes.csv', 'rb') as fAlumnes:
        csv_reader_alumnes = csv.reader(fAlumnes, dialect=csv.excel)
        csv_writer_alumnesBo = csv.writer(fAlumnesBo, dialect=csv.excel)

        primeraLinia = True
        for linia in csv_reader_alumnes:
            if primeraLinia:
                primeraLinia = False
            else:
                if len(linia)==18:
                    nomAlumneSEspais=linia[2].replace(' ','')
                    if nomAlumneSEspais in dictAlumneGrup:
                        print (nomAlumneSEspais, dictAlumneGrup[nomAlumneSEspais])
                        linia[17]=dictAlumneGrup[nomAlumneSEspais]
                        csv_writer_alumnesBo.writerow(linia)
                    else:
                        errors.append(nomAlumneSEspais)

print ("ERRORS DETECTATS: ", errors)

