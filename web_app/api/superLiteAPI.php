<?php

class headerKeys {
    const APIKEY = 'apikey';
}

/**
 * This class is used to register path handlers for the API
 
 */
class PathHandler{
    public $path;
    public $method;
    public $handler;

    public function __construct($path, $method, $handler) {
        $this->path = $path;
        $this->method = $method;
        $this->handler = $handler;
    }
    public function requestCallback(superLiteAPI $api) {
        call_user_func($this->handler, $this, $api);
    }
}


class superLiteAPI {
    private $pathHandlers = array();
    private $path = null;
    private $method = null;
    private $headers = null;
    private $apikey = null;
    public $request = null;

    public function connectDB() {
        $conn = new mysqli(SERVER_NAME, USERNAME, PASSWORD, DBNAME);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        return $conn;
    }

    public function closeDB($conn) {
        $conn->close();
    }

    public function queryDB($conn, $sql) {
        $result = $conn->query($sql);
        return $result;
    }

    public function prepareSQL($sql) {
        $conn = $this->connectDB();
        $result = $this->queryDB($conn, $sql);
        $this->closeDB($conn);
        return $result;
    }

    private function checkAPIKEY() {
        if(isset($this->headers[headerKeys::APIKEY]) && ($this->headers[headerKeys::APIKEY] === $this->apikey)) {
            return true;
        }
        else {
            return false;
        }
    }
    /**
     * This function is used to initialize the API
     */
    public function __construct($apikey) {
        $this->headers = getallheaders();
        if(isset($apikey)) {
            $this->apikey = $apikey;
            if(!$this->checkAPIKEY()) {
                http_response_code(401); // Unauthorized
                echo json_encode(array('status' => 'Unauthorized'));
                exit();
            }
        }
        $this->path = array_slice(explode('/', $_SERVER['REQUEST_URI']), 3);
        $this->method = $_SERVER['REQUEST_METHOD'];
        if ($this->method === 'POST') {

            // Check if the "Content-Type" header is set
            if (isset($_SERVER['CONTENT_TYPE'])) {
                $contentType = $_SERVER['CONTENT_TYPE'];
                // Parse data based on content type
                switch ($contentType) {
                    case 'application/json':
                    case 'application/octet-stream':
                        $rawData = file_get_contents('php://input');
                        if (substr($rawData, 0, 2) === "\x1f\x8b") {
                            // Data is Gzip-encoded, decode it
                             $parsedData = json_decode(gzdecode($rawData), true);
                        }
                        else {
                            $parsedData = json_decode($jsonData, true);
                        }
                        break;
                    
                    case 'application/x-www-form-urlencoded':
                        $parsedData = $_POST;
                        break;
                   
                    default:
                        $parsedData = null;
                        break;
                }
                $this->request = $parsedData;
            } else {
                $this->request = null;
            }
        } 
        elseif ($this->method === 'GET') {
            $this->request = $_GET;
        }
        else {
            $this->request = null;
        }
    }

    /**
     * This function is used to register a path handler
     */
    public function registerPathHandler($path, $method, $handler) {
        array_push($this->pathHandlers, new PathHandler($path, $method, $handler));
    }

    /**
     * This function is used to run all the registered path handlers
     */
    public function runPathHandlers() {
        foreach($this->pathHandlers as $handler) {
            $pathstr = implode("/", $this->path);
            if($handler->path === $pathstr && $handler->method == $this->method) {
                 $handler->requestCallback($this);
            }
        }
    }

    /**
     * This function is used to print all the registered path handlers
     */
    public function printHandlers() {
        print_r($this->pathHandlers);
    }
}
 ?>