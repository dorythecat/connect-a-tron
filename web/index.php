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
        <h3 class="measure_option_label">Filter Samples</h3>
        <input class="measure_option_number" id="measure_samples_number_keithley2000" type="number" min="1" max="100" value="1"/>
        <input class="measure_option_slider" id="measure_samples_slider_keithley2000" type="range" min="1" max="100" value="1" step="1"/>
        <select class="measure_type" id="measure_filter_type_keithley2000">
          <option value="0" selected>Repeat Average</option>
          <option value="1">Moving Average</option>
        </select>
      </div>
      <div class="measure_option" id="nplc_keithley2000">
        <h3 class="measure_option_label">NPLC</h3>
        <input class="measure_option_number" id="measure_nplc_number_keithley2000" type="number" min="0.01" max="10" value="10"/>
        <input class="measure_option_slider" id="measure_nplc_slider_keithley2000" type="range" min="0.01" max="10" value="10" step="0.01"/>
      </div>
      <div class="measure_option" id="threshold_keithley2000" style="display: none">
        <h3 class="measure_option_label">Threshold (Ω)</h3>
        <input class="measure_option_number" id="measure_threshold_number_keithley2000" type="number" min="1" max="1000" value="10"/>
        <input class="measure_option_slider" id="measure_threshold_slider_keithley2000" type="range" min="1" max="1000" value="10" step="1"/>
      </div>
      <div class="measure_option" id="bandwidth_keithley2000" style="display: none">
        <h3 class="measure_option_label">Bandwidth (Hz)</h3>
        <input class="measure_option_number" id="measure_bandwidth_number_keithley2000" type="number" min="3" max="300000" value="30"/>
        <input class="measure_option_slider" id="measure_bandwidth_slider_keithley2000" type="range" min="3" max="300000" value="30" step="1"/>
      </div>
      <div class="measure_option" id="temp_main_keithley2000" style="display: none">
        <h3 class="measure_option_label">Thermocouple settings</h3>
        <select class="measure_type" id="measure_temp_type_keithley2000">
          <option value="J" selected>J Type</option>
          <option value="K">K Type</option>
          <option value="T">T Type</option>
        </select>
        <select class="measure_type" id="measure_temp_ref_keithley2000">
          <option value="0" selected>Simulated junction</option>
          <option value="1">Real junction</option>
        </select>
      </div>
      <div class="measure_option" id="temp_sim_keithley2000" style="display: none">
        <h3 class="measure_option_label">Simulated junction temperature</h3>
        <input class="measure_option_number" id="measure_temp_sim_number_keithley2000" type="number" min="0" max="50" value="23"/>
        <input class="measure_option_slider" id="measure_temp_sim_slider_keithley2000" type="range" min="0" max="50" value="23" step="1"/>
      </div>
      <div class="measure_option" id="temp_real_coef_keithley2000" style="display: none">
        <h3 class="measure_option_label">Real junction temperature coefficient</h3>
        <input class="measure_option_number" id="measure_temp_coef_number_keithley2000" type="number" min="-0.0999" max="0.0999" value="0.0002"/>
        <input class="measure_option_slider" id="measure_temp_coef_slider_keithley2000" type="range" min="-0.0999" max="0.0999" value="0.0002" step="0.0001"/>
      </div>
      <div class="measure_option" id="temp_real_voff_keithley2000" style="display:none">
        <h3 class="measure_option_label">Real junction voltage offset</h3>
        <input class="measure_option_number" id="measure_temp_voff_number_keithley2000" type="number" min="-0.0999" max="0.0999" value="0.05463"/>
        <input class="measure_option_slider" id="measure_temp_voff_slider_keithley2000" type="range" min="-0.0999" max="0.0999" value="0.05463" step="0.0001"/>
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

const div_temp_main_keithley2000 = document.getElementById('temp_main_keithley2000');
const measure_temp_type_keithley2000 = document.getElementById('measure_temp_type_keithley2000');
const measure_temp_ref_keithley2000 = document.getElementById('measure_temp_ref_keithley2000');

const div_temp_sim_keithley2000 = document.getElementById('temp_sim_keithley2000');
const measure_temp_sim_number_keithley2000 = document.getElementById('measure_temp_sim_number_keithley2000');
const measure_temp_sim_slider_keithley2000 = document.getElementById('measure_temp_sim_slider_keithley2000');

const div_temp_coef_keithley2000 = document.getElementById('temp_real_coef_keithley2000');
const measure_temp_coef_number_keithley2000 = document.getElementById('measure_temp_coef_number_keithley2000');
const measure_temp_coef_slider_keithley2000 = document.getElementById('measure_temp_coef_slider_keithley2000');

