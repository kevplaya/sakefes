"use client";
import { useMemo, useState } from "react";
import { Sake, CLASS_INFO } from "@/lib/types";
import { isFeatured, featuredNote } from "@/lib/featured";

interface Props {
  sakes: Sake[];
  selectedId: number | null;
  onSelect: (s: Sake) => void;
}

export default function BoothView({ sakes, selectedId, onSelect }: Props) {
  const [onlyFeatured, setOnlyFeatured] = useState(false);

  const groups = useMemo(() => {
    const m = new Map<string, { booth: string; brewery: string; region: string; items: Sake[]; featured: boolean; note?: string }>();
    for (const s of sakes) {
      const key = `${s.booth}::${s.brewery}`;
      if (!m.has(key)) {
        m.set(key, {
          booth: s.booth,
          brewery: s.brewery,
          region: s.region,
          items: [],
          featured: isFeatured(s),
          note: featuredNote(s),
        });
      }
      m.get(key)!.items.push(s);
    }
    return Array.from(m.values()).sort((a, b) =>
      a.booth === b.booth ? a.brewery.localeCompare(b.brewery) : a.booth.localeCompare(b.booth)
    );
  }, [sakes]);

  const featuredCount = useMemo(() => groups.filter((g) => g.featured).length, [groups]);
  const visibleGroups = useMemo(
    () => (onlyFeatured ? groups.filter((g) => g.featured) : groups),
    [groups, onlyFeatured]
  );
  const visibleItemCount = useMemo(
    () => visibleGroups.reduce((sum, g) => sum + g.items.length, 0),
    [visibleGroups]
  );

  return (
    <div className="washi-card rounded-md p-3 md:p-5">
      <div className="flex items-center gap-2 mb-3 flex-wrap">
        <span className="text-sm text-sumi/60 font-sans">
          부스 {visibleGroups.length}개 · {visibleItemCount}품목
        </span>
        <button
          onClick={() => setOnlyFeatured((v) => !v)}
          aria-pressed={onlyFeatured}
          className={`px-2.5 py-1 rounded-full text-sm font-sans border transition ${
            onlyFeatured
              ? "bg-shu text-washi border-shu shadow-sm"
              : "bg-shu/10 text-shu border-shu/40 hover:bg-shu/15"
          }`}
        >
          ★ 추천 {featuredCount}부스{onlyFeatured ? " · 해제" : ""}
        </button>
      </div>
      <div className="space-y-4 max-h-[1200px] overflow-y-auto scrollbar-thin pr-2">
        {visibleGroups.map((g) => (
          <BoothCard key={`${g.booth}-${g.brewery}`} group={g} selectedId={selectedId} onSelect={onSelect} />
        ))}
        {visibleGroups.length === 0 && (
          <div className="text-center text-sumi/50 font-sans text-sm py-8">표시할 부스 없음.</div>
        )}
      </div>
    </div>
  );
}

function BoothCard({
  group,
  selectedId,
  onSelect,
}: {
  group: { booth: string; brewery: string; region: string; items: Sake[]; featured: boolean; note?: string };
  selectedId: number | null;
  onSelect: (s: Sake) => void;
}) {
  const { booth, brewery, region, items, featured, note } = group;
  return (
    <div
      className={`rounded border ${
        featured ? "border-shu/40 bg-shu/5" : "border-sumi/15 bg-white/30"
      }`}
    >
      <div className="flex items-baseline gap-3 px-4 py-2.5 border-b border-sumi/10">
        <span className="font-serif text-xl text-shu tabular-nums tracking-wider">{booth}</span>
        <span className="font-serif text-lg text-sumi flex-1 truncate">
          {featured && <span className="text-shu mr-1">★</span>}
          {brewery}
        </span>
        <span className="text-sm text-sumi/55 font-sans truncate hidden sm:inline">{region}</span>
      </div>
      {featured && note && (
        <div className="px-4 py-1.5 text-sm text-shu/85 font-sans border-b border-shu/20 bg-shu/8">
          ↳ 추천: {note}
        </div>
      )}
      <div className="divide-y divide-sumi/8">
        {items.map((s) => {
          const isSel = s.id === selectedId;
          return (
            <button
              key={s.id}
              onClick={() => onSelect(s)}
              className={`w-full text-left px-4 py-2 text-base flex items-center gap-3 transition ${
                isSel ? "bg-shu/15" : "hover:bg-white/60"
              }`}
            >
              <span
                className="w-2.5 h-2.5 rounded-full shrink-0"
                style={{ background: CLASS_INFO[s.class].color, border: "1px solid rgba(31,29,26,0.3)" }}
              />
              <span className="flex-1 font-serif text-sumi truncate min-w-0">{s.product}</span>
              <span className="font-sans text-sm text-sumi/55 shrink-0">{s.class.split(" ")[0]}</span>
              <span className="font-sans tabular-nums text-sm text-sumi/65 shrink-0 w-12 text-right">
                <span className="text-shu/85">{s.aroma}</span>
                <span className="text-sumi/30 mx-0.5">/</span>
                <span className="text-ai/85">{s.richness}</span>
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
