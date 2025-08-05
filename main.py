from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

def calcular_volumenes(pressure):
    def getSpecificVolumes(pressure: float):
        # Punto crítico
        Pc = 10.0  # MPa
        vc = 0.0035  # m³/kg
        
        if pressure >= Pc:
         return round(vc, 6), round(vc, 6)
    
        # Relación empírica solo para vapor
        specific_volume_vapor = round(vc * (Pc / pressure) ** 3.0, 6)
        
        # Relación empírica para líquido (menos pronunciada)
        specific_volume_liquid = round(vc * (pressure / Pc) ** 0.5, 6)


        return round(specific_volume_liquid, 6), round(specific_volume_vapor, 6)

@app.get("/phase-change-diagram")
async def phase_change(pressure: float = Query(..., ge=1, le=10)):
    result = calcular_volumenes(pressure)
    if result:
        vf, vg = result
        return {"specific_volume_liquid": vf, "specific_volume_vapor": vg}
    return JSONResponse(content={"error": "Invalid pressure"}, status_code=400)

