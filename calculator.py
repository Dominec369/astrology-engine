"""
Astrology Engine — Astronomical calculation core.

Uses Swiss Ephemeris (swisseph) for all ephemeris calculations.
Placidus house system only (intentional design choice).
No business logic, no proprietary algorithms — pure astronomical/astrological
computation using public-domain ephemeris data.
"""

from __future__ import annotations

from datetime import datetime, date, time, timedelta
from typing import Optional, List, Dict, Any, Tuple

import swisseph as swe
import pytz

from config import ASPECTS, ASPECT_MATCH_ORDER


# ── Swiss Ephemeris Setup ─────────────────────────────────────────────────

# Set ephemeris path (uses built-in JPL ephemeris if available)
# swe.set_ephe_path()  # Default path, or set explicitly if needed.


# ── Planet ID Constants ────────────────────────────────────────────────────

# Standard planets used in natal and transit charts
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

# Additional points (optional)
ADDITIONAL_POINTS = {
    "True Node": swe.TRUE_NODE,
    "Mean Node": swe.MEAN_NODE,
    "Chiron": swe.CHIRON,
}

# Flag bits for Swiss Ephemeris
SweFlag = int

# Speed flag to get position + speed
FLAG_SWIEPH = swe.FLG_SWIEPH
FLAG_SPEED = swe.FLG_SPEED
FLAG_ALL = FLAG_SWIEPH | FLAG_SPEED


# ── Helper Functions ───────────────────────────────────────────────────────


def _julian_day(dt: datetime) -> float:
    """Convert a timezone-aware datetime to Julian Day Number."""
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware. "
                         "Use pytz to localize before calling.")
    # Swiss Ephemeris expects UTC
    utc_dt = dt.astimezone(pytz.UTC)
    return swe.julday(
        utc_dt.year, utc_dt.month, utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    )


def _calc_position(jd: float, planet_id: int,
                   flags: int = FLAG_ALL) -> Dict[str, float]:
    """Calculate a single planet position at a Julian Day."""
    result = swe.calc_ut(jd, planet_id, flags)
    longitude = result[0][0]
    latitude = result[0][1]
    distance_au = result[0][2]
    speed_long = result[0][3]  # degrees/day

    return {
        "longitude": longitude,
        "latitude": latitude,
        "distance_au": distance_au,
        "speed": speed_long,
        "is_retrograde": speed_long < 0,
    }


def _calc_houses(jd: float, latitude: float, longitude: float) -> Dict[str, Any]:
    """Calculate Placidus houses and angles.

    Note: Placidus is intentionally the only supported house system.
    """
    # Swiss Ephemeris: houses takes geographic longitude, latitude, and "house system" char
    # For Placidus, the house system character is 'P'
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')

    return {
        "house_system": "Placidus",
        "cusps": list(cusps),  # houses 1-12, indexed 0-11
        "ascendant": float(ascmc[0]),
        "mc": float(ascmc[1]),
        "armc": float(ascmc[2]),
        "vertex": float(ascmc[3]),
        "equatorial_ascendant": float(ascmc[4]),
        "co_ascendant_koch": float(ascmc[5]),
        "co_ascendant_munkasey": float(ascmc[6]),
    }


def _get_house_of_position(longitude: float, cusps: List[float]) -> int:
    """Determine which Placidus house a given longitude falls into.

    cusps is a 12-element list where cusps[0] = House 1 cusp (ASC),
    cusps[1] = House 2, ..., cusps[11] = House 12.
    """
    longitude = longitude % 360.0

    # The Swiss Ephemeris returns 12 cusps directly
    # We check each house interval: cusps[i] to cusps[(i+1) % 12]
    for i in range(12):
        cusp_i = cusps[i] % 360.0
        cusp_next = cusps[(i + 1) % 12] % 360.0

        # Handle wrap-around (e.g., 29 Pisces -> 1 Aries)
        if cusp_i < cusp_next:
            if cusp_i <= longitude < cusp_next:
                return i + 1  # houses are 1-indexed
        else:
            # Wraps around 0° Aries
            if longitude >= cusp_i or longitude < cusp_next:
                return i + 1

    return 12


# ── Main Calculation Functions ─────────────────────────────────────────────


def calculate_natal(
    birth_date: date,
    birth_time: time,
    latitude: float,
    longitude: float,
    timezone_str: str,
    include_speed: bool = True,
) -> Dict[str, Any]:
    """Calculate a complete natal (birth) chart.

    Args:
        birth_date: Date of birth (date object).
        birth_time: Time of birth (time object).
        latitude: Geographic latitude of birth location (decimal degrees).
        longitude: Geographic longitude of birth location (decimal degrees).
        timezone_str: IANA timezone string (e.g., 'America/New_York').
        include_speed: Whether to include planetary speed/retrograde data.

    Returns:
        Dict containing planet positions, houses, angles, and metadata.
    """
    # Build timezone-aware datetime
    tz = pytz.timezone(timezone_str)
    dt_local = datetime.combine(birth_date, birth_time)
    dt_local = tz.localize(dt_local)

    # Julian Day
    jd = _julian_day(dt_local)

    # Calculate house cusps
    houses = _calc_houses(jd, latitude, longitude)

    # Calculate planet positions
    flags = FLAG_ALL if include_speed else FLAG_SWIEPH
    planet_positions = {}
    for name, pid in PLANETS.items():
        pos = _calc_position(jd, pid, flags)
        pos["house"] = _get_house_of_position(pos["longitude"], houses["cusps"])
        planet_positions[name] = pos

    # Additional points
    for name, pid in ADDITIONAL_POINTS.items():
        try:
            pos = _calc_position(jd, pid, flags)
            pos["house"] = _get_house_of_position(pos["longitude"], houses["cusps"])
            planet_positions[name] = pos
        except Exception:
            # Chiron or other points may fail depending on ephemeris
            pass

    return {
        "birth_date": birth_date.isoformat(),
        "birth_time": birth_time.isoformat(),
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone_str,
        "julian_day": jd,
        "houses": houses,
        "planets": planet_positions,
    }


