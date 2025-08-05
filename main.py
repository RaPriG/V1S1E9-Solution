from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

def get_phase_data(pressure: float):
    if not (1 <= pressure <= 10):
        return None

    vc = 0.0035   # volumen crítico
    delta = (10 - pressure) / 9  # valor que decrece de 1 a 0

    # Aplicamos una interpolación simétrica
    vf = vc - delta * (vc - 0.0011)
    vg = vc + delta * (0.015 - vc)

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
