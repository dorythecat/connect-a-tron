<?php
$url = "http://127.0.0.1:8000/system/interfaces";

$headers = array(
  'Accept: application/json'
);

$context = stream_context_create([
  'http' => [
    'header' => $headers
  ]
]);

try {
  $response = (array) json_decode(file_get_contents($url, false, $context));

  if (!$response) throw new Exception("Could not fetch data from API!");

  $keithley2000_enable = in_array("keithley2000", $response["dmm"]);
  $hantek_dso2d15_enable = in_array("hantek_dso2d15", $response["oscilloscope"]);
} catch (Exception $e) {
  echo 'Exception found when loading webpage: ', $e->getMessage();
  exit(1);
}
?>
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
<?php
if ($keithley2000_enable) echo '<div class="instrument" id="keithley2000">';
else echo '<div class="instrument" style="display: none" id="keithley2000">';
?>
    <div class="name"><h2>Keithley 2000</h2></div>
    <div class="result" id="result_keithley2000">
      <a>-</a><a>-</a><a>-</a><a>-.</a><a>-</a><a>-</a><a>-</a><a></a><a>V</a><a>D</a><a>C</a>
    </div>
    <div id="front_panel_keithley2000">
      <div id="left_front_panel_keithley2000">
        <h3 class="key_label_keithley2000" id="shift_key_label_keithley2000">SHIFT</h3><button class="key_keithley2000" id="shift_key_keithley2000"></button>
        <h3 class="key_label_keithley2000">LOCAL</h3><button class="key_keithley2000" id="local_key_keithley2000"></button>
        <h3 id="power_key_label_keithley2000">POWER</h3><button class="key_keithley2000" id="power_key_keithley2000"></button>
      </div>
      <div id="center_front_panel_keithley2000">
        <div class="center_front_panel_row_keithley2000">
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">MX+B</h3><button class="top_button_keithley2000" id="dcv_button_keithley2000">DCV</button></div>
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">%</h3><button class="top_button_keithley2000" id="acv_button_keithley2000">ACV</button></div>
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">dBm</h3><button class="top_button_keithley2000" id="dci_button_keithley2000">DCI</button></div>
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">dB</h3><button class="top_button_keithley2000" id="aci_button_keithley2000">ACI</button></div>
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">CONT</h3><button class="top_button_keithley2000" id="r2_button_keithley2000">Ω2</button></div>
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">DIODE</h3><button class="top_button_keithley2000" id="r4_button_keithley2000">Ω4</button></div>
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">PERIOD</h3><button class="top_button_keithley2000" id="freq_button_keithley2000">FREQ</button></div>
          <div class="top_button_div_keithley2000"><h3 class="button_text_keithley2000">TCOUPL</h3><button class="top_button_keithley2000" id="temp_button_keithley2000">TEMP</button></div>
        </div>
        <div class="center_front_panel_row_keithley2000">
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000">DELAY</h3><button class="lower_button_left_keithley2000" id="ex_trig_button_keithley2000">EX TRIG</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000">HOLD</h3><button class="lower_button_right_keithley2000" id="trig_button_keithley2000">TRIG</button></div>
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000">LIMITS</h3><button class="lower_button_left_keithley2000" id="store_button_keithley2000">STORE</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000">ON/OFF</h3><button class="lower_button_right_keithley2000" id="recall_button_keithley2000">RECALL</button></div>
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000">TEST</h3><button class="lower_button_left_keithley2000" id="filter_button_keithley2000">FILTER</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000">CAL</h3><button class="lower_button_right_keithley2000" id="rel_button_keithley2000">REL</button></div>
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000" style="user-select: none; color: #997">FILLER</h3><button class="lower_button_left_keithley2000" id="left_button_keithley2000">⮜</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000" style="user-select: none; color: #997">FILLER</h3><button class="lower_button_right_keithley2000" id="right_button_keithley2000">➤</button></div>
        </div>
        <div class="center_front_panel_row_keithley2000">
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000">SAVE</h3><button class="lower_button_left_keithley2000" id="open_button_keithley2000">OPEN</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000">SETUP</h3><button class="lower_button_right_keithley2000" id="close_button_keithley2000">CLOSE</button></div>
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000">CONFIG</h3><button class="lower_button_left_keithley2000" id="step_button_keithley2000">STEP</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000">HALT</h3><button class="lower_button_right_keithley2000" id="scan_button_keithley2000">SCAN</button></div>
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000">GPIB</h3><button class="lower_button_left_keithley2000" id="digits_button_keithley2000">DIGITS</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000">RS232</h3><button class="lower_button_right_keithley2000" id="rate_button_keithley2000">RATE</button></div>
          <div class="lower_button_div_left_keithley2000"><h3 class="button_text_keithley2000" style="user-select: none; color: #997">FILLER</h3><button class="lower_button_left_keithley2000" id="exit_button_keithley2000">EXIT</button></div>
          <div class="lower_button_div_right_keithley2000"><h3 class="button_text_keithley2000" style="user-select: none; color: #997">FILLER</h3><button class="lower_button_right_keithley2000" id="enter_button_keithley2000">ENTER</button></div>
        </div>
      </div>
      <div id="right_front_panel_keithley2000">
        <button style="background: none; border: none"><span id="range_up_button_keithley2000"></span></button>
        <div style="align-items: center"><button id="auto_button_keithley2000">AUTO</button></div>
        <button style="background: none; border: none"><span id="range_down_button_keithley2000"></span</button>
      </div>
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

