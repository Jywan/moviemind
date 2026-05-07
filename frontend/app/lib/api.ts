const BASE_URL = "http://localhost:8000";

export async function getGenreStats() {
    const res = await fetch(`${BASE_URL}/analysis/genre`);
    return res.json();
}

export async function getYearTrend() {
    const res = await fetch(`${BASE_URL}/analysis/year-trend`);
    return res.json();
}