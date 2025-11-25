from ..services.insights_service import InsightsService

class InsightsController:
    def __init__(self):
        self.service = InsightsService()

    def busiest_hours(self, lat, lon, radius):
        return self.service.compute_busiest_hours(lat, lon, radius)

    def hotspots(self, lat, lon, radius):
        return self.service.compute_hotspots(lat, lon, radius)