<?php
if ($hantek_dso2d15_enable) echo '<div class="instrument" id="hantek_dso2d15">';
else echo '<div class="instrument" style="display:none" id="hantek_dso2d15">';
?>
    <div class="name"><h2>Hantek DSO2D15</h2></div>
    <div class="result" id="result_hantek_dso2d15">
      <canvas id="waveform_hantek_dso2d15" width="800" height="480"></canvas>
    </div>
    <div class="settings">
      <button class="measure_button" id="measure_button_hantek_dso2d15">Measure</button>
      <div class="measure_option" id="probe_hantek_dso2d15">
        <h3 class="measure_option_label">Probe attenuation</h3>
        <select class="measure_type" id="probe_value_hantek_dso2d15">
          <option value="1">1x</option>
          <option value="10">10x</option>
          <option value="50">50x</option>
          <option value="100">100x</option>
        </select>
      </div>
      <div class="measure_option" id="volt_scale_hantek_dso2d15">
        <h3 class="measure_option_label">Volts per division</h3>
        <input class="measure_option_number" id="volt_scale_number_hantek_dso2d15" type="number" min="0.001" max="10" value="1"/>
        <input class="measure_option_slider" id="volt_scale_slider_hantek_dso2d15" type="range" min="0.001" max="10" value="1" step="0.001"/>
      </div>
      <div class="measure_option" id="volt_offset_hantek_dso2d15">
        <h3 class="measure_option_label">Voltage offset</h3>
        <input class="measure_option_number" id="volt_offset_number_hantek_dso2d15" type="number" min="-50" max="50" value="0"/>
        <input class="measure_option_slider" id="volt_offset_slider_hantek_dso2d15" type="range" min="-50" max="50" value="0" step="0.01"/>
      </div>
    </div>
  </div>
</div>
</body>

<script>
// TODO: Use PHP to not send the code for unused devices, as to make page load and resource usage more optimal

// Keithley 2000
const murl_keithley2000 = 'http://127.0.0.1:8000/dmm/keithley2000/measure/'; // Keithley 2000 measurement URL
const burl_keithley2000 = 'http://127.0.0.1:8000/dmm/keithley2000/key_press'// Keithley 2000 key press URL

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
  fetch(`${murl_keithley2000}${mtype}?nplc=${nplc}&samples=${fsamples}&mov=${ftype}&thr=${thr}&bandwidth=${bandwidth}&ttype=${ttype}&tref=${tref}&simtemp=${simtemp}&tcoef=${tcoef}&voff=${voff}`).then(function(response) {
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
  }).catch(function(err) { console.error(`Fetch error: ${err}`); });
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
      div_temp_voff_keithley2000.style = div_temp_coef_keithley2000.style = 'display: none';
    } else {
      div_temp_sim_keithley2000.style = 'display: none';
      div_temp_voff_keithley2000.style = div_temp_coef_keithley2000.style = 'display: block';
    }
  } else div_temp_main_keithley2000.style = 'display: none';
});

measure_temp_ref_keithley2000.addEventListener('change', () => {
  if (measure_temp_ref_keithley2000.value === '0') {
    div_temp_sim_keithley2000.style = 'display: block';
    div_temp_voff_keithley2000.style = div_temp_coef_keithley2000.style = 'display: none';
  } else {
    div_temp_sim_keithley2000.style = 'display: none';
    div_temp_voff_keithley2000.style = div_temp_coef_keithley2000.style = 'display: block';
  } 
});

