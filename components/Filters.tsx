"use client";
import { SakeClass, CLASS_INFO } from "@/lib/types";

interface Props {
  query: string;
  onQuery: (q: string) => void;
  visibleClasses: Set<SakeClass>;
  onToggleClass: (c: SakeClass) => void;
  counts: Record<SakeClass, number>;
}

const CLASSES: SakeClass[] = ['薰 Kun', '熟 Juku', '醇 Jun', '爽 Sou', 'Other'];

export default function Filters({ query, onQuery, visibleClasses, onToggleClass, counts }: Props) {
  return (
    <div className="washi-card rounded-md p-4 space-y-4">
      <div>
        <label className="text-xs uppercase tracking-widest text-sumi/60 font-sans">Search · 검색</label>
        <input
          type="text"
          value={query}
          onChange={(e) => onQuery(e.target.value)}
          placeholder="양조장, 사케명, 부스, 지역…"
          className="mt-1 w-full bg-transparent border border-sumi/20 rounded px-3 py-2 text-sm focus:outline-none focus:border-shu/60 placeholder:text-sumi/40 font-sans"
        />
      </div>

      <div>
        <div className="text-xs uppercase tracking-widest text-sumi/60 mb-2 font-sans">Quadrant · 분면</div>
        <div className="space-y-1.5">
          {CLASSES.map((c) => {
            const info = CLASS_INFO[c];
            const on = visibleClasses.has(c);
            return (
              <button
                key={c}
                onClick={() => onToggleClass(c)}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded border text-left transition ${
                  on ? "border-sumi/30 bg-white/40" : "border-sumi/10 bg-transparent opacity-50"
                }`}
              >
                <span
                  className="inline-block w-3.5 h-3.5 rounded-full shrink-0"
                  style={{ background: info.color, border: "1px solid rgba(31,29,26,0.4)" }}
                />
                <span className="flex-1">
                  <span className="font-serif text-base font-semibold">{c.split(' ')[0]}</span>
                  <span className="ml-2 text-xs text-sumi/60 font-sans">{info.ko} · {info.ja}</span>
                </span>
                <span className="font-sans text-xs text-sumi/50 tabular-nums">{counts[c] ?? 0}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
