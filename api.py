from fastapi import FastAPI

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
async def interfaces():
    return {
            "dmm": [
                keithley2000.id
            ]
    }

@app.get("/dmm/keithley/measure")
async def keithley_measure() -> float:
    keithley2000.measure_set()
    return keithley2000.measure_get()
