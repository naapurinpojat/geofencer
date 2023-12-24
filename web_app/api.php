<?php
require_once 'config.php';
require_once 'gitversion.php';

define('DEBUG_PRINT', TRUE);
// Create a simple SVG image of a dog
function generateDogSvg($text) {
    $img = '<svg viewBox="0 0 1024 1024" class="icon" version="1.1" xmlns="http://www.w3.org/2000/svg" fill="#000000">';
    if(DEBUG_PRINT == TRUE) {
        $img = $img.'<text x="0" y="100" font-family="Courier" font-size="16" fill="black">'.$text.'</text>';
    }
    $img = $img.'<g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M432.4 453.5l-17 46.7h34.4z" fill="#FFFFFF"></path><path d="M725.3 259.7H312.2c-16.5 0-30 13.5-30 30v413.1c0 16.5 13.5 30 30 30h413.1c16.5 0 30-13.5 30-30V289.7c0-16.6-13.5-30-30-30z m-98.8 164.5h25.4V550h-25.4V424.2z m-116.5 0h40.8c15.5 0 25.5 0.6 30.2 1.9 7.2 1.9 13.2 6 18.1 12.3 4.9 6.3 7.3 14.5 7.3 24.5 0 7.7-1.4 14.2-4.2 19.5s-6.4 9.4-10.7 12.4c-4.3 3-8.7 5-13.2 6-6.1 1.2-14.8 1.8-26.4 1.8h-16.6V550H510V424.2z m-90.7 0h26.9L496.5 550h-27.6l-11-28.6h-50.3L397.2 550h-27l49.1-125.8z m229.1 273.3H352.6c-19.4 0-35.1-15.7-35.1-35.1v-295c0-5.5 4.5-10 10-10s10 4.5 10 10v295c0 8.3 6.8 15.1 15.1 15.1h295.8c5.5 0 10 4.5 10 10s-4.4 10-10 10z" fill="#FFFFFF"></path><path d="M569.4 479.2c3.4-1.3 6-3.4 7.9-6.2 1.9-2.8 2.9-6.1 2.9-9.8 0-4.6-1.3-8.4-4-11.3-2.7-3-6.1-4.8-10.2-5.6-3-0.6-9.1-0.9-18.3-0.9h-12.3v35.7h13.9c10 0.1 16.7-0.6 20.1-1.9z" fill="#FFFFFF"></path><path d="M648.4 677.5H352.6c-8.3 0-15.1-6.8-15.1-15.1v-295c0-5.5-4.5-10-10-10s-10 4.5-10 10v295c0 19.4 15.7 35.1 35.1 35.1h295.8c5.5 0 10-4.5 10-10s-4.4-10-10-10z" fill="#05ff65"></path><path d="M865 386.5c11 0 20-9 20-20s-9-20-20-20h-69.7v-56.8c0-38.6-31.4-70-70-70h-27.8v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3H611v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3h-46.5v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3H438v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3h-85.8c-38.6 0-70 31.4-70 70v56.8h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7V433h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7v46.5h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7V606h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7v56.8c0 38.6 31.4 70 70 70H343v72.5c0 11 9 20 20 20s20-9 20-20v-72.5h46.5v72.5c0 11 9 20 20 20s20-9 20-20v-72.5H516v72.5c0 11 9 20 20 20s20-9 20-20v-72.5h46.5v72.5c0 11 9 20 20 20s20-9 20-20v-72.5h82.8c38.6 0 70-31.4 70-70V646H865c11 0 20-9 20-20s-9-20-20-20h-69.7v-46.5H865c11 0 20-9 20-20s-9-20-20-20h-69.7V473H865c11 0 20-9 20-20s-9-20-20-20h-69.7v-46.5H865zM755.3 702.7c0 16.5-13.5 30-30 30H312.2c-16.5 0-30-13.5-30-30v-413c0-16.5 13.5-30 30-30h413.1c16.5 0 30 13.5 30 30v413z" fill="#283957"></path><path d="M407.6 521.4h50.3l11 28.6h27.6l-50.4-125.8h-26.9l-49 125.8h27l10.4-28.6z m24.8-67.9l17.3 46.7h-34.3l17-46.7zM535.4 502.6H552c11.5 0 20.3-0.6 26.4-1.8 4.5-1 8.9-3 13.2-6 4.3-3 7.9-7.1 10.7-12.4s4.2-11.8 4.2-19.5c0-10-2.4-18.2-7.3-24.5-4.9-6.3-10.9-10.4-18.1-12.3-4.7-1.3-14.8-1.9-30.2-1.9H510V550h25.4v-47.4z m0-57.1h12.3c9.2 0 15.2 0.3 18.3 0.9 4.1 0.7 7.5 2.6 10.2 5.6 2.7 3 4 6.8 4 11.3 0 3.7-1 7-2.9 9.8-1.9 2.8-4.6 4.9-7.9 6.2-3.4 1.3-10.1 2-20.1 2h-13.9v-35.8zM626.5 424.2h25.4V550h-25.4z" fill="#283957"></path></g></svg>';

    return $img;
}

