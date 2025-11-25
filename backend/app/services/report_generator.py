import tempfile, os, csv
from fpdf import FPDF
from ..services.insights_service import InsightsService

class ReportGenerator:
    def __init__(self):
        self.insights = InsightsService()

    def generate_area_report(self, lat, lon, radius, fmt="pdf"):
        busiest = self.insights.compute_busiest_hours(lat, lon, radius)
        hotspots = self.insights.compute_hotspots(lat, lon, radius)
        if fmt == "csv":
            fd, path = tempfile.mkstemp(suffix=".csv")
            with os.fdopen(fd, "w", newline="") as fh:
                writer = csv.writer(fh)
                writer.writerow(["type", "key", "value"])
                writer.writerow(["busiest_hours", "histogram", str(busiest.get("histogram"))])
                writer.writerow(["hotspots", "count", len(hotspots.get("hotspots", []))])
            return path
        pdf = FPDF()
        pdf.set_auto_page_break(True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "GeoSense Area Report", ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.ln(4)
        pdf.cell(0, 8, f"Location: {lat},{lon}  Radius: {radius}m", ln=1)
        pdf.ln(4)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Busiest Hours (last 7 days):", ln=1)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, str(busiest.get("histogram")))
        pdf.ln(4)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Top Hotspots:", ln=1)
        pdf.set_font("Arial", "", 11)
        for h in hotspots.get("hotspots", []):
            pdf.multi_cell(0, 6, f"{h.get('geom')} — count: {h.get('count')}")
        fd, path = tempfile.mkstemp(suffix=".pdf")
        pdf.output(path)
        return path
