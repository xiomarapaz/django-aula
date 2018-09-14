#!/bin/bash

#Cal inicialitzar les variables.
DATA_COPIA=$(date +%w)
FITXER_ORIGEN_FALTES=/root/backup/djangoaula.sql
FITXER_ORIGEN_HORARIS=/root/backup/djangohoraris.sql
FITXER_COPIA=/root/backup/djangocopia-${DATA_COPIA}.tar.gz
FITXER_PASSWORD_MYSQL=/root/passwdMysql
FITXER_COPIA_LOG=/root/copiesDjangoAula.log
SCRIPT_COPIA_EXTERNA=/root/copiaMYSERVER.bash
SCRIPT_COPIA_IES=/root/copiaIES.bash

mysqldump --defaults-extra-file=$FITXER_PASSWORD_MYSQL -u root djangoaula > $FITXER_ORIGEN_FALTES &&
mysqldump --defaults-extra-file=$FITXER_PASSWORD_MYSQL -u root djangohoraris > $FITXER_ORIGEN_HORARIS &&
tar -czvf $FITXER_COPIA $FITXER_ORIGEN_FALTES $FITXER_ORIGEN_HORARIS

if test $? -ne 0; then
        echo "ERROR!!!!!!!! Copia DIARIA, dia $DATA_COPIA" >> $FITXER_COPIA_LOG
else
        echo "Copia DIARIA, dia $DATA_COPIA correcte" >> $FITXER_COPIA_LOG
fi

. $SCRIPT_COPIA_IES $FITXER_COPIA $DATA_COPIA $FITXER_COPIA_LOG
echo $SCRIPT_COPIA_EXTERNA $FITXER_COPIA $DATA_COPIA $FITXER_COPIA_LOG
. $SCRIPT_COPIA_EXTERNA $FITXER_COPIA $DATA_COPIA $FITXER_COPIA_LOG
