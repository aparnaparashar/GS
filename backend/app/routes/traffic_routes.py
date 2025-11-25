from flask import Blueprint, request, jsonify
from ..controllers.traffic_controller import TrafficController

traffic_bp = Blueprint("traffic", __name__)
controller = TrafficController()

@traffic_bp.route("/ingest", methods=["POST"])
def ingest():
    payload = request.get_json()
    controller.ingest_events(payload)
    return jsonify({"status": "ok"}), 201

@traffic_bp.route("/recent", methods=["GET"])
def recent():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = float(request.args.get("radius", 1000))
    return jsonify(controller.recent(lat, lon, radius)), 200
