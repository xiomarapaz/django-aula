#!/bin/bash

#Cal inicialitzar les variables.
FITXERACOPIAR=$1
DATA_COPIA=$2
FITXER_COPIA_LOG=$3

USER=piolin
PASSWORD=$(cat /root/passwdSCopies)

#echo sshpass -p $PASSWORD scp $FITXERACOPIAR piolin@172.17.1.49:~/piolin/

sshpass -p $PASSWORD scp $FITXERACOPIAR piolin@172.17.1.49:~/piolin/

if test $? -ne 0; then
	echo "ERROR!!!!!!!! Copia IES $DATA_COPIA" >> $FITXER_COPIA_LOG
else
	echo "Copia IES $DATA_COPIA" >> $FITXER_COPIA_LOG
fi

