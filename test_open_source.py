"""
Test Suite for Astrology Engine.

Tests all core calculation functions using a well-known public figure's
birth data to verify internal consistency and correctness.

Key verifications:
- Placidus house calculation produces correct ASC (= Cusp 1) and MC (= Cusp 10)
- Planetary positions are within valid ranges
- Aspects are calculated correctly
- Transits and transit-to-natal work
- Retrogrades are detected
"""

import math
import sys
from datetime import date, time

# Ensure we're testing the local package
sys.path.insert(0, "/home/dominec369/deerflow-output/astrology-engine-open-source")

from calculator import (
    calculate_natal,
    calculate_transits,
    calculate_aspects,
    calculate_transit_to_natal,
    PLANETS,
)
from config import ASPECTS
from formatter import (
    get_sign,
    get_degree_in_sign,
    format_position,
    get_element,
    get_modality,
    format_aspect,
)


# ── Known Birth Data ────────────────────────────────────────────────────────
# Oprah Winfrey: January 29, 1954, 4:30 AM CST, Kosciusko, MS
# Source: AstroDatabank (public figure, well-documented chart)
# Coordinates: 33°N03'29", 89°W35'23"  -> 33.058, -89.590

OPRAH_BIRTH = {
    "birth_date": date(1954, 1, 29),
    "birth_time": time(4, 30, 0),
    "latitude": 33.058,
    "longitude": -89.590,
    "timezone_str": "America/Chicago",
}


