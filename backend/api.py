from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from enum import Enum

import interfaces.dmm.dmm as dmm
import interfaces.dmm.keithley as keithley

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

# TODO: Load instrumets from a configuration file
keithley2000 = keithley.Keithley2000()

@app.get("/system/interfaces", tags=["System"])
async def interfaces() -> dict:
    """
    Displays the available interfaces on this API.
    """
    return {
            "dmm": [
                "keithley2000"
            ]
    }

@app.get("/dmm/keithley2000", tags=["DMM"])
async def keithley2000_id() -> str:
    return keithley2000.id

class ThermocoupleType(Enum):
    J = "J"
    K = "K"
    T = "T"

@app.get("/dmm/keithley2000/measure/{typ}", tags=["DMM"])
async def keithley2000_measure(
        typ: Annotated[int, Path(title="Type of measurement to take", ge=1, le=11)],
        nplc: Annotated[float, Query(title="Number of powerline cycles per measurement", ge=0.01, le=10)] = 10,
        samples: Annotated[int, Query(title="Number of samples to average together", ge=1, le=100)] = 1,
        mov: Annotated[bool, Query(title="Wether to use a moving filter (True) or a repeat filter (False)")] = False,
        digits: Annotated[int, Query(title="Number of digits to display", ge=4, le=7)] = 7,
        thr: Annotated[int, Query(title="Threshold for continuity, in Ohms", ge=1, le=1000)] = 10,
        bandwidth: Annotated[int, Query(title="Bandwidth for AC measurements, in Hertz", ge=3, le=300000)] = 30,
        ttype: Annotated[ThermocoupleType, Query(title="Type of thermocouple attached to the multimeter")] = ThermocoupleType.J,
        tref: Annotated[bool, Query(title="Wether to use a simulated (False) or a real (True) thermocouple")] = False,
        simtemp: Annotated[int, Query(title="Simulated junction temperature, in ºC", ge=0, le=50)] = 23,
        tcoef: Annotated[float, Query(title="Real junction temperature coefficient", gt=-0.1, lt=0.1)] = 0.0002,
        voff: Annotated[float, Query(title="Real junction voltage offset", gt=-0.1, lt=0.1)] = 0.05463
    ) -> float:
    keithley2000.measure_set(dmm.MType(typ), nplc, samples, mov, digits, thr, bandwidth, ttype.value, tref, simtemp, tcoef, voff)
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
