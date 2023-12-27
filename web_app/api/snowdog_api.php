<?php
require_once '../config.php';
require_once '../gitversion.php';
require_once 'superLiteAPI.php';

class Location {
    public $lat;
    public $lon;
    public $alt;
    public $speed;
    public $ts;
    public $in_area;
    private $valid = FALSE;
    private $conn;
    private $sql;


    function __construct($lat, $lon, $alt, $speed, $ts, $in_area) {
        $utcDateTime = new DateTime($ts, new DateTimeZone('UTC'));
        // Set the Helsinki time zone for conversion
        $helsinkiTimeZone = new DateTimeZone('Europe/Helsinki');
        $utcDateTime->setTimezone($helsinkiTimeZone);
        
        // Format the local time
        $formattedTs = $utcDateTime->format('Y-m-d H:i:s');

        $this->lat = $lat;
        $this->lon = $lon;
        $this->alt = $alt;
        $this->speed = $speed;
        $this->ts = $formattedTs;//$conn->real_escape_string($ts);
        $this->in_area = $in_area;
        $this->valid = TRUE;
    }

    function storeLocation() {
        if($this->valid == TRUE) {
            $conn = new mysqli(SERVER_NAME, USERNAME, PASSWORD, DBNAME);
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }
            // realescape values
            $this->lat = $conn->real_escape_string($this->lat);
            $this->lon = $conn->real_escape_string($this->lon);
            $this->alt = $conn->real_escape_string($this->alt);
            $this->speed = $conn->real_escape_string($this->speed);
            $this->ts = $conn->real_escape_string($this->ts);
            $this->in_area = $conn->real_escape_string($this->in_area);

            $sql = "INSERT INTO location_history (lat, lon, alt, speed, ts, in_area) VALUES ($this->lat, $this->lon, $this->alt, $this->speed, '$this->ts', '$this->in_area')";
                
            // Execute the query
            $conn->query($sql);
            $rows = $conn->affected_rows;
            // Close the connection
            $conn->close();
            return $rows;
        }
    }
}

/**
 * This function is used to execute a query and return the result
 
 */
function queryHelper($sql) {
    $conn = new mysqli(SERVER_NAME, USERNAME, PASSWORD, DBNAME);
    $result = $conn->query($sql);
    $conn->close();
    return $result;
}


/**
 * This function returns the version of the API
 */
function getVersion($obj, $request) {
    header('Content-Type: application/json');
    echo json_encode(array('version' => GIT_REVISION));
}

/**
 * This function saves the location of the user
 */
function saveLocation($obj, $request) {
    print_r($request);
    if ($request !== null && ($request['api_key'] === APIKEY || $request['apikey'] === APIKEY)) {
        if(isset($request['lat']) && isset($request['lon']) && isset($request['alt']) && isset($request['speed']) && isset($request['ts']) && isset($request['in_area'])) {
            $location = new Location(
                $request['lat'],
                $request['lon'],
                $request['alt'],
                $request['speed'],
                $request['ts'],
                $request['in_area']
            );
            
            if($location->storeLocation() != 0) {
                echo json_encode(array('status' => 'Ok'));
            }
            else {
                echo json_encode(array('status' => 'Error'));
            }

        }
        else {

        }
    } else {
        // If the request data is not valid, return an error
        http_response_code(400); // Bad Request
        echo json_encode(array('status' => 'Not all fields set'));
    }
}

function getGeoJSON($obj, $request) {
    $result = queryHelper('SELECT DISTINCT in_area, MAX(ts) AS latest_ts FROM location_history GROUP BY in_area;');

    if ($result->num_rows > 0) {

        $json = [];
        while ($row = $result->fetch_assoc()) {
            array_push($json, array('in_area' => $row['in_area'], 'latest_ts' => $row['latest_ts']));
        }

    } else {
        echo "{}";
    }

    header('Content-Type: application/json');
    echo json_encode($json);
}

function lastOnline($obj, $request) {
    $result = queryHelper('SELECT max(ts) as ts FROM `location_history`');
    if ($result->num_rows > 0) {

        $json = [];
        while ($row = $result->fetch_assoc()) {
            $json = array('online' => $row['ts']);
        }
    } else {
        echo "{}";
    }

    header('Content-Type: application/json');
    echo json_encode($json);
}

/**
 * This function registers all the path handlers for the API 
 */
function snowdogAPI(){
    $api = new Api();
    $api->registerPathHandler('version', 'GET', 'getVersion');
    $api->registerPathHandler('version/ui', 'GET', 'getVersion');
    $api->registerPathHandler('location', 'POST', 'saveLocation');
    $api->registerPathHandler('geojson', 'GET', 'getGeoJSON');
    $api->registerPathHandler('lastonline', 'GET', 'lastOnline');
    $api->runPathHandlers();
}

?>