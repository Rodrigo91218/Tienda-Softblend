/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `pruebas_login` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `pruebas_login`;

CREATE TABLE IF NOT EXISTS `admin_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `admin_users` (`id`, `username`, `password`) VALUES
	(1, 'admin', '1234');

CREATE DATABASE IF NOT EXISTS `tienda_perfumes` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `tienda_perfumes`;

CREATE TABLE IF NOT EXISTS `cliente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `localidad` varchar(100) DEFAULT NULL,
  `domicilio` varchar(255) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `iva` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `cliente` (`id`, `nombre`, `apellido`, `localidad`, `domicilio`, `codigo_postal`, `telefono`, `email`, `iva`) VALUES
	(2, 'Rodrigo', 'de la Rosa', 'San Antonio de Padua', 'castelar 1000', '1718', '1189765678', 'pereira97rodrigo@gmail.com', NULL),
	(3, 'Horacio', 'Quiroga', 'Moron', 'Martin fierro 400', '2213', '1189765678', 'horacio_q@yahoo.com.ar', NULL),
	(4, 'Rodrigo', 'de la Rosa', 'San Antonio de Padua', 'castelar 1000', 'B1718', '1132456789', 'pereira97rodrigo@gmail.com', NULL);

CREATE TABLE IF NOT EXISTS `detalle_pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pedido_id` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  CONSTRAINT `detalle_pedidos_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `detalle_pedidos` (`id`, `pedido_id`, `cantidad`, `precio_unitario`) VALUES
	(1, 5, 2, 30000.00),
	(2, 6, 2, 30000.00);

CREATE TABLE IF NOT EXISTS `entregas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `metodo_entrega` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `entregas` (`id`, `metodo_entrega`) VALUES
	(1, 'Moto Mensajería'),
	(2, 'Por Correo'),
	(3, 'Retira por Mostrador'),
	(4, 'Por Correo (Interior)');

CREATE TABLE IF NOT EXISTS `factura` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pedido_id` int(11) DEFAULT NULL,
  `tipo_factura` varchar(50) DEFAULT 'B',
  `numero_factura` varchar(50) NOT NULL,
  `fecha` date NOT NULL,
  `cantidad` int(11) NOT NULL,
  `codigo_descripcion` varchar(255) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `precio_total` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  `iva` decimal(10,2) DEFAULT 0.21,
  `total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `factura` (`id`, `pedido_id`, `tipo_factura`, `numero_factura`, `fecha`, `cantidad`, `codigo_descripcion`, `precio_unitario`, `precio_total`, `subtotal`, `iva`, `total`) VALUES
	(1, 2, 'A', '1', '2024-11-05', 1, 'Pedido de perfumes', 5500.00, 5500.00, 5500.00, 1155.00, 6655.00),
	(2, 3, 'A', '2', '2024-11-05', 8, 'Pedido de perfumes', 44000.00, 44000.00, 44000.00, 9240.00, 53240.00),
	(3, 4, 'A', '3', '2024-11-05', 1, 'Pedido de perfumes', 5500.00, 5500.00, 5500.00, 1155.00, 6655.00);

CREATE TABLE IF NOT EXISTS `formas_pago` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `metodo_pago` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `formas_pago` (`id`, `metodo_pago`) VALUES
	(1, 'Tarjeta de Crédito'),
	(2, 'Tarjeta de Débito'),
	(3, 'Efectivo'),
	(4, 'Transferencia Bancaria');

CREATE TABLE IF NOT EXISTS `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date DEFAULT NULL,
  `numero_pedido` int(11) DEFAULT NULL,
  `direccion_envio` varchar(255) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `localidad_envio` varchar(100) DEFAULT NULL,
  `metodo_entrega` varchar(100) DEFAULT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `forma_pago_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `forma_pago_id` (`forma_pago_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON DELETE SET NULL,
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`forma_pago_id`) REFERENCES `formas_pago` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `pedidos` (`id`, `fecha`, `numero_pedido`, `direccion_envio`, `codigo_postal`, `localidad_envio`, `metodo_entrega`, `cliente_id`, `forma_pago_id`) VALUES
	(1, '2024-09-17', 1, 'santiago del estero 1014', '1718', 'merlo', NULL, NULL, NULL),
	(2, '2024-09-18', 1, 'santiago del estero 1014', '1718', 'merlo', NULL, NULL, NULL),
	(3, '2024-09-11', 4, 'santiago del estero 1014', '1718', 'merlo', NULL, NULL, NULL),
	(4, '2024-09-30', 6, 'santiago del estero 1014', '1718', 'merlo', NULL, NULL, NULL),
	(5, '2024-09-24', 7, 'santiago del estero 1014', '1718', 'merlo', 'Retira por Mostrador', NULL, NULL),
	(6, '2024-09-04', 1, '1', '1718', 'merlo', 'Moto Mensajería', NULL, NULL);

CREATE TABLE IF NOT EXISTS `perfumes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `aroma` tinytext NOT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `perfumes` (`id`, `nombre`, `aroma`, `imagen_url`, `stock`, `precio`) VALUES
	(1, 'Soft Blend Rosa chicle', 'Perfume floral suave con notas de rosa y jazmín.', 'imagen_rosa.jpg', 8, 5500.00),
	(2, 'Soft Blend Citrus extreme', 'Fragancia fresca con cítricos y toques amaderados.', 'softLimon.jpg', 4, 5500.00),
	(3, 'Soft blend Oceanica', 'Marino.', 'oceanica.jpg', 4, 5500.00),
	(6, 'Caramelo', 'Caramelo y miel.', 'caramelo.jpg', 2, 5500.00),
	(7, 'Nardo', 'Floral.', 'nardo.jpg', 5, 5500.00);

CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` tinytext NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usuarios` (`id`, `username`, `password`, `role`) VALUES
	(1, 'admin', 'pbkdf2:sha256:600000$uKAfES8vKZuF9z5x$528aef31d840711cf02a49c832967f7e253c5be164a88069535ec9908b63380b', 'admin');

CREATE TABLE `ventas_resumen` (
	`dia` DATE NULL,
	`mes` INT(3) NULL,
	`año` INT(5) NULL,
	`cantidad_ventas` BIGINT(21) NOT NULL,
	`total_ventas` DECIMAL(32,2) NULL,
	`total_iva` DECIMAL(32,2) NULL
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `ventas_resumen`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `ventas_resumen` AS SELECT 
    DATE(fecha) AS dia,
    MONTH(fecha) AS mes,
    YEAR(fecha) AS año,
    COUNT(*) AS cantidad_ventas,
    SUM(precio_total) AS total_ventas,
    SUM(iva) AS total_iva
FROM 
    factura
GROUP BY 
    dia, mes, año ;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
