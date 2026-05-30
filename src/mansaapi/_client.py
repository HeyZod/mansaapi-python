from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .errors import MansaAPIError

__version__ = "0.1.0"
DEFAULT_BASE_URL = "https://mansaapi.com"

Params = Optional[Dict[str, Any]]


class _HttpClient:
    def __init__(self, api_key: str, base_url: str, timeout: float) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"mansaapi-python/{__version__}",
            }
        )

    def get(self, path: str, params: Params = None) -> Dict[str, Any]:
        clean = {k: v for k, v in (params or {}).items() if v is not None}
        resp = self._session.get(
            f"{self._base_url}{path}", params=clean, timeout=self._timeout
        )
        return self._handle(resp)

    def post(self, path: str, payload: Any) -> Dict[str, Any]:
        resp = self._session.post(
            f"{self._base_url}{path}", json=payload, timeout=self._timeout
        )
        return self._handle(resp)

    @staticmethod
    def _handle(resp: requests.Response) -> Dict[str, Any]:
        try:
            body = resp.json()
        except ValueError:
            raise MansaAPIError(
                "INVALID_RESPONSE",
                f"Non-JSON response (status {resp.status_code})",
                resp.status_code,
                resp.text,
            )

        if not resp.ok or body.get("success") is False:
            err = body.get("error") or {}
            raise MansaAPIError(
                err.get("code", "UNKNOWN_ERROR"),
                err.get("message", f"Request failed with status {resp.status_code}"),
                resp.status_code,
                body,
            )
        return body


class _Markets:
    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    def get_exchanges(self) -> Dict[str, Any]:
        return self._http.get("/api/v1/markets/exchanges")

    def get_exchange(self, exchange_code: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/markets/exchanges/{exchange_code}")

    def get_stocks(self, exchange_code: str, **params: Any) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/markets/exchanges/{exchange_code}/stocks", params)

    def get_stock(self, exchange_code: str, ticker: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/markets/exchanges/{exchange_code}/stocks/{ticker}")

    def get_movers(self, exchange_code: str, **params: Any) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/markets/exchanges/{exchange_code}/movers", params)

    def get_pan_african_movers(self, **params: Any) -> Dict[str, Any]:
        return self._http.get("/api/v1/markets/movers/pan-african", params)

    def get_indices(self, exchange_code: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/markets/exchanges/{exchange_code}/indices")

    def get_index(self, exchange_code: str, code: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/markets/exchanges/{exchange_code}/indices/{code}")

    def get_etfs(self, exchange_code: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/markets/exchanges/{exchange_code}/etfs")

    def get_forex(self) -> Dict[str, Any]:
        return self._http.get("/api/v1/markets/forex")

    def get_commodities(self) -> Dict[str, Any]:
        return self._http.get("/api/v1/markets/commodities")

    def search(self, query: str, **params: Any) -> Dict[str, Any]:
        return self._http.get("/api/v1/markets/search", {"q": query, **params})

    # Premium (Starter+)
    def get_dividends(self, exchange_code: str, ticker: str, **params: Any) -> Dict[str, Any]:
        return self._http.get(
            f"/api/v1/markets/exchanges/{exchange_code}/dividends/{ticker}", params
        )

    def get_disclosures(self, exchange_code: str, **params: Any) -> Dict[str, Any]:
        return self._http.get(
            f"/api/v1/markets/exchanges/{exchange_code}/disclosures", params
        )

    def get_recommendations(self, exchange_code: str, **params: Any) -> Dict[str, Any]:
        return self._http.get(
            f"/api/v1/markets/exchanges/{exchange_code}/recommendations", params
        )

    # Premium (Pro+)
    def get_insider_trades(self, exchange_code: str, **params: Any) -> Dict[str, Any]:
        return self._http.get(
            f"/api/v1/markets/exchanges/{exchange_code}/insider-trades", params
        )


class _Identity:
    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    def get_banks(self, country: Optional[str] = None) -> Dict[str, Any]:
        return self._http.get("/api/v1/identity/banks", {"country": country})

    def get_bank(self, code: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/identity/banks/{code}")

    def get_mobile_networks(self, country: Optional[str] = None) -> Dict[str, Any]:
        return self._http.get("/api/v1/identity/mobile-networks", {"country": country})

    def lookup_mobile_network(self, phone: str) -> Dict[str, Any]:
        return self._http.get("/api/v1/identity/mobile-networks/lookup", {"phone": phone})

    def get_currencies(self) -> Dict[str, Any]:
        return self._http.get("/api/v1/identity/currencies")

    def validate_nuban(self, account: str, bank_code: str) -> Dict[str, Any]:
        return self._http.get(
            "/api/v1/identity/nuban/validate",
            {"account": account, "bank_code": bank_code},
        )


class _Location:
    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    def get_countries(self) -> Dict[str, Any]:
        return self._http.get("/api/v1/location/countries")

    def get_country(self, code: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/location/countries/{code}")

    def get_states(self, country_code: str) -> Dict[str, Any]:
        return self._http.get(f"/api/v1/location/countries/{country_code}/states")

    def get_lgas(self, country_code: str, state_code: str) -> Dict[str, Any]:
        return self._http.get(
            f"/api/v1/location/countries/{country_code}/states/{state_code}/lgas"
        )

    def get_holidays(self, country_code: str, year: int) -> Dict[str, Any]:
        return self._http.get(
            f"/api/v1/location/countries/{country_code}/holidays/{year}"
        )


class _Keys:
    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    def create(self, name: str, email: str, project_description: Optional[str] = None) -> Dict[str, Any]:
        return self._http.post(
            "/api/v1/keys",
            {
                "name": name,
                "email": email,
                "tier": "standard",
                "project_description": project_description,
            },
        )


class MansaAPI:
    """Official Python client for the Mansa API.

    Example:
        from mansaapi import MansaAPI

        mansa = MansaAPI(api_key="mansa_live_sk_...")
        bank = mansa.identity.get_bank("058")
        print(bank["data"]["name"])  # "Guaranty Trust Bank (GTBank)"
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required. Get one free at https://mansaapi.com")
        http = _HttpClient(api_key, base_url, timeout)
        self.markets = _Markets(http)
        self.identity = _Identity(http)
        self.location = _Location(http)
        self.keys = _Keys(http)
