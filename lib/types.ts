export type SakeClass = '薰 Kun' | '醇 Jun' | '爽 Sou' | '熟 Juku' | 'Other';

export interface Sake {
  id: number;
  booth: string;
  brewery: string;
  region: string;
  product: string;
  class: SakeClass;
  aroma: number;
  richness: number;
  note: string;
}

export const CLASS_INFO: Record<SakeClass, { ko: string; ja: string; color: string; desc: string }> = {
  '薰 Kun': {
    ko: '쿤슈',
    ja: 'くんしゅ',
    color: '#d97a8a',
    desc: '향↑ 맛↓ — 大吟醸·吟醸 계열. 花·果実 같은 화사한 향, 가벼운 맛.',
  },
  '爽 Sou': {
    ko: '소슈',
    ja: 'そうしゅ',
    color: '#7fb2d6',
    desc: '향↓ 맛↓ — 普通酒·本醸造·生酒. 깨끗·산뜻·淡麗.',
  },
  '醇 Jun': {
    ko: '쥰슈',
    ja: 'じゅんしゅ',
    color: '#c48a3a',
    desc: '향↓ 맛↑ — 純米·生酛·山廃. 米의 우마미와 코쿠.',
  },
  '熟 Juku': {
    ko: '쥬쿠슈',
    ja: 'じゅくしゅ',
    color: '#6b4423',
    desc: '향↑ 맛↑ — 古酒·長期熟成. 황금색·드라이프루츠·향신료 같은 복합향.',
  },
  'Other': {
    ko: '기타',
    ja: 'その他',
    color: '#9a958a',
    desc: '焼酎·泡盛·위스키·맥주·リキュール·과실주 — 사케 4분면 밖.',
  },
};
