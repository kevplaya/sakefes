"use client";

import { useMemo, useState } from "react";
import sakesData from "@/data/sakes.json";
import { Sake, SakeClass, CLASS_INFO } from "@/lib/types";
import QuadrantChart from "@/components/QuadrantChart";
import SakeDetail from "@/components/SakeDetail";
import BoothView from "@/components/BoothView";

const ALL_SAKES = sakesData as Sake[];
const ALL_CLASSES: SakeClass[] = ["薰 Kun", "醇 Jun", "爽 Sou", "熟 Juku", "Other"];
const VISIBLE_ALL = new Set<SakeClass>(ALL_CLASSES);

type View = "quadrant" | "booth";

export default function Page() {
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [view, setView] = useState<View>("quadrant");

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
      <Tabs view={view} onChange={setView} />

      <div className="grid lg:grid-cols-[1fr_360px] gap-6 mt-5">
        {view === "quadrant" ? (
          <section className="washi-card rounded-md p-3 md:p-5">
            <QuadrantChart
              sakes={ALL_SAKES}
              selectedId={selectedId}
              onSelect={(s) => setSelectedId(s?.id ?? null)}
              visibleClasses={VISIBLE_ALL}
            />
            <Legend />
          </section>
        ) : (
          <BoothView
            sakes={ALL_SAKES}
            selectedId={selectedId}
            onSelect={(s) => setSelectedId(s.id)}
          />
        )}

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

function Tabs({ view, onChange }: { view: View; onChange: (v: View) => void }) {
  return (
    <div className="mt-5 inline-flex border-b border-sumi/20">
      {([
        { v: "quadrant" as View, ko: "분류별", ja: "四分面" },
        { v: "booth" as View, ko: "부스별", ja: "ブース" },
      ]).map((t) => {
        const on = view === t.v;
        return (
          <button
            key={t.v}
            onClick={() => onChange(t.v)}
            className={`px-5 py-2.5 font-serif text-lg transition relative ${
              on ? "text-shu" : "text-sumi/55 hover:text-sumi"
            }`}
          >
            <span>{t.ko}</span>
            <span className={`ml-2 text-sm font-deco ${on ? "text-shu/70" : "text-sumi/35"}`}>
              {t.ja}
            </span>
            {on && (
              <span className="absolute left-0 right-0 -bottom-px h-0.5 bg-shu" />
            )}
          </button>
        );
      })}
    </div>
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
      <span className="inline-flex items-center gap-1.5 ml-2">
        <span className="text-shu">★</span>
        <span className="text-sumi/70 font-serif">추천</span>
      </span>
    </div>
  );
}
