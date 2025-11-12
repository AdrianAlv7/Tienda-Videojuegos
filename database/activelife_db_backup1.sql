-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: activelife_db
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `biblioteca`
--

DROP TABLE IF EXISTS `biblioteca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `id_producto` int NOT NULL,
  `fecha_adquirido` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `biblioteca_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `biblioteca_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca`
--

LOCK TABLES `biblioteca` WRITE;
/*!40000 ALTER TABLE `biblioteca` DISABLE KEYS */;
INSERT INTO `biblioteca` VALUES (2,1,2,'2025-11-07 05:34:54'),(7,1,6,'2025-11-07 20:42:06'),(9,1,7,'2025-11-07 21:17:44'),(10,1,8,'2025-11-07 21:26:10'),(11,1,9,'2025-11-07 21:49:14'),(12,1,10,'2025-11-07 22:05:56'),(13,4,2,'2025-11-10 03:10:17'),(14,4,6,'2025-11-10 03:10:17'),(15,1,11,'2025-11-11 21:30:01'),(16,6,2,'2025-11-12 00:46:13'),(17,6,6,'2025-11-12 00:46:13'),(18,6,8,'2025-11-12 00:48:09'),(19,6,9,'2025-11-12 00:48:09'),(20,6,10,'2025-11-12 00:48:09'),(21,6,12,'2025-11-12 00:48:09'),(22,6,11,'2025-11-12 02:51:28'),(23,7,6,'2025-11-12 03:53:50'),(24,7,7,'2025-11-12 03:53:50'),(25,7,9,'2025-11-12 03:53:50'),(26,7,10,'2025-11-12 03:53:50'),(27,5,2,'2025-11-12 06:41:00'),(28,5,6,'2025-11-12 06:50:22'),(29,5,7,'2025-11-12 06:51:28'),(30,5,8,'2025-11-12 06:58:06'),(31,5,12,'2025-11-12 07:00:45');
/*!40000 ALTER TABLE `biblioteca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrito`
--

DROP TABLE IF EXISTS `carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int DEFAULT '1',
  `fecha_agregado` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_usuario_producto` (`id_usuario`,`id_producto`),
  UNIQUE KEY `unq_usuario_producto` (`id_usuario`,`id_producto`),
  KEY `fk_carrito_producto` (`id_producto`),
  CONSTRAINT `fk_carrito_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`),
  CONSTRAINT `fk_carrito_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
INSERT INTO `carrito` VALUES (76,6,7,1,'2025-11-12 03:11:29'),(81,7,2,1,'2025-11-12 04:21:03'),(82,7,8,1,'2025-11-12 04:22:50'),(135,1,12,1,'2025-11-12 05:39:07'),(170,5,10,1,'2025-11-12 07:02:39');
/*!40000 ALTER TABLE `carrito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coleccion`
--

DROP TABLE IF EXISTS `coleccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coleccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_producto` int NOT NULL,
  `fecha_adquirido` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_usuario` (`id_usuario`,`id_producto`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `coleccion_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `coleccion_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coleccion`
--

LOCK TABLES `coleccion` WRITE;
/*!40000 ALTER TABLE `coleccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `coleccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_ventas`
--

DROP TABLE IF EXISTS `detalle_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `venta_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `venta_id` (`venta_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `detalle_ventas_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`),
  CONSTRAINT `detalle_ventas_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_ventas`
--

LOCK TABLES `detalle_ventas` WRITE;
/*!40000 ALTER TABLE `detalle_ventas` DISABLE KEYS */;
INSERT INTO `detalle_ventas` VALUES (2,2,2,1,24.99,24.99),(7,10,6,1,0.00,0.00),(9,12,7,1,0.00,0.00),(10,13,8,1,0.00,0.00),(11,14,9,1,0.00,0.00),(12,15,10,1,0.00,0.00),(13,16,2,1,0.00,0.00),(14,16,6,1,0.00,0.00),(15,17,11,1,0.00,0.00),(16,18,2,1,5.00,5.00),(17,18,6,1,2.00,2.00),(18,19,8,1,3.00,3.00),(19,19,9,1,3.00,3.00),(20,19,10,1,2.00,2.00),(21,19,12,1,100.00,100.00),(22,20,11,1,1234.00,1234.00),(23,21,6,1,2.00,2.00),(24,21,7,1,123.00,123.00),(25,21,9,1,3.00,3.00),(26,21,10,1,2.00,2.00),(27,22,2,1,5.00,5.00),(28,23,6,1,2.00,2.00),(29,24,7,1,123.00,123.00),(30,25,8,1,3.00,3.00),(31,26,12,1,100.00,100.00);
/*!40000 ALTER TABLE `detalle_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagenes_producto`
--

DROP TABLE IF EXISTS `imagenes_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagenes_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `nombre_imagen` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `imagenes_producto_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagenes_producto`
--

LOCK TABLES `imagenes_producto` WRITE;
/*!40000 ALTER TABLE `imagenes_producto` DISABLE KEYS */;
INSERT INTO `imagenes_producto` VALUES (1,6,'preview3.jpg'),(2,6,'preview4.jpg'),(3,6,'preview5.jpg'),(4,6,'preview6.jpg'),(5,7,'preview2.jpg'),(6,7,'preview3.jpg'),(7,7,'preview4.jpg'),(8,7,'preview2.jpg'),(9,7,'preview3.jpg'),(10,7,'preview4.jpg'),(11,9,'ama3.jpg'),(12,9,'chibi.jpg'),(13,9,'default.png'),(14,9,'ama3.jpg'),(15,9,'h2rFinal.png'),(16,2,'Zoe_dimensity2.jpg'),(17,2,'Juego_2.jpg'),(18,2,'Zoe_dimensity3.jpg'),(19,2,'preview5.jpg'),(20,12,'banner_bts.jpg'),(21,12,'bts.jpg'),(22,12,'Zoe_dimensity2.png'),(23,12,'Juego_2_1.jpg'),(24,12,'desconocido_1.png');
/*!40000 ALTER TABLE `imagenes_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `imagen` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (2,'Juego 2','Explora mundos abiertos y enfrenta desafíos épicos.','preview4.jpg',5.00),(6,'Zoe dimensity','xd moment','preview6.jpg',2.00),(7,'Zoe dimensity2','ahora es personal','bomnito777777.png',123.00),(8,'Zoe dimensity3','mejor  que nunca','preview8.jpg',3.00),(9,'Constanze Legends','ta chidos','preview3.jpg',3.00),(10,'desconocido','sepa',NULL,2.00),(11,'LOL','xdas','Diseno_sin_titulo_5.png',1234.00),(12,'bts','juego de bts','bts.jpg',100.00);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('admin','editor','cliente') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'cliente',
  `foto_perfil` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `banner` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin1','admin@correo.com','scrypt:32768:8:1$lDiShujSp5jhis1t$f0ae7b554669c2f5b521f946d8845262bcd3269b12b4c0688eebf0b6b4db63c2649eba864c0b49045e47a3743c457fa69ecceec0875819caa93a72ce2706cd7e','admin','preview5.jpg','SensroColor1.png','que ves wei',1),(2,'editor','editor@correo.com','scrypt:32768:8:1$leQ3Jm7aGRPLGFGp$f2a71b0ea227d3b7a6898d28cda227db47d35f6e7721c39c30b5a204239e66a464fc5e24367cc390014e96e2c7297b5f6e51f86f50bcf84b70bcb202841f36db','editor',NULL,NULL,NULL,1),(3,'cliente','cliente@correo.com','scrypt:32768:8:1$ynpKs2n4YfAkrX9K$ba5396b0d3c2d4b7f4c3c50e12b6d6ebf045ca81c88a48cc9ef0ea652f258f32d6d4f51a6dc7794d1b929a5c13e65b34a265c8afcdebfce3c35c0dfac7e32a49','cliente',NULL,NULL,NULL,1),(4,'uwu','uwu@gmail.com','scrypt:32768:8:1$wjvFwzsCtMnHMngd$831e7d136000835ab41a798e32c7d0712b022c7f91d9c3a3eba8ff4a206c0de290bcea2165719e3ecc3f807923d962b0290c83937f058432c959961196e2c70e','cliente','ChatGPT_Image_18_sept_2025_12_13_14_a.m..png',NULL,'None',1),(5,'alan','alan@gmail.com','scrypt:32768:8:1$4Zvn13yUsBLSDjlc$187638e8a6e90c137b82e0ef7b7851aa9a2aebb82327110eb452b1c6163c601c6d76c02b2c8315fe4a48471d8c1ed9a24d94fd315e92b04c5c83aa5a209d9f9c','cliente','494576951_1601470450527074_1449280648346500477_n.jpg','ChatGPT_Image_18_sept_2025_12_13_14_a.m..png','None',1),(6,'america','america@gmail.com','scrypt:32768:8:1$Wy8yFVwdygPfMYRg$a7a4ea8d7944775966495dfbd661c0858ae7bbcb3c9ba0246651652574fb9ffa1e44abcc821ceb56b8a461c231f3d43e02e2248d75ab52e6d486ae5368ddeb9a','cliente','bts.jpg','banner_bts.jpg','Hola soy nueva',1),(7,'nuevo','nuevo@gmail.com','scrypt:32768:8:1$B0wkSyBM1VDfJbN1$d66b952a58e3f65dc469df6614e5caa497b1254891eea81a6bec00ebc9617360c4789fadc6f85a059266e458a487ef8911d6e9b5338fc037cdf463992d2edf19','cliente',NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`id_usuario`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,1,19.99,'2025-11-07 05:26:44'),(2,1,24.99,'2025-11-07 05:34:54'),(3,1,14.99,'2025-11-07 05:36:40'),(4,1,2.00,'2025-11-07 07:03:26'),(5,1,2.00,'2025-11-07 07:03:31'),(6,1,9.99,'2025-11-07 18:50:57'),(10,1,777.00,'2025-11-07 20:42:05'),(11,1,29.99,'2025-11-07 20:54:22'),(12,1,3.00,'2025-11-07 21:17:44'),(13,1,3.00,'2025-11-07 21:26:10'),(14,1,50.00,'2025-11-07 21:49:14'),(15,1,2.00,'2025-11-07 22:05:56'),(16,4,11.00,'2025-11-10 03:10:17'),(17,1,1234.00,'2025-11-11 21:30:01'),(18,6,7.00,'2025-11-12 00:46:13'),(19,6,108.00,'2025-11-12 00:48:09'),(20,6,1234.00,'2025-11-12 02:51:28'),(21,7,130.00,'2025-11-12 03:53:50'),(22,5,5.00,'2025-11-12 06:41:00'),(23,5,2.00,'2025-11-12 06:50:22'),(24,5,123.00,'2025-11-12 06:51:28'),(25,5,3.00,'2025-11-12 06:58:06'),(26,5,100.00,'2025-11-12 07:00:45');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-12  1:08:03
