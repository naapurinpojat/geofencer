use nmea_parser::*;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use redis::{Client, Commands, Connection, RedisResult};
use std::time::Duration;

fn main() {
    // Replace "/dev/EG25.NMEA" with the appropriate device file on your system
    let device_path = "/dev/rfcomm0";

    // Create a channel for communication between producer and consumer threads
    let (tx, rx) = mpsc::channel::<String>();
    let rx = Arc::new(Mutex::new(rx));

    // Spawn the producer thread
    let producer_handle = thread::spawn(move || {
        produce_lines(device_path, tx);
    });

    // Spawn the consumer thread
    let consumer_handle = thread::spawn(move || {
        consume_lines(rx);
    });

    // Wait for both threads to finish
    producer_handle.join().unwrap();
    consumer_handle.join().unwrap();
}

fn produce_lines(device_path: &str, sender: mpsc::Sender<String>) {
    let file = match File::open(device_path) {
        Ok(file) => file,
        Err(err) => {
            eprintln!("Error opening device file '{}': {:?}", device_path, err);
            return;
        }
    };

    let reader = BufReader::new(file);

    println!("Reading from device file '{}'", device_path);

    for line in reader.lines() {
        match line {
            Ok(line) => {
                if sender.send(line).is_err() {
                    // The consumer has disconnected, exit the loop
                    break;
                }
            }
            Err(err) => {
                if err.kind() == io::ErrorKind::TimedOut {
                    eprintln!("Timeout reading from device file");
                } else {
                    eprintln!("Error reading from device file: {:?}", err);
                }
                break;
            }
        }

        // Add a delay (you can adjust the duration as needed)
        // thread::sleep(Duration::from_millis(100));
    }
}

fn set_key_value(connection: &mut Connection, key: &str, value: &str) -> RedisResult<()> {
    // Set the key-value pair in Redis
    connection.set(key, value)
}

fn consume_lines(rx: Arc<Mutex<mpsc::Receiver<String>>>) {
    let mut parser = NmeaParser::new();
    //let client = Client::open("redis://127.0.0.1/").expect("Failed to connect to Redis");
    //let mut connection = client.get_connection().expect("Failed to get connection");

    loop {
        let received_line = rx.lock().unwrap().recv();
        match received_line {
            Ok(line) => {
                // Process the received line (print it in this case)
                if parser.parse_sentence(&line).is_ok() {
                    match parser.parse_sentence(&line).ok() {
                        Some(ParsedMessage::VesselDynamicData(vdd)) => {
                            println!("MMSI:    {}", vdd.mmsi);
                            println!("Speed:   {:.1} kts", vdd.sog_knots.unwrap_or_default());
                            println!("Heading: {}°", vdd.heading_true.unwrap_or_default());
                            //gps_data.heading = vdd.heading_true.unwrap_or_default();
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
                            //gps_data.latitude = gga.latitude.unwrap_or_default();
                            //gps_data.longitude = gga.longitude.unwrap_or_default();
                            //gps_data.altitude = gga.altitude.unwrap_or_default();

                            //println!("");
                        }
                        Some(ParsedMessage::Rmc(rmc)) => {
                            //println!("Source:  {}", rmc.source);
                            println!("Speed:   {:.1} kts", rmc.sog_knots.unwrap_or_default());
                            println!("Bearing: {}°", rmc.bearing.unwrap_or_default());
                            println!("Time:    {}", rmc.timestamp.unwrap_or_default());
                            //gps_data.timestamp = rmc.timestamp.unwrap_or_default().to_string();
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
                            //gps_data.speed = vtg.sog_kph.unwrap_or_default();
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
            Err(_) => {
                // The producer has disconnected, exit the loop
                break;
            }
        }
    }
}
