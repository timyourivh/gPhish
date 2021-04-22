<?php

require_once('datahandler.php');


switch ($_SERVER["REQUEST_URI"]) {
    case '/':
        # index
        DataHandler::logIp();
        return false;
        break;
    case '/login':
        # index
        DataHandler::logLogin();
        return false;
        break;
    
    default:
        return false;
        break;
}