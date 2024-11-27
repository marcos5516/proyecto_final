-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 27-11-2024 a las 01:54:32
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `SistemaControlEscolar`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Alumnos`
--

CREATE TABLE `Alumnos` (
  `id_alumno` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `fecha_nac` date DEFAULT NULL,
  `id_carrera` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Alumnos`
--

INSERT INTO `Alumnos` (`id_alumno`, `id_usuario`, `estado`, `fecha_nac`, `id_carrera`) VALUES
(1, 3, 'Activo', '2000-01-15', 1),
(2, 4, 'Activo', '1999-09-01', 2),
(3, 5, 'Activo', '2001-02-23', 3),
(4, 11, 'Activo', '1987-06-24', 4),
(6, 7, 'Activo', NULL, NULL),
(7, 9, 'Activo', '2002-09-09', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Alumno_Grupo`
--

CREATE TABLE `Alumno_Grupo` (
  `id_alumno` int(11) NOT NULL,
  `id_grupo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Alumno_Materia`
--

CREATE TABLE `Alumno_Materia` (
  `id` int(11) NOT NULL,
  `id_alumno` int(11) DEFAULT NULL,
  `id_materia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Alumno_Materia`
--

INSERT INTO `Alumno_Materia` (`id`, `id_alumno`, `id_materia`) VALUES
(3, 1, 1),
(4, 1, 1),
(5, 1, 2),
(6, 1, 1),
(25, 7, 1);

--
-- Disparadores `Alumno_Materia`
--
DELIMITER $$
CREATE TRIGGER `after_insert_alumno_materia` AFTER INSERT ON `Alumno_Materia` FOR EACH ROW BEGIN
    DECLARE cupos_restantes INT;

    -- Obtener los cupos restantes de la materia
    SELECT cupos_disponibles INTO cupos_restantes
    FROM Materias
    WHERE id_materia = NEW.id_materia;

    -- Si los cupos restantes son 0, crear un nuevo grupo
    IF cupos_restantes = 0 THEN
        INSERT INTO Grupos (nombre_grupo, fecha, carrera, materia, salon, horario, semestre, max_alumnos, maestro)
        SELECT CONCAT('Grupo de ', nombre_materia), CURDATE(), id_carrera, id_materia, 'Aula 101', '08:00-10:00', semestre, 30, 1
        FROM Materias
        WHERE id_materia = NEW.id_materia;

        -- Reiniciar el contador de cupos
        UPDATE Materias
        SET cupos_disponibles = cupo_maximo
        WHERE id_materia = NEW.id_materia;
    ELSE
        -- Actualizar los cupos de la materia
        UPDATE Materias
        SET cupos_disponibles = cupos_disponibles - 1
        WHERE id_materia = NEW.id_materia;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Carreras`
--

CREATE TABLE `Carreras` (
  `id_carrera` int(11) NOT NULL,
  `nombre_carrera` varchar(100) NOT NULL,
  `semestres` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Carreras`
--

INSERT INTO `Carreras` (`id_carrera`, `nombre_carrera`, `semestres`) VALUES
(1, 'Ingeniería en Computación', 9),
(2, 'Ingeniería Civil', 9),
(3, 'Medicina', 12),
(4, 'Derecho', 7),
(5, 'Mercadotecnia', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Grupos`
--

CREATE TABLE `Grupos` (
  `id_grupo` int(11) NOT NULL,
  `nombre_grupo` varchar(100) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `carrera` int(11) DEFAULT NULL,
  `materia` int(11) DEFAULT NULL,
  `salon` varchar(50) DEFAULT NULL,
  `horario` varchar(50) DEFAULT NULL,
  `semestre` varchar(10) DEFAULT NULL,
  `max_alumnos` int(11) DEFAULT NULL,
  `maestro` int(11) DEFAULT NULL,
  `alumnos_inscritos` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Horarios`
--

CREATE TABLE `Horarios` (
  `id_horario` int(11) NOT NULL,
  `turno` varchar(20) DEFAULT NULL,
  `hora` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Maestros`
--

CREATE TABLE `Maestros` (
  `id_maestro` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_carrera` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Maestros`
--

INSERT INTO `Maestros` (`id_maestro`, `id_usuario`, `id_carrera`) VALUES
(1, 12, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Maestro_Materia`
--

CREATE TABLE `Maestro_Materia` (
  `id_maestro` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Materias`
--

CREATE TABLE `Materias` (
  `id_materia` int(11) NOT NULL,
  `nombre_materia` varchar(100) NOT NULL,
  `id_carrera` int(11) DEFAULT NULL,
  `creditos` int(11) DEFAULT NULL,
  `semestre` varchar(10) DEFAULT NULL,
  `cupo_maximo` int(11) NOT NULL DEFAULT 30,
  `cupos_disponibles` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Materias`
--

INSERT INTO `Materias` (`id_materia`, `nombre_materia`, `id_carrera`, `creditos`, `semestre`, `cupo_maximo`, `cupos_disponibles`) VALUES
(1, 'Matematicas', 1, 8, '1', 3, 0),
(2, 'Programación básica', 1, 8, '1', 3, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Salones`
--

CREATE TABLE `Salones` (
  `id_salon` int(11) NOT NULL,
  `nombre_salon` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Salones`
--

INSERT INTO `Salones` (`id_salon`, `nombre_salon`) VALUES
(1, 'Aula 101'),
(2, 'Laboratorio A'),
(3, 'Aula 202');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuarios`
--

CREATE TABLE `Usuarios` (
  `id_usuario` int(11) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contraseña` varchar(100) NOT NULL,
  `perfil` enum('Administrador','Maestro','Alumno') NOT NULL,
  `nombre_usuario` varchar(50) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido_paterno` varchar(50) DEFAULT NULL,
  `apellido_materno` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Usuarios`
--

INSERT INTO `Usuarios` (`id_usuario`, `correo`, `contraseña`, `perfil`, `nombre_usuario`, `nombre`, `apellido_paterno`, `apellido_materno`) VALUES
(1, 'alan@alumnos.com', '123', 'Administrador', 'alan', 'Alan', 'Lara', 'Lara'),
(3, 'Leo@alumnos.com', '123', 'Alumno', 'Leo', 'Leonardo', 'Palacios', 'Palacios'),
(4, 'luis@alumnos.com', '123', 'Alumno', 'luis', 'Luis', 'Solano', 'Luna'),
(5, 'Javier@alumnos.com', '123', 'Alumno', 'Javier', 'Javier', 'Lopez', 'Sanchez'),
(7, 'Prueba@alumnos.com', '123', 'Alumno', 'Prueba', 'Prueba', 'Prueba', 'Prueba'),
(9, 'Lisa@alumnos.com', '123', 'Alumno', 'Lisa', 'Lisa', 'Cruz', 'Torres'),
(11, 'messi@alumnos.com', '123', 'Alumno', 'messi', 'Lionel', 'Messi', 'Cuccitini'),
(12, 'Alam@alumnos.com', '123', 'Maestro', 'Alam', 'Alam', 'Padilla', 'Gonzalez');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Alumnos`
--
ALTER TABLE `Alumnos`
  ADD PRIMARY KEY (`id_alumno`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_carrera` (`id_carrera`);

--
-- Indices de la tabla `Alumno_Grupo`
--
ALTER TABLE `Alumno_Grupo`
  ADD PRIMARY KEY (`id_alumno`,`id_grupo`),
  ADD KEY `id_grupo` (`id_grupo`);

--
-- Indices de la tabla `Alumno_Materia`
--
ALTER TABLE `Alumno_Materia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_alumno` (`id_alumno`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `Carreras`
--
ALTER TABLE `Carreras`
  ADD PRIMARY KEY (`id_carrera`);

--
-- Indices de la tabla `Grupos`
--
ALTER TABLE `Grupos`
  ADD PRIMARY KEY (`id_grupo`),
  ADD KEY `carrera` (`carrera`),
  ADD KEY `materia` (`materia`),
  ADD KEY `maestro` (`maestro`);

--
-- Indices de la tabla `Horarios`
--
ALTER TABLE `Horarios`
  ADD PRIMARY KEY (`id_horario`);

--
-- Indices de la tabla `Maestros`
--
ALTER TABLE `Maestros`
  ADD PRIMARY KEY (`id_maestro`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_carrera` (`id_carrera`);

--
-- Indices de la tabla `Maestro_Materia`
--
ALTER TABLE `Maestro_Materia`
  ADD PRIMARY KEY (`id_maestro`,`id_materia`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `Materias`
--
ALTER TABLE `Materias`
  ADD PRIMARY KEY (`id_materia`),
  ADD KEY `id_carrera` (`id_carrera`);

--
-- Indices de la tabla `Salones`
--
ALTER TABLE `Salones`
  ADD PRIMARY KEY (`id_salon`);

--
-- Indices de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Alumnos`
--
ALTER TABLE `Alumnos`
  MODIFY `id_alumno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `Alumno_Materia`
--
ALTER TABLE `Alumno_Materia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `Carreras`
--
ALTER TABLE `Carreras`
  MODIFY `id_carrera` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `Grupos`
--
ALTER TABLE `Grupos`
  MODIFY `id_grupo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `Horarios`
--
ALTER TABLE `Horarios`
  MODIFY `id_horario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `Maestros`
--
ALTER TABLE `Maestros`
  MODIFY `id_maestro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `Salones`
--
ALTER TABLE `Salones`
  MODIFY `id_salon` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Alumnos`
--
ALTER TABLE `Alumnos`
  ADD CONSTRAINT `alumnos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `alumnos_ibfk_2` FOREIGN KEY (`id_carrera`) REFERENCES `Carreras` (`id_carrera`) ON DELETE SET NULL;

--
-- Filtros para la tabla `Alumno_Grupo`
--
ALTER TABLE `Alumno_Grupo`
  ADD CONSTRAINT `alumno_grupo_ibfk_1` FOREIGN KEY (`id_alumno`) REFERENCES `Alumnos` (`id_alumno`),
  ADD CONSTRAINT `alumno_grupo_ibfk_2` FOREIGN KEY (`id_grupo`) REFERENCES `Grupos` (`id_grupo`);

--
-- Filtros para la tabla `Alumno_Materia`
--
ALTER TABLE `Alumno_Materia`
  ADD CONSTRAINT `alumno_materia_ibfk_1` FOREIGN KEY (`id_alumno`) REFERENCES `Alumnos` (`id_alumno`),
  ADD CONSTRAINT `alumno_materia_ibfk_2` FOREIGN KEY (`id_materia`) REFERENCES `Materias` (`id_materia`);

--
-- Filtros para la tabla `Grupos`
--
ALTER TABLE `Grupos`
  ADD CONSTRAINT `grupos_ibfk_1` FOREIGN KEY (`carrera`) REFERENCES `Carreras` (`id_carrera`),
  ADD CONSTRAINT `grupos_ibfk_2` FOREIGN KEY (`materia`) REFERENCES `Materias` (`id_materia`),
  ADD CONSTRAINT `grupos_ibfk_3` FOREIGN KEY (`maestro`) REFERENCES `Maestros` (`id_maestro`);

--
-- Filtros para la tabla `Maestros`
--
ALTER TABLE `Maestros`
  ADD CONSTRAINT `maestros_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `maestros_ibfk_2` FOREIGN KEY (`id_carrera`) REFERENCES `Carreras` (`id_carrera`) ON DELETE SET NULL;

--
-- Filtros para la tabla `Maestro_Materia`
--
ALTER TABLE `Maestro_Materia`
  ADD CONSTRAINT `maestro_materia_ibfk_1` FOREIGN KEY (`id_maestro`) REFERENCES `Maestros` (`id_maestro`),
  ADD CONSTRAINT `maestro_materia_ibfk_2` FOREIGN KEY (`id_materia`) REFERENCES `Materias` (`id_materia`);

--
-- Filtros para la tabla `Materias`
--
ALTER TABLE `Materias`
  ADD CONSTRAINT `materias_ibfk_1` FOREIGN KEY (`id_carrera`) REFERENCES `Carreras` (`id_carrera`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
