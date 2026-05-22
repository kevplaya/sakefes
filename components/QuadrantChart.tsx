"use client";

import { useMemo, useState } from "react";
import { Sake, CLASS_INFO, SakeClass } from "@/lib/types";

interface Props {
  sakes: Sake[];
  selectedId: number | null;
  onSelect: (s: Sake | null) => void;
  visibleClasses: Set<SakeClass>;
}

// Axis range 2..11. 6 remains the class-boundary divider.
const AX_MIN = 2;
const AX_MAX = 11;
const CENTER = 6;

const W = 720;
const H = 720;
const PAD = 56;
const UNIT_PX = (W - PAD * 2) / (AX_MAX - AX_MIN);

function xScale(v: number) {
  return PAD + ((v - AX_MIN) / (AX_MAX - AX_MIN)) * (W - PAD * 2);
}
function yScale(v: number) {
  return H - PAD - ((v - AX_MIN) / (AX_MAX - AX_MIN)) * (H - PAD * 2);
}

function jitter(id: number, range = 0.35) {
  const a = Math.sin(id * 12.9898) * 43758.5453;
  const b = Math.sin(id * 78.233) * 43758.5453;
  return [(a - Math.floor(a) - 0.5) * range, (b - Math.floor(b) - 0.5) * range];
}

