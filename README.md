# mansaapi (Python)

Official Python SDK for [Mansa API](https://mansaapi.com) — African market data, bank codes, location, and financial identity in one clean REST layer.

[![PyPI version](https://img.shields.io/pypi/v/mansaapi.svg)](https://pypi.org/project/mansaapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Install

```bash
pip install mansaapi
```

## Quick start

```python
from mansaapi import MansaAPI

mansa = MansaAPI(api_key="mansa_live_sk_...")

# GTBank by code
bank = mansa.identity.get_bank("058")
print(bank["data"]["name"])        # "Guaranty Trust Bank (GTBank)"
print(bank["data"]["swift_code"])  # "GTBINGLA"

# Pan-African market movers
movers = mansa.markets.get_pan_african_movers(limit=10)

# Nigerian public holidays 2026
holidays = mansa.location.get_holidays("NG", 2026)
```

Get a free API key at [mansaapi.com](https://mansaapi.com) — 100 requests/day, no credit card.

---

## Markets

```python
mansa.markets.get_exchanges()
mansa.markets.get_stocks("NGX", sector="Banking", limit=20)
mansa.markets.get_stock("NGX", "GTCO")
mansa.markets.get_movers("NGX", type="gainers")
mansa.markets.get_pan_african_movers()
mansa.markets.get_indices("NGX")
mansa.markets.get_etfs("NGX")
mansa.markets.get_forex()
mansa.markets.get_commodities()
mansa.markets.search("Zenith", exchange="NGX")
```

### Premium endpoints

Starter tier or higher for dividends, disclosures, recommendations.
Pro tier for insider trades. See [mansaapi.com/pricing](https://mansaapi.com/pricing).

```python
mansa.markets.get_dividends("NGX", "GTCO")          # Starter+
mansa.markets.get_disclosures("NGX", symbol="GTCO")  # Starter+
mansa.markets.get_recommendations("NGX")             # Starter+
mansa.markets.get_insider_trades("NGX", days=30)     # Pro+
```

---

## Identity

```python
mansa.identity.get_banks()                     # all African banks
mansa.identity.get_banks(country="NG")         # filter by country
mansa.identity.get_bank("057")                 # single bank by code
mansa.identity.get_mobile_networks(country="GH")
mansa.identity.lookup_mobile_network("08031234567")
mansa.identity.get_currencies()
mansa.identity.validate_nuban("0123456789", "058")
```

---

## Location

```python
mansa.location.get_countries()
mansa.location.get_country("NG")
mansa.location.get_states("NG")
mansa.location.get_lgas("NG", "LA")        # Lagos LGAs
mansa.location.get_holidays("NG", 2026)
```

---

## Error handling

```python
from mansaapi import MansaAPI, MansaAPIError

mansa = MansaAPI(api_key="mansa_live_sk_...")

try:
    data = mansa.markets.get_insider_trades("NGX")
except MansaAPIError as err:
    print(err.code)     # "TIER_REQUIRED"
    print(err.status)   # 403
    print(err.message)  # "This endpoint requires a professional tier key..."
```

### Error codes

| Code | Status | Meaning |
|---|---|---|
| `INVALID_API_KEY` | 401 | Key not found or revoked |
| `RATE_LIMIT_EXCEEDED` | 429 | Daily request limit reached |
| `TIER_REQUIRED` | 403 | Endpoint requires a higher tier |
| `NOT_FOUND` | 404 | Resource not found |
| `UPSTREAM_ERROR` | 502 | Upstream data source unreachable |

---

## Supported exchanges

NGX (Nigeria), GSE (Ghana), NSE (Kenya), JSE (South Africa), BRVM (West Africa), DSE (Tanzania), LUSE (Zambia).

---

## Links

- [Documentation](https://mansaapi.com/docs)
- [Python quickstart](https://mansaapi.com/docs/quickstart/python)
- [Pricing](https://mansaapi.com/pricing)
- [OpenAPI spec](https://mansaapi.com/openapi.json)
- [api@mansamarkets.com](mailto:api@mansamarkets.com)
