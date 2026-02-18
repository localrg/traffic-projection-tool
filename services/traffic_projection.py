import re
from typing import Tuple


# ---------------------------------------------------------------------------
# Keyword templates per practice area
# ---------------------------------------------------------------------------
KEYWORD_TEMPLATES = {
    "personal_injury": [
        "personal injury lawyer {city}",
        "{city} personal injury attorney",
        "car accident lawyer {city}",
        "{city} car accident attorney",
        "truck accident lawyer {city}",
    ],
    "car_accidents": [
        "car accident lawyer {city}",
        "{city} car accident attorney",
        "auto accident lawyer {city}",
        "{city} auto accident lawyer",
        "car crash attorney {city}",
    ],
    "truck_accidents": [
        "truck accident lawyer {city}",
        "{city} truck accident attorney",
        "18 wheeler accident lawyer {city}",
        "{city} 18 wheeler attorney",
        "semi truck accident lawyer {city}",
    ],
    "family_law": [
        "divorce lawyer {city}",
        "{city} divorce attorney",
        "family law attorney {city}",
        "child custody lawyer {city}",
        "{city} family lawyer",
    ],
    "criminal_defense": [
        "criminal defense lawyer {city}",
        "{city} criminal attorney",
        "dui lawyer {city}",
        "{city} dui attorney",
        "drug crime lawyer {city}",
    ],
    "immigration": [
        "immigration lawyer {city}",
        "{city} immigration attorney",
        "deportation lawyer {city}",
        "visa attorney {city}",
        "green card lawyer {city}",
    ],
    "hvac": [
        "hvac repair {city}",
        "{city} hvac company",
        "ac repair {city}",
        "heating repair {city}",
        "hvac installation {city}",
    ],
    "tree_services": [
        "tree removal {city}",
        "tree service {city}",
        "{city} tree trimming",
        "tree cutting service {city}",
        "stump removal {city}",
    ],
    "dental": [
        "dentist {city}",
        "{city} dental office",
        "teeth whitening {city}",
        "emergency dentist {city}",
        "dental implants {city}",
    ],
}

# ---------------------------------------------------------------------------
# Baseline monthly search volumes per keyword (Tier 1 city)
# ---------------------------------------------------------------------------
BASELINE_VOLUMES = {
    "personal_injury": [1300, 880, 720, 590, 170],
    "car_accidents": [720, 590, 480, 390, 210],
    "truck_accidents": [1200, 980, 880, 720, 480],
    "family_law": [2400, 1900, 880, 720, 590],
    "criminal_defense": [1600, 1300, 2900, 1900, 480],
    "immigration": [1800, 1200, 480, 590, 390],
    "hvac": [2900, 1900, 2400, 1600, 1300],
    "tree_services": [1600, 1300, 880, 720, 590],
    "dental": [3600, 2400, 880, 1200, 1300],
}

# ---------------------------------------------------------------------------
# Average CPC by practice area (USD)
# ---------------------------------------------------------------------------
AVERAGE_CPC = {
    "personal_injury": 350,
    "car_accidents": 380,
    "truck_accidents": 450,
    "family_law": 175,
    "criminal_defense": 205,
    "immigration": 120,
    "hvac": 45,
    "tree_services": 25,
    "dental": 15,
}

# ---------------------------------------------------------------------------
# Average case / job value by practice area (USD)
# ---------------------------------------------------------------------------
CASE_VALUES = {
    "personal_injury": 16500,
    "car_accidents": 15000,
    "truck_accidents": 66000,
    "family_law": 25000,
    "criminal_defense": 8000,
    "immigration": 5000,
    "hvac": 350,
    "tree_services": 800,
    "dental": 1200,
}

