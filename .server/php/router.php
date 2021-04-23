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
        if(isset($_POST['redir_url'])){
            header('Location: ' . $_POST['redir_url']);
            die();
        }
        echo "<b>Error 503:</b> Service Unavailable, try again later.";
        return true;
        break;
    
    default:
        return false;
        break;
}