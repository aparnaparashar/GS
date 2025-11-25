import React from "react";

export default function Dashboard() {
  return (
    <div>
      <h2 className="text-lg font-semibold">Insights</h2>
      <div className="mt-3 grid gap-3">
        <div className="p-3 border rounded">
          <h3 className="font-medium">Busiest Hours</h3>
          <p className="text-sm text-gray-600">6 — 8 PM (Auto-detected from traffic data)</p>
        </div>
        <div className="p-3 border rounded">
          <h3 className="font-medium">Quiet Zones (Evening)</h3>
          <p className="text-sm text-gray-600">Parks and waterfront promenades</p>
        </div>
        <div className="p-3 border rounded">
          <h3 className="font-medium">Route Comparison</h3>
          <p className="text-sm text-gray-600">Fastest vs Eco vs Cheapest visible on map</p>
        </div>
      </div>
    </div>
  );
}
