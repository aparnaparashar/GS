from . import db
from sqlalchemy.dialects.postgresql import JSON
from geoalchemy2 import Geometry
from datetime import datetime

class POI(db.Model):
    __tablename__ = "pois"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(128), nullable=True)
    properties = db.Column(JSON, nullable=True)
    geom = db.Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

class TrafficEvent(db.Model):
    __tablename__ = "traffic_events"
    id = db.Column(db.BigInteger, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    geom = db.Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    speed = db.Column(db.Float, nullable=True)
    congestion_level = db.Column(db.Integer, nullable=True)
    raw = db.Column(JSON, nullable=True)
