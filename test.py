from pynmeagps import NMEAReader                                                                                                          
import json

stream = open('/dev/EG25.NMEA', 'rb')
nmr = NMEAReader(stream, nmeaonly=True)
for (raw_data, parsed_data) in nmr:
        try:
                if parsed_data.identity == 'GPGGA':
                        if parsed_data.quality == 1:
                                print(parsed_data)
        except:
                pass
