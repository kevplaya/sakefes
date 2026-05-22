"use client";

import { useMemo, useState } from "react";
import sakesData from "@/data/sakes.json";
import { Sake, SakeClass } from "@/lib/types";
import QuadrantChart from "@/components/QuadrantChart";
import SakeDetail from "@/components/SakeDetail";
import Filters from "@/components/Filters";

const ALL_SAKES = sakesData as Sake[];
const ALL_CLASSES: SakeClass[] = ["薰 Kun", "醇 Jun", "爽 Sou", "熟 Juku", "Other"];

export default function Page() {
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [visibleClasses, setVisibleClasses] = useState<Set<SakeClass>>(
    new Set(ALL_CLASSES)
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return ALL_SAKES;
    return ALL_SAKES.filter((s) =>
      [s.product, s.brewery, s.booth, s.region, s.note]
        .join(" ")
        .toLowerCase()
        .includes(q)
    );
  }, [query]);

  const counts = useMemo(() => {
    const c: Record<SakeClass, number> = {
      "薰 Kun": 0,
      "醇 Jun": 0,
      "爽 Sou": 0,
      "熟 Juku": 0,
      Other: 0,
    };
    for (const s of filtered) c[s.class]++;
    return c;
  }, [filtered]);

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

  // All sakes sharing same integer (aroma, richness) as selected — within currently
  // visible classes + active search filter so cluster respects user's view.
  const cluster = useMemo(() => {
    if (!selected) return [];
    return filtered.filter(
      (s) =>
        visibleClasses.has(s.class) &&
        s.aroma === selected.aroma &&
        s.richness === selected.richness
    );
  }, [selected, filtered, visibleClasses]);

  return (
    <main className="min-h-screen px-4 md:px-8 py-6 md:py-10 max-w-[1400px] mx-auto">
      <Header />

      <div className="grid lg:grid-cols-[1fr_360px] gap-6 mt-6">
        <section className="washi-card rounded-md p-3 md:p-5">
          <QuadrantChart
            sakes={filtered}
            selectedId={selectedId}
            onSelect={(s) => setSelectedId(s?.id ?? null)}
            visibleClasses={visibleClasses}
          />
        </section>

        <aside className="space-y-4">
          <Filters
            query={query}
            onQuery={setQuery}
            visibleClasses={visibleClasses}
            counts={counts}
            onToggleClass={(c) => {
              const next = new Set(visibleClasses);
              if (next.has(c)) next.delete(c);
              else next.add(c);
              setVisibleClasses(next);
            }}
          />
          <SakeDetail
            sake={selected}
            onClose={() => setSelectedId(null)}
            related={related}
            cluster={cluster}
            onSelect={(s) => setSelectedId(s.id)}
          />
        </aside>
      </div>

      <Footer total={ALL_SAKES.length} shown={filtered.length} />
    </main>
  );
}

function Header() {
  return (
    <header className="flex items-center justify-between">
      <div>
        <div className="font-deco text-shu text-xs tracking-[0.4em] mb-1">
          清 酒 地 圖 · SAKE MAP
        </div>
        <h1 className="font-serif text-3xl md:text-4xl text-sumi leading-tight">
          2026 서울사케페스티벌
          <span className="ml-3 text-shu text-2xl">四 分 面 圖</span>
        </h1>
        <p className="text-sm text-sumi/70 mt-1 font-sans">
          SSI 香味特性 분류 · 691품목 향(香) × 맛(味) 점수제
        </p>
      </div>
      <div className="hidden md:flex flex-col items-end gap-1 text-sumi/60 font-deco">
        <div className="kanji-vertical text-2xl text-shu/80">薰爽醇熟</div>
      </div>
    </header>
  );
}

function Footer({ total, shown }: { total: number; shown: number }) {
  return (
    <footer className="mt-8 text-xs text-sumi/50 font-sans flex flex-wrap items-center gap-x-4 gap-y-1">
      <span>출처: <a className="underline hover:text-shu" href="https://www.sakefestival.co.kr/44" target="_blank" rel="noreferrer">sakefestival.co.kr/44</a></span>
      <span>·</span>
      <span><a className="underline hover:text-shu" href="https://www.sakefestival.co.kr/45" target="_blank" rel="noreferrer">/45</a></span>
      <span>·</span>
      <span>분류 기준: <a className="underline hover:text-shu" href="https://www.bosa.co.kr/news/articleView.html?idxno=2109371" target="_blank" rel="noreferrer">SSI 4타입 (보사뉴스)</a></span>
      <span>·</span>
      <span>표시 {shown}/{total} 품목</span>
    </footer>
  );
}
