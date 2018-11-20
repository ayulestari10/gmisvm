-- phpMyAdmin SQL Dump
-- version 4.8.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 19, 2018 at 01:20 PM
-- Server version: 10.1.33-MariaDB
-- PHP Version: 7.2.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gmisvm`
--

-- --------------------------------------------------------

--
-- Table structure for table `ciri_pelatihan`
--

CREATE TABLE `ciri_pelatihan` (
  `id_ciri_pelatihan` int(11) NOT NULL,
  `ket` enum('O','S') NOT NULL,
  `kelas` varchar(11) NOT NULL,
  `ciri1` double NOT NULL,
  `ciri2` double NOT NULL,
  `ciri3` double NOT NULL,
  `ciri4` double NOT NULL,
  `ciri5` double NOT NULL,
  `ciri6` double NOT NULL,
  `ciri7` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ciri_pengujian`
--

CREATE TABLE `ciri_pengujian` (
  `id_ciri_pengujian` int(11) NOT NULL,
  `ket` enum('O','S') NOT NULL,
  `ciri1` double NOT NULL,
  `ciri2` double NOT NULL,
  `ciri3` double NOT NULL,
  `ciri4` double NOT NULL,
  `ciri5` double NOT NULL,
  `ciri6` double NOT NULL,
  `ciri7` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `file_uji`
--

CREATE TABLE `file_uji` (
  `id_file` int(11) NOT NULL,
  `nama_file` varchar(225) NOT NULL,
  `jumlah_wajah` int(4) NOT NULL,
  `jumlah_bahagia` int(4) NOT NULL,
  `jumlah_sedih` int(4) NOT NULL,
  `jumlah_marah` int(4) NOT NULL,
  `jumlah_jijik` int(4) NOT NULL,
  `jumlah_kaget` int(4) NOT NULL,
  `jumlah_takut` int(4) NOT NULL,
  `jumlah_natural` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `hasil`
--

CREATE TABLE `hasil` (
  `id_hasil` int(11) NOT NULL,
  `id_file` int(11) DEFAULT NULL,
  `ket` enum('O','S') NOT NULL,
  `jumlah_wajah_terdeteksi` int(4) NOT NULL,
  `klasifikasi_bahagia` int(4) DEFAULT NULL,
  `klasifikasi_sedih` int(4) DEFAULT NULL,
  `klasifikasi_marah` int(4) DEFAULT NULL,
  `klasifikasi_jijik` int(4) DEFAULT NULL,
  `klasifikasi_kaget` int(4) DEFAULT NULL,
  `klasifikasi_takut` int(4) DEFAULT NULL,
  `klasifikasi_natural` int(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `pengujian`
--

CREATE TABLE `pengujian` (
  `id_pengujian` int(11) NOT NULL,
  `id_file` int(11) NOT NULL,
  `id_ciri_pengujian_s` int(11) DEFAULT NULL,
  `id_ciri_pengujian_o` int(11) DEFAULT NULL,
  `hasil_opencv` varchar(225) DEFAULT NULL,
  `hasil_sendiri` varchar(225) DEFAULT NULL,
  `direktori` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ciri_pelatihan`
--
ALTER TABLE `ciri_pelatihan`
  ADD PRIMARY KEY (`id_ciri_pelatihan`);

--
-- Indexes for table `ciri_pengujian`
--
ALTER TABLE `ciri_pengujian`
  ADD PRIMARY KEY (`id_ciri_pengujian`);

--
-- Indexes for table `file_uji`
--
ALTER TABLE `file_uji`
  ADD PRIMARY KEY (`id_file`);

--
-- Indexes for table `hasil`
--
ALTER TABLE `hasil`
  ADD PRIMARY KEY (`id_hasil`),
  ADD KEY `nama_file` (`id_file`),
  ADD KEY `id_file` (`id_file`);

--
-- Indexes for table `pengujian`
--
ALTER TABLE `pengujian`
  ADD PRIMARY KEY (`id_pengujian`),
  ADD KEY `id_ciri_pengujian` (`id_ciri_pengujian_s`),
  ADD KEY `id_ciri_pengujian_o` (`id_ciri_pengujian_o`),
  ADD KEY `id_file` (`id_file`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ciri_pelatihan`
--
ALTER TABLE `ciri_pelatihan`
  MODIFY `id_ciri_pelatihan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ciri_pengujian`
--
ALTER TABLE `ciri_pengujian`
  MODIFY `id_ciri_pengujian` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `file_uji`
--
ALTER TABLE `file_uji`
  MODIFY `id_file` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `hasil`
--
ALTER TABLE `hasil`
  MODIFY `id_hasil` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pengujian`
--
ALTER TABLE `pengujian`
  MODIFY `id_pengujian` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pengujian`
--
ALTER TABLE `pengujian`
  ADD CONSTRAINT `id_ciri_o` FOREIGN KEY (`id_ciri_pengujian_o`) REFERENCES `ciri_pengujian` (`id_ciri_pengujian`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `id_ciri_s` FOREIGN KEY (`id_ciri_pengujian_s`) REFERENCES `ciri_pengujian` (`id_ciri_pengujian`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `id_file` FOREIGN KEY (`id_file`) REFERENCES `file_uji` (`id_file`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
