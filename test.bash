#Fitxer bash per executar tots els tests d'una tirada i saber si el programa fa el que ha de fer... almenys en els casos més representatius.
export PATH=$PATH:/home/administrador/Descargas/
#Opcions de test --keepdb, guarda la BD entre execucions. --parellel

python manage.py test aula.apps.assignatures.tests.MySeleniumTests --keepdb --parallel
python manage.py test aula.apps.presencia.tests.MySeleniumTests --keepdb --parallel
python manage.py test aula.apps.presencia.tests.SimpleTest --keepdb --parallel
python manage.py test aula.apps.presenciaSetmanal.tests --keepdb --parallel

