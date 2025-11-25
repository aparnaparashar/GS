from ..services.traffic_service import TrafficService

class TrafficController:
    def __init__(self):
        self.service = TrafficService()

    def ingest_events(self, payload):
        if isinstance(payload, dict):
            events = [payload]
        else:
            events = payload
        return self.service.ingest(events)

    def recent(self, lat, lon, radius):
        return self.service.recent(lat, lon, radius)
