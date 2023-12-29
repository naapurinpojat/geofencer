from datetime import datetime
import sys
import gpxpy

def gpx_to_nmea(gpx_file):
    gpx = None
    with open(gpx_file, 'r') as file:
        gpx = gpxpy.parse(file)
        #print(gpx.tracks[0].segments[0].points)

    nmea_logs = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Extract relevant data from GPX point
                latitude = point.latitude
                longitude = point.longitude
                elevation = point.elevation
                time = datetime.now()

                # Format data into NMEA sentence
                nmea_sentence = f"$GPGGA,{time:%H%M%S},{latitude:.6f},{longitude:.6f},1,08,0.9,{elevation:.2f},M,,M,,*"
                checksum = 0
                for char in nmea_sentence[1:]:
                    checksum ^= ord(char)
                nmea_sentence += f"{checksum:02X}"

                nmea_logs.append(nmea_sentence)

    return nmea_logs

# Example usage
gpx_file_path = sys.argv[1]
nmea_logs = gpx_to_nmea(gpx_file_path)


# Open the file in write mode
with open(f"{gpx_file_path}_nmea_txt", 'w') as file:
    # Write each element of the array to a new line in the file
    for item in nmea_logs:
        file.write(str(item) + '\n')

