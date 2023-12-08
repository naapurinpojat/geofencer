use nmea_parser::*;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn main() {
    // Replace "/dev/EG25.NMEA" with the appropriate device file on your system
    let mut parser = NmeaParser::new();
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
                    match parser.parse_sentence(&line).unwrap() {
                        ParsedMessage::VesselDynamicData(vdd) => {
                            println!("MMSI:    {}", vdd.mmsi);
                            println!("Speed:   {:.1} kts", vdd.sog_knots.unwrap());
                            println!("Heading: {}°", vdd.heading_true.unwrap());
                            //println!("");
                        }
                        ParsedMessage::VesselStaticData(vsd) => {
                            println!("MMSI:  {}", vsd.mmsi);
                            println!("Flag:  {}", vsd.country().unwrap());
                            println!("Name:  {}", vsd.name.unwrap());
                            println!("Type:  {}", vsd.ship_type);
                            //println!("");
                        }
                        ParsedMessage::Gga(gga) => {
                            //println!("Source:    {}", gga.source);
                            println!("Latitude:  {:.3}°", gga.latitude.unwrap());
                            println!("Longitude: {:.3}°", gga.longitude.unwrap());
                            println!("Quality:  {}°", gga.quality);
                            println!("Satellites: {}", gga.satellite_count.unwrap());
                            println!("Altitude:   {:.1} m", gga.altitude.unwrap());

                            //println!("");
                        }
                        ParsedMessage::Rmc(rmc) => {
                            //println!("Source:  {}", rmc.source);
                            println!("Speed:   {:.1} kts", rmc.sog_knots.unwrap());
                            println!("Bearing: {}°", rmc.bearing.unwrap());
                            println!("Time:    {}", rmc.timestamp.unwrap());
                            //println!("");
                        }
                        ParsedMessage::Gsa(gsa) => {
                            //println!("Source: {}", gsa.source);
                            println!("PDOP:   {}", gsa.pdop.unwrap());
                            println!("HDOP:   {}", gsa.hdop.unwrap());
                            println!("VDOP:   {}", gsa.vdop.unwrap());
                            //println!("");
                        }
                        ParsedMessage::Gsv(gsv) => {
                            println!("DBG: {:?}", gsv);
                        }
                        ParsedMessage::Vtg(vtg) => {
                            //println!("Source: {}", vtg.source);
                            println!("Bearing: {}°", vtg.cog_true.unwrap());
                            println!("Speed:   {:.1} kph", vtg.sog_kph.unwrap());
                            //println!("");
                        }
                        ParsedMessage::Incomplete => {
                            //println!("data incomplete {:?}", sentence);
                        }
                        _ => {
                            //println!("{:?}", sentence);
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
