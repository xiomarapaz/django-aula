ALTER TABLE `extHoraris_grup` ADD
    `codiXtec` varchar(50) NOT NULL;

ALTER TABLE `extHoraris_grup`
  MODIFY `nom` varchar(50) NOT NULL UNIQUE;
