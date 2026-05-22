import json, os, re
from collections import defaultdict

with open('/Users/user/fun/sakefes/scored.json','r',encoding='utf-8') as f:
    entries = json.load(f)

# Update each brewery MD
brew_dir = '/Users/user/fun/sakefes/breweries'
by_key = defaultdict(list)
for e in entries:
    by_key[(e['booth'], e['brewery'])].append(e)

for f in sorted(os.listdir(brew_dir)):
    if not f.endswith('.md'): continue
    path = os.path.join(brew_dir, f)
    with open(path,'r',encoding='utf-8') as fp:
        text = fp.read()
    name_m = re.search(r'^# (.+)$', text, re.M)
    booth_m = re.search(r'\*\*부스\*\*: (\S+)', text)
    if not name_m or not booth_m: continue
    name = name_m.group(1).strip()
    booth = booth_m.group(1)
    items = by_key.get((booth, name), [])
    if not items: continue
    head = text.split('## 참가품목')[0]
    body = "## 참가품목\n\n"
    body += "| 종류 | 향(0-10) | 맛(0-10) | 품목 | 추정근거 |\n|---|---|---|---|---|\n"
    for e in items:
        body += f"| {e['class']} | {e['aroma']} | {e['richness']} | {e['product']} | {e['note']} |\n"
    with open(path,'w',encoding='utf-8') as fp:
        fp.write(head + body)

# Build comprehensive scored MD
out = """# 2026 서울사케페스티벌 - 사케 691품목 점수제 분류

**기준**: SSI(日本酒サービス研究会) 4타입 분류법
**참조**: [보사뉴스 기사](https://www.bosa.co.kr/news/articleView.html?idxno=2109371), [SAKETIMES](https://jp.sake-times.com/knowledge/word/sake_g_word_4type), [SSI 香味特性別分類](https://www.fbo.or.jp/webch/ssisake002/s0027)

## 점수 축
- **향 (Aroma) 0-10**: 0=무향, 10=極香. 大吟醸>吟醸>純米吟醸>純米>本醸造>普通酒. 古酒/AWA(스파클링) 가산. 効母특수(花酵母/CEL-24 등) 가산.
- **맛 (Richness) 0-10**: 0=極淡麗, 10=極濃醇. 純米>生酛/山廃>本醸造>大吟醸>普通酒. 古酒/原酒/無濾過/きょうしゅ 가산.

## 4분면 매핑 (SSI 표준)

```
        향(aroma)↑
              |
    ① 薰 Kun  |  ④ 熟 Juku
      향↑맛↓   |   향↑맛↑
              |
   ───────────+─────────── → 맛(richness)
              |
    ② 爽 Sou  |  ③ 醇 Jun
      향↓맛↓   |   향↓맛↑
              |
```

| 분면 | 명칭 | 한자 | 향 | 맛 | 대표 유형 |
|---|---|---|---|---|---|
| ① | 薰酒 (쿤슈) | 薰 | 6+ | <6 | 大吟醸·吟醸·純米大吟醸·純米吟醸 |
| ② | 爽酒 (소슈) | 爽 | <6 | <6 | 普通酒·本醸造·生酒·しぼりたて |
| ③ | 醇酒 (쥰슈) | 醇 | <6 | 6+ | 純米·特別純米·生酛·山廃 |
| ④ | 熟酒 (쥬쿠슈) | 熟 | 6+ | 6+ | 5년+장기숙성·古酒·貴醸酒 |
| ★ | 기타 | Other | - | - | 焼酎·泡盛·위스키·맥주·リキュール·과실주 |

## 점수 부여 로직
1. **개별품목 오버라이드** (조사된 약 130+ 항목): 일본어/한국어 자료 직접 조사 → 정확 점수
2. **양조장 baseline**: 130+ 양조장 별 (향, 맛, 기본분류) 사전 등록 (출하 라인업 기반)
3. **이름 키워드 델타**: 정미율·효모·제법 키워드로 가산/감산

조사 출처: SAKETIME (saketime.jp), SAKETIMES (jp.sake-times.com), 蔵元 공식사이트, hasegawasaketen, IMADEYA, 矢島酒店, 鍵屋, 大和屋酒舗, 일본·한국 주판매점 등.

---
"""

from collections import Counter
c = Counter(e['class'] for e in entries)
out += "## 집계\n\n| 분면 | 품목수 | 비율 |\n|---|---|---|\n"
for k in ['薰 Kun','醇 Jun','爽 Sou','熟 Juku','Other']:
    v = c.get(k,0)
    out += f"| {k} | {v} | {v/len(entries)*100:.1f}% |\n"
out += f"| **합계** | **{len(entries)}** | 100% |\n\n---\n\n"

def section(title, key, sort_by_score=True):
    items = [e for e in entries if e['class']==key]
    if sort_by_score:
        items.sort(key=lambda e:(-e['aroma'],-e['richness'],e['booth']))
    else:
        items.sort(key=lambda e:(e['booth'],e['brewery']))
    s = f"## {title} ({len(items)}품목)\n\n"
    s += "| 부스 | 양조장 | 품목 | 향 | 맛 | 근거 |\n|---|---|---|---|---|---|\n"
    for e in items:
        s += f"| {e['booth']} | {e['brewery']} | {e['product']} | {e['aroma']} | {e['richness']} | {e['note']} |\n"
    s += "\n"
    return s

out += section("① 薰 Kun (향↑ 맛↓) — 긴죠·다이긴죠계", '薰 Kun')
out += section("② 爽 Sou (향↓ 맛↓) — 보통주·혼죠조·나마계", '爽 Sou')
out += section("③ 醇 Jun (향↓ 맛↑) — 준마이·키모토·야마하이계", '醇 Jun')
out += section("④ 熟 Juku (향↑ 맛↑) — 장기숙성·고슈계", '熟 Juku')
out += section("★ Other — 쇼츄·아와모리·위스키·리큐어·맥주·과실주", 'Other')

with open('/Users/user/fun/sakefes/SAKE_SCORED.md','w',encoding='utf-8') as f:
    f.write(out)

print("Wrote SAKE_SCORED.md and updated brewery MDs.")
print(f"Lines: {out.count(chr(10))}")
