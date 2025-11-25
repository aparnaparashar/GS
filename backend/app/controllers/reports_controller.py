from ..services.report_generator import ReportGenerator

class ReportsController:
    def __init__(self):
        self.generator = ReportGenerator()

    def generate_area_report(self, lat, lon, radius, fmt="pdf"):
        return self.generator.generate_area_report(lat, lon, radius, fmt=fmt)
