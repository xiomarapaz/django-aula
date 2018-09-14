#!/bin/bash

#Cal inicialitzar les variables.
DATA_COPIA=$(date +%F)
FITXER_ORIGEN_FALTES=/root/backup/djangoaulaSetmanal.sql
FITXER_ORIGEN_HORARIS=/root/backup/djangohorarisSetmanal.sql
DIR_WEB=/opt/django-aula/
FITXER_ORIGEN_WEB=/root/backup/djangoaulaSetmanalWeb.tar.gz
FITXER_COPIA=/root/backup/djangocopia-${DATA_COPIA}.tar.gz
FITXER_PASSWORD_MYSQL=/root/passwdMysql
FITXER_COPIA_LOG=/root/copiesDjangoAula.log
SCRIPT_COPIA_EXTERNA=/root/copiaMYSERVER.bash
SCRIPT_COPIA_IES=/root/copiaIES.bash


tar -czvf $FITXER_ORIGEN_WEB $DIR_WEB
mysqldump --defaults-extra-file=$FITXER_PASSWORD_MYSQL -u root djangoaula > $FITXER_ORIGEN_FALTES &&
mysqldump --defaults-extra-file=$FITXER_PASSWORD_MYSQL -u root djangohoraris > $FITXER_ORIGEN_HORARIS &&
tar -czvf $FITXER_COPIA $FITXER_ORIGEN_FALTES $FITXER_ORIGEN_HORARIS $FITXER_ORIGEN_WEB

if test $? -ne 0; then
	echo "ERROR!!!!!!!! Copia SETMANAL, setmana $DATA_COPIA" >> $FITXER_COPIA_LOG
else
	echo "Copia SETMANAL, setmana $DATA_COPIA correcte" >> $FITXER_COPIA_LOG
fi

. $SCRIPT_COPIA_IES $FITXER_COPIA $DATA_COPIA $FITXER_COPIA_LOG
. $SCRIPT_COPIA_EXTERNA $FITXER_COPIA $DATA_COPIA $FITXER_COPIA_LOG