def calculate_transits(
    target_date: Optional[date] = None,
    latitude: float = 0.0,
    longitude: float = 0.0,
    timezone_str: str = "UTC",
) -> Dict[str, Any]:
    """Calculate transiting planet positions for a given date.

    Args:
        target_date: Date for transit calculation (defaults to today).
        latitude: Geographic latitude (for house calculation).
        longitude: Geographic longitude (for house calculation).
        timezone_str: IANA timezone string.

    Returns:
        Dict with transit planet positions and house data.
    """
    if target_date is None:
        target_date = date.today()

    tz = pytz.timezone(timezone_str)
    dt_local = datetime.combine(target_date, time(12, 0, 0))
    dt_local = tz.localize(dt_local)

    jd = _julian_day(dt_local)
    houses = _calc_houses(jd, latitude, longitude)

    planet_positions = {}
    for name, pid in PLANETS.items():
        pos = _calc_position(jd, pid, FLAG_ALL)
        pos["house"] = _get_house_of_position(pos["longitude"], houses["cusps"])
        planet_positions[name] = pos

    for name, pid in ADDITIONAL_POINTS.items():
        try:
            pos = _calc_position(jd, pid, FLAG_ALL)
            pos["house"] = _get_house_of_position(pos["longitude"], houses["cusps"])
            planet_positions[name] = pos
        except Exception:
            pass

    return {
        "date": target_date.isoformat(),
        "julian_day": jd,
        "houses": houses,
        "planets": planet_positions,
    }


def calculate_aspects(
    positions1: Dict[str, Dict[str, float]],
    positions2: Optional[Dict[str, Dict[str, float]]] = None,
) -> List[Dict[str, Any]]:
    """Calculate aspects between two sets of planetary positions.

    If positions2 is None, calculates aspects within positions1
    (i.e., natal chart aspects).

    Args:
        positions1: Dict of {planet_name: {longitude: float, ...}}
        positions2: Optional second set of positions (for synastry / transit).

    Returns:
        List of aspect dicts with planet_a, planet_b, aspect_name, orb, angle.
    """
    aspects = []

    if positions2 is None:
        # Intra-chart aspects (e.g., natal aspects)
        planets = list(positions1.items())
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                p1_name, p1_data = planets[i]
                p2_name, p2_data = planets[j]
                _check_aspect(aspects, p1_name, p1_data["longitude"],
                              p2_name, p2_data["longitude"])
    else:
        # Inter-chart aspects (e.g., transit-to-natal or synastry)
        for p1_name, p1_data in positions1.items():
            for p2_name, p2_data in positions2.items():
                _check_aspect(aspects, p1_name, p1_data["longitude"],
                              p2_name, p2_data["longitude"])

    return aspects


def _check_aspect(aspects_list: List[Dict], p1: str, l1: float,
                  p2: str, l2: float) -> None:
    """Check if two longitudes form an aspect and append if so."""
    # Calculate angular separation
    diff = abs(l1 - l2) % 360.0
    if diff > 180.0:
        diff = 360.0 - diff

    # Check against each aspect type (widest orb first)
    for aspect_name, aspect_data in ASPECT_MATCH_ORDER:
        target_angle = aspect_data["angle"]
        max_orb = aspect_data["orb"]
        separation = abs(diff - target_angle)

        if separation <= max_orb:
            aspects_list.append({
                "planet_a": p1,
                "planet_b": p2,
                "aspect": aspect_name,
                "angle": diff,
                "orb": separation,
                "exact_longitude_a": l1,
                "exact_longitude_b": l2,
            })
            break  # Only match the tightest applicable aspect


def calculate_transit_to_natal(
    natal_data: Dict[str, Any],
    target_date: Optional[date] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    timezone_str: Optional[str] = None,
) -> Dict[str, Any]:
    """Calculate current transits against a natal chart.

    Args:
        natal_data: Output of calculate_natal().
        target_date: Date for transit calculation (defaults to today).
        latitude, longitude, timezone_str: Override location (uses natal
            location by default).

    Returns:
        Dict with transit positions, transit-to-natal aspects, and metadata.
    """
    if latitude is None:
        latitude = natal_data["latitude"]
    if longitude is None:
        longitude = natal_data["longitude"]
    if timezone_str is None:
        timezone_str = natal_data["timezone"]

    # Calculate transit positions
    transit_data = calculate_transits(target_date, latitude, longitude, timezone_str)

    # Calculate transit-to-natal aspects
    transit_to_natal = calculate_aspects(
        transit_data["planets"], natal_data["planets"]
    )

    # Also calculate transit aspects among themselves
    transit_aspects = calculate_aspects(transit_data["planets"])

    return {
        "transit_data": transit_data,
        "natal_data_summary": {
            "birth_date": natal_data["birth_date"],
            "birth_time": natal_data["birth_time"],
            "latitude": natal_data["latitude"],
            "longitude": natal_data["longitude"],
        },
        "transit_to_natal_aspects": transit_to_natal,
        "transit_aspects": transit_aspects,
    }
