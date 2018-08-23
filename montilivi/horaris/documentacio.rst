Instal·lació inicial
==========================
 
Cal instal·lar les utilitats de python per fer fitxers de Excel.

::

    sudo pip install xlutils

Crear la BD
----------------

.. code:: sql

    CREATE DATABASE gitdjangohoraris CHARACTER SET utf8;
    CREATE USER 'userdjangohoraris'@'localhost' IDENTIFIED BY 'patata';
    GRANT ALL PRIVILEGES ON gitdjangohoraris.* TO 'userdjangohoraris'@'localhost';
    
Canvia el nom de l'usuari i el password dins la instrucció anterior.

Si utilitzes la versió 5.7 del Mysql això ja no cal, per defecte ja utilitza INNODB:

.. code:: sql

    SET storage_engine=INNODB;

Configura settings
---------------------

Configura el fitxer "horaris/settings.py" apartat BD per tal que apunti a la BD corresponent amb el nom de l'usuari.


Fes migració
---------------

.. code:: bash

    python manage.py makemigrations
    python migrate

Crea superusuari
----------------------

.. code:: bash

    python manage.py createsuperuser

Creació del menú "dels grups, aules i profes".
--------------------------------------

Una possibilitat és crear-les manualment des de l'administració, amb l'usuari administrador create anteriorment.

Un cop creades les pots exportar per utilitzar-les altres anys.

Cal importar les dades inicials, aules i grups.

::
    bash montilivi/scriptsCarregaInicial/exportar.bash

Creació d'usuari per entrar horaris
------------------------------------------

Crear usuari universal a la consola Django, també es pot fer via administració.

::

	from django.contrib.auth.models import User
	user = User.objects.create_user('horaris', '', 'horaris')

Canvi any
=============

Esborrar els horaris
Esborrar els profes.

::

  use djangohoraris;
  DELETE FROM `extHoraris_entradahorari`;
  DELETE FROM `extHoraris_profe`;

Carregar els profes de nou. Els has d'obtenir del domini.

::

  python montilivi/scriptsCarregaInicial/obtenirDadesDomini.py

Carregar les dades al programa d'horarism fent webscrapping de la weppe de l'INS. Ho deixa tot dins el fitxer:

::

  /var/dadesProtegides/horaris/profes/profes.csv

A partir d'aquí si accedeixes a l'aplicació com a root pots fer canvis.

    Opció del menú "Carregar CSV Profes".

TODO
==========

- Parlar amb Secretaria per veure si podríen introduir la informació dels grups de EMV,ITC,LAB,INS i en general tots el que tenen varis grups.
!- Els grups anteriors ara son grups separats, com que ja tindrem informació al SAGA, cap problema.
- (si es pot)Intentar obtenir les dades les matèries disponibles a partir del SAGA. Cal un llistat, CURS, MATÈRIA.
