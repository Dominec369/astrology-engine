"""
Astrology Engine — Standard astrological configuration data.

This module contains public-domain astrological reference data:
- Orb tables for aspects
- Tropical zodiac sign data
- Sign rulers, element/modality assignments
- Standard aspect list

This is standard astrological knowledge, not proprietary.
"""

# ── Tropical Zodiac Sign Data ──────────────────────────────────────────────

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

# Tropical zodiac starting points (0° Aries = 0.0, 30° per sign)
SIGN_START_DEGREES = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0,
                      180.0, 210.0, 240.0, 270.0, 300.0, 330.0]

# ── Elements ────────────────────────────────────────────────────────────────

ELEMENTS = {
    "Aries": "Fire",
    "Taurus": "Earth",
    "Gemini": "Air",
    "Cancer": "Water",
    "Leo": "Fire",
    "Virgo": "Earth",
    "Libra": "Air",
    "Scorpio": "Water",
    "Sagittarius": "Fire",
    "Capricorn": "Earth",
    "Aquarius": "Air",
    "Pisces": "Water",
}

# ── Modalities ──────────────────────────────────────────────────────────────

MODALITIES = {
    "Aries": "Cardinal",
    "Taurus": "Fixed",
    "Gemini": "Mutable",
    "Cancer": "Cardinal",
    "Leo": "Fixed",
    "Virgo": "Mutable",
    "Libra": "Cardinal",
    "Scorpio": "Fixed",
    "Sagittarius": "Mutable",
    "Capricorn": "Cardinal",
    "Aquarius": "Fixed",
    "Pisces": "Mutable",
}

# ── Sign Rulers (Traditional / Modern for outer planets) ──────────────────

RULERS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Pluto",  # Modern ruler; traditional: Mars
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Uranus",  # Modern ruler; traditional: Saturn
    "Pisces": "Neptune",   # Modern ruler; traditional: Jupiter
}

# ── Dignities (Essential Dignities by Triplicity, Term, etc. - placeholder) ─
# Standard rulers by element triplicity (day/night)
TRIPLICITY_RULERS = {
    "Fire": ("Sun", "Jupiter"),
    "Earth": ("Venus", "Moon"),
    "Air": ("Saturn", "Mercury"),
    "Water": ("Mars", "Venus"),
}

# ── Aspect Definitions ─────────────────────────────────────────────────────

# Standard orbs: Conjunction 8°, Opposition 8°, Trine 8°, Square 8°,
# Sextile 6°, Quincunx 3°, Semi-square 2°, Sesquiquadrate 2°

ASPECTS = {
    "Conjunction": {
        "angle": 0.0,
        "orb": 8.0,
        "symbol": "\u260c",     # ☌
        "keyword": "Union, blending, intensity",
    },
    "Opposition": {
        "angle": 180.0,
        "orb": 8.0,
        "symbol": "\u260d",     # ☍
        "keyword": "Tension, polarity, awareness",
    },
    "Trine": {
        "angle": 120.0,
        "orb": 8.0,
        "symbol": "\u25b3",     # △
        "keyword": "Flow, ease, talent",
    },
    "Square": {
        "angle": 90.0,
        "orb": 8.0,
        "symbol": "\u25a1",     # □
        "keyword": "Challenge, friction, growth",
    },
    "Sextile": {
        "angle": 60.0,
        "orb": 6.0,
        "symbol": "\u260c",     # ⚹
        "keyword": "Opportunity, harmony, support",
    },
    "Quincunx": {
        "angle": 150.0,
        "orb": 3.0,
        "symbol": "\u26b7",
        "keyword": "Adjustment, irritation, health",
    },
    "Semi-square": {
        "angle": 45.0,
        "orb": 2.0,
        "symbol": "\u2220",
        "keyword": "Friction, irritation, tension",
    },
    "Sesquiquadrate": {
        "angle": 135.0,
        "orb": 2.0,
        "symbol": "\u27be",
        "keyword": "Frustration, blockage, agitation",
    },
}

# Sort by orb width (widest first) for match ordering
ASPECT_MATCH_ORDER = sorted(
    ASPECTS.items(), key=lambda x: x[1]["orb"], reverse=True
)

# ── Planet Weights (standard astrological weighting) ────────────────────────
# Used for overall chart interpretation

PLANET_WEIGHTS = {
    "Sun": 10,
    "Moon": 10,
    "Mercury": 8,
    "Venus": 8,
    "Mars": 8,
    "Jupiter": 6,
    "Saturn": 6,
    "Uranus": 4,
    "Neptune": 4,
    "Pluto": 4,
}

# ── House System ───────────────────────────────────────────────────────────
# Placidus is intentionally the only supported house system.

SUPPORTED_HOUSE_SYSTEM = "Placidus"
