from datetime import datetime
import sys
import gpxpy
import serial
import time
import logging

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)

# Define the NMEA logs
nmea_logs = [
    "$GPGGA,123519,6010.1234,N,02345.6789,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,123529,6010.1245,N,02345.6801,E,1,08,0.9,545.4,M,46.9,M,,*4A",
    "$GPGGA,123539,6010.1256,N,02345.6813,E,1,08,0.9,545.4,M,46.9,M,,*4D",
    "$GPGGA,123549,6010.1267,N,02345.6825,E,1,08,0.9,545.4,M,46.9,M,,*42",
    "$GPGGA,123559,6010.1278,N,02345.6837,E,1,08,0.9,545.4,M,46.9,M,,*45",
    "$GPGGA,123609,6010.1289,N,02345.6849,E,1,08,0.9,545.4,M,46.9,M,,*48",
    "$GPGGA,123619,6010.1300,N,02345.6861,E,1,08,0.9,545.4,M,46.9,M,,*4B",
    "$GPGGA,123629,6010.1311,N,02345.6873,E,1,08,0.9,545.4,M,46.9,M,,*4E",
    "$GPGGA,123639,6010.1322,N,02345.6885,E,1,08,0.9,545.4,M,46.9,M,,*43",
    "$GPGGA,123649,6010.1333,N,02345.6897,E,1,08,0.9,545.4,M,46.9,M,,*46",
    "$GPGGA,123659,6010.1344,N,02345.6909,E,1,08,0.9,545.4,M,46.9,M,,*49",
    "$GPGGA,123709,6010.1355,N,02345.6921,E,1,08,0.9,545.4,M,46.9,M,,*4C",
    "$GPGGA,123719,6010.1366,N,02345.6933,E,1,08,0.9,545.4,M,46.9,M,,*4F",
    "$GPGGA,123729,6010.1377,N,02345.6945,E,1,08,0.9,545.4,M,46.9,M,,*44",
    "$GPGGA,123739,6010.1388,N,02345.6957,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,123749,6010.1399,N,02345.6969,E,1,08,0.9,545.4,M,46.9,M,,*4A",
    "$GPGGA,123759,6010.1410,N,02345.6981,E,1,08,0.9,545.4,M,46.9,M,,*4D",
    "$GPGGA,123809,6010.1421,N,02345.6993,E,1,08,0.9,545.4,M,46.9,M,,*42",
    "$GPGGA,123819,6010.1432,N,02345.7005,E,1,08,0.9,545.4,M,46.9,M,,*45",
    "$GPGGA,123829,6010.1443,N,02345.7017,E,1,08,0.9,545.4,M,46.9,M,,*48",
    "$GPGGA,123839,6010.1454,N,02345.7029,E,1,08,0.9,545.4,M,46.9,M,,*4B",
    "$GPGGA,123849,6010.1465,N,02345.7041,E,1,08,0.9,545.4,M,46.9,M,,*4E",
    "$GPGGA,123859,6010.1476,N,02345.7053,E,1,08,0.9,545.4,M,46.9,M,,*43",
    "$GPGGA,123909,6010.1487,N,02345.7065,E,1,08,0.9,545.4,M,46.9,M,,*46",
    "$GPGGA,123919,6010.1498,N,02345.7077,E,1,08,0.9,545.4,M,46.9,M,,*49",
    "$GPGGA,123929,6010.1509,N,02345.7089,E,1,08,0.9,545.4,M,46.9,M,,*4C",
    "$GPGGA,123939,6010.1520,N,02345.7101,E,1,08,0.9,545.4,M,46.9,M,,*4F",
    "$GPGGA,123949,6010.1531,N,02345.7113,E,1,08,0.9,545.4,M,46.9,M,,*44",
    "$GPGGA,123959,6010.1542,N,02345.7125,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,124009,6010.1553,N,02345.7137,E,1,08,0.9,545.4,M,46.9,M,,*4A",
    "$GPGGA,124019,6010.1564,N,02345.7149,E,1,08,0.9,545.4,M,46.9,M,,*4D",
    "$GPGGA,124029,6010.1575,N,02345.7161,E,1,08,0.9,545.4,M,46.9,M,,*42",
    "$GPGGA,124039,6010.1586,N,02345.7173,E,1,08,0.9,545.4,M,46.9,M,,*45",
    "$GPGGA,124049,6010.1597,N,02345.7185,E,1,08,0.9,545.4,M,46.9,M,,*48",
    "$GPGGA,124059,6010.1608,N,02345.7197,E,1,08,0.9,545.4,M,46.9,M,,*4B",
    "$GPGGA,124109,6010.1619,N,02345.7209,E,1,08,0.9,545.4,M,46.9,M,,*4E",
    "$GPGGA,124119,6010.1630,N,02345.7221,E,1,08,0.9,545.4,M,46.9,M,,*43",
    "$GPGGA,124129,6010.1641,N,02345.7233,E,1,08,0.9,545.4,M,46.9,M,,*46",
    "$GPGGA,124139,6010.1652,N,02345.7245,E,1,08,0.9,545.4,M,46.9,M,,*49",
    "$GPGGA,124149,6010.1663,N,02345.7257,E,1,08,0.9,545.4,M,46.9,M,,*4C",
    "$GPGGA,124159,6010.1674,N,02345.7269,E,1,08,0.9,545.4,M,46.9,M,,*4F",
    "$GPGGA,124209,6010.1685,N,02345.7281,E,1,08,0.9,545.4,M,46.9,M,,*44",
    "$GPGGA,124219,6010.1696,N,02345.7293,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,124229,6010.1707,N,02345.7305,E,1,08,0.9,545.4,M,46.9,M,,*4A",
    "$GPGGA,124239,6010.1718,N,02345.7317,E,1,08,0.9,545.4,M,46.9,M,,*4D",
    "$GPGGA,124249,6010.1729,N,02345.7329,E,1,08,0.9,545.4,M,46.9,M,,*42",
    "$GPGGA,124259,6010.1740,N,02345.7341,E,1,08,0.9,545.4,M,46.9,M,,*45",
    "$GPGGA,124309,6010.1751,N,02345.7353,E,1,08,0.9,545.4,M,46.9,M,,*48",
    "$GPGGA,124319,6010.1762,N,02345.7365,E,1,08,0.9,545.4,M,46.9,M,,*4B",
    "$GPGGA,124329,6010.1773,N,02345.7377,E,1,08,0.9,545.4,M,46.9,M,,*4E",
    "$GPGGA,124339,6010.1784,N,02345.7389,E,1,08,0.9,545.4,M,46.9,M,,*43",
    "$GPGGA,124349,6010.1795,N,02345.7401,E,1,08,0.9,545.4,M,46.9,M,,*46",
    "$GPGGA,124359,6010.1806,N,02345.7413,E,1,08,0.9,545.4,M,46.9,M,,*49",
    "$GPGGA,124409,6010.1817,N,02345.7425,E,1,08,0.9,545.4,M,46.9,M,,*4C",
    "$GPGGA,124419,6010.1828,N,02345.7437,E,1,08,0.9,545.4,M,46.9,M,,*4F",
    "$GPGGA,124429,6010.1839,N,02345.7449,E,1,08,0.9,545.4,M,46.9,M,,*44",
    "$GPGGA,124439,6010.1850,N,02345.7461,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,124449,6010.1861,N,02345.7473,E,1,08,0.9,545.4,M,46.9,M,,*4A",
    "$GPGGA,124459,6010.1872,N,02345.7485,E,1,08,0.9,545.4,M,46.9,M,,*4D",
]


