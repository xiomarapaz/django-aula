# This Python file uses the following encoding: utf-8

#--
from aula.apps.alumnes.models import Alumne, Grup, Nivell
from aula.apps.presencia.models import ControlAssistencia
from aula.apps.missatgeria.models import Missatge
from aula.apps.usuaris.models import Professor

from django.db.models import Q 

from datetime import date 
from django.contrib.auth.models import Group

import csv, time

from aula.apps.extSaga.models import Grup2Aula
from django.core.management.base import BaseCommand, CommandError, CommandParser
import datetime

class Command(BaseCommand):
    help = 'Crea un alumne de Django'

    #Pas de parametres variables rotllu llista o diccionari.
    #http://stackoverflow.com/questions/3394835/args-and-kwargs

    def add_arguments(self, parser):
        #type: (CommandParser)->None
        # Positional arguments
        parser.add_argument('ralc', help="Numero indentificador únic de l'alumne.", type=str)
        parser.add_argument('nom', help="Nom alumne", type=str)
        parser.add_argument('cognom', type=str)
        parser.add_argument('datanaixement', type=str)
        parser.add_argument('grup', type=str)
        
    def handle(self, *args, **options):
        try:
            self.stdout.write(u'Anem a crear l\'alumne' + unicode(args))

            #Cal fer comprovacions dels paràmetres.
            a=Alumne()
            a.ralc = options['ralc']
            a.nom = options['nom']
            a.cognoms = options['cognom']
            a.data_neixement = datetime.datetime.strptime(options['datanaixement'], "%d-%m-%Y").date()
            grup = Grup.objects.get(nom_grup=options['grup'])
            a.grup = grup
            a.estat_sincronitzacio = 'MAN'
            a.data_alta = date.today()
            a.motiu_bloqueig = u'No sol·licitat'
            a.tutors_volen_rebre_correu = False
            a.save()

        except Exception as ex:
            import sys
            self.stdout.write(u"Error en el procés: " + unicode(ex) + u"\n" + unicode(sys.exc_info()))
            raise CommandError(
                    u'sintaxi: python manage.py createalumn [RALC] [Nom] [Cognoms] [dataNaixament] [grup] \n'
                    u'Exemple d\'ús: python manage.py createalumn 11111111111  "Josep" "Serra Xoriguera(m)" 08-12-2001 "DAM2"')
            
