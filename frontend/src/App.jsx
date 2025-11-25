import React, { useState } from "react";
import MapView from "./components/MapView";
import RouteInputPanel from "./components/RouteInputPanel";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [routeParams, setRouteParams] = useState(null);

  return (
    <div className="h-screen flex flex-col">
      <header className="bg-white shadow p-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold">GeoSense</h1>
        <div className="text-sm text-gray-600">TomTom-powered maps & routing</div>
      </header>

      <main className="flex-1 flex">
        <aside className="w-96 border-r p-4 overflow-auto">
          <RouteInputPanel onPlan={(params) => setRouteParams(params)} />
          <hr className="my-4" />
          <Dashboard />
        </aside>

        <section className="flex-1">
          <MapView routeParams={routeParams} />
        </section>
      </main>
    </div>
  );
}