def gpx_to_nmea(point):
    # Extract relevant data from GPX point
    latitude = point.latitude
    longitude = point.longitude
    elevation = point.elevation
    time = datetime.now()

    lat_deg = int(float(latitude))
    lat_min = (float(latitude) - lat_deg) * 60

    lon_deg = int(float(longitude))
    lon_min = (float(longitude) - lon_deg) * 60

    # Format data into NMEA sentence
    nmea_sentence = f"$GPGGA,{time:%H%M%S},{lat_deg:02d}{lat_min:.2f},N,{'' if lat_deg >= 0 else '-'}{lon_deg:03d}{lon_min:.2f},E,1,08,0.9,{elevation:.2f},M,46.9,M,,*"
    checksum = 0
    for char in nmea_sentence[1:]:
        checksum ^= ord(char)
    nmea_sentence += f"{checksum:02X}"

    return nmea_sentence


def main(args):
    # Emulated serial port configuration
    serial_port = serial.Serial("/dev/EG27.NMEA", baudrate=38400, timeout=1)

    try:
        logging.info(len(args))
        logging.info(args)

        if len(args) > 1:
            with open(args[1], "r") as file:
                delay_test = False
                if len(args) == 3 and args[2] == "delay_test":
                    delay_test = True
                    logging.info("Running Delay test")

                gpx = gpxpy.parse(file)
                while True:
                    for track in gpx.tracks:
                        track_copy = track.clone()
                        for segment in track_copy.segments:
                            logging.debug(f"Points before reduce {len(segment.points)}")
                            segment.reduce_points(2.5)
                            logging.info(f"Points after reduce {len(segment.points)}")
                            for i, point in enumerate(segment.points):
                                nmea_sentence = gpx_to_nmea(point)
                                logging.debug(nmea_sentence)
                                serial_port.write(nmea_sentence.encode())
                                serial_port.flush()

                                if delay_test:
                                    if i == 50:
                                        logging.info(
                                            "Sleep for 4 minutes (no NMEA updates in such period)"
                                        )
                                        time.sleep(4 * 60)
                                        logging.info("return from break")
                                    if i == 100:
                                        logging.info("Same point for 10 minutes")
                                        time_start = int(time.time_ns() / 1000000000)
                                        time_end = time_start

                                        while (time_end - time_start) < (10 * 60):
                                            nmea_sentence = gpx_to_nmea(point)
                                            logging.debug(nmea_sentence)
                                            serial_port.write(nmea_sentence.encode())
                                            serial_port.flush()

                                            time.sleep(1)
                                            time_end = int(time.time_ns() / 1000000000)
                                        logging.info("returning to running normal")
                                    if i == 200:
                                        logging.info("Same point for 60 minutes")
                                        time_start = int(time.time_ns() / 1000000000)
                                        time_end = time_start

                                        while (time_end - time_start) < (60 * 60):
                                            nmea_sentence = gpx_to_nmea(point)
                                            logging.debug(nmea_sentence)
                                            serial_port.write(nmea_sentence.encode())
                                            serial_port.flush()

                                            time.sleep(1)
                                            time_end = int(time.time_ns() / 1000000000)
                                        logging.info("returning to running normal")

                                time.sleep(1)
        else:
            # Write NMEA logs to the emulated serial port
            for log in nmea_logs:
                serial_port.write(log.encode())
                serial_port.flush()
                time.sleep(1)

    finally:
        logging.info("exit emulator")
        # Close the emulated serial port
        serial_port.close()


if __name__ == "__main__":
    main(sys.argv)
