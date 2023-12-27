<?php
require_once '../config.php';
require_once '../gitversion.php';

class PathHandler{
    public $path;
    public $method;
    public $handler;

    public function __construct($path, $method, $handler) {
        $this->path = $path;
        $this->method = $method;
        $this->handler = $handler;
    }
    public function requestCallback($request) {
        call_user_func($this->handler, $this, $request);
    }
}

class Api {

    private $pathHandlers = array();
    private $path = null;
    private $methods = array('GET', 'POST', 'PUT', 'DELETE');
    private $method = null;
    public $request = null;
    public function __construct() {
        $this->path = array_slice(explode('/', $_SERVER['REQUEST_URI']), 3);
        $this->method = $_SERVER['REQUEST_METHOD'];
        if ($this->method === 'POST') {

            // Check if the "Content-Type" header is set
            if (isset($_SERVER['CONTENT_TYPE'])) {
                
                $contentType = $_SERVER['CONTENT_TYPE'];
   
                // Parse data based on content type
                switch ($contentType) {
                    case 'application/json':
                        // Parse JSON data
                        $jsonData = file_get_contents('php://input');
                        $parsedData = json_decode($jsonData, true);
                        break;
                    
                    case 'application/x-www-form-urlencoded':
                        // Parse form data
                        $parsedData = $_POST;
                        break;
                    
                    default:
                        // Unsupported content type
                        $parsedData = null;
                        break;
                }
                $this->request = $parsedData;
            } else {
                // Content Type header is not set
                $this->request = null;
            }
        } 
        elseif ($this->method === 'GET') {
            $this->request = $_GET;
        }
        else {
            // This is not a POST request
            $this->request = null;
        }
    }

    public function registerPathHandler($path, $method, $handler) {
        array_push($this->pathHandlers, new PathHandler($path, $method, $handler));
    }

    public function runPathHandlers() {
        foreach($this->pathHandlers as $handler) {
            $pathstr = implode("/", $this->path);
            if($handler->path === $pathstr && $handler->method == $this->method) {
                 $handler->requestCallback($this->request);
            }
        }
    }

    public function printHandlers() {
        print_r($this->pathHandlers);
    }
}

function getVersion($obj, $request) {
    header('Content-Type: application/json');
    echo json_encode(array('version' => GIT_REVISION));
}

function saveLocation($obj, $request) {
    print_r($request);
}

$api = new Api();
//print_r($api);
$api->registerPathHandler('version', 'GET', 'getVersion');
$api->registerPathHandler('version/ui', 'GET', 'getVersion');
$api->registerPathHandler('location', 'POST', 'saveLocation');
//$api->printHandlers();
//$path = array_slice(explode('/', $_SERVER['REQUEST_URI']), 3);

$api->runPathHandlers();

?>
