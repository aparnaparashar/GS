from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app(config_object: Config = None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config_object or Config())

    db.init_app(app)

    from .routes.tomtom_routing_routes import tomtom_bp
    from .routes.poi_routes import poi_bp
    from .routes.traffic_routes import traffic_bp
    from .routes.insights_routes import insights_bp
    from .routes.reports_routes import reports_bp

    app.register_blueprint(tomtom_bp, url_prefix="/api/v1/tomtom")
    app.register_blueprint(poi_bp, url_prefix="/api/v1/pois")
    app.register_blueprint(traffic_bp, url_prefix="/api/v1/traffic")
    app.register_blueprint(insights_bp, url_prefix="/api/v1/insights")
    app.register_blueprint(reports_bp, url_prefix="/api/v1/reports")

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
