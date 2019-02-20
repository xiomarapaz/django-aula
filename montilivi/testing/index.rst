Donar permisos a les BD de test:

::

	GRANT ALL PRIVILEGES ON devel_djangoaula.* TO 'test_devel_userdjangoaula'@'localhost';
	GRANT ALL PRIVILEGES ON devel_djangoaula.* TO 'test_devel_userdjangoaula'@'localhost';


Com fer testing sobre el servidor, connectem al servidor amb la opció -X, cal instal·lar firefox en el server.

::

    ssh -p 8222 -C -X root@[adrecaMonti]

Baixa el geckodriver, mozilla automàtic:

    https://github.com/mozilla/geckodriver/releases

Configura el fitxer test.bash indica on està el geckodriver.

Executa test.bash

