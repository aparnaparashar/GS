from ..models import POI
from .. import db
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import text

class POIService:
    def search(self, q=None, lat=None, lon=None, radius=1000):
        qfilter = POI.query
        if q:
            qfilter = qfilter.filter(POI.name.ilike(f"%{q}%"))
        if lat and lon:
            point = f"SRID=4326;POINT({float(lon)} {float(lat)})"
            sql = text("""
                SELECT id, name, category, ST_AsGeoJSON(geom) as geojson,
                       properties
                  FROM pois
                 WHERE ST_DWithin(geom::geography, ST_GeomFromText(:pt)::geography, :radius)
                 ORDER BY ST_Distance(geom::geography, ST_GeomFromText(:pt)::geography) ASC
                 LIMIT 200
            """)
            res = db.session.execute(sql, {"pt": point, "radius": radius})
            out = []
            for row in res:
                out.append({
                    "id": row.id,
                    "name": row.name,
                    "category": row.category,
                    "geom": row.geojson,
                    "properties": row.properties
                })
            return out
        else:
            items = qfilter.limit(200).all()
            return [{"id": p.id, "name": p.name, "category": p.category} for p in items]

    def create(self, data):
        name = data.get("name")
        category = data.get("category")
        lat = data.get("lat")
        lon = data.get("lon")
        properties = data.get("properties", {})
        if not name or lat is None or lon is None:
            raise ValueError("name, lat, lon required")
        geom = from_shape(Point(float(lon), float(lat)), srid=4326)
        poi = POI(name=name, category=category, properties=properties, geom=geom)
        db.session.add(poi)
        db.session.commit()
        return {"id": poi.id, "name": poi.name}
