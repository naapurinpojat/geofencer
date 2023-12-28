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

    function getSQLclause() {
        $this->sql = "INSERT INTO location_history (lat, lon, alt, speed, ts, in_area) VALUES ($this->lat, $this->lon, $this->alt, $this->speed, '$this->ts', '$this->in_area')";
        return $this->sql;
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
            return $sql;
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
function saveLocation($obj, $api) {
    if(isset($api->request['lat']) && isset($api->request['lon']) && isset($api->request['alt']) && isset($api->request['speed']) && isset($api->request['ts']) && isset($api->request['in_area'])) {
        $location = new Location(
            $api->request['lat'],
            $api->request['lon'],
            $api->request['alt'],
            $api->request['speed'],
            $api->request['ts'],
            $api->request['in_area']
        );
        if($location->storeLocation() != 0) {
            echo json_encode(array('status' => 'Ok'));
        }
        else {
            echo json_encode(array('status' => 'Error'));
        }
    }
    else {
        if($api->request != null) {
            $locations = array();
            foreach($api->request as $req) {
                if(isset($req['lat']) && isset($req['lon']) && isset($req['alt']) && isset($req['speed']) && isset($req['ts']) && isset($req['in_area'])) {
                    $location = new Location(
                        $req['lat'],
                        $req['lon'],
                        $req['alt'],
                        $req['speed'],
                        $req['ts'],
                        $req['in_area']
                    );
                    array_push($locations, $location);
                }
            }
            if(count($locations) > 0) {
                $conn = $api->connectDB();
                $rows = 0;
                foreach($locations as $location) {
                    $result = $conn->query($location->getSQLclause());
                    $rows += $conn->affected_rows;
                }
                $api->closeDB($conn);
                echo json_encode(array('status' => 'Ok', 'rows' => $rows));
            }
        }
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
    $json = [];
    $result = queryHelper('SELECT max(ts) as ts FROM `location_history`');
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
           $json['online'] = $row['ts'];
        }
    } else {

    }

    $result = queryHelper('SELECT * FROM route_percentage order by drive_date DESC LIMIT 1;');
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $json['driven'] = $row['drive_date'];
        }
    } else {

    }

    header('Content-Type: application/json');
    echo json_encode($json);
}

function lastDriven($obj, $request) {
    $result = queryHelper('SELECT * FROM route_percentage order by drive_date DESC LIMIT 1;');
    if ($result->num_rows > 0) {
        $json = [];
        while ($row = $result->fetch_assoc()) {
            $json['driven'] = $row['drive_date'];
        }
    } else {

    }

    header('Content-Type: application/json');
    echo json_encode($json);
}

/**
 * This function registers all the path handlers for the API 
 */
function snowdogAPI(){
    $api = new superLiteAPI(APIKEY);
    $api->registerPathHandler('version', 'GET', 'getVersion');
    $api->registerPathHandler('version/ui', 'GET', 'getVersion');
    $api->registerPathHandler('location', 'POST', 'saveLocation');
    $api->registerPathHandler('geojson', 'GET', 'getGeoJSON');
    $api->registerPathHandler('lastonline', 'GET', 'lastOnline');
    $api->registerPathHandler('lastdriven', 'GET', 'lastDriven');
    $api->runPathHandlers();
}

?>