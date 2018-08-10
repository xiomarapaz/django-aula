==============================
 Dia 17 començem de nou
==============================

Treure la lletra final de cada grup
----------------------------------------

.. code:: python

    from aula.apps.alumnes.models import Grup
    grups = Grup.objects.all()
    for grup in grups:
        if grup.nom_grup[-1:].lower() == 'a':
            print "Modificant:" + grup.nom_grup + "->" + grup.nom_grup[0:-1]
            grup.nom_grup = grup.nom_grup[0:-1]
            grup.descripcio_grup = grup.nom_grup
            grup.save()


Versió light
---------------

Per esborrar les imparticions de les primeres setamanes sense modificar dates

.. code:: sql

    DELETE FROM presencia_controlassistencia
    WHERE impartir_id IN (SELECT presencia_impartir.id FROM presencia_impartir
    WHERE presencia_impartir.dia_impartir <= '2014-09-15');

    DELETE FROM presencia_impartir
    WHERE presencia_impartir.dia_impartir <= '2014-09-15';

    DELETE FROM presencia_controlassistencia
    WHERE impartir_id IN (SELECT presencia_impartir.id FROM presencia_impartir
    WHERE presencia_impartir.dia_impartir >= '2015-06-01');

    DELETE FROM presencia_impartir
    WHERE presencia_impartir.dia_impartir >= '2015-06-01';


Per fer-ho bé
-------------------

(Todo) Cal esborrar al menys:

	Presencia: controls d'assistència, imparticions
	Alumnes: Alumne
	Usuaris: (tots excepte equip directiu )
	Horaris: horaris i festius
	Kronowin: Franja2Aula, Grup2Aula
	Saga: Grup2Aula
	Missatgeria: Destinatari, DetallMissatge, Missatge
	Assignatures: Assignatura

.. code:: mysql

  //General
  DELETE FROM `incidencies_incidencia`;
  DELETE FROM `incidencies_expulsio`;
  DELETE FROM `incidencies_expulsiodelcentre`;


  DELETE FROM `presencia_controlassistencia`;
  DELETE FROM `baixes_feina`;
  DELETE FROM `presencia_impartir`;

  DELETE FROM `horaris_horari`;

  DELETE FROM `assignatures_uf`;
  DELETE FROM `assignatures_ufavisos`;
  DELETE FROM `avaluacioQualitativa_respostaavaluacioqualitativa`;
  DELETE FROM `avaluacioQualitativa_avaluacioqualitativa`;
  DELETE FROM `assignatures_assignatura`;

  //Alumnes

  DELETE FROM `tutoria_actuacio`;
  DELETE FROM `tutoria_cartaabsentisme`;
  DELETE FROM `tutoria_seguimenttutorial`;
  DELETE FROM `tutoria_tutorindividualitzat`;

  DELETE FROM `alumnes_alumne`;

  //Kronowin
  DELETE FROM `extKronowin_franja2aula`;
  DELETE FROM `extKronowin_grup2aula`;

  //Saga alumnes
  DELETE FROM `extSaga_grup2aula`;

  //Missatgeria
  DELETE FROM `missatgeria_destinatari`;
  DELETE FROM `missatgeria_detallmissatge`;
  DELETE FROM `missatgeria_missatge`;

  //Usuaris
  DELETE FROM `tutoria_tutor`;
  DELETE from auth_user_groups where user_id not in(SELECT id FROM auth_user WHERE username='root');
  DELETE FROM usuaris_accio;
  DELETE FROM usuaris_loginusuari;
  DELETE FROM usuaris_onetimepasswd;  
  DELETE FROM usuaris_abstractonetimepasswd;
  DELETE FROM `auth_user` WHERE username<>'root';

- Regenerem els horaris des de l'administració i llestos.

- Ara hauríem de configurar les dates festives.


Reconfigurar inici de curs.

.. code:: python

from datetime import date
from aula.apps.alumnes.models import Curs
cursos = Curs.objects.all()
for curs in cursos:
    curs.data_inici_curs = date(2017,9,12)
    curs.data_fi_curs = date(2018,6,1)
    curs.save()


