from django.db import connection
from django.contrib.auth.models import User


def resetUsuaris():
	from django.contrib.auth.models import User

	for i in range(1,51):

		u = User.objects.get(username="profe"+str(i))
		u.first_name="Professor"+str(i)
		u.set_password('1234')
		u.last_login = None
		u.last_name='Cognom'+str(i)
		u.email=''
		u.is_active=True
		u.save()


with connection.cursor() as cursor:
	cursor.execute("DELETE FROM `incidencies_incidencia`")
	cursor.execute("DELETE FROM `presencia_controlassistencia`")
	cursor.execute("UPDATE `presencia_impartir` SET `dia_passa_llista`=NULL, `professor_passa_llista_id`=NULL, `professor_guardia_id`=NULL;")
	cursor.execute("DELETE FROM `assignatures_ufavisos`")
	cursor.execute("DELETE FROM `assignatures_uf`")

resetUsuaris()
