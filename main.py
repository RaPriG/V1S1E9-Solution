from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

def get_phase_data(pressure: float):
    if not (1 <= pressure <= 10):
        return None

    vc = 0.0035
    vf_min = 0.0011
    vg_max = 0.015
    pc = 10

    vf = vf_min + ((vc - vf_min) / (pc - 1)) * (pressure - 1)
    vg = vg_max - ((vg_max - vc) / (pc - 1)) * (pressure - 1)

    vf = round(vf, 6)
    vg = round(vg, 6)
    
    return {
        "specific_volume_liquid": vf,
        "specific_volume_vapor": vg
    }

@app.get("/phase-change-diagram")
async def get_phase_change(pressure: float = Query(..., ge=1, le=10)):
    data = get_phase_data(pressure)
    if data:
        return JSONResponse(content=data)
    return JSONResponse(content={"error": "Pressure out of range"}, status_code=400)
