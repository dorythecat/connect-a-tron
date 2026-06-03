import json

from fastapi import FastAPI, Path, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BeforeValidator, model_validator
from typing import Annotated, Literal
from typing_extensions import Self
from enum import Enum

import interfaces.dmm.dmm as dmm
import interfaces.dmm.keithley as keithley

import interfaces.oscilloscope.hantek as hantek

app = FastAPI(
    title="Connect-a-tron API",
    summary="API for Connect-a-tron web service",
    description="""
    Connect-a-tron is a framework that links up all of your lab and test equipment, and interfaces with it, abstracting away all of the complicated and messy setup, all for a smooth user experience.
    """,
    version="0.0.0",
    openapi_tags=[
        {
            "name": "System",
            "description": "Everything relating to the general configuration of the Connect-a-tron backend."
        },
        {
            "name": "DMM",
            "description": "A DMM, or digital multimeter, is a device that can measure various values on a circuit, like voltage, current, and resistance, amongst others."
        },
        {
            "name": "Oscilloscope",
            "description": "An oscilloscope is a device that can sample voltages at a fast enough rate and with enough accuraccy as to allow viewing the waveforms of said voltage."
        }
    ],
    license_info={
        "name": "GNU Affero General Public License v3.0 or later",
        "identifier": "AGPL-3.0-or-later"
    }
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("settings.json", "r") as f:
    settings = json.load(f)

if "keithley2000" in settings and "enabled" in settings["keithley2000"] and settings["keithley2000"]["enabled"]:
    port = settings["keithley2000"]["port"] if "port" in settings["keithley2000"] else "/dev/ttyUSB0"
    baud_rate = settings["keithley2000"]["baud_rate"] if "baud_rate" in settings["keithley2000"] else 9600
    keithley2000 = keithley.Keithley2000(port, baud_rate)
else:
    keithley2000 = None

if "hantek_dso2d15" in settings and "enabled" in settings["hantek_dso2d15"] and settings["hantek_dso2d15"]["enabled"]:
    port = settings["hantek_dso2d15"]["port"] if "port" in settings["hantek_dso2d15"] else "/dev/usbtmc0"
    hantek_dso2d15 = hantek.DSO2D15(port)
else:
    hantek_dso2d15 = None

@app.get("/system/interfaces", tags=["System"])
async def interfaces() -> dict:
    """
    Display the available interfaces on this API.
    """
    interfaces = {
        "dmm": [],
        "oscilloscope": []
    }
    if keithley2000 is not None:
        interfaces["dmm"].append("keithley2000")
    if hantek_dso2d15 is not None:
        interfaces["oscilloscope"].append("hantek_dso2d15")
    return interfaces

# Keithley 2000
@app.get("/dmm/keithley2000", tags=["DMM"])
async def keithley2000_id() -> str:
    return keithley2000.id

class Keithley2000Measure(BaseModel):
    typ: Annotated[int, Path(title="Type of measurement to take", ge=1, le=11)]
    nplc: Annotated[float, Query(title="Number of powerline cycles per measurement", ge=0.01, le=10)] = 10
    samples: Annotated[int, Query(title="Number of samples to average together", ge=1, le=100)] = 1
    mov: Annotated[bool, Query(title="Wether to use a moving filter (True) or a repeat filter (False)")] = False
    digits: Annotated[int, Query(title="Number of digits to display", ge=4, le=7)] = 7
    thr: Annotated[int, Query(title="Threshold for continuity, in Ohms", ge=1, le= 1000)] = 10
    bandwidth: Annotated[int, Query(title="Bandwidth for AC measurements, in Hertz", ge=3, le=300000)] = 30
    ttype: Annotated[Literal["J", "K", "T"], Query(title="Type of thermocouple attached to the multimeter")] = "J"
    tref: Annotated[bool, Query(title="Wether to use a simulated (False) or real (True) thermocouple")] = False
    simtemp: Annotated[int, Query(title="Simulated junction temperature, in ºC", ge=0, le=50)] = 23
    tcoef: Annotated[float, Query(title="Real junction temperature coefficient", gt=-0.1, lt=0.1)] = 0.0002
    voff: Annotated[float, Query(title="Real junction voltage offset", gt=-0.1, lt=0.1)] = 0.05463

@app.get("/dmm/keithley2000/measure/{typ}", tags=["DMM"])
async def keithley2000_measure(data: Keithley2000Measure = Depends()) -> float:
    keithley2000.measure_set(
        dmm.MType(data.typ),
        data.nplc,
        data.samples,
        data.mov,
        data.digits,
        data.thr,
        data.bandwidth,
        data.ttype.value,
        data.tref,
        data.simtemp,
        data.tcoef,
        data.voff
    )
    return keithley2000.measure_get()

@app.get("/dmm/keithley2000/input", tags=["DMM"])
async def keithley2000_input() -> bool:
    return keithley2000.input

@app.get("/dmm/keithley2000/beeper", tags=["DMM"])
async def keithley2000_beeper() -> bool:
    return keithley2000.beeper

@app.post("/dmm/keithley2000/beeper", tags=["DMM"])
async def keithley2000_beeper(on: bool = False) -> None:
    keithley2000.beeper = on

class DisplaySettings(BaseModel):
    enabled: bool
    text: str

@app.get("/dmm/keithley2000/display", tags=["DMM"])
async def keithley2000_display() -> DisplaySettings:
    return DisplaySettings(
        enabled=keithley2000.display,
        text=keithley2000.text
    )

@app.post("/dmm/keithley2000/display", tags=["DMM"])
async def keithley2000_display(enable: bool = True, text: str = "") -> None:
    keithley2000.display = enable
    keithley2000.text = text

@app.get("/dmm/keithley2000/autozero", tags=["DMM"])
async def keithley2000_autozero() -> bool:
    return keithley2000.autozero

@app.post("/dmm/keihtley2000/autozero", tags=["DMM"])
async def keithley2000_autozero(on: bool = True) -> None:
    keithley2000.autozero = on

@app.get("/dmm/keithley2000/key_press", tags=["DMM"])
async def keithley2000_key_press() -> int:
    return keithley2000.key_press

@app.post("/dmm/keithley2000/key_press", tags=["DMM"])
async def keithley2000_key_press(key: int) -> None:
    keithley2000.key_press = key

# Hantek DSO2D15
@app.get("/oscilloscope/hantek_dso2d15", tags=["Oscilloscope"])
async def hantek_dso2d15_id() -> str:
    return hantek_dso2d15.id

# TODO(maybe): Support more trigger modes than just EDGE
class HantekDSO2D15GetWaveform(BaseModel):
    channel: Annotated[Literal[1], BeforeValidator(int), Query(title="Channel to read waveform from")] = 1 # TODO: Support channel 2
    probe: Annotated[Literal[1, 10, 50, 100], BeforeValidator(int), Query(title="Attenuation factor of the connected probe")] = 1
    volt_scale: Annotated[float, Query(title="Vertiroot_validator not definedcal scale of the measurement, in volts per division", ge=0.001, le=1000)] = 1
    volt_offset: Annotated[float, Query(title="Voltage offset from the ground point, in Volts")] = 0
    time_scale: Annotated[Literal[0.000000002, 0.000000005, 0.00000001, 0.00000002, 0.00000005, 0.0000001, 0.0000002, 0.0000005, 0.000001, 0.000002, 0.000005, 0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100], BeforeValidator(float), Query(title="Horizontal scale of the measurement, in seconds per division")] = 0.0005
    time_offset: Annotated[float, Query(title="Time offset from the trigger point, in seconds")] = 0
    invert: Annotated[bool, Query(title="Wether to invert the waveform")] = False
    coupling: Annotated[Literal["DC", "AC", "GND"], Query(title="Coupling mode to use for the measurement")] = "DC"
    bw_limit: Annotated[bool, Query(title="Wether to activate the 20MHz bandwith filter, to filter out high frequency noise")] = False
    trigger_level: Annotated[float, Query(title="Trigger level, in Volts")] = 0
    trigger_slope: Annotated[Literal["RISI", "FALL", "EITH"], Query("Wether to trigger on the rising, falling, or either slope")] = "RISI"

    @model_validator(mode='after')
    def verify(self) -> Self:
        if not 0.001 < (self.volt_scale / self.probe) <= 10:
            if 0.001 != self.volt_scale / self.probe:
                raise ValueError("Vertical scale out of bounds!")
            self.volt_scale = 0.00101 # Make it 1mV without making it 1mV, so that the oscilloscope understands it
        if abs(self.volt_offset) > 50 * self.probe:
            raise ValueError("Vertical offset out of bounds!")
        if abs(self.trigger_level) > 4 * self.volt_scale:
            raise ValueError("Trigger level out of bounds!")
        return self

@app.get("/oscilloscope/hantek_dso2d15/waveform", tags=["Oscilloscope"])
def hantek_dso2d15_get_waveform(data: HantekDSO2D15GetWaveform = Depends()) -> list[float]:
    hantek_dso2d15.channel_conf(
        channel=data.channel,
        scale=data.volt_scale,
        offset=data.volt_offset,
        probe=data.probe,
        invert=data.invert,
        coupling=data.coupling,
        bw_limit=data.bw_limit
    )
    hantek_dso2d15.time_conf(scale=data.time_scale, offset=data.time_offset)
    hantek_dso2d15.trigger_conf_edge(data.channel, data.trigger_level, data.trigger_slope)
    return hantek_dso2d15.get_waveform()

class HantekDSO2D15SetWaveform(BaseModel):
    freq: Annotated[float, Query(title="Frequency of the wave, in Hertz", ge=0.1, le=25000000)] = 1000
    amp: Annotated[float, Query(title="Amplitude of the wave, in Volts", ge=0.01, le=7)] = 1
    offset: Annotated[float, Query(title="Voltage offset of the wave, in Volts", ge=-3, le=3)] = 0
    typ: Annotated[Literal["SINE", "SQUA", "RAMP", "EXP", "NOIS", "DC", "ARB1", "ARB2", "ARB3", "ARB4"], Query(title="Type of the generated wave")] = "SINE"
    duty: Annotated[int, Query(title="Duty cycle of the wave, in percentage", ge=0, le=100)] = 50
    mod: Annotated[Literal["NONE", "AM", "FM"], Query(title="Type of modulation to apply to the wave")] = "NONE"
    mod_type: Annotated[Literal["SINE", "SQUA", "RAMP"], Query(title="Waveform to modulate into the wave")] = "SINE"
    mod_freq: Annotated[int, Query(title="Frequency of modulation, in Hertz", ge=100, le=50000)] = 1000
    mod_depth: Annotated[int, Query(title="In AM modulation, the modulation depth. In FM modulation, the modulation deviation", ge=100, le=50000)] = 100

    @model_validator(mode='after')
    def verify(self) -> Self:
        if self.mod_type == "FM" and self.mod_depth > 10000:
            raise ValueError("Modulation depth out of bounds!")
        return self

@app.post("/oscilloscope/hantek_dso2d15/waveform", tags=["Oscilloscope"])
def hantek_dso2d15_set_waveform(data: HantekDSO2D15SetWaveform = Depends()) -> None:
    hantek_dso2d15.set_waveform(
        data.freq, data.amp, data.offset, data.typ, data.duty, data.mod, data.mod_type, data.mod_freq, data.mod_depth
    )

@app.get("/oscilloscope/hantek_dso2d15/keypad_lock", tags=["Oscilloscope"])
def hantek_dso2d15_keypad_lock_get() -> bool:
    return hantek_dso2d15.keypad_lock

@app.post("/oscilloscope/hantek_dso2d15/keypad_lock", tags=["Oscilloscope"])
def hantek_dso2d15_keypad_lock_set(value: bool = True) -> None:
    hantek_dso2d15.keypad_lock = value

@app.get("/oscilloscope/hantek_dso2d15/trigger_status", tags=["Oscilloscope"])
def hantek_dso2d15_trigger_status() -> bool:
    return hantek_dso2d15.trigger_status

@app.get("/oscilloscope/hantek_dso2d15/frequency", tags=["Oscilloscope"])
def hantek_dso2d15_frequency(channel: Annotated[Literal[1, 2], BeforeValidator(int)] = 1) -> float:
    return hantek_dso2d15.frequency(channel)

@app.get("/oscilloscope/hantek_dso2d15/period", tags=["Oscilloscope"])
def hantek_dso2d15_period(chanel: Annotated[Literal[1, 2], BeforeValidator(int)] = 1) -> float:
    return hantek_dso2d15.period(channel)

@app.get("/oscilloscope/hantek_dso2d15/rms", tags=["Oscilloscope"])
def hantek_dso2d15_rms(channel: Annotated[Literal[1, 2], BeforeValidator(int)] = 1) -> float:
    return hantek_dso2d15.rms(channel)

@app.get("/oscilloscope/hantek_dso2d15/ppk", tags=["Oscilloscope"])
def hantek_dso2d15_ppk(channel: Annotated[Literal[1, 2], BeforeValidator(int)] = 1) -> float:
    return hantek_dso2d15.ppk(channel)
