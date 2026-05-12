from fastapi import FastAPI
from pydantic import BaseModel

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

@app.get("/dmm/keithley2000/measure", tags=["DMM"])
async def keithley2000_measure() -> float:
    # TODO: Actually implement a proper measurement endpoint
    keithley2000.measure_set()
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
