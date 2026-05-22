import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "2026 서울사케페스티벌 · 사케 4분면 지도",
  description:
    "SSI 4타입 (薰·爽·醇·熟) 기준 691품목 향×맛 점수제 분류. 클릭으로 상세 정보 확인.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500;700&family=Noto+Sans+KR:wght@400;500&family=Shippori+Mincho:wght@500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