// Sync sliders and number displays
measure_samples_slider_keithley2000.addEventListener('input', () => {
  measure_samples_number_keithley2000.value = measure_samples_slider_keithley2000.value;
});

measure_samples_number_keithley2000.addEventListener('input', () => {
  measure_samples_slider_keithley2000.value = measure_samples_number_keithley2000.value = Math.max(1, Math.min(100, measure_samples_number_keithley2000.value));
});

measure_nplc_slider_keithley2000.addEventListener('input', () => {
  measure_nplc_number_keithley2000.value = measure_nplc_slider_keithley2000.value;
});

measure_nplc_number_keithley2000.addEventListener('input', () => {
  measure_nplc_slider_keithley2000.value = measure_nplc_number_keithley2000.value = Math.max(0.01, Math.min(10, measure_nplc_number_keithley2000.value));
});

measure_threshold_slider_keithley2000.addEventListener('input', () => {
  measure_threshold_number_keithley2000.value = measure_threshold_slider_keithley2000.value;
});

measure_threshold_number_keithley2000.addEventListener('input', () => {
  measure_threshold_slider_keithley2000.value = measure_threshold_number_keithley2000.value = Math.max(1, Math.min(1000, measure_threshold_number_keithley2000.value));
});

measure_bandwidth_slider_keithley2000.addEventListener('input', () => {
  measure_bandwidth_number_keithley2000.value = measure_bandwidth_slider_keithley2000.value;
});

measure_bandwidth_number_keithley2000.addEventListener('input', () => {
  measure_bandwidth_slider_keithley2000.value = measure_bandwidth_number_keithley2000.value = Math.max(3, Math.min(300000, measure_bandwidth_number_keithley2000.value));
});

measure_temp_sim_slider_keithley2000.addEventListener('input', () => {
  measure_temp_sim_number_keithley2000.value = measure_temp_sim_slider_keithley2000.value;
});

measure_temp_sim_number_keithley2000.addEventListener('input', () => {
  measure_temp_sim_slider_keithley2000.value = measure_temp_sim_number_keithley2000.value = Math.max(0, Math.min(50, measure_temp_sim_number_keithley2000.value));
});

measure_temp_coef_slider_keithley2000.addEventListener('input', () => {
  measure_temp_coef_number_keithley2000.value = measure_temp_coef_slider_keithley2000.value;
});

measure_temp_coef_number_keithley2000.addEventListener('input', () => {
  measure_temp_coef_slider_keithley2000.value = measure_temp_coef_number_keithley2000.value = Math.max(-0.0999, Math.min(0.0999, measure_temp_coef_number_keithley2000.value));
});

measure_temp_voff_slider_keithley2000.addEventListener('input', () => {
  measure_temp_voff_number_keithley2000.value = measure_temp_voff_slider_keithley2000.value;
});

measure_temp_voff_number_keithley2000.addEventListener('input', () => {
  measure_temp_voff_slider_keithley2000.value = measure_temp_voff_number_keithley2000.value = Math.max(-0.0999, Math.min(0.0999, measure_temp_voff_number_keithley2000.value));
});

