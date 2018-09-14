#!/bin/bash
DOM=$(date +%u -d '1 days ago')

mkdir /tmp/djangoexport
if test $DOM -eq "7"; then
    DOM=6
fi
echo "POSA EL PASSWORD DEL SERVER OVH ON TENS LA COPIA"
scp mrbackup@vps84155.ovh.net:~/djangocopia-$DOM.tar.gz.gpg /tmp/djangoexport/
if test $? -ne 0; then
    echo "Restauració ok"
else
    echo "Restauració erronea"
fi
echo "POSA EL PASSWORD PER DESENCRIPTAR"
gpg -o /tmp/djangoexport/djangocopia-$DOM.tar.gz -d /tmp/djangoexport/djangocopia-$DOM.tar.gz.gpg
if test $? -ne 0; then
    echo "Desecriptació ok"
else
    echo "Desencriptació erronea"
fi
tar -xzvf /tmp/djangoexport/djangocopia-$DOM.tar.gz -C /tmp/djangoexport/
echo "POSA EL PASSWORD DEL MYSQL -- Alerta que no sigui la BD en Producció"
read -s MYSQLPASS
#Fes copia de seguretat
mysqldump -p$MYSQLPASS -u root djangoaula > /tmp/djangoexport/backup.sql
#Esborrar la BD
for i in `mysql -uroot -p$MYSQLPASS djangoaula -e "show tables" | grep -v Tables_in` ; do  echo $i && mysql -uroot -p$MYSQLPASS djangoaula -e "SET FOREIGN_KEY_CHECKS = 0; drop table $i ; SET FOREIGN_KEY_CHECKS = 1" ; done
#Crear la BD
mysql -u root -p$MYSQLPASS djangoaula < /tmp/djangoexport/root/backup/djangoaula.sql

