<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Connect-a-tron</title>

  <link rel="stylesheet" href="styles.css">
</head>

<body>

<div id="page-title">
  <h1>CONNECT-A-TRON</h1>
</div>

<h2>Keithley 2000</h1>
<p id="measure_result">Ready for measurement...</p>
<button id="measure_button">Measure</button>

</body>

<script>
const measure_url = "http://127.0.0.1:8000/dmm/keithley2000/measure/1";

const measure_result = document.getElementById("measure_result");

document.getElementById("measure_button").onclick = () => {
  measure_result.innerHTML = "Measuring...";
  fetch(measure_url).then(function(response) {
    return response.json();
  }).then(function(data) {
    measure_result.innerHTML = `${data} V`;
  }).catch(function(err) {
    measure_result.innerHTML = "ERROR OCURRED DURING MEASUREMENT"
    console.error(`Fetch Error: ${err}`);
  });
}
</script>

</html>