// Front panel buttons
document.getElementById("shift_key_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=1`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("dcv_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=2`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("acv_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=3`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("dci_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=4`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("aci_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=5`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("r2_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=6`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("r4_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=7`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("freq_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=8`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("temp_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=16`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("range_up_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=11`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("local_key_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=17`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("ex_trig_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=18`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("trig_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=19`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("store_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=20`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("recall_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=21`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("filter_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=22`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("rel_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=23`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("left_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=24`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("right_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=15`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("auto_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=12`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("open_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=26`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("close_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=27`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("step_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=28`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("scan_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=29`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("digits_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=30`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("rate_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=31`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("exit_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=32`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("enter_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=14`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

document.getElementById("range_down_button_keithley2000").onclick = () => {
  fetch(`${burl_keithley2000}?key=13`, { method: "POST" }).catch(function(err) { console.error(`Button press error: ${err}`); });
}

// Hantek DSO2D15
const murl_hantek_dso2d15 = 'http://127.0.0.1:8000/oscilloscope/hantek_dso2d15/waveform';

const result_hantek_dso2d15 = document.getElementById('result_hantek_dso2d15');
const waveform_hantek_dso2d15 = document.getElementById('waveform_hantek_dso2d15');

const probe_value_hantek_dso2d15 = document.getElementById('probe_value_hantek_dso2d15');

const volt_scale_number_hantek_dso2d15 = document.getElementById('volt_scale_number_hantek_dso2d15');
const volt_scale_slider_hantek_dso2d15 = document.getElementById('volt_scale_slider_hantek_dso2d15');

const volt_offset_number_hantek_dso2d15 = document.getElementById('volt_offset_number_hantek_dso2d15');
const volt_offset_slider_hantek_dso2d15 = document.getElementById('volt_offset_slider_hantek_dso2d15');

// The display is not 100% faithful, but I personally refuse to measure pixels just to make it so. If you have a complaint, well, it's FOSS for a reason...
document.getElementById('measure_button_hantek_dso2d15').onclick = () => {
  let probe = probe_value_hantek_dso2d15.value;
  let volt_scale = volt_scale_number_hantek_dso2d15.value;
  fetch(`${murl_hantek_dso2d15}?probe=${probe}&volt_scale=${volt_scale}`).then(function(response) {
    return response.json();
  }).then(function(data) {
    // Useful variables for rendering
    const yScale = 500; // 1 V / division (should adjust to selected scale once that's implemented)

    const ctx = waveform_hantek_dso2d15.getContext('2d');
    ctx.clearRect(0, 0, 800, 480);

    // Draw the grid (TODO: Make this also run on reloading the page)
    ctx.beginPath();
    ctx.strokeStyle = '#333333';
    ctx.lineWidth = 1;
    ctx.lineJoin = 'miter';
    ctx.lineCap = 'butt';

    // Horizontal lines
    for (let i = 1; i < 480; i += 60) {
      ctx.moveTo(0, i);
      ctx.lineTo(800, i);
    }

    // Vertical lines
    for (let i = -350; i < 400; i += 50) {
      ctx.moveTo(i + 400, 0);
      ctx.lineTo(i + 400, 480);
    }
    ctx.stroke();

    // Generate the actual waveform
    ctx.beginPath();
    ctx.strokeStyle = '#ffff00';
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    let y = 240 - (data[0] * yScale);
    ctx.moveTo(0, y);
    // We only need to sample every fifth point, since that's the canvas resolution we have
    for (let i = 1; i < 800; i++) {
      y = 240 - (data[i * 5] * yScale);
      ctx.lineTo(i, y);
    }
    ctx.stroke();
  }).catch(function(err) { console.error(`Fetch error: ${err}`); });
}

probe_value_hantek_dso2d15.addEventListener('input', () => {
  // TODO: Make step sizes also change
  const probe = probe_value_hantek_dso2d15.value;

  volt_scale_slider_hantek_dso2d15.min = volt_scale_number_hantek_dso2d15.min = 0.001 * probe;
  volt_scale_slider_hantek_dso2d15.max = volt_scale_number_hantek_dso2d15.max = 10 * probe;

  volt_offset_slider_hantek_dso2d15.min = volt_offset_number_hantek_dso2d15.min = -50 * probe;
  volt_offset_slider_hantek_dso2d15.max = volt_offset_number_hantek_dso2d15.max = 50 * probe;
});

volt_scale_slider_hantek_dso2d15.addEventListener('input', () => {
  volt_scale_number_hantek_dso2d15.value = volt_scale_slider_hantek_dso2d15.value;
});

volt_scale_number_hantek_dso2d15.addEventListener('input', () => {
  volt_scale_slider_hantek_dso2d15.value = volt_scale_number_hantek_dso2d15.value = Math.max(volt_scale_number_hantek_dso2d15.min, Math.min(volt_scale_number_hantek_dso2d15.max, volt_scale_number_hantek_dso2d15.value));
});

volt_offset_slider_hantek_dso2d15.addEventListener('input', () => {
  volt_offset_number_hantek_dso2d15.value = volt_offset_slider_hantek_dso2d15.value;
});

volt_offset_number_hantek_dso2d15.addEventListener('input', () => {
  volt_offset_slider_hantek_dso2d15.value = volt_offset_number_hantek_dso2d15.value = Math.max(volt_offset_number_hantek_dso2d15.min, Math.min(volt_offset_number_hantek_dso2d15.max, volt_offset_number_hantek_dso2d15.value));
});

</script>
</html>