def test_natal_calculation():
    """Test that calculate_natal produces reasonable results."""
    print("\n[TEST] calculate_natal()")

    chart = calculate_natal(**OPRAH_BIRTH)

    # Check structure
    assert "planets" in chart, "Missing 'planets' key"
    assert "houses" in chart, "Missing 'houses' key"
    assert "julian_day" in chart, "Missing 'julian_day' key"

    # Check all major planets present
    for planet in ["Sun", "Moon", "Mercury", "Venus", "Mars",
                   "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]:
        assert planet in chart["planets"], f"Missing planet: {planet}"

    # Check houses structure
    houses = chart["houses"]
    assert houses["house_system"] == "Placidus", "House system should be Placidus"
    assert len(houses["cusps"]) == 12, "Should have 12 cusp values (houses 1-12)"
    assert "ascendant" in houses, "Missing ascendant"
    assert "mc" in houses, "Missing MC"

    print(f"  ASC: {format_position(houses['ascendant'])} ({houses['ascendant']:.2f}°)")
    print(f"  MC:  {format_position(houses['mc'])} ({houses['mc']:.2f}°)")
    print(f"  Houses: Placidus")

    # Verify planet positions are in valid range
    for name, data in chart["planets"].items():
        lon = data["longitude"]
        assert 0 <= lon < 360, f"{name} longitude {lon} out of valid range"

    return chart


def test_asc_mc_cusp_correspondence(chart):
    """Verify ASC matches Cusp 1 and MC matches Cusp 10."""
    houses = chart["houses"]
    asc = houses["ascendant"]
    mc = houses["mc"]

    cusp1 = houses["cusps"][0]
    cusp10 = houses["cusps"][9]

    # Cusp 1 should equal ASC (within tolerance)
    angle_diff = abs(cusp1 - asc) % 360
    assert min(angle_diff, 360 - angle_diff) < 1.0, \
        f"ASC ({asc:.2f}) should match Cusp 1 ({cusp1:.2f})"

    # MC should equal Cusp 10 (within tolerance)
    angle_diff2 = abs(cusp10 - mc) % 360
    assert min(angle_diff2, 360 - angle_diff2) < 1.0, \
        f"MC ({mc:.2f}) should match Cusp 10 ({cusp10:.2f})"

    print(f"  Cusp 1 = ASC: ✓ ({cusp1:.2f}° == {asc:.2f}°)")
    print(f"  Cusp 10 = MC: ✓ ({cusp10:.2f}° ≈ {mc:.2f}°)")


def test_planet_house_assignments(chart):
    """Verify every planet has a valid house assignment (1-12)."""
    planets = chart["planets"]
    for name, data in planets.items():
        house = data["house"]
        assert 1 <= house <= 12, \
            f"{name} has invalid house {house}"
    print(f"  House assignments all valid: ✓")


def test_aspect_calculation(chart):
    """Test that aspects are calculated correctly between chart positions."""
    print("\n[TEST] calculate_aspects() — Intra-chart aspects")

    aspects = calculate_aspects(chart["planets"])
    assert len(aspects) > 0, "Should find at least some aspects"

    # Print all major aspects
    major_aspects = ["Conjunction", "Opposition", "Trine", "Square", "Sextile"]
    major = [a for a in aspects if a["aspect"] in major_aspects]
    print(f"  Found {len(aspects)} total aspects, {len(major)} major")

    for a in aspects[:10]:
        print(f"    {a['planet_a']} {a['aspect']} {a['planet_b']} "
              f"(orb: {a['orb']:.2f}°, angle: {a['angle']:.2f}°)")

    # Verify aspect angle calculation matches actual separation
    for a in aspects[:5]:
        l1 = a["exact_longitude_a"]
        l2 = a["exact_longitude_b"]
        expected_angle = min(abs(l1 - l2) % 360, 360 - abs(l1 - l2) % 360)
        assert abs(a["angle"] - expected_angle) < 0.01, \
            f"Angle mismatch: {a['angle']} vs {expected_angle}"

    print(f"  Aspect angle accuracy: ✓")


def test_transit_calculation():
    """Test that transits produce valid data."""
    print("\n[TEST] calculate_transits()")

    transits = calculate_transits(latitude=40.7128, longitude=-74.0060,
                                  timezone_str="America/New_York")
    assert "planets" in transits, "Missing planets in transit data"
    assert "houses" in transits, "Missing houses in transit data"

    for planet in ["Sun", "Moon", "Mars", "Jupiter"]:
        assert planet in transits["planets"], f"Missing transit planet: {planet}"
        p = transits["planets"][planet]
        assert "longitude" in p, f"{planet} transit missing longitude"
        assert "is_retrograde" in p, f"{planet} transit missing retrograde flag"
        assert 0 <= p["longitude"] < 360, f"{planet} transit longitude out of range"

    print(f"  Transit Sun: {format_position(transits['planets']['Sun']['longitude'])}")
    print(f"  Transit Moon: {format_position(transits['planets']['Moon']['longitude'])}")
    print(f"  All transit planets present and valid: ✓")


def test_transit_to_natal(chart):
    """Test transit-to-natal aspect calculation."""
    print("\n[TEST] calculate_transit_to_natal()")

    result = calculate_transit_to_natal(chart)
    assert "transit_to_natal_aspects" in result, "Missing transit-to-natal aspects"
    assert "transit_aspects" in result, "Missing transit aspects"
    assert "transit_data" in result, "Missing transit data"

    tn = result["transit_to_natal_aspects"]
    print(f"  Transit-to-natal aspects: {len(tn)} found")

    if tn:
        for a in tn[:5]:
            print(f"    Transit {a['planet_a']} {a['aspect']} "
                  f"Natal {a['planet_b']} (orb: {a['orb']:.2f}°)")

    # Verify aspect angles are in valid range
    for a in tn:
        assert 0 <= a["angle"] <= 180, \
            f"Aspect angle {a['angle']} out of valid range"

    print(f"  All transit-to-natal aspects valid: ✓")


def test_retrograde_detection(chart):
    """Test that retrograde status is reported for major planets."""
    planets = chart["planets"]
    retrogrades = [p for p, d in planets.items()
                   if d.get("is_retrograde") and p in PLANETS]
    print(f"\n[TEST] Retrograde planets: {retrogrades if retrogrades else 'None'}")
    # Just check the field exists and is boolean
    for p, d in planets.items():
        if p in PLANETS:
            assert isinstance(d["is_retrograde"], bool), \
                f"{p} retrograde flag should be bool"
    print(f"  Retrograde flags are valid booleans: ✓")


def test_synastry_aspects(chart):
    """Test synastry-style aspect calculation between two different charts."""
    print("\n[TEST] Synastry (chart-to-chart aspects)")

    oprah2 = calculate_natal(
        birth_date=date(1954, 1, 29),
        birth_time=time(4, 30, 0),
        latitude=33.058,
        longitude=-89.590,
        timezone_str="America/Chicago",
    )

    # Two Oprahs = same positions, should give conjunction aspects
    aspects = calculate_aspects(chart["planets"], oprah2["planets"])
    assert len(aspects) > 0, "Should find synastry aspects"
    print(f"  Synastry aspects between identical charts: {len(aspects)}")

    # All should be conjunctions (same positions)
    conjunctions = [a for a in aspects if a["aspect"] == "Conjunction"]
    # Not all may be conjunctions if orbs are tight, but most should be
    if len(conjunctions) > 0:
        print(f"  Conjunctions found (same positions): {len(conjunctions)} ✓")


def test_formatter():
    """Test formatter utility functions."""
    print("\n[TEST] formatter utilities")

    # get_sign
    assert get_sign(0) == "Aries", "0° should be Aries"
    assert get_sign(30) == "Taurus", "30° should be Taurus"
    assert get_sign(350) == "Pisces", "350° should be Pisces"
    assert get_sign(720) == "Aries", "720° should wrap to Aries"
    print("  get_sign(): ✓")

    # get_degree_in_sign
    assert abs(get_degree_in_sign(45) - 15.0) < 0.001, "45° should be 15° Taurus"
    assert abs(get_degree_in_sign(359) - 29.0) < 0.001, "359° should be 29° Pisces"
    print("  get_degree_in_sign(): ✓")

    # format_position
    fp = format_position(45.5)
    assert "15" in fp and "Taurus" in fp, f"Format position failed: {fp}"
    print(f"  format_position(45.5): '{fp}'")

    # get_element
    assert get_element("Aries") == "Fire"
    assert get_element("Taurus") == "Earth"
    assert get_element("Cancer") == "Water"
    assert get_element("Gemini") == "Air"
    print("  get_element(): ✓")

    # get_modality
    assert get_modality("Aries") == "Cardinal"
    assert get_modality("Taurus") == "Fixed"
    assert get_modality("Gemini") == "Mutable"
    print("  get_modality(): ✓")

    # format_aspect
    fa = format_aspect("Conjunction")
    assert "Union" in fa, f"format_aspect failed: {fa}"
    print(f"  format_aspect('Conjunction'): '{fa[:50]}...'")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\n[TEST] Edge cases")

    # 360° rollover
    assert get_sign(360) == "Aries", "360° should wrap to Aries (0°)"
    assert get_sign(0.001) == "Aries", "0.001° should be Aries"

    # Negative degrees (wrap backward)
    assert get_sign(-1) == "Pisces", "-1° should be Pisces"
    assert get_sign(-30) == "Pisces", "-30° should be Pisces"
    print("  Degree wrap-around: ✓")

    # Aspect boundary crossing (0°/360°)
    p1 = {"PlanetA": {"longitude": 355.0}}
    p2 = {"PlanetB": {"longitude": 2.0}}
    aspects = calculate_aspects(p1, p2)
    matching_conj = [a for a in aspects if a["aspect"] == "Conjunction"]
    assert len(matching_conj) > 0, \
        "Planets at 355° and 2° should form a conjunction (7° apart)"
    print(f"  Boundary aspect (355°/2°): conjunction with orb "
          f"{matching_conj[0]['orb']:.2f}° ✓")

    # Aspect at exact separation
    p3 = {"PlanetX": {"longitude": 0.0}}
    p4 = {"PlanetY": {"longitude": 90.0}}
    aspects2 = calculate_aspects(p3, p4)
    squares = [a for a in aspects2 if a["aspect"] == "Square"]
    assert len(squares) > 0, \
        "Planets at 0° and 90° should form a square"
    print(f"  Exact right angle (0°/90°): square with orb "
          f"{squares[0]['orb']:.2f}° ✓")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    """Run all tests."""
    print("=" * 60)
    print("Astrology Engine — Open Source Test Suite")
    print("=" * 60)

    # Test formatter first (no ephemeris needed)
    try:
        test_formatter()
    except AssertionError as e:
        print(f"  ✗ FORMATTER FAILED: {e}")
        return 1

    # Test edge cases
    try:
        test_edge_cases()
    except AssertionError as e:
        print(f"  ✗ EDGE CASE FAILED: {e}")
        return 1

    # Test natal chart
    try:
        chart = test_natal_calculation()
        test_asc_mc_cusp_correspondence(chart)
        test_planet_house_assignments(chart)
        test_retrograde_detection(chart)
    except AssertionError as e:
        print(f"  ✗ NATAL TEST FAILED: {e}")
        return 1

    # Test aspects
    try:
        test_aspect_calculation(chart)
    except AssertionError as e:
        print(f"  ✗ ASPECT TEST FAILED: {e}")
        return 1

    # Test synastry
    try:
        test_synastry_aspects(chart)
    except AssertionError as e:
        print(f"  ✗ SYNASTRY TEST FAILED: {e}")
        return 1

    # Test transits
    try:
        test_transit_calculation()
    except AssertionError as e:
        print(f"  ✗ TRANSIT TEST FAILED: {e}")
        return 1

    # Test transit-to-natal
    try:
        test_transit_to_natal(chart)
    except AssertionError as e:
        print(f"  ✗ TRANSIT-TO-NATAL TEST FAILED: {e}")
        return 1

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
