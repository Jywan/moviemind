import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "MovieMind",
    description: "영화 분석 및 추천 대시보드",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="ko">
            <body>{children}</body>
        </html>
    );
}
