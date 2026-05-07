"use client";

import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

type YearTrend = {
    year: number;
    movie_count: number;
    avg_rating: number;
    avg_revenue: number;
};

export default function YearTrendChart({ data }: { data: YearTrend[] }) {
    return (
        <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">연도별 영화 트렌드</h2>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data} margin={{ left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3"/>
                    <XAxis dataKey="year" tick={{ fontSize: 11 }}/>
                    <YAxis yAxisId="left" domain={[0, 10]} />
                    <YAxis yAxisId="right" orientation="right"/>
                    <Tooltip />
                    <Legend />
                    <Line yAxisId="left" type="monotone" dataKey="avg_rating" stroke="#6366f1" name="평균 평점" dot={false} />
                    <Line yAxisId="right" type="monotone" dataKey="movie_count" stroke="#f59e0b" name="영화 수" dot={false} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}