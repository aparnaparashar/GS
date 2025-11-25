from flask import Blueprint, request, send_file
from ..controllers.reports_controller import ReportsController

reports_bp = Blueprint("reports", __name__)
controller = ReportsController()

@reports_bp.route("/area_report", methods=["GET"])
def area_report():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = float(request.args.get("radius", 2000))
    fmt = request.args.get("format", "pdf")
    report_path = controller.generate_area_report(lat, lon, radius, fmt=fmt)
    if fmt == "pdf":
        return send_file(report_path, as_attachment=True, download_name="area_report.pdf")
    else:
        return send_file(report_path, as_attachment=True, download_name="area_report.csv")
