import React, { useState } from "react";

export default function RouteInputPanel({ onPlan }) {
  const [origin, setOrigin] = useState("12.9715987,77.594566");
  const [destination, setDestination] = useState("12.935242,77.624481");

  function handlePlan(e) {
    e.preventDefault();
    const parse = (s) => {
      const [lat, lng] = s.split(",").map((v) => parseFloat(v.trim()));
      return { lat, lng };
    };
    onPlan({ start: parse(origin), end: parse(destination) });
  }

  return (
    <form onSubmit={handlePlan} className="space-y-3">
      <label className="block text-sm font-medium">Origin (lat,lon)</label>
      <input
        value={origin}
        onChange={(e) => setOrigin(e.target.value)}
        className="w-full p-2 border rounded"
      />

      <label className="block text-sm font-medium">Destination (lat,lon)</label>
      <input
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
        className="w-full p-2 border rounded"
      />

      <button className="mt-2 w-full bg-sky-600 text-white p-2 rounded">Plan Routes</button>
    </form>
  );
}
