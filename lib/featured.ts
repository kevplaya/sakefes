// 추천 사케 출처: featured.md (사케페스티벌 추천사케 큐레이션)
// 부스 코드 정규화 (한 자리 → 두 자리). 같은 부스에 두 양조장이면 brewery 힌트로 구분.
export const FEATURED: { booth: string; brewery?: string; note?: string }[] = [
  // 쿠마가이주류 큐레이션 (A09-14 + E17-E20)
  { booth: "A09", note: "치토세츠루" },
  { booth: "A10", note: "아즈마이치" },
  { booth: "A12", brewery: "아이하라주조", note: "우고노츠키" },
  { booth: "A12", brewery: "텐료하이주조", note: "우타시로" },
  { booth: "B03", brewery: "이마니시주조", note: "미무로스기" },
  { booth: "B03", brewery: "센킨" },
  { booth: "E17", note: "호우라이센" },
  { booth: "E18", note: "이나타히메" },
  { booth: "E19", note: "유키노보우샤" },
  { booth: "E20", note: "나베시마" },
  // 지자케CY코리아
  { booth: "F11", note: "닷사이 블루" },
  { booth: "F12", note: "치요무스비" },
  { booth: "F15", note: "시치다" },
  { booth: "G15", note: "하쿠라쿠세이" },
  // 일로
  { booth: "G02", note: "호오비덴" },
  { booth: "G05", note: "키도 紀土" },
  { booth: "G08", note: "자쿠 作" },
  { booth: "G09", note: "햐쿠쥬로 百春" },
  { booth: "H02", note: "야마모토" },
  { booth: "H03", note: "야마가타마사무네" },
  { booth: "H06", note: "타카" },
  { booth: "H15", note: "아카부" },
  { booth: "H17", note: "아키토라" },
  { booth: "H20", note: "카메이즈미" },
  { booth: "J14", note: "고젠슈" },
  { booth: "K02", note: "카제노모리" },
  // CR트레이딩
  { booth: "M01", note: "신슈키레이 (한정)" },
  { booth: "M04", note: "쵸카이산" },
  { booth: "M12", note: "아베" },
  // 사카야코리아
  { booth: "P02", note: "텐비" },
  { booth: "P03", note: "무츠핫센" },
  { booth: "L02", note: "이와테메이죠" },
  // 기타 소주/위스키
  { booth: "E14", note: "토미노호우잔" },
  { booth: "E15", note: "나나쿠보" },
  { booth: "J16", note: "츠쿠시" },
  { booth: "Q05", note: "세키토바" },
  { booth: "Q06", note: "쿠로이사니시키" },
  { booth: "U01", note: "닛카위스키" },
];

export function isFeatured(s: { booth: string; brewery: string }): boolean {
  return FEATURED.some(
    (f) => f.booth === s.booth && (!f.brewery || f.brewery === s.brewery)
  );
}

export function featuredNote(s: { booth: string; brewery: string }): string | undefined {
  const f = FEATURED.find(
    (x) => x.booth === s.booth && (!x.brewery || x.brewery === s.brewery)
  );
  return f?.note;
}
