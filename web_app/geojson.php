<?php
require_once 'config.php';
require_once 'gitversion.php';
$conn = new mysqli(SERVER_NAME, USERNAME, PASSWORD, DBNAME);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$jsonString = '{
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {},
        "geometry": {
          "coordinates": [
          ],
          "type": "LineString"
        }
      }
    ]
  }';

$phpObject = json_decode($jsonString);

// Fetch data from your_table_name
$sql = "SELECT * FROM location_history order by id";
$result = $conn->query($sql);

if ($result->num_rows > 0) {

  while ($row = $result->fetch_assoc()) {
    array_push($phpObject->features[0]->geometry->coordinates, array(floatval($row['lon']), floatval($row['lat'])));
  }
} else {
  echo "{}";
}

// Close the connection
$conn->close();
echo json_encode($phpObject);