const div_temp_voff_keithley2000 = document.getElementById('temp_real_voff_keithley2000');
const measure_temp_voff_number_keithley2000 = document.getElementById('measure_temp_voff_number_keithley2000');
const measure_temp_voff_slider_keithley2000 = document.getElementById('measure_temp_voff_slider_keithley2000');

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
  let ftype = measure_filter_type_keithley2000.value !== '0';
  let nplc = parseFloat(measure_nplc_number_keithley2000.value);
  let thr = parseFloat(measure_threshold_number_keithley2000.value);
  let bandwidth = parseInt(measure_bandwidth_number_keithley2000.value);
  let ttype = measure_temp_type_keithley2000.value;
  let tref = measure_temp_ref_keithley2000.value !== '0';
  let simtemp = parseInt(measure_temp_sim_number_keithley2000.value);
  let tcoef = parseFloat(measure_temp_coef_number_keithley2000.value);
  let voff = parseFloat(measure_temp_voff_number_keithley2000.value);
  let start_text = `----.---${symbols[mtype]}`;
  let html = '';
  for (const digit in start_text) html += start_text[digit] == '.' ? '.' : `${digit === 0 ? '' : '</a>'}<a>${start_text[digit]}`;
  result_keithley2000.innerHTML = html + '</a>';
  fetch(`${murl}${mtype}?nplc=${nplc}&samples=${fsamples}&mov=${ftype}&thr=${thr}&bandwidth=${bandwidth}&ttype=${ttype}&tref=${tref}&simtemp=${simtemp}&tcoef=${tcoef}&voff=${voff}`).then(function(response) {
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

// TODO: This function should run on reaload too, so some abstraction would be great too
measure_type_keithley2000.addEventListener('change', () => { // This thing could probably be optimized a bunch imo
  if (measure_type_keithley2000.value === '11') div_threshold_keithley2000.style = 'display: block';
  else div_threshold_keithley2000.style = 'display: none';

  if (['2', '4'].includes(measure_type_keithley2000.value)) div_bandwidth_keithley2000.style = 'display: block';
  else div_bandwidth_keithley2000.style = 'display: none';

  if (measure_type_keithley2000.value === '7') {
    div_temp_main_keithley2000.style = 'display: block';
    if (measure_temp_ref_keithley2000.value === '0') {
      div_temp_sim_keithley2000.style = 'display: block';
      div_temp_coef_keithley2000.style = 'display: none';
      div_temp_voff_keithley2000.style = 'display: none';
    } else {
      div_temp_sim_keithley2000.style = 'display: none';
      div_temp_coef_keithley2000.style = 'display: block';
      div_temp_voff_keithley2000.style = 'display: block';
    }
  } else div_temp_main_keithley2000.style = 'display: none';
});

measure_temp_ref_keithley2000.addEventListener('change', () => {
  if (measure_temp_ref_keithley2000.value === '0') {
    div_temp_sim_keithley2000.style = 'display: block';
    div_temp_coef_keithley2000.style = 'display: none';
    div_temp_voff_keithley2000.style = 'display: none';
  } else {
    div_temp_sim_keithley2000.style = 'display: none';
    div_temp_coef_keithley2000.style = 'display: block';
    div_temp_voff_keithley2000.style = 'display: block';
  } 
});

// Sync sliders and number displays
measure_samples_slider_keithley2000.addEventListener('input', () => {
  measure_samples_number_keithley2000.value = measure_samples_slider_keithley2000.value;
});

measure_samples_number_keithley2000.addEventListener('input', () => {
  measure_samples_number_keithley2000.value = Math.max(1, Math.min(100, measure_samples_number_keithley2000.value));
  measure_samples_slider_keithley2000.value = measure_samples_number_keithley2000.value;
});

measure_nplc_slider_keithley2000.addEventListener('input', () => {
  measure_nplc_number_keithley2000.value = measure_nplc_slider_keithley2000.value;
});

measure_nplc_number_keithley2000.addEventListener('input', () => {
  measure_nplc_number_keithley2000.value = Math.max(0.01, Math.min(10, measure_nplc_number_keithley2000.value));
  measure_nplc_slider_keithley2000.value = measure_nplc_number_keithley2000.value;
});

measure_threshold_slider_keithley2000.addEventListener('input', () => {
  measure_threshold_number_keithley2000.value = measure_threshold_slider_keithley2000.value;
});

measure_threshold_number_keithley2000.addEventListener('input', () => {
  measure_threshold_number_keithley2000.value = Math.max(1, Math.min(1000, measure_threshold_number_keithley2000.value));
  measure_threshold_slider_keithley2000.value = measure_threshold_number_keithley2000.value;
});

measure_bandwidth_slider_keithley2000.addEventListener('input', () => {
  measure_bandwidth_number_keithley2000.value = measure_bandwidth_slider_keithley2000.value;
});

measure_bandwidth_number_keithley2000.addEventListener('input', () => {
  measure_bandwidth_number_keithley2000.value = Math.max(3, Math.min(300000, measure_bandwidth_number_keithley2000.value));
  measure_bandwidth_slider_keithley2000.value = measure_bandwidth_number_keithley2000.value;
});

measure_temp_sim_slider_keithley2000.addEventListener('input', () => {
  measure_temp_sim_number_keithley2000.value = measure_temp_sim_slider_keithley2000.value;
});

measure_temp_sim_number_keithley2000.addEventListener('input', () => {
  measure_temp_sim_number_keithley2000.value = Math.max(0, Math.min(50, measure_temp_sim_number_keithley2000.value));
  measure_temp_sim_slider_keithley2000.value = measure_temp_sim_number_keithley2000.value;
});

measure_temp_coef_slider_keithley2000.addEventListener('input', () => {
  measure_temp_coef_number_keithley2000.value = measure_temp_coef_slider_keithley2000.value;
});

measure_temp_coef_number_keithley2000.addEventListener('input', () => {
  measure_temp_coef_number_keithley2000.value = Math.max(-0.0999, Math.min(0.0999, measure_temp_coef_number_keithley2000.value));
  measure_temp_coef_slider_keithley2000.value = measure_temp_coef_number_keithley2000.value;
});

measure_temp_voff_slider_keithley2000.addEventListener('input', () => {
  measure_temp_voff_number_keithley2000.value = measure_temp_voff_slider_keithley2000.value;
});

measure_temp_voff_number_keithley2000.addEventListener('input', () => {
  measure_temp_voff_number_keithley2000.value = Math.max(-0.0999, Math.min(0.0999, measure_temp_voff_number_keithley2000.value));
  measure_temp_voff_slider_keithley2000.value = measure_temp_voff_number_keithley2000.value;
});
</script>
</html>
