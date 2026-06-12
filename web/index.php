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
          <option value="1" selected>1x</option>
          <option value="10">10x</option>
          <option value="50">50x</option>
          <option value="100">100x</option>
        </select>
      </div>
      <div class="measure_option" id="volt_scale_hantek_dso2d15">
        <h3 class="measure_option_label">Voltage scale (V/div)</h3>
        <input class="measure_option_number" id="volt_scale_number_hantek_dso2d15" type="number" min="0.001" max="10" value="1"/>
        <input class="measure_option_slider" id="volt_scale_slider_hantek_dso2d15" type="range" min="0.001" max="10" value="1" step="0.001"/>
      </div>
      <div class="measure_option" id="volt_offset_hantek_dso2d15">
        <h3 class="measure_option_label">Voltage offset (V)</h3>
        <input class="measure_option_number" id="volt_offset_number_hantek_dso2d15" type="number" min="-50" max="50" value="0"/>
        <input class="measure_option_slider" id="volt_offset_slider_hantek_dso2d15" type="range" min="-50" max="50" value="0" step="0.01"/>
      </div>
      <div class="measure_option" id="time_scale_hantek_dso2d15">
        <h3 class="measure_option_label">Time scale</h3>
        <select class="measure_type" id="time_scale_value_hantek_dso2d15">
          <option value="0.000000002">2ns/div</option>
          <option value="0.000000005">5ns/div</option>
          <option value="0.00000001">10ns/div</option>
          <option value="0.00000002">20ns/div</option>
          <option value="0.00000005">50ns/div</option>
          <option value="0.0000001">100ns/div</option>
          <option value="0.0000002">200ns/div</option>
          <option value="0.0000005">500ns/div</option>
          <option value="0.000001">1us/div</option>
          <option value="0.000002">2us/div</option>
          <option value="0.000005">5us/div</option>
          <option value="0.00001">10us/div</option>
          <option value="0.00002">20us/div</option>
          <option value="0.00005">50us/div</option>
          <option value="0.0001">100us/div</option>
          <option value="0.0002">200us/div</option>
          <option value="0.0005" selected>500us/div</option>
          <option value="0.001">1ms/div</option>
          <option value="0.002">2ms/div</option>
          <option value="0.005">5ms/div</option>
          <option value="0.01">10ms/div</option>
          <option value="0.02">20ms/div</option>
          <option value="0.05">50ms/div</option>
          <option value="0.1">100ms/div</option>
          <option value="0.2">200ms/div</option>
          <option value="0.5">500ms/div</option>
          <option value="1">1s/div</option>
          <option value="2">2s/div</option>
          <option value="5">5s/div</option>
          <option value="10">10s/div</option>
          <option value="20">20s/div</option>
          <option value="50">50s/div</option>
          <option value="100">100s/div</option>
        </select>
      </div>
    </div>
    <div class="measure_option" id="time_offset_hantek_dso2d15">
      <h3 class="measure_option_label">Time offset (s)</h3>
      <input class="measure_option_number" id="time_offset_number_hantek_dso2d15" type="number" min="-1" max="1" value="0"/>
      <input class="measure_option_slider" id="time_offset_slider_hantek_dso2d15" type="range" min="-1" max="1" value="0" step="0.0001"/>
    </div>
    <div class="measure_option" id="invert_hantek_dso2d15">
      <h3 class="measure_option_label">Invert</h3>
      <input class="measure_option_checkbox" id="invert_value_hantek_dso2d15" type="checkbox"/>
    </div>
    <div class="measure_option" id="coupling_hantek_dso2d15">
      <h3 class="meaasure_option_label">Coupling mode</h3>
      <select class="measure_type" id="coupling_value_hantek_dso2d15">
        <option value="DC" selected>DC</option>
        <option value="AC">AC</option>
        <option value="GND">GND</option>
      </select>
    </div>
    <div class="measure_option" id="bw_limit_hantek_dso2d15">
      <h3 class="measure_option_label">Bandwidth limit</h3>
      <input class="measure_option_checkbox" id="bw_limit_value_hantek_dso2d15" type="checkbox"/>
    </div>
    <div class="measure_option" id="trigger_level_hantek_dso2d15">
      <h3 class="measure_option_label">Trigger level (V)</h3>
      <input class="measure_option_number" id="trigger_level_number_hantek_dso2d15" type="number" min="-4" max="4" value="0"/>
      <input class="measure_option_slider" id="trigger_level_slider_hantek_dso2d15" type="range" min="-4" max="4" value="0" step="0.001"/>
    </div>
    <div class="measure_option" id="triger_slope_hantek_dso2d15">
      <h3 class="measure_option_label">Trigger slope</h3>
      <select class="measure_type" id="trigger_slope_value_hantek_dso2d15">
        <option value="RISI" selected>Rising</option>
        <option value="FALL">Falling</option>
        <option value="EITH">Either</option>
      </select>
    </div>
  </div>
</div>
</body>

<?php
if ($keithley2000_enable) echo '<script src="scripts/keithley2000.js"></script>';
if ($hantek_dso2d15_enable) echo '<script src="scripts/hantek_dso2d15.js"></script>';
?>

</html>
