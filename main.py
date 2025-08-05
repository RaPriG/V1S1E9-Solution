from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Datos tomados de la gráfica
data_points = [
    {"P": 0.05, "vf": 0.00105, "vg": 30.0},  # Aprox. a 0.05 MPa
    {"P": 10.0, "vf": 0.0035, "vg": 0.0035},  # Punto crítico
]

def linear_interpolate(p, p1, p2, v1, v2):
    """Interpolación lineal"""
    return v1 + (p - p1) * (v2 - v1) / (p2 - p1)

@app.get("/phase-change-diagram")
async def phase_change_diagram(pressure: float = Query(..., ge=0.05, le=10.0)):
    p1, p2 = data_points[0]["P"], data_points[1]["P"]
    vf1, vf2 = data_points[0]["vf"], data_points[1]["vf"]
    vg1, vg2 = data_points[0]["vg"], data_points[1]["vg"]

    if pressure == 0.05:
        return {
            "specific_volume_liquid": 0.00105,
            "specific_volume_vapor": 30.0
        }
    if pressure == 10.0:
        return JSONResponse(content={
            "specific_volume_liquid": vf2,
            "specific_volume_vapor": vg2
        })

    vf_interp = linear_interpolate(pressure, p1, p2, vf1, vf2)
    vg_interp = linear_interpolate(pressure, p1, p2, vg1, vg2)

    return JSONResponse(content={
        "specific_volume_liquid": round(vf_interp, 6),
        "specific_volume_vapor": round(vg_interp, 6)
    })




