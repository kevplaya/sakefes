# 사케페스 · 2026 서울사케페스티벌 4분면 지도

SSI(日本酒サービス研究会) **薰·爽·醇·熟 4타입** 분류를 활용해, 2026 서울사케페스티벌 출품 **691 품목**을 향(香) × 맛(味) 좌표에 점수제로 시각화한 웹앱.

- **데이터**: [sakefestival.co.kr/44](https://www.sakefestival.co.kr/44) + [/45](https://www.sakefestival.co.kr/45)
- **분류 기준**: [SSI 4타입 (보사뉴스)](https://www.bosa.co.kr/news/articleView.html?idxno=2109371) / [SAKETIMES](https://jp.sake-times.com/knowledge/word/sake_g_word_4type)
- **좌표**: X = 맛(richness) 0–10, Y = 향(aroma) 0–10, 중앙 (6,6)이 분면 경계
- **점수 부여**: 蔵元 라인업·정미율·효모·제법 키워드 + 일·한 자료 직접 조사

## 분면

| 분면 | 명칭 | 좌표 | 대표 유형 |
|---|---|---|---|
| ① 薰 Kun (쿤슈) | 향↑맛↓ | 좌상 | 大吟醸·吟醸·純米大吟醸·純米吟醸 |
| ② 爽 Sou (소슈) | 향↓맛↓ | 좌하 | 普通酒·本醸造·生酒·しぼりたて |
| ③ 醇 Jun (쥰슈) | 향↓맛↑ | 우하 | 純米·特別純米·生酛·山廃 |
| ④ 熟 Juku (쥬쿠슈) | 향↑맛↑ | 우상 | 古酒·長期熟成·貴醸酒 |
| ★ Other | — | — | 焼酎·泡盛·위스키·맥주·リキュール |

## 개발

```bash
npm install
npm run dev      # http://localhost:3000
npm run build
npm run start
```

## Vercel 배포

1. Vercel 계정에서 New Project → Import GitHub 저장소 `kevplaya/sakefes`
2. Framework Preset: **Next.js** (자동 인식)
3. Deploy. 추가 설정 불필요 (데이터는 `data/sakes.json` 정적 임베드)

또는 CLI:

```bash
npx vercel --prod
```

## 데이터 재생성

원본 HTML에서 다시 추출하려면:

```bash
python3 classify.py    # 점수 부여 → scored.json
python3 build_md.py    # SAKE_SCORED.md + 양조장 MD 갱신
# data/sakes.json 동기화 (id 추가):
python3 -c "import json; e=json.load(open('scored.json')); \
  out=[{**v,'id':i} for i,v in enumerate(e)]; \
  json.dump(out, open('data/sakes.json','w'), ensure_ascii=False, indent=0)"
```

## 라이선스

데이터: 행사 공식 사이트의 공개 라인업 정보. 분류·점수는 본 프로젝트의 휴리스틱·조사 결과(참고용).
