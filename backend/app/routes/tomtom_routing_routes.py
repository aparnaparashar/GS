from flask import Blueprint, request, jsonify
from ..controllers.tomtom_routing_controller import TomTomRoutingController

tomtom_bp = Blueprint("tomtom_routing", __name__)
controller = TomTomRoutingController()

@tomtom_bp.route("/route", methods=["GET"])
def get_three_routes():
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    via = request.args.get("via")
    vehicle_type = request.args.get("vehicleType", "car")
    if not origin or not destination:
        return jsonify({"error": "origin and destination are required"}), 400
    try:
        resp = controller.get_comparison_routes(origin=origin, destination=destination, via=via, vehicle_type=vehicle_type)
        return jsonify(resp), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "internal_server_error", "details": str(e)}), 500
