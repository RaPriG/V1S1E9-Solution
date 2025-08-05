from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

def get_phase_data(pressure: float):
    if not (1 <= pressure <= 10):
        return None

    vc = 0.0035  # volumen crítico en m^3/kg

    # vf cambia poco con la presión, crecimiento lento
    vf = 0.00105 + (vc - 0.00105) * ((10 - pressure) / 9) ** 0.3

    # vg crece mucho con baja presión (comportamiento no lineal)
    vg = vc + (0.05 - vc) * ((10 - pressure) / 9) ** 2.2

    return {
        "specific_volume_liquid": round(vf, 6),
        "specific_volume_vapor": round(vg, 6)
    }

@app.get("/phase-change-diagram")
async def get_phase_change(pressure: float = Query(..., ge=1, le=10)):
    data = get_phase_data(pressure)
    if data:
        return JSONResponse(content=data)
    return JSONResponse(content={"error": "Pressure out of range"}, status_code=400)
