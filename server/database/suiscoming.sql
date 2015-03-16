--- Database Suniscoming ---
--- Author: Eri Jonhson Oliveira da Silva ---
--- Author: Ordan Silva Santos ---

CREATE DATABASE `suniscoming` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `suniscoming`;

CREATE TABLE `tb_master` (
  `id_master` INT NOT NULL AUTO_INCREMENT,
  `nm_email` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nm_password` VARCHAR(255) NOT NULL,
  `nr_killed` INT DEFAULT 0,
  `nr_life` INT DEFAULT 0,
  `dt_record` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (`nm_email`),
  PRIMARY KEY (`id_master`)
);