function generateFailImage() {
    $img = '<svg viewBox="0 0 1024 1024" class="icon" version="1.1" xmlns="http://www.w3.org/2000/svg" fill="#000000">
    <g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M432.4 453.5l-17 46.7h34.4z" fill="#FFFFFF"></path><path d="M725.3 259.7H312.2c-16.5 0-30 13.5-30 30v413.1c0 16.5 13.5 30 30 30h413.1c16.5 0 30-13.5 30-30V289.7c0-16.6-13.5-30-30-30z m-98.8 164.5h25.4V550h-25.4V424.2z m-116.5 0h40.8c15.5 0 25.5 0.6 30.2 1.9 7.2 1.9 13.2 6 18.1 12.3 4.9 6.3 7.3 14.5 7.3 24.5 0 7.7-1.4 14.2-4.2 19.5s-6.4 9.4-10.7 12.4c-4.3 3-8.7 5-13.2 6-6.1 1.2-14.8 1.8-26.4 1.8h-16.6V550H510V424.2z m-90.7 0h26.9L496.5 550h-27.6l-11-28.6h-50.3L397.2 550h-27l49.1-125.8z m229.1 273.3H352.6c-19.4 0-35.1-15.7-35.1-35.1v-295c0-5.5 4.5-10 10-10s10 4.5 10 10v295c0 8.3 6.8 15.1 15.1 15.1h295.8c5.5 0 10 4.5 10 10s-4.4 10-10 10z" fill="#FFFFFF"></path><path d="M569.4 479.2c3.4-1.3 6-3.4 7.9-6.2 1.9-2.8 2.9-6.1 2.9-9.8 0-4.6-1.3-8.4-4-11.3-2.7-3-6.1-4.8-10.2-5.6-3-0.6-9.1-0.9-18.3-0.9h-12.3v35.7h13.9c10 0.1 16.7-0.6 20.1-1.9z" fill="#FFFFFF"></path><path d="M648.4 677.5H352.6c-8.3 0-15.1-6.8-15.1-15.1v-295c0-5.5-4.5-10-10-10s-10 4.5-10 10v295c0 19.4 15.7 35.1 35.1 35.1h295.8c5.5 0 10-4.5 10-10s-4.4-10-10-10z" fill="#ff0505"></path><path d="M865 386.5c11 0 20-9 20-20s-9-20-20-20h-69.7v-56.8c0-38.6-31.4-70-70-70h-27.8v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3H611v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3h-46.5v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3H438v-67.3c0-11-9-20-20-20s-20 9-20 20v67.3h-85.8c-38.6 0-70 31.4-70 70v56.8h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7V433h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7v46.5h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7V606h-69.7c-11 0-20 9-20 20s9 20 20 20h69.7v56.8c0 38.6 31.4 70 70 70H343v72.5c0 11 9 20 20 20s20-9 20-20v-72.5h46.5v72.5c0 11 9 20 20 20s20-9 20-20v-72.5H516v72.5c0 11 9 20 20 20s20-9 20-20v-72.5h46.5v72.5c0 11 9 20 20 20s20-9 20-20v-72.5h82.8c38.6 0 70-31.4 70-70V646H865c11 0 20-9 20-20s-9-20-20-20h-69.7v-46.5H865c11 0 20-9 20-20s-9-20-20-20h-69.7V473H865c11 0 20-9 20-20s-9-20-20-20h-69.7v-46.5H865zM755.3 702.7c0 16.5-13.5 30-30 30H312.2c-16.5 0-30-13.5-30-30v-413c0-16.5 13.5-30 30-30h413.1c16.5 0 30 13.5 30 30v413z" fill="#283957"></path><path d="M407.6 521.4h50.3l11 28.6h27.6l-50.4-125.8h-26.9l-49 125.8h27l10.4-28.6z m24.8-67.9l17.3 46.7h-34.3l17-46.7zM535.4 502.6H552c11.5 0 20.3-0.6 26.4-1.8 4.5-1 8.9-3 13.2-6 4.3-3 7.9-7.1 10.7-12.4s4.2-11.8 4.2-19.5c0-10-2.4-18.2-7.3-24.5-4.9-6.3-10.9-10.4-18.1-12.3-4.7-1.3-14.8-1.9-30.2-1.9H510V550h25.4v-47.4z m0-57.1h12.3c9.2 0 15.2 0.3 18.3 0.9 4.1 0.7 7.5 2.6 10.2 5.6 2.7 3 4 6.8 4 11.3 0 3.7-1 7-2.9 9.8-1.9 2.8-4.6 4.9-7.9 6.2-3.4 1.3-10.1 2-20.1 2h-13.9v-35.8zM626.5 424.2h25.4V550h-25.4z" fill="#283957"></path></g></svg>';
    return $img;
}

