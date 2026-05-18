<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Connect-a-tron</title>

  <link rel="stylesheet" href="styles.css" title="Default (Dark)"/>
</head>

<body>
<div id="page_title"><h1>CONNECT-A-TRON</h1></div>

<div id="instruments">
  <div class="instrument" id="keithley2000">
    <div class="name"><h2>Keithley 2000</h2></div>
    <div class="result" id="result_keithley2000">
      <a>-</a><a>-</a><a>-</a><a>-.</a><a>-</a><a>-</a><a>-</a><a></a><a>V</a><a>D</a><a>C</a>
    </div>
    <div class="settings">
      <button class="measure_button" id="measure_button_keithley2000">Measure</button>
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
      <div class="measure_option" id="filter_keithley2000">
        <label class="measure_option_label" for="measure_samples_number_keithley2000">Filter Samples</label>
        <input class="measure_option_number" id="measure_samples_number_keithley2000" name="measure_samples_number_keithley2000" type="number" min="1" max="100" value="1"/>
        <input class="measure_option_slider" id="measure_samples_slider_keithley2000" type="range" min="1" max="100" value="1" step="1"/>
        <select class="measure_type" id="measure_filter_type_keithley2000">
          <option value="0" selected>Repeat Average</option>
          <option value="1">Moving Average</option>
        </select>
      </div>
      <div class="measure_option" id="nplc_keithley2000">
        <label class="measure_option_label" for="measure_nplc_number_keithley2000">NPLC</label>
        <input class="measure_option_number" id="measure_nplc_number_keithley2000" name="measure_nplc_number_keithley2000" type="number" min="0.01" max="10" value="10"/>
        <input class="measure_option_slider" id="measure_nplc_slider_keithley2000" type="range" min="0.01" max="10" value="10" step="0.01"/>
      </div>
      <div class="measure_option" id="threshold_keithley2000" style="display: none">
        <label class="measure_option_label" for="measure_threshold_number_keithley2000">Threshold (Ω)</label>
        <input class="measure_option_number" id="measure_threshold_number_keithley2000" name="measure_threshold_number_keithley2000" type="number" min="1" max="1000" value="10"/>
        <input class="measure_option_slider" id="measure_threshold_slider_keithley2000" type="range" min="1" max="1000" value="10" step="1"/>
      </div>
      <div class="measure_option" id="bandwidth_keithley2000" style="display: none">
        <label class="measure_option_label" for="measure_bandwidth_number_keithley2000">Bandwidth (Hz)</label>
        <input class="measure_option_number" id="measure_bandwidth_number_keithley2000" name="measure_bandwidth_number_keithley2000" type="number" min="3" max="300000" value="30"/>
        <input class="measure_option_slider" id="measure_bandwidth_slider_keithley2000" type="range" min="3" max="300000" value="30" step="1"/>
      </div>
    </div>
  </div>
</div>
</body>

<script>
const murl = 'http://127.0.0.1:8000/dmm/keithley2000/measure/';

const result_keithley2000 = document.getElementById('result_keithley2000');
const measure_type_keithley2000 = document.getElementById('measure_type_keithley2000');

const measure_samples_number_keithley2000 = document.getElementById('measure_samples_number_keithley2000');
const measure_samples_slider_keithley2000 = document.getElementById('measure_samples_slider_keithley2000');
const measure_filter_type_keithley2000 = document.getElementById('measure_filter_type_keithley2000');

const measure_nplc_number_keithley2000 = document.getElementById('measure_nplc_number_keithley2000');
const measure_nplc_slider_keithley2000 = document.getElementById('measure_nplc_slider_keithley2000');

const div_threshold_keithley2000 = document.getElementById('threshold_keithley2000');
const measure_threshold_number_keithley2000 = document.getElementById('measure_threshold_number_keithley2000');
const measure_threshold_slider_keithley2000 = document.getElementById('measure_threshold_slider_keithley2000');

const div_bandwidth_keithley2000 = document.getElementById('bandwidth_keithley2000');
const measure_bandwidth_number_keithley2000 = document.getElementById('measure_bandwidth_number_keithley2000');
const measure_bandwidth_slider_keithley2000 = document.getElementById('measure_bandwidth_slider_keithley2000');

const symbols = [ // Symbols the DMM uses for each measurement type
  "", // Filler so it's 1-indexed
  "VDC",
  "VAC",
  "ADC",
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
  let fsamples = parseInt(measure_samples_number_keithley2000.value);
  let ftype = measure_filter_type_keithley2000.value !== "0";
  let nplc = parseFloat(measure_nplc_number_keithley2000.value);
  let thr = parseFloat(measure_threshold_number_keithley2000.value);
  let bandwidth = parseInt(measure_bandwidth_number_keithley2000.value);
  let start_text = `----.---${symbols[mtype]}`;
  let html = '';
  for (const digit in start_text) html += start_text[digit] == '.' ? '.' : `${digit === 0 ? '' : '</a>'}<a>${start_text[digit]}`;
  result_keithley2000.innerHTML = html + '</a>';
  fetch(`${murl}${mtype}?nplc=${nplc}&samples=${fsamples}&mov=${ftype}&thr=${thr}&bandwidth=${bandwidth}`).then(function(response) {
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

measure_type_keithley2000.addEventListener('change', () => {
  if (measure_type_keithley2000.value === '11') div_threshold_keithley2000.style = 'display: block';
  else div_threshold_keithley2000.style = 'display: none';

  if (['2', '4'].includes(measure_type_keithley2000.value)) div_bandwidth_keithley2000.style = 'display: block';
  else div_bandwidth_keithley2000.style = 'display: none';
});

// Sync sliders and number displays
measure_samples_slider_keithley2000.addEventListener('input', () => {
  measure_samples_number_keithley2000.value = measure_samples_slider_keithley2000.value;
});

measure_samples_number_keithley2000.addEventListener('input', () => {
  measure_samples_slider_keithley2000.value = measure_samples_number_keithley2000.value;
});

measure_nplc_slider_keithley2000.addEventListener('input', () => {
  measure_nplc_number_keithley2000.value = measure_nplc_slider_keithley2000.value;
});

measure_nplc_number_keithley2000.addEventListener('input', () => {
  measure_nplc_slider_keithley2000.value = measure_nplc_number_keithley2000.value;
});

measure_threshold_slider_keithley2000.addEventListener('input', () => {
  measure_threshold_number_keithley2000.value = measure_threshold_slider_keithley2000.value;
});

measure_threshold_number_keithley2000.addEventListener('input', () => {
  measure_threshold_slider_keithley2000.value = measure_threshold_number_keithley2000.value;
});

measure_bandwidth_slider_keithley2000.addEventListener('input', () => {
  measure_bandwidth_number_keithley2000.value = measure_bandwidth_slider_keithley2000.value;
});

measure_bandwidth_number_keithley2000.addEventListener('input', () => {
  measure_bandwidth_slider_keithley2000.value = measure_bandwidth_number_keithley2000.value;
});
</script>
</html>
