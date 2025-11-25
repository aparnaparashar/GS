from flask import Blueprint, request, jsonify
from ..controllers.poi_controller import POIController

poi_bp = Blueprint("pois", __name__)
controller = POIController()

@poi_bp.route("/", methods=["GET"])
def list_pois():
    q = request.args.get("q")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = float(request.args.get("radius", 1000))
    pois = controller.search_pois(q=q, lat=lat, lon=lon, radius=radius)
    return jsonify(pois), 200

@poi_bp.route("/", methods=["POST"])
def add_poi():
    data = request.get_json()
    poi = controller.create_poi(data)
    return jsonify(poi), 201
