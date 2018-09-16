#!/bin/bash
# Requisits: gpg i lftp

#Obtenir parametres com una funció
FITXER_COPIA=$1
DATA_COPIA=$2
FITXER_COPIA_LOG=$3

#Cal inicialitzar les variables.
FITXERCOPIAXIFRAT=${FITXER_COPIA}.gpg
USER_HOSTING=programa
PASSWORD_HOSTING=$(cat /root/passwdHosting)
PASSWORD_XIFRAT="" #Cal entrar el password

#Copia amb el mateix nom però amb extensió .gpg
#Per restaurar gpg -o restore.tar.gz -d backup.tar.gz.gpg
rm $FITXERCOPIAXIFRAT
echo $PASSWORD_XIFRAT| gpg --batch --no-tty --passphrase-fd 0 -c $FITXER_COPIA && lftp -e "cd backup_faltes; put $FITXERCOPIAXIFRAT; quit" -u $USER_HOSTING,$PASSWORD_HOSTING programaraplicaciones.com
if test $? -ne 0; then
	echo "ERROR!!!!!!!! Copia EXTERNA $DATA_COPIA" >> $FITXER_COPIA_LOG
else
	echo "Copia EXTERNA $DATA_COPIA" >> $FITXER_COPIA_LOG
fi

