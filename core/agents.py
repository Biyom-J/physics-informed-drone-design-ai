import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"


def aerodynamics_agent(mission):
    prompt = f"""
    You are an aerodynamics engineer.

    Mission:
    {mission}

    Generate 20 different aerodynamic designs.

    For each design provide:

    - wing_area_m2
    - drag_coefficient
    - propeller_diameter_inch
    - fuselage_design

    Return ONLY valid JSON list.

    Example:

    [
      {{
        "wing_area_m2": 1.2,
        "drag_coefficient": 0.05,
        "propeller_diameter_inch": 24,
        "fuselage_design": "Blended body"
      }}
    ]
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


def propulsion_agent(mission):
    prompt = f"""
    You are a propulsion engineer.

    Mission:
    {mission}

    Generate 20 propulsion proposals.

    For each proposal provide:

    - battery_mAh
    - motor_KV
    - motor_type
    - voltage

    Return ONLY JSON list.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


def structures_agent(mission):
    prompt = f"""
    You are a structural engineer.

    Mission:
    {mission}

    Generate 20 structural proposals.

    For each proposal provide:

    - material
    - estimated_weight_kg
    - safety_factor
    - estimated_cost_usd

    Return ONLY JSON list.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


def control_agent(mission):
    prompt = f"""
    You are a control engineer.

    Mission:
    {mission}

    Generate 20 control proposals.

    For each proposal provide:

    - kp
    - ki
    - kd
    - wind_tolerance
    - navigation_method

    Return ONLY JSON list.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    mission = {
        "payload_kg": 5,
        "range_km": 10,
        "crosswind_m_s": 15,
        "environment": "dense urban",
        "gps_available": False,
        "budget_usd": 5000,
        "single_drone": True
    }

    print("\n=== AERODYNAMICS ===")
    print(aerodynamics_agent(mission))

    print("\n=== PROPULSION ===")
    print(propulsion_agent(mission))

    print("\n=== STRUCTURES ===")
    print(structures_agent(mission))

    print("\n=== CONTROL ===")
    print(control_agent(mission))