 #encoding: utf-8
 #scp root@faltes.institutmontilivi.cat:/root/backup/djangohoraris.sql .
 #scp root@faltes.institutmontilivi.cat:/root/backup/djangoaula.sql .

import subprocess
print ("password Servidor producció django:")
subprocess.call("scp root@faltes.institutmontilivi.cat:/root/backup/djangohoraris.sql /tmp/", shell=True)
print ("password Servidor producció django:")
subprocess.call("scp root@faltes.institutmontilivi.cat:/root/backup/djangoaula.sql /tmp/", shell=True)
print ("important BD, password BD local de desenvolupament")
subprocess.call("mysql -u root -p < creaBDDesenvolupament.sql", shell=True)
#subprocess.call("mysql -u root -p < djangoaula.sql", shell=True)
sqlHoraris="mysql -u root -p devel_horaris < /tmp/djangohoraris.sql"
sqlDjango="mysql -u root -p devel_djangoaula < /tmp/djangoaula.sql"
subprocess.call(sqlHoraris, shell=True)
subprocess.call(sqlDjango, shell=True)

