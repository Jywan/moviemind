const BASE_URL = "http://localhost:8000";

export async function getGenreStats() {
    const res = await fetch(`${BASE_URL}/analysis/genre`);
    return res.json();
}

export async function getYearTrend() {
    const res = await fetch(`${BASE_URL}/analysis/year-trend`);
    return res.json();
}

export async function getTopDirectors() {
    const res = await fetch(`${BASE_URL}/analysis/top-directors`);
    return res.json();
}

export async function getTopActors() {
    const res = await fetch(`${BASE_URL}/analysis/top-actors`);
    return res.json();
}

export async function getRoiAnalysis() {
    const res = await fetch(`${BASE_URL}/analysis/roi`);
    return res.json();
}