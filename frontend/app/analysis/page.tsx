import { getTopDirectors, getTopActors, getRoiAnalysis } from "../lib/api";

type Person = {
    director?: string;
    actor?: string;
    movie_count: number;
    avg_rating: number;
};

type RoiItem = {
    title: string;
    year: number;
    budget: number;
    revenue: number;
    roi: number;
};

function RankTable({ title, data, nameKey }: {title: string, data: Person[], nameKey: "director" | "actor"}) {
    return (
        <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">{title}</h2>
            <table className="w-full text-sm">
                <thead>
                    <tr className="text-left text-gray-500 border-b">
                        <th className="pb-2">이름</th>
                        <th className="pb-2">영화 수</th>
                        <th className="pb-2">평균 평점</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, i) => (
                        <tr key={i} className="border-b last:border-0">
                            <td className="py-2">{row[nameKey]}</td>
                            <td className="py-2">{row.movie_count}</td>
                            <td className="py-2">{row.avg_rating}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

function RoiTable({ data }: { data: RoiItem[] }) {
    return (
        <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">예산 대비 수익률 TOP 10</h2>
            <table className="w-full text-sm">
                <thead>
                    <tr className="text-left text-gray-500 border-b">
                        <th className="pb-2">영화</th>
                        <th className="pb-2">연도</th>
                        <th className="pb-2">예산</th>
                        <th className="pb-2">수익</th>
                        <th className="pb-2">ROI (%)</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, i) => (
                        <tr key={i} className="border-b last:border-0">
                            <th className="pb-2">{row.title}</th>
                            <th className="pb-2">{row.year}</th>
                            <td className="py-2">${(row.budget / 1_000_000).toFixed(1)}M</td>
                            <td className="py-2">${(row.revenue / 1_000_000).toFixed(1)}M</td>
                            <td className="py-2 text-green-600 font-medium">{row.roi.toLocaleString()}%</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default async function AnalysisPage() {
    const [directors, actors, roi] = await Promise.all([
        getTopDirectors(),
        getTopActors(),
        getRoiAnalysis(),
    ]);

    return (
        <main className="min-h-screen bg-gray-50 p-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">분석</h1>
            <div className="grid grid-cols-2 gap-6 mb-6">
                <RankTable title="인기 감독 TOP 10" data={directors} nameKey="director" />
                <RankTable title="인기 배우 TOP 10" data={actors} nameKey="actor" />
            </div>
            <RoiTable data={roi}/>
        </main>
    );
}