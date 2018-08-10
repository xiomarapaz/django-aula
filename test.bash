export PATH=$PATH:/home/administrador/Descargas/
#Opcions de test --keepdb, guarda la BD entre execucions. --parellel

#python manage.py test aula.apps.assignatures.tests.MySeleniumTests --keepdb --parallel
#python manage.py test aula.apps.presencia.tests.MySeleniumTests --keepdb --parallel
#python manage.py test aula.apps.presencia.tests.SimpleTest --keepdb --parallel
python manage.py test aula.apps.presenciaSetmanal.tests --keepdb --parallel

