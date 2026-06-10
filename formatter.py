"""
Astrology Engine — Formatting utilities for astrological calculations.

Pure utility functions for formatting positions, signs, aspects, etc.
No business logic or proprietary algorithms.
"""

from config import SIGNS, SIGN_START_DEGREES, ELEMENTS, MODALITIES, ASPECTS


def get_sign(degrees: float) -> str:
    """Return the tropical zodiac sign for a given ecliptic longitude (0-360)."""
    degrees = degrees % 360.0
    index = int(degrees // 30)
    return SIGNS[index]


def get_sign_index(degrees: float) -> int:
    """Return the 0-based sign index for a given ecliptic longitude."""
    degrees = degrees % 360.0
    return int(degrees // 30)


def get_degree_in_sign(degrees: float) -> float:
    """Return the degree within the sign (0.0 to 29.999...) for a given longitude."""
    degrees = degrees % 360.0
    return degrees % 30.0


def format_position(degrees: float, show_seconds: bool = False) -> str:
    """Format a zodiac position as a human-readable string.

    Example: 45.5 -> "15° Gemini 30'"
    """
    sign = get_sign(degrees)
    deg_in_sign = get_degree_in_sign(degrees)
    sign_num = int(deg_in_sign)
    minutes = int((deg_in_sign - sign_num) * 60)
    seconds = int(((deg_in_sign - sign_num) * 60 - minutes) * 60)

    if show_seconds:
        return f"{sign_num}°{sign} {minutes}'{seconds}\""
    return f"{sign_num}°{sign} {minutes}'"


def format_position_decoupled(degrees: float) -> str:
    """Return (degrees_in_sign, sign_name) tuple for structured use."""
    sign = get_sign(degrees)
    deg_in_sign = get_degree_in_sign(degrees)
    return deg_in_sign, sign


def get_element(sign_name: str) -> str:
    """Return the element (Fire, Earth, Air, Water) for a given sign."""
    return ELEMENTS.get(sign_name, "Unknown")


def get_modality(sign_name: str) -> str:
    """Return the modality (Cardinal, Fixed, Mutable) for a given sign."""
    return MODALITIES.get(sign_name, "Unknown")


def format_aspect(aspect_name: str) -> str:
    """Return a formatted description of an aspect type."""
    aspect = ASPECTS.get(aspect_name)
    if not aspect:
        return f"Unknown aspect: {aspect_name}"
    return (f"{aspect_name} ({aspect['symbol']}) "
            f"— {aspect['keyword']}. "
            f"Orb: {aspect['orb']}° | Angle: {aspect['angle']}°")


def format_planet_position(planet_name: str, longitude: float) -> str:
    """Format a full planet position string."""
    pos_str = format_position(longitude)
    return f"{planet_name}: {pos_str}"


def format_aspect_line(p1_name: str, p1_long: float,
                       p2_name: str, p2_long: float,
                       aspect_name: str, orb: float) -> str:
    """Format a complete aspect line between two planets."""
    angle_diff = abs(p1_long - p2_long) % 360
    if angle_diff > 180:
        angle_diff = 360 - angle_diff
    return (f"{p1_name} ({format_position(p1_long)}) "
            f"{aspect_name} "
            f"{p2_name} ({format_position(p2_long)}) "
            f"— orb: {orb:.2f}°, angle: {angle_diff:.2f}°")
