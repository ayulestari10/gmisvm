-- phpMyAdmin SQL Dump
-- version 4.8.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 03, 2018 at 10:43 AM
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

--
-- Dumping data for table `file_uji`
--

INSERT INTO `file_uji` (`id_file`, `nama_file`, `jumlah_wajah`, `jumlah_bahagia`, `jumlah_sedih`, `jumlah_marah`, `jumlah_jijik`, `jumlah_kaget`, `jumlah_takut`, `jumlah_natural`) VALUES
(1, '551db76d6bb3f7dc4ef956b4-750-563.png', 7, 7, 0, 0, 0, 0, 0, 0),
(2, '1540733487283.png', 2, 1, 0, 0, 0, 0, 0, 1),
(3, 'Stock Photos Vectors Shutterstock.png', 2, 0, 0, 0, 2, 0, 0, 0),
(4, 'Serious Group Images, Stock Photos Vectors Shutterstock(4).png', 2, 0, 0, 0, 0, 0, 0, 2),
(5, 'Scared Group Images, Stock Photos Vectors Shutterstock(3).png', 2, 0, 0, 0, 0, 0, 2, 0),
(6, 'Shocked Group Images, Stock Photos Vectors Shutterstock(2).png', 2, 0, 0, 0, 0, 2, 0, 0),
(7, 'Angry Group Images, Stock Photos Vectors Shutterstock(15).png', 4, 0, 0, 4, 0, 0, 0, 0),
(9, 'Angry Group Images, Stock Photos Vectors Shutterstock(3).png', 2, 0, 0, 2, 0, 0, 0, 0),
(10, 'Similar Images, Stock Photos Vectors of Five Sad Women Team Portrait - 33174448 Shutterstock(2).png', 3, 3, 0, 0, 0, 0, 0, 0),
(11, 'Five sad women team portrait.png', 3, 3, 0, 0, 0, 0, 0, 0),
(12, 'Serious Group Images, Stock Photos Vectors Shutterstock.png', 4, 0, 0, 0, 0, 0, 0, 4),
(13, 'Serious Group Images, Stock Photos Vectors Shutterstock(6).png', 7, 0, 0, 0, 0, 0, 0, 7),
(14, 'Serious Group Images, Stock Photos Vectors Shutterstock(5).png', 6, 0, 0, 0, 0, 0, 0, 6),
(15, 'Serious Group Images, Stock Photos Vectors Shutterstock(3).png', 4, 0, 0, 0, 0, 0, 0, 4),
(16, 'Serious Group Images, Stock Photos Vectors Shutterstock(2).png', 7, 0, 0, 0, 0, 0, 0, 7),
(17, 'Serious Group Images, Stock Photos Vectors Shutterstock(1).png', 5, 0, 0, 0, 0, 0, 0, 5),
(18, 'Serious Group Images, Stock Photos Vectors Shutterstock (2).png', 6, 0, 0, 0, 0, 0, 0, 6),
(19, 'Scared Group Images, Stock Photos Vectors Shutterstock.png', 4, 1, 0, 0, 0, 1, 2, 0),
(20, 'Scared Group Images, Stock Photos Vectors Shutterstock(6).png', 2, 0, 0, 0, 0, 0, 2, 0),
(21, 'Scared Group Images, Stock Photos Vectors Shutterstock(7).png', 2, 0, 0, 0, 0, 0, 2, 0),
(22, 'Scared Group Images, Stock Photos Vectors Shutterstock(5).png', 3, 0, 0, 0, 0, 1, 0, 2),
(23, 'Scared Group Images, Stock Photos Vectors Shutterstock(4).png', 3, 0, 0, 0, 0, 2, 1, 0),
(24, 'Scared Group Images, Stock Photos Vectors Shutterstock(2).png', 3, 0, 0, 0, 0, 0, 3, 0),
(25, 'Shocked Group Images, Stock Photos Vectors Shutterstock(11).png', 4, 0, 0, 0, 0, 4, 0, 0),
(26, 'Shocked Group Images, Stock Photos Vectors Shutterstock(10).png', 2, 0, 0, 0, 0, 2, 0, 0),
(27, 'Shocked Group Images, Stock Photos Vectors Shutterstock(9).png', 4, 0, 0, 0, 0, 4, 0, 0),
(28, 'Shocked Group Images, Stock Photos Vectors Shutterstock(8).png', 4, 0, 0, 0, 0, 4, 0, 0),
(29, 'Shocked Group Images, Stock Photos Vectors Shutterstock(7).png', 4, 0, 0, 0, 0, 4, 0, 0),
(30, 'Scared Group Images, Stock Photos Vectors Shutterstock (2).png', 3, 0, 0, 0, 0, 0, 3, 0),
(32, 'Shocked Group Images, Stock Photos Vectors Shutterstock(6).png', 4, 0, 0, 0, 0, 4, 0, 0),
(33, 'Shocked Group Images, Stock Photos Vectors Shutterstock(5).png', 4, 0, 0, 0, 0, 4, 0, 0),
(34, 'Shocked Group Images, Stock Photos Vectors Shutterstock(4).png', 4, 0, 0, 0, 0, 4, 0, 0),
(35, 'Shocked Group Images, Stock Photos Vectors Shutterstock(3).png', 2, 0, 0, 0, 0, 2, 0, 0),
(36, 'Shocked Group Images, Stock Photos Vectors Shutterstock.png', 2, 0, 0, 0, 0, 2, 0, 0),
(37, 'Shocked Group Images, Stock Photos Vectors Shutterstock(1).png', 4, 0, 0, 0, 0, 4, 0, 0),
(38, 'Angry Group Images, Stock Photos Vectors Shutterstock(13).png', 3, 0, 0, 3, 0, 0, 0, 0),
(39, 'Angry Group Images, Stock Photos Vectors Shutterstock(12).png', 2, 0, 0, 2, 0, 0, 0, 0),
(40, 'Angry Group Images, Stock Photos Vectors Shutterstock(10).png', 2, 0, 0, 2, 0, 0, 0, 0),
(41, 'Angry Group Images, Stock Photos Vectors Shutterstock(11).png', 2, 0, 0, 2, 0, 0, 0, 0),
(42, 'Angry Group Images, Stock Photos Vectors Shutterstock(9).png', 2, 0, 0, 2, 0, 0, 0, 0),
(43, 'Angry Group Images, Stock Photos Vectors Shutterstock(8).png', 3, 0, 0, 3, 0, 0, 0, 0),
(44, 'Angry Group Images, Stock Photos Vectors Shutterstock(7).png', 3, 0, 0, 3, 0, 0, 0, 0),
(45, 'Angry Group Images, Stock Photos Vectors Shutterstock(6).png', 2, 0, 0, 2, 0, 0, 0, 0),
(46, 'Angry Group Images, Stock Photos Vectors Shutterstock(5).png', 3, 0, 0, 3, 0, 0, 0, 0),
(47, 'Similar Images, Stock Photos Vectors of Front View Two Angry Businesspeople Using - 397094602 Shutter[...].png', 2, 0, 0, 2, 0, 0, 0, 0),
(48, 'Angry Group Images, Stock Photos Vectors Shutterstock(2).png', 5, 0, 0, 5, 0, 0, 0, 0),
(49, 'Sadness Group Images, Stock Photos Vectors Shutterstock(14).png', 3, 0, 3, 0, 0, 0, 0, 0),
(50, 'Angry Group Images, Stock Photos Vectors Shutterstock(1).png', 5, 1, 0, 4, 0, 0, 0, 0),
(51, 'Similar Images, Stock Photos Vectors of Five Sad Women Team Portrait - 33174448 Shutterstock.png', 5, 5, 0, 0, 0, 0, 0, 0),
(52, 'Similar Images, Stock Photos Vectors of Five Sad Women Team Portrait - 33174448 Shutterstock(1).png', 5, 5, 0, 0, 0, 0, 0, 0),
(53, 'Sadness Group Images, Stock Photos Vectors Shutterstock(6).png', 4, 0, 4, 0, 0, 0, 0, 0),
(54, 'Sadness Group Images, Stock Photos Vectors Shutterstock.png', 3, 0, 3, 0, 0, 0, 0, 0),
(55, 'Sadness Group Images, Stock Photos Vectors Shutterstock(1).png', 4, 0, 4, 0, 0, 0, 0, 0),
(56, 'Sadness Group Images, Stock Photos Vectors Shutterstock(2).png', 4, 0, 4, 0, 0, 0, 0, 0),
(57, 'Disgusted Images, Stock Photos Vectors Shutterstock (2).png', 3, 0, 0, 0, 3, 0, 0, 0),
(58, 'Sadness Group Images, Stock Photos Vectors Shutterstock(5).png', 4, 0, 4, 0, 0, 0, 0, 0),
(59, 'Sadness Group Images, Stock Photos Vectors Shutterstock(4).png', 3, 0, 3, 0, 0, 0, 0, 0),
(60, 'Sadness Group Images, Stock Photos Vectors Shutterstock(3).png', 2, 0, 2, 0, 0, 0, 0, 0),
(61, 'Sadness Group Images, Stock Photos Vectors Shutterstock (2).png', 5, 0, 5, 0, 0, 0, 0, 0),
(62, 'Disgusted Images, Stock Photos Vectors Shutterstock(7).png', 3, 0, 0, 0, 3, 0, 0, 0),
(63, 'Disgusted Images, Stock Photos Vectors Shutterstock(1).png', 3, 0, 0, 0, 3, 0, 0, 0),
(64, 'Disgusted Images, Stock Photos Vectors Shutterstock(4).png', 3, 0, 0, 0, 3, 0, 0, 0),
(65, 'Sadness Group Images, Stock Photos Vectors Shutterstock(13).png', 3, 0, 3, 0, 0, 0, 0, 0),
(66, 'Sadness Group Images, Stock Photos Vectors Shutterstock(12).png', 3, 0, 3, 0, 0, 0, 0, 0),
(67, 'Angry Group Images, Stock Photos Vectors Shutterstock.png', 3, 0, 0, 3, 0, 0, 0, 0),
(68, 'Sadness Group Images, Stock Photos Vectors Shutterstock(11).png', 3, 0, 3, 0, 0, 0, 0, 0),
(69, 'Similar Images, Stock Photos Vectors of Sad Serious Five Business People Standing - 69947545 Shutters[...](3).png', 5, 0, 0, 0, 0, 0, 0, 5),
(70, 'Similar Images, Stock Photos Vectors of Sad Serious Five Business People Standing - 69947545 Shutters[...].png', 3, 3, 0, 0, 0, 0, 0, 0),
(71, 'Similar Images, Stock Photos Vectors of Sad Serious Five Business People Standing - 69947545 Shutters[...](1).png', 4, 4, 0, 0, 0, 0, 0, 0),
(72, 'Sad serious five business people standing in a row and looking at camera isolated on white background.png', 5, 5, 0, 0, 0, 0, 0, 0),
(73, 'Sadness Group Images, Stock Photos Vectors Shutterstock(7).png', 5, 0, 5, 0, 0, 0, 0, 0),
(74, 'Angry Group Images, Stock Photos Vectors Shutterstock (2).png', 3, 0, 0, 3, 0, 0, 0, 0),
(75, 'Angry Group Images, Stock Photos Vectors Shutterstock(4).png', 3, 0, 0, 3, 0, 0, 0, 0),
(76, 'Angry Group Images, Stock Photos Vectors Shutterstock(14).png', 3, 0, 0, 3, 0, 0, 0, 0),
(77, 'Similar Images, Stock Photos Vectors of Two Girls Looking Each Other Angry - 161941682 Shutterstock.png', 2, 0, 0, 2, 0, 0, 0, 0),
(78, 'Similar Images, Stock Photos Vectors of Two Girls Looking Each Other Angry - 161941682 Shutterstock(3).png', 2, 0, 0, 0, 0, 0, 0, 2),
(79, 'Angry Group Images, Stock Photos Vectors Shutterstock(4).png', 3, 0, 0, 3, 0, 0, 0, 0),
(80, 'Angry Group Images, Stock Photos Vectors Shutterstock (2).png', 3, 0, 0, 3, 0, 0, 0, 0),
(81, 'Similar Images, Stock Photos Vectors of Two Girls Looking Each Other Angry - 161941682 Shutterstock(2).png', 2, 0, 0, 0, 0, 0, 0, 2),
(82, 'Similar Images, Stock Photos Vectors of Two Girls Looking Each Other Angry - 161941682 Shutterstock(1).png', 2, 0, 2, 0, 0, 0, 0, 0),
(83, 'Similar Images, Stock Photos Vectors of Composition Angry People Faces - 514840840 Shutterstock.png', 4, 0, 0, 0, 0, 4, 0, 0),
(84, 'Similar Images, Stock Photos Vectors of Composition Angry People Faces - 514840840 Shutterstock(1).png', 3, 3, 0, 0, 0, 0, 0, 0),
(85, 'Angry Group Images, Stock Photos Vectors Shutterstock(16).png', 2, 0, 0, 2, 0, 0, 0, 0),
(86, 'Angry Group Images, Stock Photos Vectors Shutterstock(17).png', 2, 0, 0, 0, 0, 0, 2, 0),
(87, 'Angry Group Images, Stock Photos Vectors Shutterstock(18).png', 2, 0, 0, 0, 0, 0, 2, 0),
(88, 'Angry Group Images, Stock Photos Vectors Shutterstock(19).png', 2, 0, 0, 0, 2, 0, 0, 0),
(89, 'Angry Group Images, Stock Photos Vectors Shutterstock(20).png', 2, 0, 0, 0, 2, 0, 0, 0),
(90, 'Angry Group Images, Stock Photos Vectors Shutterstock(21).png', 2, 0, 0, 2, 0, 0, 0, 0),
(91, 'Sadness Group Images, Stock Photos Vectors Shutterstock (3).png', 2, 0, 1, 1, 0, 0, 0, 0),
(92, 'Sadness Group Images, Stock Photos Vectors Shutterstock(8).png', 3, 0, 3, 0, 0, 0, 0, 0),
(93, 'Sadness Group Images, Stock Photos Vectors Shutterstock(9).png', 2, 0, 2, 0, 0, 0, 0, 0),
(94, 'Sadness Group Images, Stock Photos Vectors Shutterstock(10).png', 2, 0, 2, 0, 0, 0, 0, 0),
(95, 'Sadness Group Images, Stock Photos Vectors Shutterstock(15).png', 2, 0, 2, 0, 0, 0, 0, 0),
(96, 'Sadness Group Images, Stock Photos Vectors Shutterstock(16).png', 2, 0, 2, 0, 0, 0, 0, 0),
(97, 'Disgusted Group Images, Stock Photos Vectors Shutterstock.png', 2, 0, 0, 0, 2, 0, 0, 0),
(98, 'Disgusted Group Images, Stock Photos Vectors Shutterstock(1).png', 2, 0, 0, 0, 2, 0, 0, 0),
(99, 'Disgusted Group Images, Stock Photos Vectors Shutterstock(2).png', 3, 0, 0, 0, 3, 0, 0, 0),
(100, 'Happy Group Images, Stock Photos Vectors Shutterstock.png', 6, 6, 0, 0, 0, 0, 0, 0),
(101, 'Happy Group Images, Stock Photos Vectors Shutterstock(1).png', 4, 4, 0, 0, 0, 0, 0, 0),
(103, 'Happy Group Images, Stock Photos Vectors Shutterstock(3).png', 4, 4, 0, 0, 0, 0, 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `file_uji`
--
ALTER TABLE `file_uji`
  ADD PRIMARY KEY (`id_file`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `file_uji`
--
ALTER TABLE `file_uji`
  MODIFY `id_file` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=104;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
