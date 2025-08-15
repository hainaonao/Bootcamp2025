-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: eduspark
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videos` (
  `video_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `principle` text,
  `view` int DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `created_by` int DEFAULT NULL,
  `lesson_id` int DEFAULT NULL,
  `url_video` varchar(255) DEFAULT NULL,
  `likes` int DEFAULT '0',
  `thumbnail` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`video_id`),
  KEY `lesson_id` (`lesson_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`lesson_id`),
  CONSTRAINT `videos_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
INSERT INTO `videos` VALUES (1,'Sản phẩm STEM rạp chiếu bóng mini','Ánh sáng','Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý',10,'2025-07-30 13:55:44',1,1,'/static/video/vd1.mp4',1,'/static/img/bg1.png'),(2,'Mô hình vòng tuần hoàn của nước','Sự chuyển thể của nước và vòng tuần hoàn và vòng tuần hoàn của nước trong tự nhiên','Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý',20,'2025-07-30 13:55:44',1,1,'/static/video/vd2.mp4',3,'/static/img/bg1.png'),(3,'Thí nghiệm giãn nở của không khí','Không khí có ở đâu? Tính chất và thành phần của không khí','Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý',23,'2025-07-30 13:55:44',1,1,'/static/video/vd3.mp4',5,'/static/img/bg1.png'),(4,'Thí nghiệm chuyển động của không khí','Không khí có ở đâu? Tính chất và thành phần của không khí; Gió, bão và phòng chống bão','Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý',24,'2025-07-30 13:55:44',1,1,'/static/video/vd4.mp4',7,'/static/img/bg1.png'),(5,'Điện thoại nối dây','Âm thanh và sự truyền âm thanh','Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý',25,'2025-07-30 13:55:44',1,1,'/static/video/vd5.mp4',2,'/static/img/bg1.png'),(6,'Sản phẩm STEM rạp chiếu bóng mini','Ánh sáng','Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý, Giải thích nguyên lý',26,'2025-07-30 13:55:44',1,1,'/static/video/vd1.mp4',4,'/static/img/bg1.png');
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-14 19:47:28
