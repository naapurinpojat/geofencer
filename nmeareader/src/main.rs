use nmea_parser::*;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

struct GPSData {
    latitude: f64,
    longitude: f64,
    altitude: f64,
    speed: f64,
    heading: f64,
    timestamp: String,
}

fn main() {
    // Replace "/dev/EG25.NMEA" with the appropriate device file on your system
    let mut parser = NmeaParser::new();
    let mut gps_data = GPSData {
        latitude: 0.0,
        longitude: 0.0,
        altitude: 0.0,
        speed: 0.0,
        heading: 0.0,
        timestamp: String::new(),
    };
    let device_path = "/dev/rfcomm0";

    // Open the device file
    let file = match File::open(&device_path) {
        Ok(file) => file,
        Err(err) => {
            eprintln!("Error opening device file '{}': {:?}", device_path, err);
            return;
        }
    };

    // Create a buffered reader for the file
    let reader = BufReader::new(file);

    println!("Reading from device file '{}'", device_path);

    // Iterate over the lines in the reader
    for line in reader.lines() {
        match line {
            Ok(line) => {
                //println!("{}", line);

                if parser.parse_sentence(&line).is_ok() {
                    match parser.parse_sentence(&line).ok() {
                        Some(ParsedMessage::VesselDynamicData(vdd)) => {
                            println!("MMSI:    {}", vdd.mmsi);
                            println!("Speed:   {:.1} kts", vdd.sog_knots.unwrap_or_default());
                            println!("Heading: {}°", vdd.heading_true.unwrap_or_default());
                            gps_data.heading = vdd.heading_true.unwrap_or_default();
                            //println!("");
                        }
                        Some(ParsedMessage::VesselStaticData(vsd)) => {
                            println!("MMSI:  {}", vsd.mmsi);
                            println!("Flag:  {}", vsd.country().unwrap());
                            println!("Name:  {}", vsd.name.unwrap());
                            println!("Type:  {}", vsd.ship_type);
                            //println!("");
                        }
                        Some(ParsedMessage::Gga(gga)) => {
                            //println!("Source:    {}", gga.source);
                            println!("Latitude:  {:.3}°", gga.latitude.unwrap_or_default());
                            println!("Longitude: {:.3}°", gga.longitude.unwrap_or_default());
                            println!("Quality:  {}°", gga.quality);
                            println!("Satellites: {}", gga.satellite_count.unwrap_or_default());
                            println!("Altitude:   {:.1} m", gga.altitude.unwrap_or_default());
                            gps_data.latitude = gga.latitude.unwrap_or_default();
                            gps_data.longitude = gga.longitude.unwrap_or_default();
                            gps_data.altitude = gga.altitude.unwrap_or_default();

                            //println!("");
                        }
                        Some(ParsedMessage::Rmc(rmc)) => {
                            //println!("Source:  {}", rmc.source);
                            println!("Speed:   {:.1} kts", rmc.sog_knots.unwrap_or_default());
                            println!("Bearing: {}°", rmc.bearing.unwrap_or_default());
                            println!("Time:    {}", rmc.timestamp.unwrap_or_default());
                            gps_data.timestamp = rmc.timestamp.unwrap_or_default().to_string();
                            //println!("");
                        }
                        Some(ParsedMessage::Gsa(gsa)) => {
                            //println!("Source: {}", gsa.source);
                            println!("PDOP:   {}", gsa.pdop.unwrap_or_default());
                            println!("HDOP:   {}", gsa.hdop.unwrap_or_default());
                            println!("VDOP:   {}", gsa.vdop.unwrap_or_default());
                            //println!("");
                        }
                        Some(ParsedMessage::Gsv(gsv)) => {
                            println!("DBG: {:?}", gsv);
                        }
                        Some(ParsedMessage::Vtg(vtg)) => {
                            //println!("Source: {}", vtg.source);
                            println!("Bearing: {}°", vtg.cog_true.unwrap_or_default());
                            println!("Speed:   {:.1} kph", vtg.sog_kph.unwrap_or_default());
                            gps_data.speed = vtg.sog_kph.unwrap_or_default();
                            //println!("");
                        }
                        Some(ParsedMessage::Incomplete) => {
                            //println!("data incomplete {:?}", sentence);
                        }
                        _ => {
                            println!("{:?}", line);
                        }
                    }
                }
            }
            Err(err) => {
                if err.kind() == io::ErrorKind::TimedOut {
                    // Handle timeout if needed
                    eprintln!("Timeout reading from device file");
                } else {
                    eprintln!("Error reading from device file: {:?}", err);
                }
                break;
            }
        }

        // Add a delay (you can adjust the duration as needed)
        //std::thread::sleep(Duration::from_millis(100));
    }
}
