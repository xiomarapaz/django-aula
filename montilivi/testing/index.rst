Com fer testing sobre el servidor, connectem al servidor amb la opció -X, cal instal·lar firefox en el server.

::

    ssh -p 8222 -C -X root@faltes.institutmontilivi.cat

Baixa el geckodriver, mozilla automàtic:

    https://github.com/mozilla/geckodriver/releases

Configura el fitxer test.bash indica on està el geckodriver.

Executa test.bash

