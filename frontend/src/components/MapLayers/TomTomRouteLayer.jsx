import { useEffect } from "react";
import axios from "axios";
import maplibregl from "maplibre-gl";

const lineStyles = {
  fastest: { color: "#007bff", width: 6 },
  cheapest: { color: "#ffc107", width: 5 },
  eco: { color: "#28a745", width: 5 },
};

export default function TomTomRouteLayer({ map, start, end }) {
  useEffect(() => {
    if (!map || !start || !end) return;
    let mounted = true;

    async function loadRoutes() {
      try {
        const origin = `${start.lat},${start.lng}`;
        const destination = `${end.lat},${end.lng}`;

        const resp = await axios.get("/api/v1/tomtom/route", {
          params: { origin, destination, vehicleType: "car" },
        });

        if (!mounted) return;
        const data = resp.data;
        const routes = data.routes || {};
        let allCoords = [];

        const addRoute = (key, pts) => {
          const layerId = `route-${key}`;
          const sourceId = `route-src-${key}`;
          if (map.getLayer(layerId)) map.removeLayer(layerId);
          if (map.getSource(sourceId)) map.removeSource(sourceId);
          const coordinates = (pts || []).map((p) => [p.longitude, p.latitude]);
          if (coordinates.length === 0) return;
          map.addSource(sourceId, {
            type: "geojson",
            data: { type: "Feature", geometry: { type: "LineString", coordinates } },
          });
          map.addLayer({
            id: layerId,
            type: "line",
            source: sourceId,
            layout: { "line-join": "round", "line-cap": "round" },
            paint: { "line-color": lineStyles[key].color, "line-width": lineStyles[key].width, "line-opacity": 0.95 },
          });
          return coordinates;
        };

        if (routes.fastest && routes.fastest.summary) {
          const pts = routes.fastest.summary.legs?.[0]?.points || routes.fastest.summary.shape || [];
          const coords = addRoute("fastest", pts);
          if (coords) allCoords = allCoords.concat(coords);
        }
        if (routes.cheapest && routes.cheapest.summary) {
          const pts = routes.cheapest.summary.legs?.[0]?.points || routes.cheapest.summary.shape || [];
          const coords = addRoute("cheapest", pts);
          if (coords) allCoords = allCoords.concat(coords);
        }
        if (routes.eco && routes.eco.summary) {
          const pts = routes.eco.summary.legs?.[0]?.points || routes.eco.summary.shape || [];
          const coords = addRoute("eco", pts);
          if (coords) allCoords = allCoords.concat(coords);
        }

        if (allCoords.length > 0) {
          const bbox = allCoords.reduce((b, c) => b.extend(c), new maplibregl.LngLatBounds(allCoords[0], allCoords[0]));
          map.fitBounds(bbox, { padding: 60, linear: true });
        }
      } catch (err) {
        console.error("Error loading routes:", err);
      }
    }

    loadRoutes();
    return () => { mounted = false; };
  }, [map, start, end]);

  return null;
}
