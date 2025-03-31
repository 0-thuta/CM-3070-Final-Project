-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: survsys
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camera`
--

DROP TABLE IF EXISTS `camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camera` (
  `camera_id` int NOT NULL AUTO_INCREMENT,
  `camera_index` int NOT NULL,
  `camera_model` varchar(100) DEFAULT NULL,
  `camera_zone` varchar(50) DEFAULT NULL,
  `zone_x1` int DEFAULT NULL,
  `zone_y1` int DEFAULT NULL,
  `zone_x2` int DEFAULT NULL,
  `zone_y2` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`camera_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `camera_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camera`
--

/*!40000 ALTER TABLE `camera` DISABLE KEYS */;
INSERT INTO `camera` VALUES (1,1,'HD Webcam','Tester',0,0,540,1080,1);
/*!40000 ALTER TABLE `camera` ENABLE KEYS */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  `gmail` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','password','admin','admin@gmail.com','2025-03-31 07:58:18');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `video` (
  `video_id` int NOT NULL AUTO_INCREMENT,
  `video_name` varchar(100) DEFAULT NULL,
  `video_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `video_location` varchar(100) DEFAULT NULL,
  `video_description` text,
  `user_id` int NOT NULL,
  `camera_id` int NOT NULL,
  PRIMARY KEY (`video_id`),
  KEY `user_id` (`user_id`),
  KEY `camera_id` (`camera_id`),
  CONSTRAINT `video_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `video_ibfk_2` FOREIGN KEY (`camera_id`) REFERENCES `camera` (`camera_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video`
--

/*!40000 ALTER TABLE `video` DISABLE KEYS */;
INSERT INTO `video` VALUES (1,'intrusion_20240917_064457.mp4','2024-09-16 22:44:57','static/intrusions videos/intrusion_20240917_064457.mp4','Intrusion detected',1,1),(2,'intrusion_20250131_012357.mp4','2025-01-30 17:23:57','static/intrusions videos/intrusion_20250131_012357.mp4','Intrusion detected',1,1),(3,'intrusion_20250319_052357.mp4','2025-03-18 21:23:57','static/intrusions videos/intrusion_20250319_052357.mp4','Intrusion detected',1,1),(4,'intrusion_20250331_062357.mp4','2025-03-30 22:23:57','static/intrusions videos/intrusion_20250331_062357.mp4','Intrusion detected',1,1);
/*!40000 ALTER TABLE `video` ENABLE KEYS */;

--
-- Dumping routines for database 'survsys'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-31 18:21:21
