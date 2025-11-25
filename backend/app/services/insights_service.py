from .. import db
from sqlalchemy import text

class InsightsService:
    def compute_busiest_hours(self, lat, lon, radius):
        pt = f"SRID=4326;POINT({float(lon)} {float(lat)})"
        sql = text("""
            SELECT extract(hour from timestamp) as hour, count(*) as cnt
              FROM traffic_events
             WHERE timestamp > now() - interval '7 day'
               AND ST_DWithin(geom::geography, ST_GeomFromText(:pt)::geography, :radius)
             GROUP BY hour
             ORDER BY hour
        """)
        res = db.session.execute(sql, {"pt": pt, "radius": radius})
        hist = {int(row.hour): int(row.cnt) for row in res}
        return {"histogram": hist}

    def compute_hotspots(self, lat, lon, radius):
        pt = f"SRID=4326;POINT({float(lon)} {float(lat)})"
        sql = text("""
            SELECT ST_AsGeoJSON(geom) as geojson, count(*) as cnt
              FROM traffic_events
             WHERE timestamp > now() - interval '7 day'
               AND ST_DWithin(geom::geography, ST_GeomFromText(:pt)::geography, :radius)
             GROUP BY geojson
             ORDER BY cnt DESC
             LIMIT 20
        """)
        res = db.session.execute(sql, {"pt": pt, "radius": radius})
        out = [{"geom": row.geojson, "count": int(row.cnt)} for row in res]
        return {"hotspots": out}
