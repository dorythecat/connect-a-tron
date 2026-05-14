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
    <div id="result_keithley2000">
      <a class="digit">-</a>
      <a class="digit">-</a>
      <a class="digit">-</a>
      <a class="digit">-.</a>
      <a class="digit">-</a>
      <a class="digit">-</a>
      <a class="digit">-</a>
      <a class="digit">-</a>
    </div>
    <button id="measure_button">Measure</button>
  </div>
</div>

</body>

<script>
const measure_url = 'http://127.0.0.1:8000/dmm/keithley2000/measure/1';

const result_keithley2000 = document.getElementById('result_keithley2000');

document.getElementById('measure_button').onclick = () => {
  fetch(measure_url).then(function(response) {
    return response.json();
  }).then(function(data) {
    data = parseFloat(data);
    let microvolt = Math.abs(data) <= 0.1;
    data = String((data * (microvolt ? 1000 : 1)).toFixed(microvolt ? 4 : 5 - Math.floor(Math.log10(Math.abs(data)))));
    while (data.length < (8 + data.startsWith('-'))) data = data.startsWith('-') ? `-0${data.slice(1)}` : `0${data}`;

    let html = data.startsWith('-') ? '' : '<a class="digit">';
    for (const digit in data) html += data[digit] === '.' ? '.' : `</a><a class="digit">${data[digit]}`;
    result_keithley2000.innerHTML = html + '</a>';
  }).catch(function(err) {
    result_keithley2000.innerHTML = 'ERROR OCURRED DURING MEASUREMENT'
    console.error(`Fetch Error: ${err}`);
  });
}
</script>

</html>
