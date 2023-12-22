USE juhavdph_snowdog;

CREATE TABLE `location_history` (
  `id` int(11) NOT NULL,
  `lat` decimal(10,7) NOT NULL,
  `lon` decimal(10,7) NOT NULL,
  `alt` decimal(10,2) NOT NULL,
  `speed` decimal(10,2) NOT NULL,
  `ts` timestamp NOT NULL DEFAULT current_timestamp(),
  `in_area` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

INSERT INTO `location_history` (`id`, `lat`, `lon`, `alt`, `speed`, `ts`, `in_area`) VALUES
(17, 62.8059060, 22.9163710, 39.90, 0.00, '2023-12-21 16:02:24', 'Kertunlaakso'),
(16, 62.8059050, 22.9163700, 40.10, 0.00, '2023-12-21 15:59:24', 'Kertunlaakso'),
(15, 62.8059225, 22.9163893, 44.20, 0.00, '2023-12-21 15:55:47', 'Kertunlaakso'),
(14, 62.8059225, 22.9163893, 44.20, 0.00, '2023-12-21 09:55:47', 'Kertunlaakso'),
(13, 62.8059225, 22.9163893, 44.20, 0.00, '2023-12-21 09:55:47', 'Kertunlaakso'),
(7, 62.8059170, 22.9163570, 42.70, 0.00, '2023-12-21 13:44:20', 'Kertunlaakso'),
(12, 62.8059050, 22.9163820, 40.20, 0.00, '2023-12-21 13:56:23', 'Kertunlaakso'),
(9, 62.8059160, 22.9163550, 42.70, 0.00, '2023-12-21 13:47:20', 'Kertunlaakso'),
(10, 62.8059170, 22.9163560, 42.60, 0.00, '2023-12-21 13:50:21', 'Kertunlaakso'),
(11, 62.8059160, 22.9163930, 37.90, 0.00, '2023-12-21 13:53:22', 'Kertunlaakso'),
(18, 62.8059290, 22.9163640, 36.50, 0.00, '2023-12-21 16:05:25', 'Kertunlaakso'),
(19, 62.8059280, 22.9163670, 36.30, 0.00, '2023-12-21 16:08:25', 'Kertunlaakso'),
(20, 62.8058800, 22.9163450, 39.60, 0.00, '2023-12-21 16:10:26', 'Kertunlaakso'),
(21, 62.8058860, 22.9163510, 39.00, 0.00, '2023-12-21 16:13:26', 'Kertunlaakso'),
(22, 62.8058860, 22.9163580, 37.20, 0.00, '2023-12-21 16:16:27', 'Kertunlaakso'),
(23, 62.8058860, 22.9163540, 37.40, 0.00, '2023-12-21 16:19:28', 'Kertunlaakso'),
(24, 62.8058860, 22.9163520, 37.60, 0.00, '2023-12-21 16:22:28', 'Kertunlaakso'),
(25, 62.8058860, 22.9163550, 37.50, 0.00, '2023-12-21 16:25:29', 'Kertunlaakso'),
(26, 62.8059090, 22.9163450, 32.20, 0.00, '2023-12-21 16:32:20', 'Kertunlaakso'),
(27, 62.8059080, 22.9163490, 32.40, 0.00, '2023-12-21 16:35:21', 'Kertunlaakso'),
(28, 62.8059080, 22.9163540, 32.20, 0.00, '2023-12-21 16:39:34', 'Kertunlaakso'),
(29, 62.8059225, 22.9163893, 44.20, 0.00, '2023-12-19 10:59:01', 'Frami'),
(30, 62.8059080, 22.9163570, 32.20, 0.00, '2023-12-21 16:42:35', 'Kertunlaakso'),
(31, 62.8059080, 22.9163610, 32.00, 0.00, '2023-12-21 16:45:36', 'Kertunlaakso'),
(32, 62.8059080, 22.9163620, 32.10, 0.00, '2023-12-21 16:48:36', 'Kertunlaakso'),
(33, 62.8059150, 22.9163960, 33.40, 0.00, '2023-12-21 16:51:37', 'Kertunlaakso'),
(34, 62.8059150, 22.9163980, 33.90, 0.00, '2023-12-21 16:54:38', 'Kertunlaakso'),
(35, 62.8059500, 22.9163830, 39.50, 0.00, '2023-12-21 16:57:39', 'Kertunlaakso'),
(36, 62.8059320, 22.9163710, 39.50, 0.00, '2023-12-21 17:00:39', 'Kertunlaakso'),
(37, 62.8059270, 22.9163550, 33.90, 0.00, '2023-12-21 17:03:40', 'Kertunlaakso'),
(38, 62.8059030, 22.9163810, 34.70, 0.00, '2023-12-21 17:06:41', 'Kertunlaakso'),
(39, 62.8059050, 22.9163870, 34.60, 0.00, '2023-12-21 17:09:51', 'Kertunlaakso'),
(40, 62.8059080, 22.9163620, 33.80, 0.00, '2023-12-21 17:12:52', 'Kertunlaakso'),
(41, 62.8059110, 22.9163570, 33.30, 0.00, '2023-12-21 17:15:53', 'Kertunlaakso'),
(42, 62.8059140, 22.9163550, 33.80, 0.00, '2023-12-21 17:18:54', 'Kertunlaakso'),
(43, 62.8059150, 22.9163540, 33.90, 0.00, '2023-12-21 17:21:54', 'Kertunlaakso'),
(44, 62.8059150, 22.9163540, 34.40, 0.00, '2023-12-21 17:24:55', 'Kertunlaakso'),
(45, 62.8059160, 22.9163550, 34.90, 0.00, '2023-12-21 17:28:06', 'Kertunlaakso'),
(46, 62.8059160, 22.9163540, 35.10, 0.00, '2023-12-21 17:31:06', 'Kertunlaakso'),
(47, 62.8059090, 22.9163510, 36.20, 0.00, '2023-12-21 17:34:07', 'Kertunlaakso'),
(48, 62.8059020, 22.9163490, 36.30, 0.00, '2023-12-21 17:37:07', 'Kertunlaakso'),
(49, 62.8058950, 22.9163540, 37.10, 0.00, '2023-12-21 17:40:08', 'Kertunlaakso'),
(50, 62.8058950, 22.9163530, 37.10, 0.00, '2023-12-21 17:43:08', 'Kertunlaakso'),
(51, 62.8059130, 22.9163180, 39.30, 0.00, '2023-12-21 17:46:09', 'Kertunlaakso'),
(52, 62.8059130, 22.9163210, 39.20, 0.00, '2023-12-21 17:49:09', 'Kertunlaakso'),
(53, 62.8059110, 22.9163190, 39.10, 0.00, '2023-12-21 17:52:10', 'Kertunlaakso'),
(54, 62.8059110, 22.9163200, 39.00, 0.00, '2023-12-21 17:55:11', 'Kertunlaakso'),
(55, 62.8059110, 22.9163190, 38.90, 0.00, '2023-12-21 17:58:11', 'Kertunlaakso'),
(56, 62.8059120, 22.9163180, 39.00, 0.00, '2023-12-21 18:01:12', 'Kertunlaakso'),
(57, 62.8059120, 22.9163190, 39.10, 0.00, '2023-12-21 18:04:23', 'Kertunlaakso'),
(58, 62.8059120, 22.9163190, 39.10, 0.00, '2023-12-21 18:07:23', 'Kertunlaakso'),
(59, 62.8059130, 22.9163220, 39.20, 0.00, '2023-12-21 18:10:24', 'Kertunlaakso'),
(60, 62.8059130, 22.9163220, 39.20, 0.00, '2023-12-21 18:13:24', 'Kertunlaakso'),
(61, 62.8059130, 22.9163220, 39.20, 0.00, '2023-12-21 18:16:25', 'Kertunlaakso'),
(62, 62.8059130, 22.9163210, 39.20, 0.00, '2023-12-21 18:19:25', 'Kertunlaakso'),
(63, 62.8059130, 22.9163210, 39.10, 0.00, '2023-12-21 18:22:26', 'Kertunlaakso'),
(64, 62.8059130, 22.9163210, 39.10, 0.00, '2023-12-21 18:25:36', 'Kertunlaakso'),
(65, 62.8059120, 22.9163220, 39.30, 0.00, '2023-12-21 18:28:37', 'Kertunlaakso'),
(66, 62.8059110, 22.9163220, 39.60, 0.00, '2023-12-21 18:31:38', 'Kertunlaakso'),
(67, 62.8059110, 22.9163230, 39.60, 0.00, '2023-12-21 18:34:38', 'Kertunlaakso'),
(68, 62.8059100, 22.9163240, 39.70, 0.00, '2023-12-21 18:37:39', 'Kertunlaakso'),
(69, 62.8059100, 22.9163240, 39.80, 0.00, '2023-12-21 18:40:39', 'Kertunlaakso'),
(71, 62.8074000, 22.9148720, 43.50, 0.00, '2023-12-21 18:44:55', 'Kertunlaakso'),
(72, 62.8082990, 22.9132890, 38.90, 0.00, '2023-12-21 18:45:06', 'Kertunlaakso'),
(73, 62.8092060, 22.9114260, 39.20, 0.00, '2023-12-21 18:45:17', 'Kertunlaakso'),
(74, 62.8097480, 22.9095440, 34.60, 0.00, '2023-12-21 18:45:27', 'Kertunlaakso'),
(75, 62.8096980, 22.9078480, 31.90, 0.00, '2023-12-21 18:45:38', 'Kertunlaakso'),
(76, 62.8089530, 22.9059730, 33.20, 0.00, '2023-12-21 18:45:48', 'Kertunlaakso'),
(77, 62.8081800, 22.9043870, 38.20, 0.00, '2023-12-21 18:45:58', 'Kertunlaakso'),
(78, 62.8074140, 22.9030880, 41.90, 0.00, '2023-12-21 18:46:09', 'Kertunlaakso'),
(79, 62.8066160, 22.9019990, 45.70, 0.00, '2023-12-21 18:46:19', ''),
(80, 62.8057210, 22.9007720, 52.80, 0.00, '2023-12-21 18:46:30', ''),
(81, 62.8051560, 22.8998470, 49.40, 0.00, '2023-12-21 18:46:40', ''),
(82, 62.8052920, 22.8975830, 48.80, 0.00, '2023-12-21 18:46:50', ''),
(83, 62.8049470, 22.8945720, 52.20, 0.00, '2023-12-21 18:47:01', ''),
(84, 62.8046620, 22.8919410, 53.40, 0.00, '2023-12-21 18:47:11', ''),
(85, 62.8048090, 22.8892700, 51.70, 0.00, '2023-12-21 18:47:21', ''),
(86, 62.8050040, 22.8864380, 50.30, 0.00, '2023-12-21 18:47:32', ''),
(87, 62.8052110, 22.8836070, 43.50, 0.00, '2023-12-21 18:47:42', ''),
(88, 62.8053750, 22.8810750, 40.40, 0.00, '2023-12-21 18:47:53', ''),
(89, 62.8059860, 22.8797440, 40.50, 0.00, '2023-12-21 18:48:03', ''),
(90, 62.8071230, 22.8788530, 39.80, 0.00, '2023-12-21 18:48:13', ''),
(91, 62.8083340, 22.8783950, 37.70, 0.00, '2023-12-21 18:48:24', ''),
(92, 62.8085930, 22.8794930, 37.30, 0.00, '2023-12-21 18:48:34', ''),
(93, 62.8075470, 22.8783320, 34.00, 0.00, '2023-12-21 18:48:45', ''),
(94, 62.8068020, 22.8741510, 38.60, 0.00, '2023-12-21 18:48:55', ''),
(95, 62.8060080, 22.8698410, 41.10, 0.00, '2023-12-21 18:49:05', ''),
(96, 62.8048850, 22.8653610, 40.80, 0.00, '2023-12-21 18:49:16', ''),
(97, 62.8036270, 22.8616360, 39.80, 0.00, '2023-12-21 18:49:26', ''),
(98, 62.8022020, 22.8583290, 37.50, 0.00, '2023-12-21 18:49:36', ''),
(99, 62.8006250, 22.8546000, 34.80, 0.00, '2023-12-21 18:49:47', ''),
(100, 62.7993600, 22.8508710, 35.00, 0.00, '2023-12-21 18:49:57', ''),
(101, 62.7982280, 22.8466700, 35.70, 0.00, '2023-12-21 18:50:08', ''),
(102, 62.7974990, 22.8429340, 38.90, 0.00, '2023-12-21 18:50:18', ''),
(103, 62.7969180, 22.8390520, 34.30, 0.00, '2023-12-21 18:50:28', ''),
(104, 62.7963390, 22.8347260, 28.40, 0.00, '2023-12-21 18:50:39', ''),
(105, 62.7964310, 22.8316510, 27.50, 0.00, '2023-12-21 18:50:51', ''),
(106, 62.7967190, 22.8331600, 37.70, 0.00, '2023-12-21 18:51:02', ''),
(107, 62.7956770, 22.8333280, 37.00, 0.00, '2023-12-21 18:51:12', ''),
(108, 62.7953440, 22.8331590, 34.70, 0.00, '2023-12-21 18:51:23', ''),
(109, 62.7952890, 22.8311520, 39.90, 0.00, '2023-12-21 18:51:33', ''),
(110, 62.7950240, 22.8291390, 40.50, 0.00, '2023-12-21 18:51:43', ''),
(111, 62.7946620, 22.8273270, 41.50, 0.00, '2023-12-21 18:51:54', 'Itikanristeys'),
(112, 62.7941300, 22.8250500, 39.40, 0.00, '2023-12-21 18:52:04', ''),
(113, 62.7934140, 22.8224170, 37.50, 0.00, '2023-12-21 18:52:15', ''),
(114, 62.7930490, 22.8201910, 39.60, 0.00, '2023-12-21 18:52:25', ''),
(115, 62.7927690, 22.8194570, 41.40, 0.00, '2023-12-21 18:52:35', ''),
(116, 62.7915780, 22.8196790, 38.40, 0.00, '2023-12-21 18:52:46', ''),
(117, 62.7904110, 22.8195330, 39.40, 0.00, '2023-12-21 18:52:56', 'Frami'),
(118, 62.7890940, 22.8193610, 44.80, 0.00, '2023-12-21 18:53:07', 'Frami'),
(119, 62.7879360, 22.8192280, 42.40, 0.00, '2023-12-21 18:53:17', 'Frami'),
(120, 62.7867290, 22.8191290, 39.20, 0.00, '2023-12-21 18:53:27', ''),
(121, 62.7854350, 22.8195910, 40.50, 0.00, '2023-12-21 18:53:38', ''),
(122, 62.7842810, 22.8204040, 40.50, 0.00, '2023-12-21 18:53:48', ''),
(123, 62.7833480, 22.8211640, 46.00, 0.00, '2023-12-21 18:53:59', ''),
(124, 62.7826320, 22.8199140, 40.60, 0.00, '2023-12-21 18:54:09', ''),
(125, 62.7817700, 22.8184240, 37.50, 0.00, '2023-12-21 18:54:19', ''),
(126, 62.7807020, 22.8169300, 38.10, 0.00, '2023-12-21 18:54:30', ''),
(127, 62.7796860, 22.8163980, 44.50, 0.00, '2023-12-21 18:54:40', ''),
(128, 62.7789500, 22.8170190, 47.10, 0.00, '2023-12-21 18:54:50', 'telakka'),
(129, 62.7787060, 22.8167290, 49.90, 0.00, '2023-12-21 18:55:01', 'telakka'),
(130, 62.7790890, 22.8168450, 47.60, 0.00, '2023-12-21 18:55:11', ''),
(131, 62.7801440, 22.8164860, 47.90, 0.00, '2023-12-21 18:55:22', ''),
(132, 62.7809000, 22.8170710, 45.70, 0.00, '2023-12-21 18:55:32', ''),
(133, 62.7814700, 22.8157670, 49.20, 0.00, '2023-12-21 18:55:42', ''),
(134, 62.7823280, 22.8142190, 43.70, 0.00, '2023-12-21 18:55:53', ''),
(135, 62.7833040, 22.8137140, 45.90, 0.00, '2023-12-21 18:56:03', ''),
(136, 62.7838050, 22.8132940, 48.00, 0.00, '2023-12-21 18:56:14', ''),
(137, 62.7833600, 22.8110920, 47.20, 0.00, '2023-12-21 18:56:25', ''),
(138, 62.7829770, 22.8086460, 50.90, 0.00, '2023-12-21 18:56:36', ''),
(139, 62.7826690, 22.8071370, 56.50, 0.00, '2023-12-21 18:56:47', ''),
(140, 62.7818850, 22.8071960, 59.00, 0.00, '2023-12-21 18:56:57', ''),
(141, 62.7811910, 22.8081720, 58.80, 0.00, '2023-12-21 18:57:07', ''),
(142, 62.7803750, 22.8079420, 62.70, 0.00, '2023-12-21 18:57:18', ''),
(143, 62.7794540, 22.8067510, 73.40, 0.00, '2023-12-21 18:57:28', ''),
(144, 62.7783950, 22.8060540, 83.20, 0.00, '2023-12-21 18:57:39', ''),
(145, 62.7778820, 22.8054640, 91.20, 0.00, '2023-12-21 18:57:49', 'start'),
(146, 62.7776960, 22.8055750, 85.80, 0.00, '2023-12-21 18:57:59', 'start'),
(147, 62.7777560, 22.8056520, 91.70, 0.00, '2023-12-21 18:59:30', 'start'),
(148, 62.7781220, 22.8057550, 87.70, 0.00, '2023-12-21 18:59:40', 'start'),
(149, 62.7789380, 22.8063290, 82.60, 0.00, '2023-12-21 18:59:51', ''),
(150, 62.7799750, 22.8072110, 71.40, 0.00, '2023-12-21 19:00:01', ''),
(151, 62.7807200, 22.8085280, 61.10, 0.00, '2023-12-21 19:00:11', ''),
(152, 62.7815560, 22.8074340, 57.10, 0.00, '2023-12-21 19:00:22', ''),
(153, 62.7824030, 22.8071290, 53.50, 0.00, '2023-12-21 19:00:32', ''),
(154, 62.7828210, 22.8067360, 51.90, 0.00, '2023-12-21 19:00:42', ''),
(155, 62.7833290, 22.8050040, 52.10, 0.00, '2023-12-21 19:00:53', ''),
(156, 62.7841420, 22.8048730, 50.60, 0.00, '2023-12-21 19:01:03', ''),
(157, 62.7851970, 22.8066500, 47.90, 0.00, '2023-12-21 19:01:14', ''),
(158, 62.7861090, 22.8080960, 47.70, 0.00, '2023-12-21 19:01:24', ''),
(159, 62.7865960, 22.8090280, 48.30, 0.00, '2023-12-21 19:01:34', ''),
(160, 62.7876590, 22.8105760, 45.50, 0.00, '2023-12-21 19:01:45', ''),
(161, 62.7887050, 22.8123270, 41.00, 0.00, '2023-12-21 19:01:56', ''),
(162, 62.7890030, 22.8128130, 41.30, 0.00, '2023-12-21 19:02:07', ''),
(163, 62.7894450, 22.8136260, 42.20, 0.00, '2023-12-21 19:02:18', ''),
(164, 62.7903410, 22.8154300, 39.90, 0.00, '2023-12-21 19:02:28', ''),
(165, 62.7905710, 22.8181850, 41.30, 0.00, '2023-12-21 19:02:39', ''),
(166, 62.7906150, 22.8194720, 45.00, 0.00, '2023-12-21 19:02:49', ''),
(167, 62.7914670, 22.8197080, 42.50, 0.00, '2023-12-21 19:02:59', ''),
(168, 62.7926080, 22.8199160, 42.50, 0.00, '2023-12-21 19:03:10', ''),
(169, 62.7932130, 22.8217730, 47.80, 0.00, '2023-12-21 19:03:20', ''),
(170, 62.7937630, 22.8240280, 44.20, 0.00, '2023-12-21 19:03:30', ''),
(171, 62.7941530, 22.8253250, 44.30, 0.00, '2023-12-21 19:03:41', 'Itikanristeys'),
(172, 62.7942780, 22.8257350, 47.00, 0.00, '2023-12-21 19:04:41', 'Itikanristeys'),
(173, 62.7951300, 22.8261520, 45.30, 0.00, '2023-12-21 19:04:52', ''),
(174, 62.7954320, 22.8289120, 43.60, 0.00, '2023-12-21 19:05:02', ''),
(175, 62.7959690, 22.8329500, 39.80, 0.00, '2023-12-21 19:05:12', ''),
(176, 62.7966140, 22.8379610, 46.60, 0.00, '2023-12-21 19:05:23', ''),
(177, 62.7973170, 22.8423920, 51.10, 0.00, '2023-12-21 19:05:33', ''),
(178, 62.7981620, 22.8468350, 47.80, 0.00, '2023-12-21 19:05:43', ''),
(179, 62.7993340, 22.8514120, 45.10, 0.00, '2023-12-21 19:05:54', ''),
(180, 62.8006540, 22.8552020, 42.20, 0.00, '2023-12-21 19:06:04', ''),
(181, 62.8022480, 22.8589770, 43.90, 0.00, '2023-12-21 19:06:15', ''),
(182, 62.8036690, 22.8624920, 40.00, 0.00, '2023-12-21 19:06:25', ''),
(183, 62.8049200, 22.8661930, 42.20, 0.00, '2023-12-21 19:06:35', ''),
(184, 62.8059400, 22.8706350, 37.90, 0.00, '2023-12-21 19:06:46', ''),
(185, 62.8065670, 22.8745400, 39.20, 0.00, '2023-12-21 19:06:56', ''),
(186, 62.8069710, 22.8776990, 46.70, 0.00, '2023-12-21 19:07:07', ''),
(187, 62.8070380, 22.8783720, 47.10, 0.00, '2023-12-21 19:07:17', ''),
(188, 62.8061030, 22.8793670, 42.60, 0.00, '2023-12-21 19:07:27', ''),
(189, 62.8052690, 22.8799750, 39.80, 0.00, '2023-12-21 19:07:38', ''),
(190, 62.8052880, 22.8822000, 40.60, 0.00, '2023-12-21 19:07:49', ''),
(191, 62.8050580, 22.8854650, 46.50, 0.00, '2023-12-21 19:08:01', ''),
(192, 62.8048710, 22.8881510, 50.90, 0.00, '2023-12-21 19:08:11', ''),
(193, 62.8046750, 22.8911810, 51.10, 0.00, '2023-12-21 19:08:22', ''),
(194, 62.8048110, 22.8939230, 53.50, 0.00, '2023-12-21 19:08:32', ''),
(195, 62.8052370, 22.8966180, 50.90, 0.00, '2023-12-21 19:08:42', ''),
(196, 62.8051640, 22.8993760, 50.20, 0.00, '2023-12-21 19:08:53', ''),
(197, 62.8055000, 22.9005410, 53.10, 0.00, '2023-12-21 19:09:03', ''),
(198, 62.8064080, 22.9017910, 53.70, 0.00, '2023-12-21 19:09:14', ''),
(199, 62.8072900, 22.9029950, 50.40, 0.00, '2023-12-21 19:09:24', 'Kertunlaakso'),
(200, 62.8080370, 22.9042180, 45.50, 0.00, '2023-12-21 19:09:34', 'Kertunlaakso'),
(201, 62.8088760, 22.9059320, 41.90, 0.00, '2023-12-21 19:09:45', 'Kertunlaakso'),
(202, 62.8094920, 22.9074950, 40.00, 0.00, '2023-12-21 19:09:55', 'Kertunlaakso'),
(203, 62.8098930, 22.9089280, 40.70, 0.00, '2023-12-21 19:10:06', 'Kertunlaakso'),
(204, 62.8093660, 22.9107420, 40.70, 0.00, '2023-12-21 19:10:16', 'Kertunlaakso'),
(205, 62.8086200, 22.9125540, 42.40, 0.00, '2023-12-21 19:10:26', 'Kertunlaakso'),
(206, 62.8076350, 22.9142230, 45.00, 0.00, '2023-12-21 19:10:37', 'Kertunlaakso'),
(207, 62.8071060, 22.9148150, 46.10, 0.00, '2023-12-21 19:10:47', 'Kertunlaakso'),
(208, 62.8065330, 22.9142100, 46.60, 0.00, '2023-12-21 19:10:58', 'Kertunlaakso'),
(209, 62.8060120, 22.9153550, 49.40, 0.00, '2023-12-21 19:11:08', 'Kertunlaakso'),
(210, 62.8059370, 22.9161130, 48.50, 0.00, '2023-12-21 19:11:18', 'Kertunlaakso'),
(211, 62.8059200, 22.9163000, 44.30, 0.00, '2023-12-21 19:11:29', 'Kertunlaakso'),
(213, 62.8078420, 22.9038850, 44.00, 0.00, '2023-12-22 06:09:10', 'Kertunlaakso'),
(214, 62.8068620, 22.9024140, 46.10, 0.00, '2023-12-22 06:09:21', ''),
(215, 62.8058270, 22.9010340, 50.20, 0.00, '2023-12-22 06:09:32', ''),
(216, 62.8051610, 22.8999470, 51.10, 0.00, '2023-12-22 06:09:42', ''),
(217, 62.8052980, 22.8973970, 48.00, 0.00, '2023-12-22 06:09:53', ''),
(218, 62.8049480, 22.8947100, 46.70, 0.00, '2023-12-22 06:10:03', ''),
(219, 62.8046980, 22.8919180, 50.90, 0.00, '2023-12-22 06:10:14', ''),
(220, 62.8048240, 22.8894140, 53.20, 0.00, '2023-12-22 06:10:24', ''),
(221, 62.8049870, 22.8868050, 50.90, 0.00, '2023-12-22 06:10:34', ''),
(222, 62.8051970, 22.8836350, 41.00, 0.00, '2023-12-22 06:10:45', ''),
(223, 62.8053780, 22.8810990, 36.60, 0.00, '2023-12-22 06:10:55', ''),
(224, 62.8056470, 22.8800670, 34.00, 0.00, '2023-12-22 06:11:05', ''),
(225, 62.8068180, 22.8791350, 35.90, 0.00, '2023-12-22 06:11:16', ''),
(226, 62.8079100, 22.8783920, 34.40, 0.00, '2023-12-22 06:11:26', ''),
(227, 62.8087000, 22.8791570, 33.70, 0.00, '2023-12-22 06:11:37', ''),
(228, 62.8078630, 22.8794280, 32.10, 0.00, '2023-12-22 06:11:47', ''),
(229, 62.8070700, 22.8759620, 30.00, 0.00, '2023-12-22 06:11:57', ''),
(230, 62.8062860, 22.8714730, 28.90, 0.00, '2023-12-22 06:12:08', ''),
(231, 62.8054080, 22.8674320, 26.40, 0.00, '2023-12-22 06:12:18', ''),
(232, 62.8043310, 22.8637490, 32.70, 0.00, '2023-12-22 06:12:28', ''),
(233, 62.8029300, 22.8600870, 35.00, 0.00, '2023-12-22 06:12:39', ''),
(234, 62.8015130, 22.8568530, 38.90, 0.00, '2023-12-22 06:12:49', ''),
(235, 62.8002100, 22.8536410, 38.50, 0.00, '2023-12-22 06:12:59', ''),
(236, 62.7989430, 22.8495440, 35.80, 0.00, '2023-12-22 06:13:10', ''),
(237, 62.7979530, 22.8455190, 31.80, 0.00, '2023-12-22 06:13:20', ''),
(238, 62.7971480, 22.8409290, 33.50, 0.00, '2023-12-22 06:13:31', ''),
(239, 62.7965960, 22.8368830, 34.00, 0.00, '2023-12-22 06:13:41', ''),
(240, 62.7961940, 22.8333430, 34.10, 0.00, '2023-12-22 06:13:51', ''),
(241, 62.7967630, 22.8318910, 31.40, 0.00, '2023-12-22 06:14:02', ''),
(242, 62.7964590, 22.8333960, 30.30, 0.00, '2023-12-22 06:14:12', ''),
(243, 62.7954770, 22.8332890, 34.60, 0.00, '2023-12-22 06:14:23', ''),
(244, 62.7953280, 22.8327870, 37.20, 0.00, '2023-12-22 06:15:13', ''),
(245, 62.7952310, 22.8302360, 39.30, 0.00, '2023-12-22 06:15:24', ''),
(246, 62.7948310, 22.8281360, 39.90, 0.00, '2023-12-22 06:15:34', 'Itikanristeys'),
(247, 62.7944290, 22.8261660, 37.20, 0.00, '2023-12-22 06:15:45', 'Itikanristeys'),
(248, 62.7938110, 22.8239090, 36.20, 0.00, '2023-12-22 06:15:55', ''),
(249, 62.7932290, 22.8213340, 43.50, 0.00, '2023-12-22 06:16:06', ''),
(250, 62.7930930, 22.8196620, 45.80, 0.00, '2023-12-22 06:16:16', ''),
(251, 62.7923830, 22.8197160, 46.50, 0.00, '2023-12-22 06:16:27', ''),
(252, 62.7912530, 22.8196470, 42.50, 0.00, '2023-12-22 06:16:37', ''),
(253, 62.7900650, 22.8195060, 40.50, 0.00, '2023-12-22 06:16:47', 'Frami'),
(254, 62.7887520, 22.8193580, 45.70, 0.00, '2023-12-22 06:16:58', 'Frami'),
(255, 62.7875840, 22.8192140, 46.50, 0.00, '2023-12-22 06:17:08', 'Frami'),
(256, 62.7866870, 22.8195510, 41.90, 0.00, '2023-12-22 06:17:19', 'Frami'),
(257, 62.7868230, 22.8213450, 38.60, 0.00, '2023-12-22 06:17:29', 'Frami'),
(258, 62.7867230, 22.8222960, 35.10, 0.00, '2023-12-22 06:17:39', 'Frami'),
(259, 62.7864500, 22.8225700, 36.20, 0.00, '2023-12-22 06:17:50', 'Frami'),
(260, 62.8052360, 22.8973280, 35.30, 0.00, '2023-12-22 15:48:20', ''),
(261, 62.8070230, 22.9025970, 32.40, 0.00, '2023-12-22 15:48:56', ''),
(262, 62.8077460, 22.9036890, 34.10, 0.00, '2023-12-22 15:49:07', 'Kertunlaakso'),
(263, 62.8085870, 22.9052780, 34.60, 0.00, '2023-12-22 15:49:18', 'Kertunlaakso'),
(264, 62.8092770, 22.9068790, 34.10, 0.00, '2023-12-22 15:49:29', 'Kertunlaakso'),
(265, 62.8096970, 22.9081220, 32.30, 0.00, '2023-12-22 15:49:39', 'Kertunlaakso'),
(266, 62.8097500, 22.9093870, 33.00, 0.00, '2023-12-22 15:49:50', 'Kertunlaakso'),
(267, 62.8092400, 22.9112340, 34.60, 0.00, '2023-12-22 15:50:00', 'Kertunlaakso'),
(268, 62.8084650, 22.9128830, 36.40, 0.00, '2023-12-22 15:50:10', 'Kertunlaakso'),
(269, 62.8075390, 22.9143990, 39.10, 0.00, '2023-12-22 15:50:21', 'Kertunlaakso'),
(270, 62.8069320, 22.9145100, 36.40, 0.00, '2023-12-22 15:50:31', 'Kertunlaakso'),
(271, 62.8063020, 22.9146790, 36.00, 0.00, '2023-12-22 15:50:42', 'Kertunlaakso'),
(272, 62.8058560, 22.9157220, 36.60, 0.00, '2023-12-22 15:50:52', 'Kertunlaakso'),
(273, 62.8059300, 22.9161910, 36.80, 0.00, '2023-12-22 15:51:02', 'Kertunlaakso'),
(274, 62.8059020, 22.9160810, 53.80, 0.00, '2023-12-22 15:56:18', 'Kertunlaakso'),
(275, 62.8059150, 22.9161780, 49.80, 0.00, '2023-12-22 15:59:23', 'Kertunlaakso'),
(276, 62.8059140, 22.9162400, 48.50, 0.00, '2023-12-22 16:02:23', 'Kertunlaakso'),
(277, 62.8059260, 22.9161240, 53.90, 0.00, '2023-12-22 16:04:54', 'Kertunlaakso'),
(278, 62.8059100, 22.9161280, 52.20, 0.00, '2023-12-22 16:07:55', 'Kertunlaakso'),
(279, 62.8059080, 22.9161520, 50.10, 0.00, '2023-12-22 16:10:56', 'Kertunlaakso'),
(280, 62.8059000, 22.9161790, 48.10, 0.00, '2023-12-22 16:13:57', 'Kertunlaakso'),
(281, 62.8058860, 22.9161970, 49.00, 0.00, '2023-12-22 16:16:58', 'Kertunlaakso'),
(282, 62.8058850, 22.9162000, 48.80, 0.00, '2023-12-22 16:19:58', 'Kertunlaakso'),
(283, 62.8058850, 22.9162010, 49.00, 0.00, '2023-12-22 16:22:59', 'Kertunlaakso'),
(284, 62.8058860, 22.9161960, 48.40, 0.00, '2023-12-22 16:25:59', 'Kertunlaakso'),
(285, 62.8058890, 22.9161910, 48.20, 0.00, '2023-12-22 16:29:10', 'Kertunlaakso'),
(286, 62.8058910, 22.9161970, 48.00, 0.00, '2023-12-22 16:32:10', 'Kertunlaakso'),
(287, 62.8058660, 22.9159820, 57.40, 0.00, '2023-12-22 16:36:05', 'Kertunlaakso'),
(288, 62.8058850, 22.9160410, 54.40, 0.00, '2023-12-22 16:39:28', 'Kertunlaakso'),
(289, 62.8058810, 22.9160120, 49.80, 0.00, '2023-12-22 16:42:29', 'Kertunlaakso'),
(290, 62.8059050, 22.9161200, 47.90, 0.00, '2023-12-22 16:45:00', 'Kertunlaakso'),
(291, 62.8059330, 22.9161760, 42.70, 0.00, '2023-12-22 17:04:26', 'Kertunlaakso'),
(292, 62.8059270, 22.9161700, 43.20, 0.00, '2023-12-22 17:07:57', 'Kertunlaakso'),
(293, 62.8059310, 22.9161770, 43.40, 0.00, '2023-12-22 17:09:05', 'Kertunlaakso'),
(294, 62.8059210, 22.9161090, 44.60, 0.00, '2023-12-22 17:19:47', 'Kertunlaakso'),
(295, 62.8059210, 22.9161340, 44.60, 0.00, '2023-12-22 17:22:47', 'Kertunlaakso'),
(296, 62.8059160, 22.9161580, 43.70, 0.00, '2023-12-22 17:25:48', 'Kertunlaakso'),
(297, 62.8059180, 22.9161570, 43.80, 0.00, '2023-12-22 17:28:49', 'Kertunlaakso'),
(298, 62.8059150, 22.9161670, 43.50, 0.00, '2023-12-22 17:31:49', 'Kertunlaakso'),
(299, 62.8059120, 22.9161640, 43.30, 0.00, '2023-12-22 17:34:50', 'Kertunlaakso'),
(300, 62.8059100, 22.9161680, 42.80, 0.00, '2023-12-22 17:38:01', 'Kertunlaakso'),
(301, 62.8059100, 22.9161750, 42.30, 0.00, '2023-12-22 17:41:01', 'Kertunlaakso'),
(302, 62.8058870, 22.9162480, 38.70, 0.00, '2023-12-22 17:44:02', 'Kertunlaakso'),
(303, 62.8058910, 22.9162420, 39.30, 0.00, '2023-12-22 17:47:02', 'Kertunlaakso'),
(304, 62.8058920, 22.9162370, 39.30, 0.00, '2023-12-22 17:50:02', 'Kertunlaakso'),
(305, 62.8058920, 22.9162360, 39.20, 0.00, '2023-12-22 17:53:04', 'Kertunlaakso'),
(306, 62.8058940, 22.9162350, 39.10, 0.00, '2023-12-22 17:56:04', 'Kertunlaakso'),
(307, 62.8058940, 22.9162310, 39.20, 0.00, '2023-12-22 17:59:05', 'Kertunlaakso'),
(308, 62.8058940, 22.9162330, 39.10, 0.00, '2023-12-22 18:02:05', 'Kertunlaakso'),
(309, 62.8058860, 22.9163180, 30.90, 0.00, '2023-12-22 18:19:56', 'Kertunlaakso'),
(310, 62.8058860, 22.9163180, 30.90, 0.00, '2023-12-22 18:20:51', 'Kertunlaakso'),
(311, 62.8059460, 22.9161260, 55.50, 0.00, '2023-12-22 18:26:06', 'Kertunlaakso'),
(312, 62.8059570, 22.9161530, 56.00, 0.00, '2023-12-22 18:29:34', 'Kertunlaakso'),
(313, 62.8060020, 22.9161160, 58.30, 0.00, '2023-12-22 18:30:54', 'Kertunlaakso'),
(314, 62.8059990, 22.9161130, 57.80, 0.00, '2023-12-22 18:33:55', 'Kertunlaakso'),
(315, 62.8059920, 22.9161210, 56.60, 0.00, '2023-12-22 18:36:55', 'Kertunlaakso'),
(316, 62.8059880, 22.9161210, 55.80, 0.00, '2023-12-22 18:39:56', 'Kertunlaakso'),
(317, 62.8059810, 22.9161230, 54.60, 0.00, '2023-12-22 18:43:06', 'Kertunlaakso'),
(318, 62.8059730, 22.9161300, 53.40, 0.00, '2023-12-22 18:46:08', 'Kertunlaakso'),
(319, 62.8059660, 22.9161380, 52.10, 0.00, '2023-12-22 18:49:08', 'Kertunlaakso'),
(320, 62.8059640, 22.9161410, 51.80, 0.00, '2023-12-22 18:52:09', 'Kertunlaakso'),
(321, 62.8059640, 22.9161390, 51.60, 0.00, '2023-12-22 18:55:19', 'Kertunlaakso'),
(322, 62.8059590, 22.9161440, 50.80, 0.00, '2023-12-22 18:58:20', 'Kertunlaakso'),
(323, 62.8059550, 22.9161470, 50.00, 0.00, '2023-12-22 19:01:20', 'Kertunlaakso'),
(324, 62.8059670, 22.9161050, 44.40, 0.00, '2023-12-22 19:04:21', 'Kertunlaakso'),
(325, 62.8059640, 22.9161080, 44.40, 0.00, '2023-12-22 19:07:22', 'Kertunlaakso'),
(326, 62.8059620, 22.9161060, 43.70, 0.00, '2023-12-22 19:10:22', 'Kertunlaakso'),
(327, 62.8059330, 22.9161340, 39.20, 0.00, '2023-12-22 19:13:22', 'Kertunlaakso'),
(328, 62.8059020, 22.9163410, 34.30, 0.00, '2023-12-22 19:43:18', 'Kertunlaakso'),
(329, 62.8058470, 22.9162550, 49.80, 0.00, '2023-12-22 19:44:08', 'Kertunlaakso'),
(330, 62.8058430, 22.9162090, 47.90, 0.00, '2023-12-22 19:47:09', 'Kertunlaakso'),
(331, 62.8059080, 22.9162090, 43.40, 0.00, '2023-12-22 19:49:39', 'Kertunlaakso'),
(332, 62.8059100, 22.9161820, 44.20, 0.00, '2023-12-22 19:52:39', 'Kertunlaakso'),
(333, 62.8059100, 22.9161790, 44.50, 0.00, '2023-12-22 19:55:40', 'Kertunlaakso'),
(334, 62.8059100, 22.9161740, 45.10, 0.00, '2023-12-22 19:58:41', 'Kertunlaakso'),
(335, 62.8059110, 22.9161740, 45.30, 0.00, '2023-12-22 20:01:41', 'Kertunlaakso'),
(336, 62.8059110, 22.9161640, 45.50, 0.00, '2023-12-22 20:04:42', 'Kertunlaakso'),
(337, 62.8059220, 22.9161170, 46.30, 0.00, '2023-12-22 20:07:42', 'Kertunlaakso');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `location_history`
--
ALTER TABLE `location_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ts_index` (`id`,`lat`,`lon`,`alt`,`speed`,`ts`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `location_history`
--
ALTER TABLE `location_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=338;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;