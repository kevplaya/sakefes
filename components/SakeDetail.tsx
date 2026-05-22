"use client";
import { Sake, CLASS_INFO } from "@/lib/types";

interface Props {
  sake: Sake | null;
  onClose: () => void;
  related: Sake[];
  cluster: Sake[];
  onSelect: (s: Sake) => void;
}

export default function SakeDetail({ sake, onClose, related, cluster, onSelect }: Props) {
  if (!sake) {
    return (
      <div className="washi-card rounded-md p-6 text-center text-sumi/60 font-serif">
        <div className="text-6xl text-shu/30 mb-3">徳</div>
        <div className="text-base">차트의 점을 클릭하면 상세 정보가 표시됩니다.</div>
      </div>
    );
  }
  const info = CLASS_INFO[sake.class];
  const clusterOthers = cluster.filter((c) => c.id !== sake.id);

  return (
    <div className="washi-card rounded-md p-5 space-y-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span
              className="inline-block w-3.5 h-3.5 rounded-full"
              style={{ background: info.color, border: "1px solid rgba(31,29,26,0.4)" }}
            />
            <span className="font-serif text-base text-sumi/70">{sake.class} · {info.ko}</span>
          </div>
          <h2 className="font-serif text-2xl leading-tight text-sumi">{sake.product}</h2>
          <div className="text-base text-sumi/70 mt-1 font-sans">{sake.brewery}</div>
        </div>
        <button
          onClick={onClose}
          className="text-sumi/40 hover:text-shu text-3xl leading-none font-serif"
          aria-label="close"
        >
          ×
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <ScoreBox label="향 · 香" value={sake.aroma} color="#b6313a" />
        <ScoreBox label="맛 · 味" value={sake.richness} color="#1d3b73" />
      </div>

      <dl className="text-base divide-y divide-sumi/10">
        <Row k="부스" v={sake.booth} />
        <Row k="지역" v={sake.region} />
        <Row k="분류 근거" v={sake.note} />
        <Row k="분면 특징" v={info.desc} />
      </dl>

      {clusterOthers.length > 0 && (
        <div>
          <div className="text-sm uppercase tracking-widest text-sumi/60 mb-2 font-sans">
            같은 좌표 (향{sake.aroma} 맛{sake.richness}) · {cluster.length}품목
          </div>
          <div className="space-y-1 max-h-72 overflow-y-auto scrollbar-thin">
            {clusterOthers.map((c) => (
              <button
                key={c.id}
                onClick={() => onSelect(c)}
                className="w-full text-left px-2.5 py-2 rounded hover:bg-white/60 text-base flex items-start gap-2"
              >
                <span
                  className="w-2.5 h-2.5 rounded-full shrink-0 mt-1.5"
                  style={{ background: CLASS_INFO[c.class].color }}
                />
                <span className="flex-1 min-w-0">
                  <span className="block font-serif truncate">{c.product}</span>
                  <span className="block text-sm text-sumi/55 font-sans truncate">
                    {c.booth} · {c.brewery}
                  </span>
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {related.length > 0 && (
        <div>
          <div className="text-sm uppercase tracking-widest text-sumi/60 mb-2 font-sans">같은 양조장 다른 품목</div>
          <div className="space-y-1 max-h-56 overflow-y-auto scrollbar-thin">
            {related.map((r) => (
              <button
                key={r.id}
                onClick={() => onSelect(r)}
                className="w-full text-left px-2.5 py-2 rounded hover:bg-white/60 text-base flex items-center gap-2"
              >
                <span
                  className="w-2.5 h-2.5 rounded-full shrink-0"
                  style={{ background: CLASS_INFO[r.class].color }}
                />
                <span className="flex-1 truncate font-serif">{r.product}</span>
                <span className="text-sm text-sumi/50 font-sans tabular-nums">
                  {r.aroma}/{r.richness}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ScoreBox({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="rounded border border-sumi/15 bg-white/40 p-3">
      <div className="text-sm text-sumi/60 font-sans">{label}</div>
      <div className="flex items-baseline gap-1 mt-0.5">
        <div className="font-serif text-4xl tabular-nums" style={{ color }}>{value}</div>
        <div className="text-sm text-sumi/40 font-sans">/ 10</div>
      </div>
      <div className="mt-2 h-1.5 rounded-full bg-sumi/10 overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${value * 10}%`, background: color }} />
      </div>
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="py-2 grid grid-cols-[90px_1fr] gap-3">
      <dt className="text-sm uppercase tracking-widest text-sumi/55 font-sans pt-0.5">{k}</dt>
      <dd className="text-base text-sumi/90 font-serif leading-relaxed">{v}</dd>
    </div>
  );
}
