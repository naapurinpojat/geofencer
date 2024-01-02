<?php
require_once 'credentials.php';
$mysqlserver = getenv('SQL_SERVER');

if ($mysqlserver !== false) {
    define('SERVER_NAME', $mysqlserver);
} else {
    define('SERVER_NAME', "localhost");
}
