==================================================
Documentació de com fer la carrega inicial
==================================================

.. index:: index

HowTO carrega inicial.
========================

Suposem que partim d'una BD pelada.

**Creació BD**

Accedim a la consola de MySQL i executem (compte cal canviar XXXXX pel password):

.. code:: sql

    CREATE DATABASE djangoaula CHARACTER SET utf8;
    CREATE USER 'userdjangoaula'@'localhost' IDENTIFIED BY 'XXXXX';
    GRANT ALL PRIVILEGES ON djangoaula.* TO 'userdjangoaula'@'localhost';
    USE djangoaula;
    SET storage_engine=INNODB;

Versió nova (Ubuntu 16.04)

.. code:: sql

    CREATE DATABASE djangoaula CHARACTER SET utf8;
    CREATE USER 'userdjangoaula'@'localhost' IDENTIFIED BY 'XXXXX';
    GRANT ALL PRIVILEGES ON djangoaula.* TO 'userdjangoaula'@'localhost';
    USE djangoaula;

**Ara crearem l'estructura de la BD**

.. code:: bash
    
    python manage.py syncdb

Nova...

.. code:: bash

    python manage.py migrate

**Configurar accés superusuari**

Aquí també es configura un accés de superusuari, per defecte és administrador, canvia'l a root.

La versió vella ja ho fa sol.

A la nova versió.

.. code:: bash

    python manage.py createsuperuser #IMPORTANT: Creo usuari root

**Assigna el superusuari al grup direcció**

.. code:: bash

    python ../../manage.py shell < assignaAdministradorARoot.py
    python ./assignaAdministradorARoot.py

Ara cal configurar les dades inicials, normalment son dades de proves. Però ja les he adaptat per la primer càrrega inicial.

.. code:: bash
    
    bash /scripts/fixtures.sh

Importem els nivells, cursos, que es troben a la mateixa carpeta d'aquest document.

.. code:: bash

    bash ./importar.bash

Generem els grups i fem que **els cursos s'inicien a la data correcte**.

Maniuplem el fitxer **crearGrups.py**, hi ha una part on indica quan comença i quan s'acaba una assignatura.

.. code:: bash

    python ../../manage.py shell
    %run ./crearGrups.py

    #Alternativament pots fer copy paste interactiu.
    %cpaste
    #Inserim el fitxer aquí.
    CTRL-D

Comprovar usuari administrador (root), assignar-li el grup de direcció.

    http://localhost:8000/admin/auth/user/

**Modifico franges horaries**

Esborra la taula i carrega fixtures d'aquest directori

.. code:: python

    python ../../manage.py shell < carregaFrangesHoraries.py


Segueixo el procés de carrega de l'administració

    http://127.0.0.1:8000/utils/carregaInicial/

Carrega d'horaris
-------------------

Si hem fet servir el programa d'horaris via web fet a Montilvi. Simplement entrem a la web identificant-nos com a root, ja sortirà la opció d'exportar a CSV.

Accedim a la web:

http://127.0.0.1:8000/extKronowin/sincronitzaKronowin/

Anem a sincronitzar els horaris, aquests es troben a la carpeta **/var/dadesProtegides/aula/horaris/horaris.csv**

Associem els grups i les franges:

http://127.0.0.1:8000/extKronowin/assignaGrups/

http://127.0.0.1:8000/extKronowin/assignaFranges/

Modificar tipus d'assignatura
--------------------------------
Un cop hem carregat els horaris, cal modificar el tipus d'assignatura.

Executem el fitxer **passarAssignaturesAUF.py**

.. code:: bash

    python manage.py shell 
    %run passarAssignaturesAUF.py

    #De forma alternativa pots fer copy/paste.
    %cpaste
    #Inserim el fitxer aquí.
    CTRL-D

Regenerar horaris
----------------------

Iniciar el procés de regeneració, tarda un ou i mig.

Alternativa carrega horaris
-------------------------------------

Accedim a la web i seguim les instruccions a partir KronoWin:

http://127.0.0.1:8000/utils/opcionsSincro/

Carregar alumnes
----------------------

Simplement carreguem el fitxer que ens passa en Xevi.S.

Carregar alumnes vell
------------------------

En xevi.S m'ha passat un fitxer amb les dades corresponents. Problema el grup no està informat. El que fem temporalment és agafar el pla estudis i el nivell del saga i així podem crear un camp grup que correspon a la fusió d'aquests dos camps.

  - Fusiono els camps en el camp del grup 15. Faig un mid(40) i un mid(20)
  - Guardo com a CSV i elimino els camps sobrants.
  - Passo l'script de processat en python (procés detallat a continuació).

Primer processem el fitxer perque les dades dels alumnes siguin correctes.

.. code:: bash

    cd /var/djangofaltes/proves/carregaInicial
    python alumnesSagaMonti2DJangoAula.py

Importem alumnes seguim els pasos per sincrontizar. Associem grups i sincronitzem. M'he trobat alguns alumnes sense grups.

http://127.0.0.1:8000/utils/carregaInicial/

El fitxer està a **/var/dadesProtegides/aula/alumnes/alumnesModificat.csv**

Assignar dates festives
--------------------------

Veure calendari escolar vigent:

http://www2.girona.cat/documents/11622/5588529/calendari-escolar2015-2016.pdf

Assignar direcció
------------------------

Assignar tots els membres de direcció.

Ves a l'administració users > filtra per profes i marcar el profe que fa de director.

Modificar els tutors
------------------------

Coord. Profes > Tutors > Tutors Grup

/var/dadesProtegides/aula/tutors.pdf

Taules a modificar
---------------------

No és necessari però potser: django-sites


Com obtenir fixtures
========================

La idea és omplir les dades sobre el programa i després exportar-les a través d'un JSON.

.. code:: bash

  cd /var/djangofaltes/aula/apps/alumnes/fixtures
  python /var/djangofaltes/manage.py dumpdata alumnes.nivell alumnes.grup alumnes.curs --indent 2 > dades.json

Com canviar dates dels grups
=================================

Per fer proves puc canviar les dades del curs.

.. code:: bash

    python ../../manage.py shell < canviarDatesGrup.py

        





