"use client";

import { useMemo, useState } from "react";
import { Sake, CLASS_INFO, SakeClass } from "@/lib/types";

interface Props {
  sakes: Sake[];
  selectedId: number | null;
  onSelect: (s: Sake | null) => void;
  visibleClasses: Set<SakeClass>;
}

// Axis range: 0..12 with 6 as visual center.
// Data values are 0..10 — fall inside this range with 6 acting as the cross divider.
const AX_MIN = 0;
const AX_MAX = 12;
const CENTER = 6;

const W = 720;
const H = 720;
const PAD = 56;

function xScale(v: number) {
  return PAD + ((v - AX_MIN) / (AX_MAX - AX_MIN)) * (W - PAD * 2);
}
function yScale(v: number) {
  // higher aroma = visually higher on screen → invert
  return H - PAD - ((v - AX_MIN) / (AX_MAX - AX_MIN)) * (H - PAD * 2);
}

// Deterministic jitter to avoid stacked dots
function jitter(id: number, range = 0.35) {
  const a = Math.sin(id * 12.9898) * 43758.5453;
  const b = Math.sin(id * 78.233) * 43758.5453;
  return [(a - Math.floor(a) - 0.5) * range, (b - Math.floor(b) - 0.5) * range];
}

export default function QuadrantChart({ sakes, selectedId, onSelect, visibleClasses }: Props) {
  const [hover, setHover] = useState<Sake | null>(null);

  const dots = useMemo(() =>
    sakes
      .filter((s) => visibleClasses.has(s.class))
      .map((s) => {
        const [jx, jy] = jitter(s.id);
        return {
          ...s,
          cx: xScale(s.richness + jx),
          cy: yScale(s.aroma + jy),
        };
      }),
    [sakes, visibleClasses]
  );

  return (
    <div className="relative w-full">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full h-auto block"
        onClick={() => onSelect(null)}
      >
        {/* washi background */}
        <defs>
          <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#fbf3e0" />
            <stop offset="100%" stopColor="#f0e6cc" />
          </linearGradient>
          <radialGradient id="dotG" cx="40%" cy="40%" r="60%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#000000" stopOpacity="0" />
          </radialGradient>
          <pattern id="grid" width="56" height="56" patternUnits="userSpaceOnUse">
            <path d="M 56 0 L 0 0 0 56" fill="none" stroke="#c9bca0" strokeWidth="0.4" />
          </pattern>
        </defs>
        <rect width={W} height={H} fill="url(#bg)" />
        <rect x={PAD} y={PAD} width={W - PAD * 2} height={H - PAD * 2} fill="url(#grid)" opacity="0.65" />

        {/* Quadrant fills (subtle) */}
        <rect x={xScale(CENTER)} y={yScale(AX_MAX)} width={xScale(AX_MAX) - xScale(CENTER)} height={yScale(CENTER) - yScale(AX_MAX)} fill="#6b4423" opacity="0.05" />
        <rect x={PAD} y={yScale(AX_MAX)} width={xScale(CENTER) - PAD} height={yScale(CENTER) - yScale(AX_MAX)} fill="#d97a8a" opacity="0.05" />
        <rect x={PAD} y={yScale(CENTER)} width={xScale(CENTER) - PAD} height={yScale(AX_MIN) - yScale(CENTER)} fill="#7fb2d6" opacity="0.05" />
        <rect x={xScale(CENTER)} y={yScale(CENTER)} width={xScale(AX_MAX) - xScale(CENTER)} height={yScale(AX_MIN) - yScale(CENTER)} fill="#c48a3a" opacity="0.05" />

        {/* Cross divider at 6,6 (center) */}
        <line x1={xScale(CENTER)} y1={PAD} x2={xScale(CENTER)} y2={H - PAD} stroke="#1f1d1a" strokeWidth="1" strokeDasharray="2 4" opacity="0.5" />
        <line x1={PAD} y1={yScale(CENTER)} x2={W - PAD} y2={yScale(CENTER)} stroke="#1f1d1a" strokeWidth="1" strokeDasharray="2 4" opacity="0.5" />

        {/* Axis frame */}
        <rect x={PAD} y={PAD} width={W - PAD * 2} height={H - PAD * 2} fill="none" stroke="#1f1d1a" strokeWidth="1.2" />

        {/* Axis ticks 0..12 (label 6 emphasized) */}
        {Array.from({ length: 13 }).map((_, i) => (
          <g key={`tx-${i}`}>
            <line x1={xScale(i)} y1={H - PAD} x2={xScale(i)} y2={H - PAD + 4} stroke="#1f1d1a" strokeWidth="0.6" />
            <text x={xScale(i)} y={H - PAD + 18} textAnchor="middle" fontSize="11" fill="#5a5651" fontFamily="serif" fontWeight={i === 6 ? 700 : 400}>{i}</text>
          </g>
        ))}
        {Array.from({ length: 13 }).map((_, i) => (
          <g key={`ty-${i}`}>
            <line x1={PAD - 4} y1={yScale(i)} x2={PAD} y2={yScale(i)} stroke="#1f1d1a" strokeWidth="0.6" />
            <text x={PAD - 8} y={yScale(i) + 4} textAnchor="end" fontSize="11" fill="#5a5651" fontFamily="serif" fontWeight={i === 6 ? 700 : 400}>{i}</text>
          </g>
        ))}

        {/* Axis labels */}
        <text x={W / 2} y={H - 14} textAnchor="middle" fontSize="14" fill="#1f1d1a" fontFamily="serif" letterSpacing="0.2em">맛 · 味 (richness) →</text>
        <text transform={`translate(18 ${H / 2}) rotate(-90)`} textAnchor="middle" fontSize="14" fill="#1f1d1a" fontFamily="serif" letterSpacing="0.2em">향 · 香 (aroma) ↑</text>

        {/* Quadrant labels at corners */}
        <QLabel x={xScale(3)} y={yScale(9)} title="薰" sub="Kun" ko="쿤슈" color="#b6313a" />
        <QLabel x={xScale(9)} y={yScale(9)} title="熟" sub="Juku" ko="쥬쿠슈" color="#6b4423" />
        <QLabel x={xScale(3)} y={yScale(3)} title="爽" sub="Sou" ko="소슈" color="#1d3b73" />
        <QLabel x={xScale(9)} y={yScale(3)} title="醇" sub="Jun" ko="쥰슈" color="#8b6314" />

        {/* Center marker (6,6) */}
        <circle cx={xScale(CENTER)} cy={yScale(CENTER)} r="3" fill="#b6313a" />
        <text x={xScale(CENTER) + 6} y={yScale(CENTER) - 6} fontSize="10" fill="#b6313a" fontFamily="serif">中 (6,6)</text>

        {/* Dots */}
        {dots.map((s) => {
          const color = CLASS_INFO[s.class].color;
          const selected = s.id === selectedId;
          const isHover = hover?.id === s.id;
          const r = selected ? 7 : isHover ? 6 : 4.2;
          return (
            <g key={s.id}>
              {selected && (
                <circle cx={s.cx} cy={s.cy} r={r} fill={color} opacity="0.25" className="pulse-ring" />
              )}
              <circle
                cx={s.cx}
                cy={s.cy}
                r={r}
                fill={color}
                stroke={selected ? "#1f1d1a" : "rgba(31,29,26,0.4)"}
                strokeWidth={selected ? 1.6 : 0.6}
                opacity={hover && !isHover && !selected ? 0.35 : 0.85}
                onMouseEnter={() => setHover(s)}
                onMouseLeave={() => setHover(null)}
                onClick={(e) => { e.stopPropagation(); onSelect(s); }}
                style={{ cursor: "pointer", transition: "r 120ms ease, opacity 120ms ease" }}
              />
            </g>
          );
        })}

        {/* Hover tooltip */}
        {hover && (
          <g pointerEvents="none">
            <rect
              x={Math.min(W - 260, Math.max(8, xScale(hover.richness) + 10))}
              y={Math.max(8, yScale(hover.aroma) - 56)}
              width="248"
              height="48"
              rx="6"
              fill="#1f1d1a"
              opacity="0.92"
            />
            <text
              x={Math.min(W - 260, Math.max(8, xScale(hover.richness) + 10)) + 10}
              y={Math.max(8, yScale(hover.aroma) - 56) + 18}
              fontSize="12"
              fill="#f4ecdb"
              fontFamily="serif"
            >
              {hover.product.length > 30 ? hover.product.slice(0, 30) + "…" : hover.product}
            </text>
            <text
              x={Math.min(W - 260, Math.max(8, xScale(hover.richness) + 10)) + 10}
              y={Math.max(8, yScale(hover.aroma) - 56) + 36}
              fontSize="11"
              fill="#d9c89a"
              fontFamily="serif"
            >
              {hover.brewery} · {hover.class} · 향{hover.aroma} 맛{hover.richness}
            </text>
          </g>
        )}
      </svg>
    </div>
  );
}

function QLabel({ x, y, title, sub, ko, color }: { x: number; y: number; title: string; sub: string; ko: string; color: string }) {
  return (
    <g pointerEvents="none">
      <text x={x} y={y - 10} textAnchor="middle" fontSize="42" fill={color} opacity="0.16" fontFamily="serif" fontWeight={700}>{title}</text>
      <text x={x} y={y + 18} textAnchor="middle" fontSize="11" fill={color} opacity="0.7" fontFamily="serif" letterSpacing="0.2em">{sub} · {ko}</text>
    </g>
  );
}