// Your data to be returned
$data = array(
    'message' => 'Hello, this is a simple PHP GET API!',
    'timestamp' => time()
);

// Set the content type to JSON


$apikey_string = '0028b076-ca97-44c5-9603-bdfc38e2718e';
// Check if it's a GET request
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['api_key']) && ($_GET['api_key'] === $apikey_string || $_GET['api_key'] === $apikey_string) && !isset($_GET['geojson'])) {
    header('Content-Type: image/svg+xml');

    // Generate and echo the SVG image
    echo generateDogSvg(json_encode($_GET));
    // Encode the data as JSON and output it
 
    //echo json_encode($_GET);
}
elseif($_SERVER['REQUEST_METHOD'] === 'GET' && !isset($_GET['api_key']) && isset($_GET['version'])) {
    header('Content-Type: application/json');
    echo json_encode(array('version' => GIT_REVISION));
}
elseif($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['api_key']) && isset($_GET['geojson'])) {

    // Assuming you have a database connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Fetch data from your_table_name
    $sql = 'SELECT DISTINCT in_area, MAX(ts) AS latest_ts FROM location_history GROUP BY in_area;';
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

        $json = [];
        while ($row = $result->fetch_assoc()) {
            array_push($json, array('in_area' => $row['in_area'], 'latest_ts' => $row['latest_ts']));
        }

    } else {
        echo "{}";
    }

    // Close the connection
    $conn->close();
    echo json_encode($json);


}
elseif($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['api_key']) && isset($_GET['lastonline'])) {

    // Assuming you have a database connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Fetch data from your_table_name
    $sql = 'SELECT max(ts) as ts FROM `location_history`';
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

        $json = [];
        while ($row = $result->fetch_assoc()) {
            $json = array('online' => $row['ts']);
        }

    } else {
        echo "{}";
    }

    // Close the connection
    $conn->close();
    echo json_encode($json);


}
/*

*/
elseif($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['api_key']) && isset($_GET['backdoor'])) {

    // Assuming you have a database connection


    $conn = new mysqli($servername, $username, $password, $dbname);

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
    print_r($phpObject);

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


}
elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $requestData = json_decode(file_get_contents("php://input"), true);

    // Check if the request data is valid
    if ($requestData !== null && ($requestData['api_key'] === $apikey_string || $requestData['apikey'] === $apikey_string)) {
        // Merge request data with the existing data
        //$data = array_merge($data, $requestData);
        $lat = $requestData['lat'];
        $lon = $requestData['lon'];
        $alt = $requestData['alt'];
        $speed = $requestData['speed'];
        $ts = $requestData['ts'];
        $in_area = $requestData['in_area'];

        $conn = new mysqli($servername, $username, $password, $dbname);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        //$formattedTs = date('Y-m-d H:i:s', strtotime($ts));

        $utcDateTime = new DateTime($ts, new DateTimeZone('UTC'));

        // Set the Helsinki time zone for conversion
        $helsinkiTimeZone = new DateTimeZone('Europe/Helsinki');
        $utcDateTime->setTimezone($helsinkiTimeZone);
        
        // Format the local time
        $formattedTs = $utcDateTime->format('Y-m-d H:i:s');


        // Create INSERT statement
        $lat = $conn->real_escape_string($lat);
        $lon = $conn->real_escape_string($lon);
        $alt = $conn->real_escape_string($alt);
        $speed = $conn->real_escape_string($speed);
        $ts = $formattedTs;//$conn->real_escape_string($ts);
        $in_area = $conn->real_escape_string($in_area);
        
        // Create INSERT statement without prepare
        $sql = "INSERT INTO location_history (lat, lon, alt, speed, ts, in_area) VALUES ($lat, $lon, $alt, $speed, '$ts', '$in_area')";
        echo $sql;
        
        
        // Execute the query
        $conn->query($sql);
        
        // Close the connection
        $conn->close();


        echo json_encode(array('status' => 'Ok'));
    } else {
        // If the request data is not valid, return an error
        http_response_code(400); // Bad Request
        echo json_encode(array('status' => 'Invalid JSON data'));
    }
}
else {
    //header('Content-Type: application/json');
    // If it's not a GET request, return an error
    header('Content-Type: image/svg+xml');
    //http_response_code(405); // Method Not Allowed
    echo generateFailImage();
    //echo json_encode(array('error' => 'Method not allowed'));
}
?>