# ---------------------------------------------------------------------------
# Human-readable labels
# ---------------------------------------------------------------------------
PRACTICE_AREA_LABELS = {
    "personal_injury": "Personal Injury",
    "car_accidents": "Car Accidents",
    "truck_accidents": "Truck Accidents",
    "family_law": "Family Law",
    "criminal_defense": "Criminal Defense",
    "immigration": "Immigration",
    "hvac": "HVAC",
    "tree_services": "Tree Services",
    "dental": "Dental",
}

# ---------------------------------------------------------------------------
# City population tiers (US metro areas by population, lowercase)
#   Tier 1 = top 50 metros (1.0x)
#   Tier 2 = metros ranked 51-100 (0.7x)
#   Tier 3 = metros ranked 101-200 (0.5x)
#   Tier 4 = everything else (0.3x)
# ---------------------------------------------------------------------------
TIER_1_CITIES = {
    # 1-20
    "new york", "los angeles", "chicago", "houston", "phoenix",
    "philadelphia", "san antonio", "san diego", "dallas", "san jose",
    "austin", "jacksonville", "fort worth", "columbus", "charlotte",
    "indianapolis", "san francisco", "seattle", "denver", "washington",
    # 21-50
    "nashville", "oklahoma city", "el paso", "boston", "portland",
    "las vegas", "memphis", "louisville", "baltimore", "milwaukee",
    "albuquerque", "tucson", "fresno", "mesa", "sacramento",
    "atlanta", "kansas city", "omaha", "colorado springs", "raleigh",
    "long beach", "virginia beach", "miami", "oakland", "minneapolis",
    "tulsa", "tampa", "arlington", "new orleans", "orlando",
}

TIER_2_CITIES = {
    # 51-100
    "wichita", "bakersfield", "aurora", "anaheim", "santa ana",
    "riverside", "corpus christi", "lexington", "henderson", "stockton",
    "st. paul", "cincinnati", "pittsburgh", "greensboro", "anchorage",
    "plano", "lincoln", "irvine", "newark", "durham",
    "chula vista", "toledo", "fort wayne", "st. petersburg", "laredo",
    "jersey city", "chandler", "madison", "lubbock", "scottsdale",
    "reno", "buffalo", "gilbert", "glendale", "north las vegas",
    "winston-salem", "chesapeake", "norfolk", "fremont", "garland",
    "irving", "richmond", "hialeah", "boise", "spokane",
    "baton rouge", "tacoma", "san bernardino", "modesto", "fontana",
}

TIER_3_CITIES = {
    # 101-200
    "moreno valley", "des moines", "fayetteville", "yonkers", "worcester",
    "columbia", "cape coral", "mckinney", "little rock", "oxnard",
    "amarillo", "grand rapids", "salt lake city", "huntsville", "tallahassee",
    "grand prairie", "overland park", "knoxville", "port st. lucie", "brownsville",
    "newport news", "chattanooga", "tempe", "providence", "santa clarita",
    "fort lauderdale", "springfield", "dayton", "bridgeport", "jackson",
    "sioux falls", "peoria", "pomona", "ontario", "joliet",
    "elk grove", "eugene", "cary", "garden grove", "corona",
    "pembroke pines", "salem", "lancaster", "palmdale", "salinas",
    "pasadena", "rockford", "paterson", "alexandria", "macon",
    "savannah", "hayward", "charleston", "clarksville", "murfreesboro",
    "miramar", "midland", "roseville", "surprise", "denton",
    "torrance", "pompano beach", "mcallen", "killeen", "cedar rapids",
    "topeka", "olathe", "visalia", "beaumont", "west valley city",
    "thornton", "hartford", "waco", "thousand oaks", "columbia",
    "concord", "lakewood", "sterling heights", "palm bay", "abilene",
    "elizabeth", "carrollton", "birmingham", "rochester", "provo",
    "ann arbor", "bellevue", "clearwater", "west jordan", "richardson",
    "manchester", "westminster", "costa mesa", "mobile", "pueblo",
    "erie", "sandy springs", "centennial", "boulder", "naperville",
}

