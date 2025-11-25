const TOMTOM_API_KEY = import.meta.env.VITE_TOMTOM_API_KEY;
const BASE_URL = "https://api.tomtom.com/routing/1/calculateRoute";

async function fetchRoute(start, end, routeType, extraParams = "") {
  const url = `${BASE_URL}/${start.lat},${start.lng}:${end.lat},${end.lng}/json?routeType=${routeType}&key=${TOMTOM_API_KEY}${extraParams}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`TomTom API error: ${res.status}`);
  return res.json();
}

export async function getFastestRoute(start, end) {
  return fetchRoute(start, end, "fastest");
}
export async function getCheapestRoute(start, end) {
  return fetchRoute(start, end, "shortest", "&travelMode=car");
}
export async function getEcoFriendlyRoute(start, end) {
  return fetchRoute(start, end, "eco", "&travelMode=car");
}
export async function getAllRoutes(start, end) {
  try {
    const [fastest, cheapest, eco] = await Promise.all([
      getFastestRoute(start, end),
      getCheapestRoute(start, end),
      getEcoFriendlyRoute(start, end),
    ]);
    return { fastest, cheapest, eco };
  } catch (err) {
    console.error("Error fetching routes:", err);
    throw err;
  }
}
