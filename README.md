# Astrology Engine

> By Dominec369 — 29 years of astrological practice distilled into code.

A clean, open-source Python library for calculating astrological charts using the Swiss Ephemeris. Supports natal charts, transits, aspects, synastry, and 11 house systems.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Natal Chart Calculation** — Calculate complete birth charts from date, time, and location
- **Transits** — Compute transiting planet positions for any date
- **Aspects** — Full aspect detection (Conjunction, Opposition, Trine, Square, Sextile, Quincunx, Semi-square, Sesquiquadrate)
- **Synastry** — Aspect comparison between two charts
- **Transit-to-Natal** — Current transits against a birth chart
- **11 House Systems** — Placidus (default), Whole Sign, Equal, Koch, Regiomontanus, and more
- **Retrograde Detection** — Automatic detection of retrograde planets
- **Standard Astrological Data** — Tropical zodiac, sign rulers, elements, modalities

## Installation

```bash
pip install swisseph pytz
```

No additional installation required — just clone or download the library and import.

```python
from calculator import calculate_natal, calculate_transits, calculate_aspects
from formatter import format_position
```

## Quick Start

### Calculate a Natal Chart

```python
from datetime import date, time
from calculator import calculate_natal
from formatter import format_position

chart = calculate_natal(
    birth_date=date(1990, 6, 15),
    birth_time=time(14, 30, 0),
    latitude=40.7128,
    longitude=-74.0060,
    timezone_str="America/New_York",
)

# Planet positions
for planet, data in chart["planets"].items():
    print(f"{planet}: {format_position(data['longitude'])} "
          f"(House {data['house']})")

# House angles
print(f"Ascendant: {format_position(chart['houses']['ascendant'])}")
print(f"MC: {format_position(chart['houses']['mc'])}")
print(f"House system: {chart['houses']['house_system']}")
```

### Using a Different House System

```python
# Whole Sign houses
chart_whole = calculate_natal(
    birth_date=date(1990, 6, 15),
    birth_time=time(14, 30, 0),
    latitude=40.7128,
    longitude=-74.0060,
    timezone_str="America/New_York",
    house_system="W",  # Whole Sign
)

# Equal houses
chart_equal = calculate_natal(
    ..., house_system="E"
)

# Koch houses
chart_koch = calculate_natal(
    ..., house_system="K"
)
```
```

### Calculate Aspects

```python
from calculator import calculate_aspects

# Intra-chart aspects (within a single chart)
aspects = calculate_aspects(chart["planets"])

# Synastry (between two charts)
aspects = calculate_aspects(chart1["planets"], chart2["planets"])

for a in aspects:
    print(f"{a['planet_a']} {a['aspect']} {a['planet_b']} "
          f"(orb: {a['orb']:.2f}°)")
```

### Current Transits

```python
from calculator import calculate_transits

transits = calculate_transits(latitude=40.7128, longitude=-74.0060)
print(f"Transit Sun: {format_position(transits['planets']['Sun']['longitude'])}")
```

### Transit-to-Natal

```python
from calculator import calculate_transit_to_natal

result = calculate_transit_to_natal(natal_chart)
for a in result["transit_to_natal_aspects"]:
    print(f"Transit {a['planet_a']} {a['aspect']} Natal {a['planet_b']}")
```

## Module Overview

| Module | Description |
|--------|-------------|
| `calculator.py` | Core calculation engine (requires `swisseph` and `pytz`) |
| `config.py` | Standard astrological reference data (orbs, signs, elements, rulers) |
| `formatter.py` | Formatting utilities for positions, signs, and aspects |

## House Systems

All functions accept a `house_system` parameter. Default is `'P'` (Placidus).

| Code | House System |
|------|-------------|
| `P`  | **Placidus** (default) |
| `W`  | Whole Sign |
| `E`  | Equal |
| `A`  | Equal (MC) |
| `K`  | Koch |
| `R`  | Regiomontanus |
| `C`  | Campanus |
| `B`  | Alcabitius |
| `M`  | Morinus |
| `H`  | Horizontal |
| `X`  | Meridian |

Selecting a different house system changes how the 12 house cusps are calculated, which affects which planets fall in which houses. The ASC and MC remain fixed regardless of house system.

```python
from calculator import calculate_natal, HOUSE_SYSTEMS

# List all available house systems
for code, name in HOUSE_SYSTEMS.items():
    print(f"{code}: {name}")

# Calculate with Whole Sign houses
chart_ws = calculate_natal(
    ..., house_system="W"
)

# Check which system was used
print(chart_ws["houses"]["house_system"])   # "Whole Sign"
print(chart_ws["houses"]["house_system_code"])  # "W"
```

> Note: The `house_system` parameter is also available on `calculate_transits()` and `calculate_transit_to_natal()`.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Credits

**Astrology Engine** is the work of **Dominec369**, an astrologer with 29 years of experience in traditional and modern astrological practice.

- GitHub: [github.com/Dominec369/astrology-engine](https://github.com/Dominec369/astrology-engine)
- Gitee: [gitee.com/dominec/astrology-engine](https://gitee.com/dominec/astrology-engine)

Built with [Swiss Ephemeris](https://www.astro.com/swisseph/) — the gold standard in ephemeris computation.
