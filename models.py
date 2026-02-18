from pydantic import BaseModel
from typing import List


class TrafficProjectionRequest(BaseModel):
    practice_area: str
    city: str


class KeywordData(BaseModel):
    keyword: str
    volume: int
    cpc: float


class TrafficProjectionResponse(BaseModel):
    practice_area: str
    practice_area_label: str
    city: str
    keywords: List[KeywordData]
    total_monthly_searches: int
    projected_traffic: int
    ctr_assumption: str
    qualified_leads: int
    lead_conversion_rate: str
    new_clients: int
    close_rate: str
    avg_case_value: float
    monthly_revenue: float
    annual_revenue: float
    monthly_ppc_cost: float
    annual_ppc_cost: float
    cost_of_invisibility_monthly: float
    headline: str
    city_tier: int
    disclaimer: str
