#Exemple de com exportar la informació dels models
#Alerta amb la opció indent, fa llegible les dades.
python ../../manage.py dumpdata extHoraris.Grup extHoraris.Franja extHoraris.Dia extHoraris.Aula --indent 2 > /var/dadesProtegides/horaris/fixturesHoraris.json
python ../../manage.py dumpdata extHoraris.Profe --indent 2 > /var/dadesProtegides/horaris/fixturesProfes.json
