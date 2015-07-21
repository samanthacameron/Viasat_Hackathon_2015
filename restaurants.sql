-- --------------------------------------------------------
-- Host:                         hacksql.viasat.io
-- Server version:               5.5.43-0ubuntu0.14.04.1 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for texas
CREATE DATABASE IF NOT EXISTS `hackathon` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `hackathon`;


-- Dumping structure for table texas.blacklist
CREATE TABLE IF NOT EXISTS `blacklist` (
  `name` varchar(100) NOT NULL DEFAULT 'McDonalds',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table texas.blacklist: ~1 rows (approximately)
/*!40000 ALTER TABLE `blacklist` DISABLE KEYS */;
INSERT INTO `blacklist` (`name`) VALUES
	('McDonalds');
/*!40000 ALTER TABLE `blacklist` ENABLE KEYS */;


-- Dumping structure for table texas.restaurants
CREATE TABLE IF NOT EXISTS `restaurants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `address` varchar(350) NOT NULL,
  `category` varchar(50) NOT NULL,
  `votes` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8;

-- Dumping data for table texas.restaurants: ~8 rows (approximately)
/*!40000 ALTER TABLE `restaurants` DISABLE KEYS */;
INSERT INTO `restaurants` (`id`, `name`, `address`, `category`, `votes`) VALUES
	(58, 'Chick-fil-A', '2210 Briarcrest Dr Bryan, TX 77802 ', 'None', 1),
	(63, 'Fazolis', '400 Harvey Rd College Station, TX 77840 ', 'italian', 1),
	(66, 'Grub Burger Bar', '980 University Dr E Ste 400 College Station, TX 77840 ', 'burgers', 3),
	(72, 'Harvey Washbangers', '1802 Texas Ave S College Station, TX 77840 ', 'burgers', 3),
	(86, 'Cicis Pizza', '1921 S Texas Ave Bryan, TX 77802 ', 'pizza', 3),
	(89, 'Carters Burger', '3105 Texas Ave Bryan, TX 77802 ', 'burgers', 1),
	(90, 'Rudys Country Store And Bar-B-Q', '504 Harvey Rd College Station, TX 77840 ', 'bbq', 2),
	(93, 'La Familia Taqueria', '300 N Texas Ave Bryan, TX 77803 ', 'mexican', 0);
/*!40000 ALTER TABLE `restaurants` ENABLE KEYS */;


-- Dumping structure for table texas.user
CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(50) NOT NULL,
  `rest_id` int(11) DEFAULT NULL,
  `voted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`username`),
  KEY `FK_user_restaurants` (`rest_id`),
  CONSTRAINT `FK_user_restaurants` FOREIGN KEY (`rest_id`) REFERENCES `restaurants` (`id`),
  CONSTRAINT `FK_user_userlist` FOREIGN KEY (`username`) REFERENCES `userlist` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table texas.user: ~13 rows (approximately)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`username`, `rest_id`, `voted`) VALUES
	('bojeda', 90, 1),
	('cabney', 66, 1),
	('ccatalena', NULL, 0),
	('clenzen', 66, 1),
	('dayers', 90, 1),
	('dgilman', 72, 1),
	('jross', 86, 1),
	('lrutledge', 72, 1),
	('newperson', NULL, 0),
	('rmilbourne', NULL, 0),
	('scameron', 72, 1),
	('soneal', 89, 1),
	('wcrasta', 86, 1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;


-- Dumping structure for table texas.userlist
CREATE TABLE IF NOT EXISTS `userlist` (
  `username` varchar(50) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table texas.userlist: ~13 rows (approximately)
/*!40000 ALTER TABLE `userlist` DISABLE KEYS */;
INSERT INTO `userlist` (`username`) VALUES
	('bojeda'),
	('cabney'),
	('ccatalena'),
	('clenzen'),
	('dayers'),
	('dgilman'),
	('jross'),
	('lrutledge'),
	('newperson'),
	('rmilbourne'),
	('scameron'),
	('soneal'),
	('wcrasta');
/*!40000 ALTER TABLE `userlist` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
