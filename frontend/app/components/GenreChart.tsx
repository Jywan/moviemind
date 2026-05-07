"use client";

import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

type GenreStat = {
    genre_name: string;
    avg_rating: number;
    movie_count: number;
};

export default function GenreChart({ data }: { data: GenreStat[] }) {
    return (
        <div className="bt-white rouned-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">장르별 평균 평점</h2>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data} layout="vertical" margin={{ left: 80 }}>
                    <CartesianGrid strokeDasharray={"3 3"} />
                    <XAxis type="number" domain={[0, 10]} />
                    <YAxis type="category" dataKey="genre_name" tick={{ fontSize: 12 }}/>
                    <Tooltip />
                    <Bar dataKey="avg_rating" fill="#6366f1" radius={[0, 4, 4, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}