"use client";

import { useState } from "react";
import { getSimilarMovies, getRecommendations } from "../lib/api";

type Movie = {
    id?: string;
    title: string;
    release_date: string;
    vote_average: number;
    predicted_rating?: number;
};


export default function RecommendPage() {
    const [ movieId, setMovieId ] = useState("");
    const [ userId, setUserId ] = useState("");
    const [ similarMovies, setSimilarMovies ] = useState<Movie[]>([]);
    const [ recommendations, setRecommendations ] = useState<Movie[]>([]);
    const [ loadingSimilar, setLoadingSimilar ] = useState(false);
    const [ loadingRec, setLoadingRec ] = useState(false);


    async function handleSimilar() {
        if (!movieId) return;
        setLoadingSimilar(true);
        const data = await getSimilarMovies(Number(movieId));
        setSimilarMovies(data);
        setLoadingSimilar(false);
    }

    async function handleRecommend() {
        if (!userId) return;
        setLoadingRec(true);
        const data = await getRecommendations(Number(userId));
        setRecommendations(data);
        setLoadingRec(false);
    }


    return (
        <main className="min-h-screen bg-gray-50 p-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">추천</h1>
            
            <div className="grid gird-cols-2 gap-6">
                {/* 콘텐츠 기반 추천 */}
                <div className="bg-white rounded-xl shadow p-6">
                    <h2 className="text-lg font-semibold mb-4">유사 영화 추천</h2>
                    <div className="flex gap-2 mb-4">
                        <input 
                            type="number" 
                            placeholder="영화 ID (예: 862)"
                            value={movieId}
                            onChange={(e) => setMovieId(e.target.value)}
                            className="border rounded px-3 py-2 flex-1 text-sm"
                        />
                        <button
                            onClick={handleSimilar}
                            className="bg-indigo-500 text-white px-4 py-2 rounded text-sm hover:bg-indigo-600"
                        >
                            {loadingSimilar ? "검색 중...": "검색"}
                        </button>
                    </div>
                    <table className="w-full text-sm">
                        <thead>
                            <tr className="text-left text-gray-500 border-b">
                                <th className="pb-2">영화</th>
                                <th className="pb-2">개봉일</th>
                                <th className="pb-2">평점</th>
                            </tr>
                        </thead>
                        <tbody>
                            {similarMovies.map((m, i) => (
                                <tr key={i} className="border-b last:border-0">
                                    <td className="py-2">{m.title}</td>
                                    <td className="py-2">{m.release_date}</td>
                                    <td className="py-2">{m.vote_average}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* 협업 필터링 추천 */}
                <div className="bg-white rounded-xl shadow p-6">
                    <h2 className="text-lg font-semibold mb-4">사용자 맞춤 추천</h2>
                    <div className="flex gap-2 mb-4">
                        <input 
                            type="number"
                            placeholder="사용자 ID (예: 1)" 
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            className="border rounded px-3 py-2 flex-1 text-sm"
                        />
                        <button
                            onClick={handleRecommend}
                            className="bg-green-500 text-white px-4 py-2 rounded text-sm hover:bg-green-600"
                        >
                            {loadingRec ? "검색 중...": "검색"}
                        </button>
                    </div>
                    <table className="w-full text-sm">
                        <thead>
                            <tr className="text-left text-gray-500 border-b">
                                <th className="pb-2">영화</th>
                                <th className="pb-2">개봉일</th>
                                <th className="pb-2">예상 평점</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recommendations.map((m, i) => (
                                <tr key={i} className="border-b last:border-0">
                                    <td className="py-2">{m.title}</td>
                                    <td className="py-2">{m.release_date}</td>
                                    <td className="py-2">{m.predicted_rating}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    );
}