==================================================
Documentació de com fer la carrega inicial
==================================================

.. index:: índex

HowTO carrega inicial.
========================

Suposem que partim d'una BD pelada.

Accedim a la consola de MySQL i executem (compte cal canviar XXXXX pel password):

.. code:: sql

    CREATE DATABASE djangoaula CHARACTER SET utf8;
    CREATE USER 'userdjangoaula'@'localhost' IDENTIFIED BY 'XXXXX';
    GRANT ALL PRIVILEGES ON djangoaula.* TO 'userdjangoaula'@'localhost';
    USE djangoaula;
    SET storage_engine=INNODB;

Ara crearem l'estructura de la BD:

.. code:: bash
    
    python manage.py syncdb

Aquí també es configura un accés de superusuari, per defecte és administrador, canvia'l a root.

Ara cal configurar les dades inicials, normalment son dades de proves. Però ja les he adaptat per la primer càrrega inicial.

.. code:: bash
    
    bash /var/djangoaula/scripts/fixtures.sh

Importem els nivells, cursos, que es troben a la mateixa carpeta d'aquest document.

.. code:: bash

    bash ./importar.bash

Generem els grups i fem que **els cursos s'inicien a la data correcte**. Maniuplem el fitxer **crearGrups.py**, hi ha una part on indica quan comença i quan s'acaba una assignatura.

.. code:: bash

    python manage.py shell 
    %run ./crearGrups.py

    #Alternativament pots fer copy paste interactiu.
    %cpaste
    #Inserim el fitxer aquí.
    CTRL-D

Comprovar usuari administrador (root), assignar-li el grup de direcció.

    http://localhost:8000/admin/auth/user/


Posar l'administrador com a membre de l'equip directiu i d'administradors
----------------------------------------------------------------------------

Pots fer-ho manualment des de l'administració, jo només l'he afegit al grup direcció i ha funcionat.

Alternativa codi.

.. code:: python 

from django.contrib.auth.models import User, Group
g = Group.objects.get( name = 'direcció' )
ga = Group.objects.get ( name = 'administradors' )
a = User.objects.get( username = 'root' ) # Pots substituir admin per root si no funciona correctament.
a.groups = [ g, ga ]
a.save()
quit()

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

.. code:: python 
        
  from aula.apps.alumnes.models import *
  from datetime import *

  cursos = Curs.objects.all()
  for curs in cursos:
      curs.data_inici_curs = date(2015,8,16)
      curs.data_fi_curs = date(2015,9,16)
      curs.save()

  A partir d'aquí regenerem horaris via web.




