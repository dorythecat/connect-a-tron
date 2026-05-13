<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Connect-a-tron</title>
</head>

<body>

<?php
const BASE_URL = 'http://127.0.0.1:8000';

$ch = curl_init();
curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_URL => BASE_URL . '/dmm/keithley2000'
]);
$response = curl_exec($ch);
curl_close($ch);
echo $response;
?>

</body>
</html>
