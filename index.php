<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Connect-a-tron</title>
</head>

<body>

<?php
const BASE_URL = 'http://127.0.0.1:8000/dmm/keithley2000';

$ch = curl_init();
curl_setopt_array($ch, [
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_URL => BASE_URL
]);
$name = curl_exec($ch);
curl_close($ch);
echo "<h1>$name</h1>";

  if(isset($_POST['measure'])) {
    $ch = curl_init();
    curl_setopt_array($ch, [
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_URL => BASE_URL . "/measure/1" # Measure DC Voltage
    ]);
    $measure = curl_exec($ch);
    curl_close($ch);
    echo "<p>$measure VDC</p>";
  }
?>

<form method="post">
  <input type="submit" name="measure" value="Measure"/>
</form>

</body>
</html>
