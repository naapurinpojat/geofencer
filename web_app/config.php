<?php
    require_once 'credentials.php';
    $mysqlserver = getenv('SQL_SERVER');

    if ($mysqlserver !== false) {
        $servername = $mysqlserver;
    } else {
        $servername = "localhost";
    }
?>