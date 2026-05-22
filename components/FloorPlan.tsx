"use client";

export default function FloorPlan() {
  return (
    <div className="washi-card rounded-md p-3 md:p-5 space-y-6">
      <Section title="1관 · Hall 1" image="/floorplan-hall1.png" alt="2026 사케페스 1관 부스배치도">
        {/* A09-A14 sparkle highlight */}
        <SparkleBox style={{ left: "4%", top: "90.2%", width: "40.5%", height: "7%" }} />
      </Section>

      <Section title="2관 · Hall 2" image="/floorplan-hall2.png" alt="2026 사케페스 2관 부스배치도" />
    </div>
  );
}

function Section({
  title,
  image,
  alt,
  children,
}: {
  title: string;
  image: string;
  alt: string;
  children?: React.ReactNode;
}) {
  return (
    <div>
      <div className="flex items-baseline gap-3 mb-3">
        <h3 className="font-serif text-xl text-shu">{title}</h3>
        <span className="text-sm text-sumi/55 font-sans">상세는 이미지 확대</span>
      </div>
      <div className="relative rounded border border-sumi/15 overflow-hidden bg-white/40">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={image} alt={alt} className="block w-full h-auto select-none" draggable={false} />
        {children}
      </div>
    </div>
  );
}

function SparkleBox({ style }: { style: React.CSSProperties }) {
  return (
    <div className="absolute pointer-events-none" style={style}>
      <div className="sparkle-box w-full h-full rounded" />
      <span className="sparkle-dot" style={{ left: "8%", top: "-12%" }}>✦</span>
      <span className="sparkle-dot delay-1" style={{ left: "32%", top: "110%" }}>✦</span>
      <span className="sparkle-dot delay-2" style={{ left: "60%", top: "-18%" }}>✧</span>
      <span className="sparkle-dot delay-3" style={{ left: "85%", top: "118%" }}>✦</span>
      <span className="sparkle-dot delay-2" style={{ left: "50%", top: "-25%" }}>✧</span>
    </div>
  );
}