export default function QuadrantChart({ sakes, selectedId, onSelect, visibleClasses }: Props) {
  const [hover, setHover] = useState<Sake | null>(null);

  const dots = useMemo(
    () =>
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
    // aspect-square locks 1:1 — prevents iOS Safari w-full+h-auto bug where
    // SVG renders with wrong height and dots appear visually offset from axes.
    <div className="relative w-full aspect-square" style={{ touchAction: "manipulation" }}>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        preserveAspectRatio="xMidYMid meet"
        className="block w-full h-full select-none"
        onClick={() => onSelect(null)}
      >
        <defs>
          <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#fbf3e0" />
            <stop offset="100%" stopColor="#f0e6cc" />
          </linearGradient>
          <pattern id="grid" width={UNIT_PX} height={UNIT_PX} patternUnits="userSpaceOnUse" x={PAD} y={PAD}>
            <path d={`M ${UNIT_PX} 0 L 0 0 0 ${UNIT_PX}`} fill="none" stroke="#c9bca0" strokeWidth="0.4" />
          </pattern>
        </defs>
        <rect width={W} height={H} fill="url(#bg)" />
        <rect x={PAD} y={PAD} width={W - PAD * 2} height={H - PAD * 2} fill="url(#grid)" opacity="0.65" />

        {/* Quadrant fills */}
        <rect x={xScale(CENTER)} y={yScale(AX_MAX)} width={xScale(AX_MAX) - xScale(CENTER)} height={yScale(CENTER) - yScale(AX_MAX)} fill="#6b4423" opacity="0.05" />
        <rect x={PAD} y={yScale(AX_MAX)} width={xScale(CENTER) - PAD} height={yScale(CENTER) - yScale(AX_MAX)} fill="#d97a8a" opacity="0.05" />
        <rect x={PAD} y={yScale(CENTER)} width={xScale(CENTER) - PAD} height={yScale(AX_MIN) - yScale(CENTER)} fill="#7fb2d6" opacity="0.05" />
        <rect x={xScale(CENTER)} y={yScale(CENTER)} width={xScale(AX_MAX) - xScale(CENTER)} height={yScale(AX_MIN) - yScale(CENTER)} fill="#c48a3a" opacity="0.05" />

        {/* Cross divider at 6,6 */}
        <line x1={xScale(CENTER)} y1={PAD} x2={xScale(CENTER)} y2={H - PAD} stroke="#1f1d1a" strokeWidth="1" strokeDasharray="2 4" opacity="0.5" />
        <line x1={PAD} y1={yScale(CENTER)} x2={W - PAD} y2={yScale(CENTER)} stroke="#1f1d1a" strokeWidth="1" strokeDasharray="2 4" opacity="0.5" />

        {/* Frame */}
        <rect x={PAD} y={PAD} width={W - PAD * 2} height={H - PAD * 2} fill="none" stroke="#1f1d1a" strokeWidth="1.2" />

        {/* Ticks (axis 2..11) */}
        {Array.from({ length: AX_MAX - AX_MIN + 1 }).map((_, k) => {
          const i = AX_MIN + k;
          return (
            <g key={`tx-${i}`}>
              <line x1={xScale(i)} y1={H - PAD} x2={xScale(i)} y2={H - PAD + 4} stroke="#1f1d1a" strokeWidth="0.6" />
              <text x={xScale(i)} y={H - PAD + 22} textAnchor="middle" fontSize="16" fill="#5a5651" fontFamily="serif" fontWeight={i === 6 ? 700 : 400}>{i}</text>
            </g>
          );
        })}
        {Array.from({ length: AX_MAX - AX_MIN + 1 }).map((_, k) => {
          const i = AX_MIN + k;
          return (
            <g key={`ty-${i}`}>
              <line x1={PAD - 4} y1={yScale(i)} x2={PAD} y2={yScale(i)} stroke="#1f1d1a" strokeWidth="0.6" />
              <text x={PAD - 8} y={yScale(i) + 6} textAnchor="end" fontSize="16" fill="#5a5651" fontFamily="serif" fontWeight={i === 6 ? 700 : 400}>{i}</text>
            </g>
          );
        })}

        {/* Axis labels */}
        <text x={W / 2} y={H - 10} textAnchor="middle" fontSize="20" fill="#1f1d1a" fontFamily="serif" letterSpacing="0.2em">맛 · 味 (richness) →</text>
        <text transform={`translate(16 ${H / 2}) rotate(-90)`} textAnchor="middle" fontSize="20" fill="#1f1d1a" fontFamily="serif" letterSpacing="0.2em">향 · 香 (aroma) ↑</text>

        {/* Quadrant labels (centered in each half: left 2-6 mid=4, right 6-11 mid=8.5) */}
        <QLabel x={xScale(4)} y={yScale(9)} title="薰" sub="Kun" ko="쿤슈" color="#b6313a" />
        <QLabel x={xScale(8.5)} y={yScale(9)} title="熟" sub="Juku" ko="쥬쿠슈" color="#6b4423" />
        <QLabel x={xScale(4)} y={yScale(3.5)} title="爽" sub="Sou" ko="소슈" color="#1d3b73" />
        <QLabel x={xScale(8.5)} y={yScale(3.5)} title="醇" sub="Jun" ko="쥰슈" color="#8b6314" />

        {/* Center marker */}
        <circle cx={xScale(CENTER)} cy={yScale(CENTER)} r="4" fill="#b6313a" />
        <text x={xScale(CENTER) + 8} y={yScale(CENTER) - 8} fontSize="15" fill="#b6313a" fontFamily="serif">中 (6,6)</text>

        {/* Dots — visible circle + larger transparent hit area for mobile tap */}
        {dots.map((s) => {
          const color = CLASS_INFO[s.class].color;
          const selected = s.id === selectedId;
          const isHover = hover?.id === s.id;
          const r = selected ? 8 : isHover ? 7 : 5;
          return (
            <g key={s.id}>
              {selected && (
                <circle cx={s.cx} cy={s.cy} r={r + 4} fill={color} opacity="0.25" className="pulse-ring" />
              )}
              <circle
                cx={s.cx}
                cy={s.cy}
                r={r}
                fill={color}
                stroke={selected ? "#1f1d1a" : "rgba(31,29,26,0.4)"}
                strokeWidth={selected ? 1.6 : 0.6}
                opacity={hover && !isHover && !selected ? 0.35 : 0.9}
                style={{ pointerEvents: "none", transition: "r 120ms ease, opacity 120ms ease" }}
              />
              {/* Transparent larger hit target — easier mobile tap */}
              <circle
                cx={s.cx}
                cy={s.cy}
                r={16}
                fill="transparent"
                onMouseEnter={() => setHover(s)}
                onMouseLeave={() => setHover(null)}
                onClick={(e) => {
                  e.stopPropagation();
                  onSelect(s);
                }}
                style={{ cursor: "pointer" }}
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
              y={Math.max(8, yScale(hover.aroma) - 56) + 22}
              fontSize="17"
              fill="#f4ecdb"
              fontFamily="serif"
            >
              {hover.product.length > 24 ? hover.product.slice(0, 24) + "…" : hover.product}
            </text>
            <text
              x={Math.min(W - 260, Math.max(8, xScale(hover.richness) + 10)) + 10}
              y={Math.max(8, yScale(hover.aroma) - 56) + 42}
              fontSize="16"
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
      <text x={x} y={y - 10} textAnchor="middle" fontSize="52" fill={color} opacity="0.16" fontFamily="serif" fontWeight={700}>{title}</text>
      <text x={x} y={y + 22} textAnchor="middle" fontSize="16" fill={color} opacity="0.7" fontFamily="serif" letterSpacing="0.2em">{sub} · {ko}</text>
    </g>
  );
}
