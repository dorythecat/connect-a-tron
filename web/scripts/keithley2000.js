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
  "ºC",
  "SEC",
  "HZ",
  "VDC",
  "OHM"
];

document.getElementById('measure_button_keithley2000').onclick = () => {
  const mtype = parseInt(measure_type_keithley2000.value);
  const fsamples = parseInt(measure_samples_number_keithley2000.value);
  const ftype = measure_filter_type_keithley2000.value !== '0';
  const nplc = parseFloat(measure_nplc_number_keithley2000.value);
  const thr = parseFloat(measure_threshold_number_keithley2000.value);
  const bandwidth = parseInt(measure_bandwidth_number_keithley2000.value);
  const ttype = measure_temp_type_keithley2000.value;
  const tref = measure_temp_ref_keithley2000.value !== '0';
  const simtemp = parseInt(measure_temp_sim_number_keithley2000.value);
  const tcoef = parseFloat(measure_temp_coef_number_keithley2000.value);
  const voff = parseFloat(measure_temp_voff_number_keithley2000.value);
  const start_text = `----.---${symbols[mtype]}`;
  let html = '';
  for (const digit in start_text) html += start_text[digit] == '.' ? '.' : `${digit === 0 ? '' : '</a>'}<a>${start_text[digit]}`;
  result_keithley2000.innerHTML = html + '</a>';
  fetch(`${murl_keithley2000}${mtype}?nplc=${nplc}&samples=${fsamples}&mov=${ftype}&thr=${thr}&bandwidth=${bandwidth}&ttype=${ttype}&tref=${tref}&simtemp=${simtemp}&tcoef=${tcoef}&voff=${voff}`).then(function(response) {
    return response.json();
  }).then(function(data) {
    data = parseFloat(data);
    if (data > 1e20) data = mtype === 11 ? 'OPEN' : [8, 9].includes(mtype) ? `OVRFLW  ${symbols[mtype]}` : 'OVR.FLW MOHM';
    else {
      const mega = data > 100000 && [5, 6].includes(mtype);
      const kilo = data > (mtype === 9 ? 1000 : 100) && [5, 6, 9].includes(mtype);
      const milli = Math.abs(data) <= ([8, 9].includes(mtype) ? 1 : 0.1) && [1, 2, 3, 8, 9].includes(mtype);
      const millii = Math.abs(data) <= 0.01 && mtype === 3;
      const micro = data <= -1.001 && mtype === 8;
      const og_data = data;
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

function temp_set() {
  const zero_val = measure_temp_ref_keithley2000.value === '0';
  div_temp_main_keithley2000.style = 'display: block';
  div_temp_sim_keithley2000.style = `display: ${zero_val ? 'block' : 'none'}`;
  div_temp_voff_keithley2000.style = div_temp_coef_keithley2000.style = `display: ${zero_val ? 'none' : 'block'}`;
}

document.addEventListener("DOMContentLoaded", () => {
  div_threshold_keithley2000.style = `display: ${measure_type_keithley2000.value === '11' ? 'block' : 'none'}`;
  div_bandwidth_keithley2000.style = `display: ${['2', '4'].includes(measure_type_keithley2000.value) ? 'block' : 'none'}`;

  if (measure_type_keithley2000.value === '7') temp_set();
  else div_temp_main_keithley2000.style = 'display: none';

})

measure_type_keithley2000.addEventListener('change', () => {
  div_threshold_keithley2000.style = `display: ${measure_type_keithley2000.value === '11' ? 'block' : 'none'}`;
  div_bandwidth_keithley2000.style = `display: ${['2', '4'].includes(measure_type_keithley2000.value) ? 'block' : 'none'}`;

  if (measure_type_keithley2000.value === '7') temp_set();
  else div_temp_main_keithley2000.style = 'display: none';
});

measure_temp_ref_keithley2000.addEventListener('change', temp_set);

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
