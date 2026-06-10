# Astrology Engine

> By Dominec369 — 29 years of astrological practice distilled into code.

A clean, open-source Python library for calculating astrological charts using the Swiss Ephemeris. Supports natal charts, transits, aspects, and synastry with Placidus house system.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Natal Chart Calculation** — Calculate complete birth charts from date, time, and location
- **Transits** — Compute transiting planet positions for any date
- **Aspects** — Full aspect detection (Conjunction, Opposition, Trine, Square, Sextile, Quincunx, Semi-square, Sesquiquadrate)
- **Synastry** — Aspect comparison between two charts
- **Transit-to-Natal** — Current transits against a birth chart
- **Placidus Houses** — Intentional design choice; Placidus only
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

## House System

Placidus is the only supported house system. This is an intentional design choice for consistency and reliability. If you need another house system, the underlying Swiss Ephemeris can calculate many — contributions welcome.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Credits

**Astrology Engine** is the work of **Dominec369**, an astrologer with 29 years of experience in traditional and modern astrological practice.

- GitHub: [github.com/Dominec369/astrology-engine](https://github.com/Dominec369/astrology-engine)
- Gitee: [gitee.com/dominec/astrology-engine](https://gitee.com/dominec/astrology-engine)

Built with [Swiss Ephemeris](https://www.astro.com/swisseph/) — the gold standard in ephemeris computation.
