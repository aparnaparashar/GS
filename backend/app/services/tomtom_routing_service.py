import requests
from typing import List, Dict, Any, Optional
from ..config import Config
from ..utils.cache import TTLCache

CONFIG = Config()
_cache = TTLCache(default_ttl_seconds=CONFIG.ROUTING_CACHE_TTL_SECONDS)

class TomTomRoutingService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or CONFIG.TOMTOM_API_KEY
        if not self.api_key:
            raise RuntimeError("TOMTOM_API_KEY is not configured")
        self.base = CONFIG.TOMTOM_BASE_URL.rstrip("/")

    def _build_coords(self, origin: str, destination: str, waypoints: List[str]) -> str:
        coords = [origin] + waypoints + [destination]
        return ":".join(coords)

    def _call_routing(self, coords_param: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base}/routing/1/calculateRoute/{coords_param}/json"
        params = dict(params)
        params["key"] = self.api_key
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def _extract_route_summary(self, route_json: Dict[str, Any]) -> Dict[str, Any]:
        routes = route_json.get("routes") or []
        if not routes:
            return {"distance_meters": None, "travel_time_seconds": None, "legs": [], "raw": route_json}
        route = routes[0]
        summary = route.get("summary", {})
        legs = route.get("legs", [])
        shape = route.get("shape")
        return {
            "distance_meters": summary.get("lengthInMeters"),
            "travel_time_seconds": summary.get("travelTimeInSeconds"),
            "traffic_delay_seconds": summary.get("trafficDelayInSeconds", 0),
            "legs": legs,
            "shape": shape,
            "raw": route_json
        }

    def _cache_key(self, origin: str, destination: str, waypoints: List[str], variant: str, vehicle_type: str) -> str:
        return "|".join([origin, destination, ";".join(waypoints), variant, vehicle_type])

    def get_three_routes(self, origin: str, destination: str, waypoints: List[str], vehicle_type: str="car") -> Dict[str, Any]:
        coords_param = self._build_coords(origin, destination, waypoints)
        variants = {
            "fastest": {"routeType": "fastest", "travelMode": vehicle_type},
            "cheapest": {"routeType": "shortest", "travelMode": vehicle_type, "avoid": "tollRoad"},
            "eco": {"routeType": "eco", "travelMode": vehicle_type}
        }
        results: Dict[str, Any] = {}
        for name, params in variants.items():
            key = self._cache_key(origin, destination, waypoints, name, vehicle_type)
            cached = _cache.get(key)
            if cached:
                results[name] = {"from_cache": True, **cached}
                continue
            try:
                response_json = self._call_routing(coords_param=coords_param, params=params)
                summary = self._extract_route_summary(response_json)
                cost_estimate = self._estimate_cost(summary["distance_meters"], vehicle_type, variant=name)
                eco_score = self._estimate_eco_score(summary["distance_meters"], summary["travel_time_seconds"], name)
                out = {"summary": summary, "cost_estimate": cost_estimate, "eco_score": eco_score, "variant": name}
                _cache.set(key, out)
                results[name] = {"from_cache": False, **out}
            except requests.HTTPError as e:
                results[name] = {"error": f"TomTom API HTTP error: {str(e)}"}
            except Exception as e:
                results[name] = {"error": f"internal error: {str(e)}"}
        comp = self._build_comparison(results)
        return {"routes": results, "comparison": comp}

    def _estimate_cost(self, distance_meters: Optional[int], vehicle_type: str, variant: str) -> Dict[str, Any]:
        if distance_meters is None:
            return {"estimated_fuel_cost": None, "currency": "INR"}
        distance_km = distance_meters / 1000.0
        if vehicle_type == "truck":
            consumption = 0.25
        else:
            consumption = 0.08
        fuel_price_per_liter = 100.0
        fuel_cost = distance_km * consumption * fuel_price_per_liter
        if variant == "cheapest":
            fuel_cost *= 0.95
        return {"estimated_fuel_cost": round(fuel_cost, 2), "currency": "INR"}

    def _estimate_eco_score(self, distance_meters: Optional[int], travel_time_seconds: Optional[int], variant: str) -> float:
        if distance_meters is None or travel_time_seconds is None:
            return -1.0
        score = max(0.0, 100.0 - (distance_meters/1000.0)*0.5 - (travel_time_seconds/60.0)*0.2)
        if variant == "eco":
            score += 5.0
        return round(min(100.0, score), 2)

    def _build_comparison(self, results: Dict[str, Any]) -> Dict[str, Any]:
        summary = {}
        fastest = None
        cheapest = None
        best_eco = None
        for name, item in results.items():
            if "summary" not in item:
                continue
            s = item["summary"]
            travel_time = s.get("travel_time_seconds") or float("inf")
            dist = s.get("distance_meters") or float("inf")
            cost = item.get("cost_estimate", {}).get("estimated_fuel_cost") or float("inf")
            eco_score = item.get("eco_score", -1.0)
            if fastest is None or travel_time < fastest["travel_time_seconds"]:
                fastest = {"variant": name, "travel_time_seconds": travel_time, "distance_meters": dist}
            if cheapest is None or cost < cheapest["cost"]:
                cheapest = {"variant": name, "cost": cost, "distance_meters": dist}
            if best_eco is None or eco_score > best_eco["eco_score"]:
                best_eco = {"variant": name, "eco_score": eco_score, "distance_meters": dist}
        summary["fastest"] = fastest
        summary["cheapest"] = cheapest
        summary["best_eco"] = best_eco
        return summary
