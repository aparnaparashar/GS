from typing import Optional
from ..services.poi_service import POIService

class POIController:
    def __init__(self):
        self.service = POIService()

    def search_pois(self, q: Optional[str], lat: Optional[str], lon: Optional[str], radius: float):
        return self.service.search(q=q, lat=lat, lon=lon, radius=radius)

    def create_poi(self, data):
        return self.service.create(data)
