import re
import json
import time
import requests
from typing import Optional, Dict, Any
from groq import Groq
from config import Config

# ─── Константы ───────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"

PROMPT_TEMPLATE = """
You are an expert agronomist assistant.
You will receive a JSON with field properties.

Field data:
{field_json}

Based on the field produce a crop planting plan.

Return ONLY a valid JSON object with exactly these keys:
- "recommendations": list of 3 strings, each describing a suitable crop and why
- "varieties": dict where key is crop name, value is list of 2-3 best varieties with short description
- "planting_windows": dict where key is crop name, value is planting month range
- "tips": dict where key is crop name, value is one-line management tip
- "risks": list of strings describing risks

Example for "varieties":
{{
  "Tomato": [
    "Brandywine — крупноплодный, богатый вкус, хорош для тёплого климата",
    "Cherry Belle — скороспелый, устойчив к болезням",
    "Roma — мясистый, идеален для консервирования"
  ]
}}

Respond in the same language as the "language" field in the JSON.
Do not include any text outside the JSON. Do not use markdown.
"""

# ─── Геокодирование ───────────────────────────────────────────
def reverse_geocode(lat: float, lon: float) -> Optional[str]:
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"format": "jsonv2", "lat": lat, "lon": lon, "addressdetails": 1},
            headers={"User-Agent": "AgroBot/1.0"},
            timeout=10
        )
        r.raise_for_status()
        return r.json().get("display_name")
    except Exception:
        return None

# ─── Погода ───────────────────────────────────────────────────
def get_weather(lat: float, lon: float) -> Dict:
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "current_weather": True, "timezone": "auto"
            },
            timeout=10
        )
        return r.json().get("current_weather", {})
    except Exception:
        return {}

# ─── NASA климат ──────────────────────────────────────────────
def get_nasa_climate(lat: float, lon: float) -> Dict:
    try:
        r = requests.get(
            f"https://power.larc.nasa.gov/api/temporal/climatology/point"
            f"?latitude={lat}&longitude={lon}&community=AG"
            f"&parameters=ALLSKY_SFC_SW_DWN,T2M,RH2M&format=JSON",
            timeout=15
        )
        params = r.json().get("properties", {}).get("parameter", {})
        return {
            "solar_radiation": params.get("ALLSKY_SFC_SW_DWN"),
            "temperature": params.get("T2M"),
            "humidity": params.get("RH2M"),
        }
    except Exception:
        return {}

# ─── Конвертация площади ──────────────────────────────────────
def area_to_ha(value: float, unit: str) -> float:
    unit = unit.lower().strip()
    if unit in ("ha", "га", "hectare"):
        return value
    if unit in ("m2", "sqm", "м2", "m²"):
        return value / 10000
    if unit in ("ac", "acre"):
        return value * 0.404686
    raise ValueError(f"Unknown unit: {unit}")

def parse_area(text: str):
    """Парсит строку вида '0.5 ha' -> (0.5, 'ha')"""
    text = text.strip().replace(",", ".")
    parts = text.split()
    if len(parts) == 2:
        return float(parts[0]), parts[1]
    # попробуем регулярку: "500m2" или "0.5ha"
    m = re.match(r"^([\d.]+)\s*([a-zA-Zа-яА-Я2²]+)$", text)
    if m:
        return float(m.group(1)), m.group(2)
    raise ValueError("Cannot parse area")

# ─── Основная функция анализа ─────────────────────────────────
def analyze_field(data: dict, lang: str = "ru") -> Dict[str, Any]:
    """
    data: словарь с полями из FSM
    Возвращает план посева от LLM
    """
    lat = data["latitude"]
    lon = data["longitude"]

    address = reverse_geocode(lat, lon)
    weather = get_weather(lat, lon)
    nasa = get_nasa_climate(lat, lon)

    summary = {
        "language": "Russian" if lang == "ru" else "English",
        "name": data.get("name", "Field"),
        "latitude": lat,
        "longitude": lon,
        "address": address,
        "area_ha": data.get("area_ha", 0),
        "soil_type": data.get("soil_type", "unknown"),
        "soil_ph": data.get("soil_ph"),
        "soil_organic": data.get("soil_organic"),
        "soil_clay": data.get("soil_clay"),
        "soil_sand": data.get("soil_sand"),
        "soil_notes": data.get("soil_notes", ""),
        "current_weather": weather,
        "nasa_climate": nasa,
    }

    prompt = PROMPT_TEMPLATE.format(
        field_json=json.dumps(summary, ensure_ascii=False, indent=2)
    )

    client = Groq(api_key=Config.GROQ_API_KEY)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            text = response.choices[0].message.content
            cleaned = re.sub(r"```json\s*|```", "", text.strip()).strip()
            return json.loads(cleaned)

        except Exception as e:
            err = str(e)
            if "429" in err:
                wait = 20 * (attempt + 1)
                time.sleep(wait)
            else:
                raise

    raise RuntimeError("Max retries exceeded")
