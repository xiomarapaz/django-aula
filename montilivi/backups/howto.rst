Configuració copia de seguretat
=====================================

Cal instal·lar les dependències descrites a l'apartat Copia de seguretat externa.

Cal copiar els fitxers dins la carpeta de root.

Cal fer un petit directori backup, tal i com indica l'script.

.. code:: bash

    mkdir /root/backup

Cal configurar les diferents variables dels diferents scripts. (copiaDjangoAulaDiaria, copiaDjangoAulaSetmanal). La resta de scripts estiren d'aquest primer.

Cal configurar els fitxers de suport amb els passwords corresponents.

passwdMysql - Password del mysql. Cal configurar-lo així.

.. code::bash

    [client]
    password=*****

passwdCopies - Password del servidor de copies de l'IES

passwdHosting - Password del servidor de hosting extern

Cal editar el cron de forma que s'inici una copia diària i una setmanal executant els corresponents scripts.

Executem com a root la següent comanda:

.. code:: bash

    crontab -e 

.. code:: bash

    # m     h       dom     mon     dow     command
    0       0       *       *       *       bash /root/copiaDjangoAulaDiaria.bash
    0       0       *       *       0       bash /root/copiaDjangoAulaSetmanal.bash$

Copia de seguretat externa
=============================

Cal protegir-la per fer-ho ens baixem el gpg. (Ja instal·lat en Ubuntu 12.04)
Cal també lftp per transferir-la a un servidor extern.

.. code:: bash

    apt-get install lftp

.. code:: bash

    gpg -c backup.tar.gz
    #Ens Ho guarda com a backup.tar.gz

Descomprimir.

.. code:: bash

    gpg -o restore.tar.gz -d backup.tar.gz.gpg

.. code:: bash

    lftp -e 'cd backup_faltes; put prova.txt.gpg' -u programa,[PASSWORD] programaraplicaciones.com

Com descomprimir una copia externa
-------------------------------------

.. code:: bash

    gpg -d djangocopia-4.sql.gpg > restore.tar.gz #Aquí ens demanarà la contrasenya.
    tar -xzvf restore.tar.gz

Com restaurar
==================

Renombrem la BD vella com a OLDdjangofaltes. Ho podem fer amb el PHPMyAdmin amb codi no és possible.

Reecreem la BD i li assignem els permisos típics de creació.

.. code:: sql

    CREATE DATABASE djangoaula CHARACTER SET utf8;
    GRANT ALL PRIVILEGES ON djangoaula.* TO 'userdjangoaula'@'localhost';
    USE djangoaula;
    SET storage_engine=INNODB;

Executem la recuperació. 

.. code:: sql
    
    //mysql -u [uname] -p[pass] [db_to_restore] < [backupfile.sql]
    mysql -u root -p djangoaula < djangoaula.sql 
    
    

