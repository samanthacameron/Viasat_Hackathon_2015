-- --------------------------------------------------------
-- Host:                         hacksql.viasat.io
-- Server version:               5.5.43-0ubuntu0.14.04.1 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             9.2.0.4947
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for texas
CREATE DATABASE IF NOT EXISTS `texas` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `texas`;


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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

-- Dumping data for table texas.restaurants: ~10 rows (approximately)
/*!40000 ALTER TABLE `restaurants` DISABLE KEYS */;
INSERT INTO `restaurants` (`id`, `name`, `address`, `category`, `votes`) VALUES
	(1, 'Fargo\'s Pit BBQ', '720 N Texas Ave Bryan, TX 77803 ', 'bbq', 1),
	(2, 'Rudy\'s Country Store And Bar-B-Q', '504 Harvey Rd College Station, TX 77840 ', 'bbq', 1),
	(3, 'Harvey Washbangers', '1802 Texas Ave S College Station, TX 77840 ', 'burgers', 0),
	(15, 'Treebeards', '315 Travis St Downtown Houston, TX 77002 ', 'cajun', 0),
	(16, 'Fuego Tortilla Grill', '108 Poplar St College Station, TX 77840 ', 'mexican', 0),
	(17, 'Grub Burger Bar', '980 University Dr E Ste 400 College Station, TX 77840 ', 'burgers', 0),
	(18, 'Freddys Frozen Custard and Steakburgers', '930 N Earl Rudder Frwy College Station, TX 77840 ', 'burgers', 0),
	(19, 'Shipwreck Grill', '206 E Villa Maria Bryan, TX 77801 ', 'cajun', 0),
	(20, 'Heberts Cajun Cuisine Food Truck', '711 University Dr College Station, TX 77840 ', 'cajun', 0),
	(21, 'Swamp Tails', '4353 Wellborn Rd Bryan, TX 77801 ', 'cajun', 0),
	(22, 'Papa Murphys', '725 E Villa Maria Rd Bryan, TX 77802 ', 'italian', 0);
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

-- Dumping data for table texas.user: ~3 rows (approximately)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`username`, `rest_id`, `voted`) VALUES
	('clenzen', NULL, 0),
	('scameron', 2, 1),
	('wcrasta', 1, 1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;


-- Dumping structure for table texas.userlist
CREATE TABLE IF NOT EXISTS `userlist` (
  `username` varchar(50) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table texas.userlist: ~3 rows (approximately)
/*!40000 ALTER TABLE `userlist` DISABLE KEYS */;
INSERT INTO `userlist` (`username`) VALUES
	('clenzen'),
	('scameron'),
	('wcrasta');
/*!40000 ALTER TABLE `userlist` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
