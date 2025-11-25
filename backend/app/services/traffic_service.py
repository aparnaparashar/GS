from ..models import TrafficEvent
from .. import db
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from datetime import datetime

class TrafficService:
    def ingest(self, events):
        out = []
        for e in events:
            lat = e.get("lat")
            lon = e.get("lon")
            speed = e.get("speed")
            congestion = e.get("congestion_level")
            raw = e
            if lat is None or lon is None:
                continue
            geom = from_shape(Point(float(lon), float(lat)), srid=4326)
            te = TrafficEvent(geom=geom, speed=speed, congestion_level=congestion, raw=raw, timestamp=datetime.utcnow())
            db.session.add(te)
            out.append(raw)
        db.session.commit()
        return out

    def recent(self, lat, lon, radius=1000):
        from sqlalchemy import text
        point = f"SRID=4326;POINT({float(lon)} {float(lat)})"
        sql = text("""
            SELECT id, timestamp, ST_AsGeoJSON(geom) as geojson, speed, congestion_level
              FROM traffic_events
             WHERE timestamp > now() - interval '2 hour'
               AND ST_DWithin(geom::geography, ST_GeomFromText(:pt)::geography, :radius)
             ORDER BY timestamp DESC
             LIMIT 500
        """)
        res = db.session.execute(sql, {"pt": point, "radius": radius})
        return [dict(r) for r in res]
