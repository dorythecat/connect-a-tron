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
    <div class="name"><h2>Keithley 2000</h1></div>
    <div class="result" id="result_keithley2000">
      <a>-</a><a>-</a><a>-</a><a>-.</a><a>-</a><a>-</a><a>-</a><a></a><a>V</a><a>D</a><a>C</a>
    </div>
    <button id="measure_button_keithley2000">Measure</button>
    <select class="measure_type" id="measure_type_keithley2000">
      <option value="1" selected>DC Voltage</option>
      <option value="2">AC Voltage</option>
      <option value="3">DC Current</option>
      <option value="4">AC Current</option>
      <option value="5">Resistance</option>
      <option value="6">4-Wire Kelvin</option>
      <option value="7">Temperature</option>
      <option value="8">Period</option>
      <option value="9">Frequency</option>
      <option value="10">Diode</option>
      <option value="11">Continuity</option>
    </select>
  </div>
</div>

</body>

<script>
const murl = 'http://127.0.0.1:8000/dmm/keithley2000/measure/';

const result_keithley2000 = document.getElementById('result_keithley2000');
const measure_type_keithley2000 = document.getElementById('measure_type_keithley2000');

const symbols = [ // Symbols the DMM uses for each measurement type
  "", // Filler so it's 1-indexed
  "VDC",
  "VAC",
  "ADC", // TODO: Support bandwidth options
  "AAC",
  "OHM",
  "OHM",
  "ºC", // TODO: We need to support all of the options the DMM accepts
  "SEC",
  "HZ",
  "VDC",
  "OHM"
];

document.getElementById('measure_button_keithley2000').onclick = () => {
  let mtype = parseInt(measure_type_keithley2000.value);
  let start_text = `----.---${symbols[mtype]}`;
  let html = '';
  for (const digit in start_text) html += start_text[digit] == '.' ? '.' : `${digit == 0 ? '' : '</a>'}<a>${start_text[digit]}`;
  result_keithley2000.innerHTML = html + '</a>';
  fetch(murl + mtype).then(function(response) {
    return response.json();
  }).then(function(data) {
    data = parseFloat(data);
    if (data > 1e20) data = mtype === 11 ? 'OPEN' : [8, 9].includes(mtype) ? `OVRFLW  ${symbols[mtype]}` : 'OVR.FLW MOHM';
    else {
      let mega = data > 100000 && [5, 6].includes(mtype);
      let kilo = data > (mtype === 9 ? 1000 : 100) && [5, 6, 9].includes(mtype);
      let milli = Math.abs(data) <= ([8, 9].includes(mtype) ? 1 : 0.1) && [1, 2, 3, 8, 9].includes(mtype);
      let millii = Math.abs(data) <= 0.01 && mtype === 3;
      let micro = data <= 0.001 && mtype === 8;
      let og_data = data;
      data *= (micro ? 1000 : 1) * (milli ? 1000 : 1) * (kilo ? 0.001 : 1) * (mega ? 0.001 : 1);
      let digits = Math.min(5 - Math.floor(Math.log10(Math.abs(kilo ? data : og_data))), !kilo && [5, 6].includes(mtype) ? 4 : mtype === 10 ? 5 : 6, mtype === 11 ? 1 : 6) + ([8, 9].includes(mtype));
      data = String(data.toFixed(milli ? (micro ? 6 - Math.floor(Math.log10(data)) : 4 + millii) : digits));
      while (data.length < ((mtype == 11 ? 6 : 8) + data.startsWith('-'))) data = data.startsWith('-') ? `-0${data.slice(1)}` : `0${data}`;
      data += `${mega ? 'M' : (kilo ? 'K' : (micro ? 'μ' : (milli ? 'm' : (mtype === 11 ? '   ' : ' '))))}${symbols[mtype]}`;
    }

    let html = '';
    for (const digit in data) html += data[digit] === '.' ? '.' : `${digit ? '</a>' : ''}<a>${data[digit]}`;
    result_keithley2000.innerHTML = html + '</a>';
  }).catch(function(err) { console.error(`Fetch Error: ${err}`); });
}
</script>
</html>
