const murl_hantek_dso2d15 = 'http://127.0.0.1:8000/oscilloscope/hantek_dso2d15/waveform';

const result_hantek_dso2d15 = document.getElementById('result_hantek_dso2d15');
const waveform_hantek_dso2d15 = document.getElementById('waveform_hantek_dso2d15');

const probe_value_hantek_dso2d15 = document.getElementById('probe_value_hantek_dso2d15');

const volt_scale_number_hantek_dso2d15 = document.getElementById('volt_scale_number_hantek_dso2d15');
const volt_scale_slider_hantek_dso2d15 = document.getElementById('volt_scale_slider_hantek_dso2d15');

const volt_offset_number_hantek_dso2d15 = document.getElementById('volt_offset_number_hantek_dso2d15');
const volt_offset_slider_hantek_dso2d15 = document.getElementById('volt_offset_slider_hantek_dso2d15');

const time_scale_value_hantek_dso2d15 = document.getElementById('time_scale_value_hantek_dso2d15');

const time_offset_number_hantek_dso2d15 = document.getElementById('time_offset_number_hantek_dso2d15');
const time_offset_slider_hantek_dso2d15 = document.getElementById('time_offset_slider_hantek_dso2d15');

const invert_value_hantek_dso2d15 = document.getElementById('invert_value_hantek_dso2d15');

const coupling_value_hantek_dso2d15 = document.getElementById('coupling_value_hantek_dso2d15');

const bw_limit_value_hantek_dso2d15 = document.getElementById('bw_limit_value_hantek_dso2d15');

const trigger_level_number_hantek_dso2d15 = document.getElementById('trigger_level_number_hantek_dso2d15');
const trigger_level_slider_hantek_dso2d15 = document.getElementById('trigger_level_slider_hantek_dso2d15');

const trigger_slope_value_hantek_dso2d15 = document.getElementById('trigger_slope_value_hantek_dso2d15');

let yScale = 500; // Scale of the voltage divisions

// The display is not 100% faithful, but I personally refuse to measure pixels just to make it so. If you have a complaint, well, it's FOSS for a reason...
document.getElementById('measure_button_hantek_dso2d15').onclick = () => {
  const probe = probe_value_hantek_dso2d15.value;
  const volt_scale = volt_scale_number_hantek_dso2d15.value;
  const volt_offset = volt_offset_number_hantek_dso2d15.value;
  const time_scale = time_scale_value_hantek_dso2d15.value;
  const time_offset = time_offset_number_hantek_dso2d15.value;
  const invert = invert_value_hantek_dso2d15.value;
  const coupling = coupling_value_hantek_dso2d15.value;
  const bw_limit = bw_limit_value_hantek_dso2d15.value;
  const trigger_level = trigger_level_number_hantek_dso2d15.value;
  const trigger_slope = trigger_slope_value_hantek_dso2d15.value;
  fetch(`${murl_hantek_dso2d15}?probe=${probe}&volt_scale=${volt_scale}&volt_offset=${volt_offset}&time_scale=${time_scale}&time_offset=${time_offset}&invert=${invert}&coupling=${coupling}&bw_limit=${bw_limit}&trigger_level=${trigger_level}&trigger_slope=${trigger_slope}`).then(function(response) {
    return response.json();
  }).then(function(data) {
    // Variables for rendering
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
  const probe = probe_value_hantek_dso2d15.value;

  volt_scale_slider_hantek_dso2d15.min = volt_scale_number_hantek_dso2d15.min = 0.001 * probe;
  volt_scale_slider_hantek_dso2d15.max = volt_scale_number_hantek_dso2d15.max = 10 * probe;

  volt_offset_slider_hantek_dso2d15.min = volt_offset_number_hantek_dso2d15.min = -50 * probe;
  volt_offset_slider_hantek_dso2d15.max = volt_offset_number_hantek_dso2d15.max = 50 * probe;

  yScale = 500 * volt_scale; // This works pretty roughly, but well enough for the intended display
});

volt_scale_slider_hantek_dso2d15.addEventListener('input', () => {
  const volt_scale = volt_scale_number_hantek_dso2d15.value = volt_scale_slider_hantek_dso2d15.value;

  trigger_level_number_hantek_dso2d15.min = trigger_level_slider_hantek_dso2d15.min = -4 * volt_scale;
  trigger_level_number_hantek_dso2d15.max = trigger_level_slider_hantek_dso2d15.max = 4 * volt_scale;
});

volt_scale_number_hantek_dso2d15.addEventListener('input', () => {
  const volt_scale = volt_scale_slider_hantek_dso2d15.value = volt_scale_number_hantek_dso2d15.value = Math.max(volt_scale_number_hantek_dso2d15.min, Math.min(volt_scale_number_hantek_dso2d15.max, volt_scale_number_hantek_dso2d15.value));

  trigger_level_number_hantek_dso2d15.min = trigger_level_slider_hantek_dso2d15.min = -4 * volt_scale;
  trigger_level_number_hantek_dso2d15.max = trigger_level_slider_hantek_dso2d15.max = 4 * volt_scale;
});

volt_offset_slider_hantek_dso2d15.addEventListener('input', () => {
  volt_offset_number_hantek_dso2d15.value = volt_offset_slider_hantek_dso2d15.value;
});

volt_offset_number_hantek_dso2d15.addEventListener('input', () => {
  volt_offset_slider_hantek_dso2d15.value = volt_offset_number_hantek_dso2d15.value = Math.max(volt_offset_number_hantek_dso2d15.min, Math.min(volt_offset_number_hantek_dso2d15.max, volt_offset_number_hantek_dso2d15.value));
});

time_offset_slider_hantek_dso2d15.addEventListener('input', () => {
  time_offset_number_hantek_dso2d15.value = time_offset_slider_hantek_dso2d15.value;
});

time_offset_number_hantek_dso2d15.addEventListener('input', () => {
  // We don't need to do maximum and minimum values here, since it can go to wherever it pleases
  time_offset_slider_hantek_dso2d15.value = time_offset_number_hantek_dso2d15.value;
});

trigger_level_slider_hantek_dso2d15.addEventListener('input', () => {
  trigger_level_number_hantek_dso2d15.value = trigger_level_slider_hantek_dso2d15.value;
});

trigger_level_number_hantek_dso2d15.addEventListener('input', () => {
  trigger_level_slider_hantek_dso2d15.value = trigger_level_number_hantek_dso2d15.value = Math.min(trigger_level_number_hantek_dso2d15.max, Math.max(trigger_level_number_hantek_dso2d15.min, trigger_level_number_hantek_dso2d15.value));
});
