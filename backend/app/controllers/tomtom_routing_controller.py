from typing import Optional, Dict, Any
from ..services.tomtom_routing_service import TomTomRoutingService

class TomTomRoutingController:
    def __init__(self):
        self.service = TomTomRoutingService()

    def get_comparison_routes(self, origin: str, destination: str, via: Optional[str] = None, vehicle_type: str = "car") -> Dict[str, Any]:
        def _valid_coord_pair(s: str) -> bool:
            if not s: return False
            parts = s.split(",")
            return len(parts) == 2
        if not _valid_coord_pair(origin) or not _valid_coord_pair(destination):
            raise ValueError("origin and destination must be 'lat,lon'")
        waypoints = []
        if via:
            waypoints = [p.strip() for p in via.split(";") if p.strip()]
        return self.service.get_three_routes(origin=origin, destination=destination, waypoints=waypoints, vehicle_type=vehicle_type)
