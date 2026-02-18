from fastapi import APIRouter, HTTPException

from models import TrafficProjectionRequest, TrafficProjectionResponse
from services.traffic_projection import (
    KEYWORD_TEMPLATES,
    calculate_projection,
)

router = APIRouter()


@router.post("/api/traffic-projection", response_model=TrafficProjectionResponse)
async def traffic_projection(request: TrafficProjectionRequest):
    practice_area = request.practice_area.lower().strip()

    if practice_area not in KEYWORD_TEMPLATES:
        valid = ", ".join(sorted(KEYWORD_TEMPLATES.keys()))
        raise HTTPException(
            status_code=400,
            detail=f"Invalid practice_area '{request.practice_area}'. Valid options: {valid}",
        )

    if not request.city or not request.city.strip():
        raise HTTPException(status_code=400, detail="City is required.")

    result = calculate_projection(practice_area, request.city.strip())
    return result
