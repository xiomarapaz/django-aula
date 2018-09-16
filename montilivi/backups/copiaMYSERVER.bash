#!/bin/bash

#Cal inicialitzar les variables.
FITXERACOPIAR=$1
DATA_COPIA=$2
FITXER_COPIA_LOG=$3

USER=piolin
PASSWORD=$(cat /root/passwdMYSERVER)

#Cal inicialitzar les variables.
FITXERCOPIAXIFRAT=${FITXERACOPIAR}.gpg
PASSWORD_XIFRAT=""

#Copia amb el mateix nom però amb extensió .gpg
#Per restaurar gpg -o restore.tar.gz -d backup.tar.gz.gpg
rm $FITXERCOPIAXIFRAT
#echo sshpass -p $PASSWORD scp $FITXERCOPIAXIFRAT mrbackup@37.59.102.95:~/
echo $PASSWORD_XIFRAT| gpg --batch --no-tty --passphrase-fd 0 -c $FITXERACOPIAR && sshpass -p $PASSWORD scp $FITXERCOPIAXIFRAT mrbackup@37.59.102.95:~/
if test $? -ne 0; then
	echo "ERROR!!!!!!!! Copia MYSERVER $DATA_COPIA" >> $FITXER_COPIA_LOG
else
	echo "Copia MYSERVER $DATA_COPIA" >> $FITXER_COPIA_LOG
fi

