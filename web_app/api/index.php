<?php

function parseRequestData() {
    // Check if the request method is POST
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        
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
            return $parsedData;
        } else {
            // Content Type header is not set
            return null;
        }
    } else {
        // This is not a POST request
        return null;
    }
}

function handleRequestByMethod() {
    switch ($_SERVER['REQUEST_METHOD']) {
        case 'GET':
            $request = $_GET;
            break;
        case 'POST':
            $request = parseRequestData();
            break;
        default:
            $request = null;
            break;
    }
    return $request;
}


$parts = array_slice(explode('/', $_SERVER['REQUEST_URI']), 3);
print_r($parts);
echo count($parts);
$request = handleRequestByMethod();
echo $_SERVER['REQUEST_METHOD'];
print_r($request);

?>
