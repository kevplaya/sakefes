"use client";

import { useMemo, useState } from "react";
import sakesData from "@/data/sakes.json";
import { Sake, SakeClass, CLASS_INFO } from "@/lib/types";
import QuadrantChart from "@/components/QuadrantChart";
import SakeDetail from "@/components/SakeDetail";

const ALL_SAKES = sakesData as Sake[];
const ALL_CLASSES: SakeClass[] = ["薰 Kun", "醇 Jun", "爽 Sou", "熟 Juku", "Other"];
const VISIBLE_ALL = new Set<SakeClass>(ALL_CLASSES);

export default function Page() {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const selected = useMemo(
    () => ALL_SAKES.find((s) => s.id === selectedId) ?? null,
    [selectedId]
  );

  const related = useMemo(() => {
    if (!selected) return [];
    return ALL_SAKES.filter(
      (s) => s.brewery === selected.brewery && s.id !== selected.id
    );
  }, [selected]);

  const cluster = useMemo(() => {
    if (!selected) return [];
    return ALL_SAKES.filter(
      (s) => s.aroma === selected.aroma && s.richness === selected.richness
    );
  }, [selected]);

  return (
    <main className="min-h-screen px-4 md:px-8 py-6 md:py-10 max-w-[1400px] mx-auto">
      <Header />

      <div className="grid lg:grid-cols-[1fr_360px] gap-6 mt-6">
        <section className="washi-card rounded-md p-3 md:p-5">
          <QuadrantChart
            sakes={ALL_SAKES}
            selectedId={selectedId}
            onSelect={(s) => setSelectedId(s?.id ?? null)}
            visibleClasses={VISIBLE_ALL}
          />
          <Legend />
        </section>

        <aside className="space-y-4">
          <SakeDetail
            sake={selected}
            onClose={() => setSelectedId(null)}
            related={related}
            cluster={cluster}
            onSelect={(s) => setSelectedId(s.id)}
          />
        </aside>
      </div>

      <Footer total={ALL_SAKES.length} />
    </main>
  );
}

function Header() {
  return (
    <header className="flex items-center justify-between">
      <div>
        <div className="font-deco text-shu text-sm tracking-[0.4em] mb-1.5">
          清 酒 地 圖 · SAKE MAP
        </div>
        <h1 className="font-serif text-4xl md:text-5xl text-sumi leading-tight">
          2026 서울사케페스티벌
        </h1>
        <p className="text-base text-sumi/70 mt-1.5 font-sans">
          SSI 香味特性 분류 · 691품목 향(香) × 맛(味) 점수제
        </p>
      </div>
      <div className="hidden md:flex flex-col items-end gap-1 text-sumi/60 font-deco">
        <div className="kanji-vertical text-3xl text-shu/80">薰爽醇熟</div>
      </div>
    </header>
  );
}

function Legend() {
  return (
    <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm font-sans text-sumi/70">
      {(["薰 Kun", "熟 Juku", "醇 Jun", "爽 Sou", "Other"] as SakeClass[]).map((c) => (
        <span key={c} className="inline-flex items-center gap-1.5">
          <span
            className="w-3 h-3 rounded-full inline-block"
            style={{ background: CLASS_INFO[c].color, border: "1px solid rgba(31,29,26,0.3)" }}
          />
          <span className="font-serif text-sumi/85">{c.split(" ")[0]}</span>
          <span className="text-sumi/45">{CLASS_INFO[c].ko}</span>
        </span>
      ))}
    </div>
  );
}

function Footer({ total }: { total: number }) {
  return (
    <footer className="mt-8 text-sm text-sumi/50 font-sans flex flex-wrap items-center gap-x-4 gap-y-1">
      <span>출처: <a className="underline hover:text-shu" href="https://www.sakefestival.co.kr/44" target="_blank" rel="noreferrer">sakefestival.co.kr/44</a></span>
      <span>·</span>
      <span><a className="underline hover:text-shu" href="https://www.sakefestival.co.kr/45" target="_blank" rel="noreferrer">/45</a></span>
      <span>·</span>
      <span>분류 기준: <a className="underline hover:text-shu" href="https://www.bosa.co.kr/news/articleView.html?idxno=2109371" target="_blank" rel="noreferrer">SSI 4타입 (보사뉴스)</a></span>
      <span>·</span>
      <span>{total}품목</span>
    </footer>
  );
}
