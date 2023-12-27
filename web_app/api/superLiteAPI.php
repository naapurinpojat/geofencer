<?php

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

    /**
     * This function is used to initialize the API
     */
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
                        $jsonData = file_get_contents('php://input');
                        $parsedData = json_decode($jsonData, true);
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
                 $handler->requestCallback($this->request);
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