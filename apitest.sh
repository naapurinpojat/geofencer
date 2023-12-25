#!/bin/bash
echo "Testing API"
echo "Add data"
curl -X POST -H "Content-Typ5: application/json" -d '{"lat": 62.8059224833, "lon": 22.9163893333, "alt": 44.2, "speed": 0, "ts": "2023-12-21T09:55:47.000Z", "api_key": "0028b076-ca97-44c5-9603-bdfc38e2718e", "in_area": "Kertunlaakso"}' localhost/snowdog/api.php
echo ""
echo "Get version"
curl -X GET 'http://localhost/snowdog/api.php?version'
echo ""
#echo "Geofences"
curl -X GET 'http://localhost/snowdog/api.php?geojson=1&api_key=1234'
echo ""
echo "Last Online"
curl -X GET 'http://localhost/snowdog/api.php?lastonline&api_key=1234'
echo ""
