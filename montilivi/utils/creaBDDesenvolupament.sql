CREATE USER IF NOT EXISTS 'devel_userdjangoaula'@'localhost' IDENTIFIED BY 'patata';

CREATE DATABASE IF NOT EXISTS devel_djangoaula CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON devel_djangoaula.* TO 'devel_userdjangoaula'@'localhost';

CREATE DATABASE IF NOT EXISTS devel_horaris CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON horaris.* TO 'devel_userdjangoaula'@'localhost';