# ---------------------------------------------------------------------------
# Tier multipliers for search volume scaling
# ---------------------------------------------------------------------------
TIER_MULTIPLIERS = {
    1: 1.0,
    2: 0.7,
    3: 0.5,
    4: 0.3,
}

# ---------------------------------------------------------------------------
# Fixed conversion assumptions
# ---------------------------------------------------------------------------
CTR = 0.54            # CTR for positions 1-3
VISITOR_TO_LEAD = 0.04  # Website visitor -> lead
LEAD_TO_CLIENT = 0.176  # Lead -> signed client


def parse_city(city_input: str) -> str:
    """Extract the city name from inputs like 'Orlando, FL' or 'Orlando FL'."""
    city_input = city_input.strip()

    if "," in city_input:
        city_name = city_input.split(",")[0].strip()
    else:
        parts = city_input.split()
        if len(parts) >= 2 and len(parts[-1]) == 2 and parts[-1].isalpha():
            city_name = " ".join(parts[:-1])
        else:
            city_name = city_input

    return city_name


def get_city_tier(city_name: str) -> int:
    """Return the population tier (1-4) for a given city name.

    Accepts raw input like "Orlando FL", "Orlando, FL", or "orlando" —
    the state suffix is stripped and matching is case-insensitive.
    """
    city_lower = parse_city(city_name).lower().strip()

    if city_lower in TIER_1_CITIES:
        return 1
    if city_lower in TIER_2_CITIES:
        return 2
    if city_lower in TIER_3_CITIES:
        return 3
    return 4


def calculate_projection(practice_area: str, city: str) -> dict:
    """Build a full traffic projection report for the given practice area and city."""
    city_name = parse_city(city)
    city_tier = get_city_tier(city_name)
    multiplier = TIER_MULTIPLIERS[city_tier]

    templates = KEYWORD_TEMPLATES[practice_area]
    base_volumes = BASELINE_VOLUMES[practice_area]
    cpc = AVERAGE_CPC[practice_area]
    case_value = CASE_VALUES[practice_area]
    label = PRACTICE_AREA_LABELS[practice_area]

    # Build keyword list with scaled volumes
    keywords = []
    for i, template in enumerate(templates):
        keyword_text = template.replace("{city}", city_name).lower()
        volume = int(base_volumes[i] * multiplier)
        keywords.append({
            "keyword": keyword_text,
            "volume": volume,
            "cpc": cpc,
        })

    # Funnel math
    total_monthly_searches = sum(k["volume"] for k in keywords)
    projected_traffic = int(total_monthly_searches * CTR)
    qualified_leads = int(projected_traffic * VISITOR_TO_LEAD)
    new_clients = int(qualified_leads * LEAD_TO_CLIENT)
    monthly_revenue = new_clients * case_value
    annual_revenue = monthly_revenue * 12

    # PPC cost = what you'd pay Google Ads for this traffic
    monthly_ppc_cost = sum(k["volume"] * k["cpc"] for k in keywords)
    annual_ppc_cost = monthly_ppc_cost * 12

    return {
        "practice_area": practice_area,
        "practice_area_label": label,
        "city": city,
        "keywords": keywords,
        "total_monthly_searches": total_monthly_searches,
        "projected_traffic": projected_traffic,
        "ctr_assumption": "54%",
        "qualified_leads": qualified_leads,
        "lead_conversion_rate": "4%",
        "new_clients": new_clients,
        "close_rate": "17.6%",
        "avg_case_value": case_value,
        "monthly_revenue": monthly_revenue,
        "annual_revenue": annual_revenue,
        "monthly_ppc_cost": monthly_ppc_cost,
        "annual_ppc_cost": annual_ppc_cost,
        "cost_of_invisibility_monthly": monthly_ppc_cost,
        "headline": f"You're leaving an estimated ${monthly_revenue:,} on the table every month.",
        "city_tier": city_tier,
        "disclaimer": (
            "Projections based on industry-standard conversion rates "
            "and average case values. Actual results may vary."
        ),
    }
