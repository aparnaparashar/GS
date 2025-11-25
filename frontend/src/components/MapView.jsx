import React, { useRef, useEffect, useState } from "react";
import maplibregl from "maplibre-gl";
import TomTomRouteLayer from "./MapLayers/TomTomRouteLayer";
import "maplibre-gl/dist/maplibre-gl.css";

const TOMTOM_API_KEY = import.meta.env.VITE_TOMTOM_API_KEY;

export default function MapView({ routeParams }) {
  const mapContainer = useRef(null);
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const defaultCenter = [77.5946, 12.9716];

  useEffect(() => {
    if (mapRef.current) return;

    const style = {
      version: 8,
      sources: {
        "tomtom-tiles": {
          type: "raster",
          tiles: [
            `https://api.tomtom.com/map/1/tile/basic/main/{z}/{x}/{y}.png?key=${TOMTOM_API_KEY}`
          ],
          tileSize: 256
        }
      },
      layers: [
        { id: "tomtom-tiles", type: "raster", source: "tomtom-tiles" }
      ]
    };

    mapRef.current = new maplibregl.Map({
      container: mapContainer.current,
      style: style,
      center: [defaultCenter[0], defaultCenter[1]],
      zoom: 12
    });

    mapRef.current.addControl(new maplibregl.NavigationControl(), "top-right");
    setMap(mapRef.current);

    return () => mapRef.current && mapRef.current.remove();
  }, []);

  return (
    <div className="w-full h-full relative">
      <div ref={mapContainer} className="w-full h-full" />
      {map && routeParams && (
        <TomTomRouteLayer map={map} start={routeParams.start} end={routeParams.end} />
      )}
    </div>
  );
}
