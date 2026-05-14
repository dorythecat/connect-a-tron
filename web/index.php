<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Connect-a-tron</title>

  <link rel="stylesheet" href="styles.css">
</head>

<body>

<div id="page_title">
  <h1>CONNECT-A-TRON</h1>
</div>

<div id="instruments">
  <div class="instrument" id="keithley2000">
    <div class="name">
      <h2>Keithley 2000</h1>
    </div>
    <p id="result_keithley2000">
    </p>
    <button id="measure_button">Measure</button>
  </div>
</div>

</body>

<script>
const measure_url = "http://127.0.0.1:8000/dmm/keithley2000/measure/1";

const result_keithley2000 = document.getElementById("result_keithley2000");

document.getElementById("measure_button").onclick = () => {
  result_keithley2000.innerHTML = "----.--- VDC";
  fetch(measure_url).then(function(response) {
    return response.json();
  }).then(function(data) {
    data = parseFloat(data);
    console.log(data);
    if (data <= 0.1) {
      data = (data * 1000).toFixed(4);
      while (String(data).length < 8) data = `0${data}`;
      result_keithley2000.innerHTML = `${data}mVDC`;
    } else {
      data = data.toFixed(5 - Math.floor(Math.log10(data)));
      while (String(data).length < 8) data = `0${data}`;
      result_keithley2000.innerHTML = `${data} VDC`;
    }
  }).catch(function(err) {
    result_keithley2000.innerHTML = "ERROR OCURRED DURING MEASUREMENT"
    console.error(`Fetch Error: ${err}`);
  });
}
</script>

</html>
