#!/bin/bash
echo "Testing API"
echo "Add data"
curl -X POST -H "apikey:0028b076-ca97-44c5-9603-bdfc38e2718e" -H "Content-Type: application/json" -d '{"lat": 62.8059224833, "lon": 22.9163893333, "alt": 44.2, "speed": 0, "ts": "2023-12-21T09:55:47.000Z", "in_area": "Kertunlaakso"}' localhost/snowdog/api/location
echo ""
echo "Get version"
curl -X GET -H "apikey:0028b076-ca97-44c5-9603-bdfc38e2718e" 'http://localhost/snowdog/api/version'
echo ""
#echo "Geofences"
curl -X GET -H "apikey:0028b076-ca97-44c5-9603-bdfc38e2718e" 'http://localhost/snowdog/api/geojson'
echo ""
echo "Last Online"
curl -X GET -H "apikey:0028b076-ca97-44c5-9603-bdfc38e2718e" 'http://localhost/snowdog/api/lastonline'
echo ""
