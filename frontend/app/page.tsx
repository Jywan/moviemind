import { getGenreStats, getYearTrend } from "./lib/api";
import GenreChart from "./components/GenreChart";
import YearTrendChart from "./components/YearTrendChart";

export default async function Home() {
  const [genreStats, yearTrend] = await Promise.all([
    getGenreStats(),
    getYearTrend(),
  ]);

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">MovieMind Dashboard</h1>
      <div className="grid gap-6">
        <GenreChart data={genreStats} />
        <YearTrendChart data={yearTrend} />
      </div>
    </main>
  );
}