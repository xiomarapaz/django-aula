export PATH=$PATH:/home/administrador/Descargas/
#Opcions de test --keepdb, guarda la BD entre execucions. --parellel

python manage.py test extHoraris.tests.TestsIntegracio.test --keepdb --parallel

