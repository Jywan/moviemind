"use client";

export default function Error({
    error,
    reset,
}: {
    error: Error;
    reset: () => void;
}) {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen gap-4">
            <p className="text-gray-600">데이터를 불러오는 중 오류가 발생하였습니다.</p>
            <button
                onClick={reset}
                className="bg-indigo-500 text-white px-4 py-2 rounded text-sm hover:bg-indigo-600"
            >
                다시 시도
            </button>
        </div>
    );
}