from flask import Blueprint, request, jsonify
from ..controllers.insights_controller import InsightsController

insights_bp = Blueprint("insights", __name__)
controller = InsightsController()

@insights_bp.route("/busiest_hours", methods=["GET"])
def busiest_hours():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = float(request.args.get("radius", 1000))
    return jsonify(controller.busiest_hours(lat, lon, radius)), 200

@insights_bp.route("/hotspots", methods=["GET"])
def hotspots():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = float(request.args.get("radius", 2000))
    return jsonify(controller.hotspots(lat, lon, radius)), 200
