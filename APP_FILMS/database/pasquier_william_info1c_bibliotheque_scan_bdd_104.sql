-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Ven 21 Mai 2021 à 08:42
-- Version du serveur :  5.7.11
-- Version de PHP :  5.6.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `pasquier_william_info1c_bibliotheque_scan_bdd_104`
--

-- --------------------------------------------------------
--

-- Database: pasquier_william_info1c_bibliotheque_scan_bd_104
-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS pasquier_william_info1c_bibliotheque_scan_bdd_104;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS pasquier_william_info1c_bibliotheque_scan_bdd_104;

-- Utilisation de cette base de donnée

USE pasquier_william_info1c_bibliotheque_scan_bdd_104;

--
-- --------------------------------------------------------

--
-- Structure de la table `t_avis`
--

CREATE TABLE `t_avis` (
  `id_avis` int(11) NOT NULL,
  `avis_note` tinyint(5) NOT NULL,
  `avis_message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avis`
--

INSERT INTO `t_avis` (`id_avis`, `avis_note`, `avis_message`) VALUES
(2, 5, 'Franchement très beau gosse comme manga je recommande');

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_avis`
--

CREATE TABLE `t_avoir_avis` (
  `id_avoir_avis` int(11) NOT NULL COMMENT 'Valeur unique de la table liaison avoir avis',
  `fk_scan` int(11) NOT NULL COMMENT 'Clé étrangère de T_Scan',
  `fk_avis` int(11) NOT NULL COMMENT 'Clé étrangère de T_Avis'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avoir_avis`
--

INSERT INTO `t_avoir_avis` (`id_avoir_avis`, `fk_scan`, `fk_avis`) VALUES
(1, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_genre`
--

CREATE TABLE `t_avoir_genre` (
  `id_avoir_genre` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL,
  `fk_genre` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avoir_genre`
--

INSERT INTO `t_avoir_genre` (`id_avoir_genre`, `fk_scan`, `fk_genre`) VALUES
(1, 1, 2),
(2, 1, 9),
(3, 1, 10);

-- --------------------------------------------------------

--
-- Structure de la table `t_fichier`
--

CREATE TABLE `t_fichier` (
  `id_fichier` int(11) NOT NULL,
  `fichier` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_fichier`
--

INSERT INTO `t_fichier` (`id_fichier`, `fichier`) VALUES
(1, 'https://drive.google.com/file/d/1fHlyDu8dL_cchEwHSE_jALMZQ7BrJ1_G/view?usp=sharing');

-- --------------------------------------------------------

--
-- Structure de la table `t_genre`
--

CREATE TABLE `t_genre` (
  `id_genre` int(11) NOT NULL COMMENT 'Valeur unique du genre',
  `genre` varchar(30) NOT NULL COMMENT 'Genre du scan'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_genre`
--

INSERT INTO `t_genre` (`id_genre`, `genre`) VALUES
(1, 'Shonen'),
(2, 'Seinen'),
(3, 'Shojo'),
(4, 'Horreur'),
(5, 'Hentai'),
(6, 'Yaoi'),
(7, 'Yuri'),
(8, 'Exorsisme'),
(9, 'Course'),
(10, 'Aventure');

-- --------------------------------------------------------

--
-- Structure de la table `t_mail`
--

CREATE TABLE `t_mail` (
  `id_mail` int(11) NOT NULL COMMENT 'Valeur unique du mail',
  `mail` varchar(320) NOT NULL COMMENT 'Mail de la personne'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_mail`
--

INSERT INTO `t_mail` (`id_mail`, `mail`) VALUES
(1, 'williampasquier.pro@gmail.com'),
(2, 'test@test.test'),
(3, 'caca@caca.com'),
(4, 'couille@yes.com'),
(5, 'couille@yes.com'),
(6, 'rolex@rolex.com'),
(7, 'rolex@rolex.com'),
(8, 'rolex@rolex.com'),
(9, 'rolex@rolex.com'),
(10, 'rolex@rolex.com'),
(11, 'rolex@rolex.com'),
(12, 'rolex@rolex.com'),
(13, 'rolex@rolex.com'),
(16, 'fsdfw@asdfa.com'),
(18, 'homie.boy.hb17@gmail.com'),
(19, 'yes@yes.com'),
(21, 'wpasquier61@gmail.com'),
(22, 'rolex@rolex.com'),
(23, 'beaugosse@gmail.com'),
(24, 'beaugosse@gmail.com'),
(25, 'tasoeur@gmail.com'),
(26, 'rolex@rolex.com'),
(27, 'rolex@rolex.com'),
(28, 'williampasquier.pro@gmail.com'),
(29, 'williampasquier.pro@gmail.com'),
(30, 'williampasquier.pro@gmail.com'),
(31, 'lespieds@gmail.com'),
(32, 'lespieds@gmail.com');

-- --------------------------------------------------------

--
-- Structure de la table `t_motdepasse`
--

CREATE TABLE `t_motdepasse` (
  `id_motDePasse` int(11) NOT NULL COMMENT 'Valeur unique du mot de passe',
  `motDePasse` varchar(300) NOT NULL COMMENT 'Mot de passe de la personne'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_motdepasse`
--

INSERT INTO `t_motdepasse` (`id_motDePasse`, `motDePasse`) VALUES
(1, 'JeSuisUnBg17_'),
(2, 'test'),
(3, '123456'),
(4, 'lespieds'),
(5, 'lespieds'),
(6, 'superrolex17_'),
(7, 'superrolex17_'),
(8, 'superrolex17_'),
(9, 'superrolex17_'),
(10, 'superrolex17_'),
(11, 'superrolex17_'),
(12, 'superrolex17_'),
(13, 'superrolex17_'),
(16, '1234567890'),
(18, '123456'),
(19, 'super123'),
(21, '123456'),
(22, 'superrolex17_'),
(23, '123456'),
(24, '123456'),
(25, 'tonpere'),
(26, 'superrolex17_'),
(27, 'superrolex17_'),
(28, '123456'),
(29, '123456'),
(30, '123456'),
(31, 'samediilfaitbeau'),
(32, 'supercaca');

-- --------------------------------------------------------

--
-- Structure de la table `t_personne`
--

CREATE TABLE `t_personne` (
  `id_personne` int(11) NOT NULL COMMENT 'Valeur unique de la personne',
  `pers_nom` varchar(30) NOT NULL COMMENT 'Nom de famille de la personne',
  `pers_prenom` varchar(30) NOT NULL COMMENT 'Prénom de la personne',
  `pers_dateDeNaissance` date DEFAULT NULL COMMENT 'Date de naissance de la personne',
  `pers_ageValide` tinyint(1) DEFAULT NULL COMMENT 'Sera vrai si la personne à plus de 18 ans pour accéder à certain contenu',
  `fk_pseudo` int(11) DEFAULT NULL COMMENT 'Clé étrangère de T_Pseudo',
  `fk_mail` int(11) DEFAULT NULL COMMENT 'Clé étrangère de T_Mail',
  `fk_motDePasse` int(11) DEFAULT NULL COMMENT 'Clé étrangère de T_MotDePasse'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_personne`
--

INSERT INTO `t_personne` (`id_personne`, `pers_nom`, `pers_prenom`, `pers_dateDeNaissance`, `pers_ageValide`, `fk_pseudo`, `fk_mail`, `fk_motDePasse`) VALUES
(2, 'Pasquier', 'William', '2002-08-17', 0, 1, 1, 1),
(3, 'test', 'test', '1900-01-01', NULL, 2, 2, 2),
(5, 'André', 'Pasquier', '2002-09-17', NULL, NULL, NULL, NULL),
(6, 'yes', 'oui', '2004-08-16', NULL, NULL, NULL, NULL),
(7, 'yes', 'oui', '2004-08-16', NULL, NULL, NULL, NULL),
(8, 'oui', 'ouii', '2021-03-03', NULL, NULL, NULL, NULL),
(9, 'forthtest', 'fourthtest', '2021-03-03', NULL, NULL, NULL, NULL),
(11, 'Alter', 'Theo', '2002-09-19', NULL, NULL, NULL, NULL),
(12, 'Aled', 'Ekip', '2002-09-19', NULL, NULL, NULL, NULL),
(13, 'Aled', 'Ekip', '2002-09-19', NULL, NULL, NULL, NULL),
(14, 'Alter', 'Theo', '2002-09-19', NULL, NULL, NULL, NULL),
(19, 'William', 'Pasquier', '2002-08-17', NULL, NULL, NULL, NULL),
(21, 'asd', 'asd', '2002-03-12', NULL, NULL, NULL, NULL),
(22, 'Alter', 'Theo', '2002-09-19', NULL, 1, NULL, NULL),
(23, 'Beaugosse', 'Rayan', '2003-04-13', NULL, NULL, NULL, NULL),
(24, 'Martelat', 'Luigi', '1993-02-16', NULL, NULL, NULL, NULL),
(25, ' Ton père', 'Ta mère', '2021-06-08', NULL, NULL, NULL, NULL),
(26, 'Pasquier', 'William', '2002-08-17', NULL, NULL, NULL, NULL),
(27, 'Pasquier', 'William', '2002-08-17', NULL, NULL, NULL, NULL),
(28, 'Pasquier', 'William', '2005-09-17', NULL, NULL, NULL, NULL),
(29, 'Simon', 'Oui', '2002-08-17', NULL, NULL, NULL, NULL),
(30, 'Simon', 'Oui', '2002-08-17', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `t_pseudo`
--

CREATE TABLE `t_pseudo` (
  `id_pseudo` int(11) NOT NULL COMMENT 'Valeur unique du pseudo',
  `pseudo` varchar(30) NOT NULL COMMENT 'Pseudo de la personne'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_pseudo`
--

INSERT INTO `t_pseudo` (`id_pseudo`, `pseudo`) VALUES
(1, 'Homiee'),
(2, 'test'),
(4, 'SuperCaca'),
(5, 'secondtest'),
(6, 'thirdtest'),
(7, 'thirdtest'),
(8, 'thirdtest'),
(9, 'Cacaaa'),
(10, 'Cacaaa'),
(22, 'asdasd'),
(24, 'Homie17boy'),
(25, 'SuperBgParICI'),
(27, 'asd'),
(28, 'BientotLaRolex'),
(29, 'rayan.1k7'),
(30, 'Alaska'),
(31, 'tasoeur'),
(32, 'BientotLaRolex'),
(34, 'LilHomie'),
(35, 'LilHomie'),
(36, 'LilHomie'),
(37, 'Beaugosseouioui'),
(38, 'Beaugosseouioui');

-- --------------------------------------------------------

--
-- Structure de la table `t_scan`
--

CREATE TABLE IF NOT EXISTS `t_scan` (
`id_scan` int(11) NOT NULL COMMENT 'Valeur unique du scan',
  `scan_titre` varchar(60) NOT NULL COMMENT 'Titre du Scan (manga)',
  `scan_auteur` varchar(60) NOT NULL COMMENT 'Nom et prénom de l''auteur du Scan (manga)',
  `scan_dessinateur` varchar(60) NOT NULL COMMENT 'Nom et prénom du dessinateur du Scan (manga)',
  `scan_description` text NOT NULL COMMENT 'Description du scan',
  `scan_nombreDePages` int(4) NOT NULL COMMENT 'Nombre de pages du Scan (manga)',
  `scan_maisonDEdition` varchar(30) NOT NULL COMMENT 'Maison d''édition du manga',
  `fk_fichier` int(11) DEFAULT NULL COMMENT 'Clé étrangère de T_Fichier'
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Contenu de la table `t_scan`
--

INSERT INTO `t_scan` (`id_scan`, `scan_titre`, `scan_auteur`, `scan_dessinateur`, `scan_description`, `scan_nombreDePages`, `scan_maisonDEdition`, `fk_fichier`) VALUES
(1, 'Jojo''s Bizarre Adventure - Steel Ball Run - Tome 17', 'Hirohiko Araki', 'Hirohiko Araki', 'Tome 17 avec l''apparition de Funny Valentine qui est sah sexy je bande en le voyant WALLAH', 106, 'Tonkam', 1);

-- --------------------------------------------------------

--
-- Structure de la table `t_souhaiter_lire`
--

CREATE TABLE `t_souhaiter_lire` (
  `id_souhaiter_lire` int(11) NOT NULL,
  `fk_personne` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_souhaiter_lire`
--

INSERT INTO `t_souhaiter_lire` (`id_souhaiter_lire`, `fk_personne`, `fk_scan`) VALUES
(1, 2, 1);

-- --------------------------------------------------------

--
-- Structure de la table `t_telecharger`
--

CREATE TABLE `t_telecharger` (
  `id_telecharger` int(11) NOT NULL,
  `fk_personne` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_avis`
--
ALTER TABLE `t_avis`
  ADD PRIMARY KEY (`id_avis`);

--
-- Index pour la table `t_avoir_avis`
--
ALTER TABLE `t_avoir_avis`
  ADD PRIMARY KEY (`id_avoir_avis`),
  ADD KEY `fk_scan` (`fk_scan`),
  ADD KEY `fk_avis` (`fk_avis`);

--
-- Index pour la table `t_avoir_genre`
--
ALTER TABLE `t_avoir_genre`
  ADD PRIMARY KEY (`id_avoir_genre`),
  ADD KEY `fk_scan` (`fk_scan`),
  ADD KEY `fk_genre` (`fk_genre`);

--
-- Index pour la table `t_fichier`
--
ALTER TABLE `t_fichier`
  ADD PRIMARY KEY (`id_fichier`);

--
-- Index pour la table `t_genre`
--
ALTER TABLE `t_genre`
  ADD PRIMARY KEY (`id_genre`);

--
-- Index pour la table `t_mail`
--
ALTER TABLE `t_mail`
  ADD PRIMARY KEY (`id_mail`);

--
-- Index pour la table `t_motdepasse`
--
ALTER TABLE `t_motdepasse`
  ADD PRIMARY KEY (`id_motDePasse`);

--
-- Index pour la table `t_personne`
--
ALTER TABLE `t_personne`
  ADD PRIMARY KEY (`id_personne`),
  ADD KEY `fk_pseudo` (`fk_pseudo`),
  ADD KEY `fk_mail` (`fk_mail`),
  ADD KEY `fk_motDePasse` (`fk_motDePasse`);

--
-- Index pour la table `t_pseudo`
--
ALTER TABLE `t_pseudo`
  ADD PRIMARY KEY (`id_pseudo`);

--
-- Index pour la table `t_scan`
--
ALTER TABLE `t_scan`
  ADD PRIMARY KEY (`id_scan`),
  ADD KEY `fk_fichier` (`fk_fichier`);

--
-- Index pour la table `t_souhaiter_lire`
--
ALTER TABLE `t_souhaiter_lire`
  ADD PRIMARY KEY (`id_souhaiter_lire`),
  ADD KEY `fk_personne` (`fk_personne`),
  ADD KEY `fk_scan` (`fk_scan`);

--
-- Index pour la table `t_telecharger`
--
ALTER TABLE `t_telecharger`
  ADD PRIMARY KEY (`id_telecharger`),
  ADD KEY `fk_personne` (`fk_personne`),
  ADD KEY `fk_scan` (`fk_scan`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_avis`
--
ALTER TABLE `t_avis`
  MODIFY `id_avis` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_avoir_avis`
--
ALTER TABLE `t_avoir_avis`
  MODIFY `id_avoir_avis` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Valeur unique de la table liaison avoir avis', AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_avoir_genre`
--
ALTER TABLE `t_avoir_genre`
  MODIFY `id_avoir_genre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_fichier`
--
ALTER TABLE `t_fichier`
  MODIFY `id_fichier` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_genre`
--
ALTER TABLE `t_genre`
  MODIFY `id_genre` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Valeur unique du genre', AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT pour la table `t_mail`
--
ALTER TABLE `t_mail`
  MODIFY `id_mail` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Valeur unique du mail', AUTO_INCREMENT=36;
--
-- AUTO_INCREMENT pour la table `t_motdepasse`
--
ALTER TABLE `t_motdepasse`
  MODIFY `id_motDePasse` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Valeur unique du mot de passe', AUTO_INCREMENT=36;
--
-- AUTO_INCREMENT pour la table `t_personne`
--
ALTER TABLE `t_personne`
  MODIFY `id_personne` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Valeur unique de la personne', AUTO_INCREMENT=34;
--
-- AUTO_INCREMENT pour la table `t_pseudo`
--
ALTER TABLE `t_pseudo`
  MODIFY `id_pseudo` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Valeur unique du pseudo', AUTO_INCREMENT=42;
--
-- AUTO_INCREMENT pour la table `t_scan`
--
ALTER TABLE `t_scan`
  MODIFY `id_scan` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Valeur unique du scan', AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_souhaiter_lire`
--
ALTER TABLE `t_souhaiter_lire`
  MODIFY `id_souhaiter_lire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_telecharger`
--
ALTER TABLE `t_telecharger`
  MODIFY `id_telecharger` int(11) NOT NULL AUTO_INCREMENT;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_avoir_avis`
--
ALTER TABLE `t_avoir_avis`
  ADD CONSTRAINT `t_avoir_avis_ibfk_1` FOREIGN KEY (`fk_scan`) REFERENCES `t_scan` (`id_scan`),
  ADD CONSTRAINT `t_avoir_avis_ibfk_2` FOREIGN KEY (`fk_avis`) REFERENCES `t_avis` (`id_avis`);

--
-- Contraintes pour la table `t_avoir_genre`
--
ALTER TABLE `t_avoir_genre`
  ADD CONSTRAINT `t_avoir_genre_ibfk_1` FOREIGN KEY (`fk_scan`) REFERENCES `t_scan` (`id_scan`),
  ADD CONSTRAINT `t_avoir_genre_ibfk_2` FOREIGN KEY (`fk_genre`) REFERENCES `t_genre` (`id_genre`);

--
-- Contraintes pour la table `t_personne`
--
ALTER TABLE `t_personne`
  ADD CONSTRAINT `t_personne_ibfk_1` FOREIGN KEY (`fk_pseudo`) REFERENCES `t_pseudo` (`id_pseudo`) ON DELETE CASCADE,
  ADD CONSTRAINT `t_personne_ibfk_2` FOREIGN KEY (`fk_mail`) REFERENCES `t_mail` (`id_mail`) ON DELETE CASCADE,
  ADD CONSTRAINT `t_personne_ibfk_3` FOREIGN KEY (`fk_motDePasse`) REFERENCES `t_motdepasse` (`id_motDePasse`) ON DELETE CASCADE;

--
-- Contraintes pour la table `t_scan`
--
ALTER TABLE `t_scan`
  ADD CONSTRAINT `t_scan_ibfk_1` FOREIGN KEY (`fk_fichier`) REFERENCES `t_fichier` (`id_fichier`);

--
-- Contraintes pour la table `t_souhaiter_lire`
--
ALTER TABLE `t_souhaiter_lire`
  ADD CONSTRAINT `t_souhaiter_lire_ibfk_1` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`),
  ADD CONSTRAINT `t_souhaiter_lire_ibfk_2` FOREIGN KEY (`fk_scan`) REFERENCES `t_scan` (`id_scan`);

--
-- Contraintes pour la table `t_telecharger`
--
ALTER TABLE `t_telecharger`
  ADD CONSTRAINT `t_telecharger_ibfk_1` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`),
  ADD CONSTRAINT `t_telecharger_ibfk_2` FOREIGN KEY (`fk_scan`) REFERENCES `t_scan` (`id_scan`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;