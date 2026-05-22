"""
2026 서울사케페스티벌 - 사케 점수제 분류
- aroma (0-10): 향 강도
- richness (0-10): 맛 풍부도
- type: 薰/爽/醇/熟 + 기타
Based on: SSI 4-type framework (kunshu/soushu/junshu/jukushu)
Sources researched: bosa.co.kr, sake-times, sake-5.jp, brewery sites
"""
import os, re, json
from collections import defaultdict, Counter

BREW_DIR = '/Users/user/fun/sakefes/breweries'

# Brewery baseline (aroma, richness, default_class)
# Researched from official sites / SAKETIME / hasegawasaketen / SAKETIMES
BREWERY_PROFILE = {
    'A03': ('고쿠류주조', 7, 5, 'Kun'),       # 黒龍 - daiginjo focus
    'A04': ('데와자쿠라주조', 8, 5, 'Kun'),    # 出羽桜 - aromatic ginjo
    'A05': ('이시모토주조', 4, 4, 'Sou'),      # 越乃寒梅 - 淡麗辛口
    'A06': ('코시메이조주식회사', 7, 6, 'Kun'),# 越銘醸 山城屋 - aromatic
    'A07': ('이네토아가베', 5, 8, 'Other'),    # 아가베 spirit
    'A09': ('니혼세이슈', 7, 5, 'Kun'),       # 千歳鶴 - JDGJ
    'A10': ('고쵸다주조', 7, 5, 'Kun'),       # 東一 (Azumaichi) - ginjo
    'A11': ('이소지만주조', 8, 5, 'Kun'),     # 磯自慢
    'A11b': ('하츠카메양조', 6, 5, 'Kun'),    # 初亀
    'A12': ('아이하라주조', 7, 5, 'Kun'),     # 雨後の月
    'A12b': ('텐료하이주조', 6, 4, 'Kun'),    # 天領盃/雅楽代 clean light
    'A13': ('코이즈미주조', 6, 5, 'Kun'),     # 東魁盛
    'A13b': ('오모야주조', 7, 5, 'Kun'),      # 横山五十
    'A14': ('후지이양조', 7, 6, 'Kun'),
    'A14b': ('요쓰야주조', 6, 5, 'Kun'),
    'B03_센킨': ('센킨', 7, 6, 'Kun'),         # 仙禽 - modern sweet-sour
    'B03_스미카와주조장': ('스미카와주조장', 7, 6, 'Kun'),  # 東洋美人
    'B03_이마니시주조': ('이마니시주조', 6, 6, 'Kun'),     # 今西/みむろ杉
    'B03_카모니시키주조': ('카모니시키주조', 7, 5, 'Kun'),  # 加茂錦
    'B03_타사키주조': ('타사키주조', 6, 5, 'Kun'),
    'B03_나가시마켄조': ('나가시마켄조', 6, 5, 'Kun'),
    'B03_야나기타주조': ('야나기타주조', 6, 5, 'Kun'),
    'B03_야마모토주조': ('야마모토주조', 6, 6, 'Jun'),    # 山本/和の月
    'B04': ('히가주조', 5, 7, 'Other'),       # 比嘉酒造 - awamori
    'B05': ('가토키치베쇼텐', 8, 5, 'Kun'),    # 加藤吉平商店 BORN
    'B06': ('쿠마가이주류', 6, 5, 'Kun'),
    'B07': ('SODAWARI', 4, 4, 'Other'),       # hi-ball
    'B08': ('사케노이치자', 4, 5, 'Other'),    # fruity liqueurs
    'B09': ('미이노고토부키', 7, 5, 'Kun'),    # 三井の寿
    'B10': ('하마카와쇼텐', 7, 5, 'Kun'),     # 美丈夫 Bijofu
    'B11': ('기타니시주조', 7, 6, 'Kun'),     # 北西酒造 - 文楽/SARA
    'B12': ('칸코바이주조', 5, 5, 'Sou'),     # 寒紅梅
    'B13': ('지자케CY코리아', 6, 5, 'Kun'),
    'D01': ('겐비시주조', 7, 8, 'Juku'),      # 剣菱 黒松剣菱 - aged style
    'D02': ('나카노주조', 6, 5, 'Kun'),       # ちえびじん - modern colorful junmai
    'D03': ('이와사키주조', 6, 6, 'Jun'),     # 千代の福娘
    'D04': ('즈이죠주조', 6, 6, 'Jun'),       # 瑞冠
    'D05': ('에미시키주조', 7, 6, 'Kun'),     # 笑四季
    'D06': ('혼다쇼텐', 6, 6, 'Jun'),         # 龍力 Tatsuriki
    'E01': ('닷사이주조', 8, 5, 'Kun'),       # 獺祭 - all JDGJ
    'E02': ('샤타주조', 7, 5, 'Kun'),         # 天狗舞 - actually rich/醇... but exhibit lineup
    'E03': ('가모츠루주조', 7, 5, 'Kun'),     # 賀茂鶴
    'E04': ('코마사주조', 5, 7, 'Other'),     # 小正 - shochu maker
    'E05': ('킹양조', 4, 5, 'Other'),         # 사와노모토 시럽
    'E06': ('아사히주조', 6, 5, 'Kun'),       # 久保田/朝日酒造
    'E07': ('남부비진', 7, 5, 'Kun'),         # 南部美人
    'E08': ('오토코야마주조', 5, 5, 'Sou'),    # 男山 - traditional
    'E09': ('메이리슈루이', 6, 5, 'Kun'),     # 明利酒類
    'E10': ('다카라주조', 5, 4, 'Other'),     # 宝酒造 - 미오 sparkling/리큐어
    'E11': ('센다이이사와케 카츠야마주조', 8, 6, 'Kun'),  # 勝山 - all JDGJ
    'E12': ('니시노킨료', 6, 5, 'Kun'),       # 西の関
    'E13': ('키타야', 6, 6, 'Jun'),           # 喜多屋
    'E14': ('니시주조', 6, 5, 'Kun'),
    'E15': ('히가시주조', 6, 5, 'Kun'),
    'E16': ('핫카이양조', 5, 4, 'Sou'),       # 八海山 - 淡麗
    'E17': ('세키야주조', 6, 5, 'Kun'),       # 関谷 蓬莱泉
    'E18': ('이나타혼텐', 6, 5, 'Kun'),
    'E19': ('사이야주조', 7, 5, 'Kun'),       # 斉彌 - 雪の茅舎
    'E20': ('후쿠치요주조', 7, 6, 'Kun'),     # 鍋島 Nabeshima
    'F01': ('토코야마', 6, 6, 'Jun'),         # 常山 Jōzan
    'F02': ('우메노야도 주조', 5, 5, 'Other'), # 梅乃宿 - liqueur focus
    'F03': ('카네다타마다주조', 6, 5, 'Kun'),  # カネタ玉田 340
    'F04': ('나가노 메이죠', 6, 5, 'Kun'),
    'F05': ('이이누마혼케', 6, 6, 'Jun'),     # 飯沼本家 甲子
    'F06': ('니카이도주조', 4, 7, 'Other'),   # shochu
    'F07': ('요시다주조', 6, 6, 'Jun'),       # 月山 Gassan
    'F08': ('배니오토메', 5, 7, 'Other'),     # shochu
    'F09': ('타츠우마', 5, 5, 'Sou'),         # 白鹿 Hakushika
    'F10': ('하나노마이주조', 6, 5, 'Kun'),   # 花の舞
    'F11': ('닷사이블루', 8, 5, 'Kun'),       # 獺祭 Blue - all JDGJ
    'F12': ('치요무스비주조', 5, 5, 'Other'), # 千代むすび - apple liqueur
    'F13': ('나테주조점', 6, 6, 'Jun'),       # 黒牛 Kuroushi
    'F14': ('남부주조장', 6, 5, 'Kun'),       # 花垣
    'F15': ('텐잔주조', 6, 6, 'Jun'),         # 七田/天山
    'F16': ('사카타주조', 6, 5, 'Kun'),
    'F17': ('세이료주조주식회사', 6, 6, 'Jun'),# 伊予賀儀屋
    'F18': ('아오키주조', 6, 6, 'Jun'),       # 鶴齢 Kakurei
    'F19': ('도이주조장', 6, 5, 'Kun'),       # 開運 Kaiun
    'F20': ('아야키쿠주조', 6, 5, 'Kun'),     # 綾菊 オリーブ酵母
    'G01': ('미야사카양조', 7, 5, 'Kun'),     # 真澄 Masumi
    'G02': ('코바야시주조', 8, 5, 'Kun'),     # 鳳凰美田
    'G03': ('츠치야주조점', 6, 6, 'Jun'),
    'G04': ('스와미코츠루 주조장', 6, 5, 'Kun'),  # 美湖鶴
    'G05': ('헤이와주조', 6, 5, 'Kun'),       # 紀土 Kid
    'G07': ('이와세주조', 6, 5, 'Kun'),
    'G08': ('시미즈 세이자부로쇼텐', 6, 6, 'Jun'),  # 作 Zaku
    'G09': ('하야시혼텐', 6, 5, 'Kun'),       # 百春
    'G10': ('키리시마쵸 증류소', 5, 7, 'Other'),  # 이모쇼츄
    'G11': ('텐파이', 4, 5, 'Other'),         # crafts coffee blend
    'G12': ('미치자쿠라주조', 6, 6, 'Jun'),    # 三千櫻
    'G13': ('라이후쿠주조', 7, 5, 'Kun'),     # 来福
    'G14': ('후지주조', 6, 6, 'Jun'),         # 出雲富士
    'G15': ('니이자와양조점', 6, 6, 'Jun'),    # 白楽星 Hakurakusei
    'G16': ('에시칼・스피리츠', 5, 5, 'Other'),  # craft spirits
    'G17': ('야츠시카주조', 5, 7, 'Other'),    # 八鹿 - 銀座のすずめ shochu line + sake
    'G18': ('사케노카마쿠라', 5, 5, 'Other'),  # 紀州蜜柑
    'G19': ('사츠마무쏘', 5, 7, 'Other'),     # 이모쇼츄
    'G20': ('신자토주조', 5, 7, 'Other'),     # 아와모리
    'H01': ('아키타양조', 6, 5, 'Kun'),       # 不寝番 等
    'H02': ('야마모토주조점', 6, 6, 'Jun'),    # 山本 Pure Black series
    'H03': ('미토베주조', 7, 6, 'Kun'),       # 楯野川 / 楯の川
    'H04': ('고토주조점', 6, 6, 'Jun'),       # 五人娘 等
    'H05': ('신도주조점', 7, 5, 'Kun'),       # 雅山流 Gasanryu
    'H06': ('나가야마혼케주조장', 6, 5, 'Kun'),# 山猿
    'H07': ('아부노츠루주조', 7, 5, 'Kun'),
    'H08': ('야오신주조', 6, 5, 'Kun'),
    'H09': ('우라자토주조점', 6, 5, 'Kun'),
    'H10': ('쿠메지마노쿠메센', 5, 7, 'Other'),# 아와모리
    'H11': ('슈호주조장', 6, 5, 'Kun'),
    'H12': ('록카센', 6, 5, 'Kun'),           # 六歌仙
    'H13': ('코지마소우혼텐', 6, 5, 'Kun'),    # 嘉美心 / 嘉麗 Karei
    'H14': ('키쿠노츠카사주조', 7, 5, 'Kun'),  # 菊の司
    'H15': ('아카부주조', 7, 6, 'Kun'),       # 赤武 AKABU
    'H16': ('카와자와주조', 6, 6, 'Jun'),     # 山二
    'H17': ('아리미츠주조장', 6, 5, 'Kun'),
    'H19': ('타카키주조', 8, 5, 'Kun'),       # 豊能梅 CEL-24 aromatic
    'H20': ('카메이즈미주조', 6, 6, 'Jun'),   # 亀泉
    'J01': ('세토주조', 6, 5, 'Kun'),         # 東町 Azumamachi
    'J02': ('아즈마츠루주조', 7, 5, 'Kun'),    # 東鶴 Azumatsuru
    'J03': ('후쿠다주조', 7, 6, 'Kun'),       # 福海/長崎美人 Hukumi
    'J04': ('타이요주조', 6, 6, 'Jun'),       # 大洋
    'J05': ('텐세이주조', 6, 5, 'Kun'),       # 天青 Tensei
    'J11': ('센게츠주조', 4, 7, 'Other'),     # 米焼酎 球磨
    'J12': ('오토코야마혼텐', 5, 5, 'Sou'),
    'J13': ('이마다주조혼텐', 7, 6, 'Kun'),   # 福鶴 Fukucho
    'J14': ('고젠슈 츠지혼텐', 6, 8, 'Jun'),   # 御前酒 - 雄町 kimoto
    'J15': ('오치주조', 6, 5, 'Kun'),         # 大正の鶴 Taishonotsuru
    'J16': ('니시요시다주조', 4, 7, 'Other'),  # 보리쇼츄
    'J17': ('타카하시쇼텐', 6, 5, 'Kun'),
    'J18': ('와카나미주조', 6, 5, 'Kun'),
    'J19': ('키쿠비진', 6, 6, 'Jun'),          # 菊美人
    'J20': ('리브롬', 5, 4, 'Other'),         # 허브리큐어
    'K01': ('키타주조', 6, 5, 'Kun'),         # 喜多 - 北鹿?
    'K02': ('유쵸주조', 7, 7, 'Jun'),         # 風の森 Kaze no Mori
    'K03': ('미오야주조', 6, 5, 'Kun'),
    'K04': ('니시야마주조장', 6, 6, 'Kun'),    # 小鼓 Kotsuzumi - 路上花 series
    'K05': ('사와노츠루', 5, 5, 'Sou'),       # 沢の鶴
    'M01': ('사카야코리아', 7, 5, 'Kun'),
    'M03': ('스이센주조', 6, 5, 'Kun'),       # 酔仙
    'M04': ('텐쥬주조', 7, 6, 'Kun'),         # 天寿
    'M05': ('사쿠라가오주조', 7, 5, 'Kun'),    # 桜顔
    'M06': ('하마치도리주조', 7, 5, 'Kun'),    # 浜千鳥
    'M07': ('야히코주조', 6, 5, 'Kun'),       # 弥彦
    'M08': ('아키타세이슈 주식회사', 6, 6, 'Kun'),  # 高清水/出羽鶴/刈穂
    'M10': ('마츠세주조주식회사', 6, 5, 'Kun'),
    'M11': ('산요하이슈죠', 6, 5, 'Kun'),     # 山陽盃
    'M12': ('아베주조', 6, 6, 'Kun'),         # あべ Abe - modern junmai genshu
    'P01': ('히라이즈미혼포', 5, 7, 'Jun'),    # 飛良泉 - 山廃
    'P02': ('쵸슈주조', 7, 5, 'Kun'),         # 長州
    'P03': ('하치노헤주조', 7, 5, 'Kun'),     # 八仙/八戸酒造
    'P04': ('야마츄혼케주조', 5, 8, 'Jun'),    # 義侠/桔梗 Gikyo - junmai purist
    'P05': ('마치다슈조텐', 6, 5, 'Kun'),
    'P06': ('나카시마야슈죠', 6, 5, 'Kun'),    # 中島屋 寿
    'P07': ('야기슈조부', 6, 5, 'Kun'),       # 山丹正宗 Yamatan
    'P08': ('요시다슈죠', 6, 5, 'Kun'),       # 吉田蔵
    'P09': ('오누마주조점', 6, 5, 'Kun'),     # 一生青春
    'P10': ('히라코우주조', 6, 5, 'Kun'),
    'P11': ('에이쿤주조', 6, 5, 'Kun'),       # 英君
    'P13': ('류진슈조', 6, 5, 'Kun'),         # 龍神
    'P14': ('이이누마메이죠', 6, 5, 'Kun'),    # 醸し人 Flying Sugata
    'P15': ('카네미츠슈죠', 6, 5, 'Kun'),
    'Q01': ('하기노슈조', 6, 5, 'Kun'),       # 萩錦
    'Q02': ('오야타카시슈조', 6, 5, 'Kun'),
    'Q03': ('쥬하치자카리슈조', 6, 5, 'Kun'),  # 十八盛
    'Q04': ('와타나베슈조텐', 6, 6, 'Kun'),    # 蓬莱 Hourai
    'Q05': ('하마다슈죠', 5, 7, 'Other'),     # 赤兎馬 imo-shochu
    'Q06': ('오쿠치슈조', 5, 7, 'Other'),     # 이모쇼츄
    'Q07': ('토노이케슈죠텐', 6, 5, 'Kun'),
    'Q08': ('키쿠노사토슈조', 6, 5, 'Kun'),
    'Q09': ('미야오슈조', 6, 5, 'Kun'),
    'Q10': ('토미카와슈조텐', 6, 5, 'Kun'),
    'Q11': ('후미기쿠슈죠', 6, 5, 'Kun'),
    'Q12': ('야마노고토부키슈죠', 6, 5, 'Kun'),# 山の壽 - modern
    'Q13': ('토코로슈조', 6, 5, 'Kun'),       # 房島屋
    'Q14': ('신타니슈조', 6, 5, 'Kun'),
    'R01': ('토요나가슈죠', 4, 7, 'Other'),    # shochu
    'R02_쇼츄리퍼블릭': ('쇼츄리퍼블릭', 4, 7, 'Other'),
    'R02_오치아이 슈조장': ('오치아이 슈조장', 4, 7, 'Other'),
    'R03_타카자와 슈조장': ('타카자와 슈조장', 6, 6, 'Jun'),  # 喜久泉 Kikuizumi
    'R03_이치노야': ('이치노야', 5, 5, 'Other'),
    'R04': ('잇본기쿠보혼텐', 5, 7, 'Other'), # 銀紅梅 shochu
    'U01': ('닛카프론티어', 7, 7, 'Other'),    # whisky
    'U12': ('에비스 맥주', 5, 5, 'Other'),    # beer
    'L02': ('이와테메이죠', 6, 5, 'Kun'),
    'L03': ('CR트레이딩', 5, 6, 'Other'),
    'L04': ('CR트레이딩', 5, 7, 'Other'),
    # 단일 양조장 부스 미커버 — fallback default
}

# Manual product overrides for specific named products
PRODUCT_OVERRIDES = {
    # 출하조정/리큐어
    '데와자쿠라 토로케루 라프랑스': ('Other', 4, 4, '리큐어(과실)'),
    '데와자쿠라 유키메가미': ('Kun', 8, 5, '純米大吟醸(雪女神 쌀)'),
    '데와자쿠리 잇코 혼나마': ('Kun', 7, 5, '純米吟醸 生'),
    '유키만만 빙점하 5년 숙성중': ('Juku', 7, 8, '5년숙성'),
    # 越乃寒梅 series
    '코시노칸바이 벳센': ('Kun', 6, 4, '吟醸 別撰'),
    '코시노칸바이 사이': ('Kun', 7, 5, '純米吟醸 灑'),
    '코시노칸바이 아마네': ('Kun', 7, 4, '純米吟醸 浹'),
    '코시노칸바이 세이슈': ('Sou', 4, 4, '清酒(普通酒)'),
    '코시노칸바이 초토쿠센': ('Kun', 9, 5, '大吟醸 超特撰'),
    '코시노칸바이 라군': ('Jun', 6, 8, '純米 Lagoon 濃厚'),
    # 山城屋
    '야마시로야 1st Class': ('Kun', 7, 6, '純米大吟醸 1st Class'),
    '야마시로야 에이케이': ('Kun', 7, 6, '純米大吟醸 AK'),
    '야마시로야 루스이': ('Jun', 6, 7, '純米 留守居 Standard'),
    '야마시로야 가호': ('Kun', 7, 6, '純米吟醸 雅'),
    '야마시로야 후우가': ('Kun', 7, 6, '純米吟醸 風雅'),
    # 雅楽代
    '우타시로 릿카': ('Kun', 7, 5, '純米大吟醸 凜華'),
    '우타시로 즈이카': ('Kun', 7, 5, '純米大吟醸 瑞華'),
    '우타시로 히요리': ('Sou', 5, 4, '純米吟醸 日和 低알코올'),
    '우타시로 겟카': ('Kun', 6, 5, '純米吟醸 月華'),
    '우타시로 나루카미': ('Sou', 5, 4, '純米吟醸 鳴神 超辛口'),
    # 친구 블랙라벨
    '친구 블랙라벨': ('Kun', 6, 5, '東魁盛 친구 Black'),
    # 仙禽
    '카쿠메이 센킨 잇세이': ('Kun', 8, 7, '革命 一聲 프리미엄'),
    '센킨 모던': ('Kun', 7, 6, 'モダン junmai (sweet-sour acidic)'),
    '토요비진 준도이치즈': ('Kun', 7, 6, '東洋美人 純度一途'),
    # 비죠후
    '비죠후 폰 슈와': ('Kun', 7, 4, '美丈夫 ポン・シュワ Sparkling'),
    '사라 펄즈 오브 듀': ('Kun', 7, 4, 'SARA Pearls of Dew Sparkling'),
    # 칸코바이
    '칸코바이 쥰마이 야마다니시키60': ('Jun', 5, 7, '寒紅梅 純米 山田錦60'),
    # 剣菱 black pine
    '쵸토쿠센 고쿠죠 쿠로마츠 겐비시': ('Juku', 7, 8, '超特選 極上 黒松剣菱'),
    '고쿠죠 쿠로마츠 겐비시': ('Juku', 7, 8, '極上 黒松剣菱'),
    '미즈호 쿠로마츠 겐비시': ('Juku', 6, 7, '瑞穂 黒松剣菱'),
    '즈이쇼 쿠로마츠 겐비시': ('Juku', 7, 9, '瑞祥 黒松剣菱 長期熟成'),
    # 智恵美人
    '치에비진 쥰마이': ('Jun', 5, 6, '純米'),
    '치에비진 LOVE PINK': ('Kun', 6, 6, '純米 桃色 にごり 赤酵母'),
    '키츠키 블랑 큐베 치에비진 生': ('Kun', 7, 5, 'Blanc Cuvée 生'),
    '치에비진 Rouge Blanc': ('Kun', 6, 5, 'Rouge Blanc'),
    '치에비진 라팡 生': ('Kun', 6, 5, 'Lapin 봄 한정 生'),
    '치에비진 에버그린': ('Kun', 6, 5, 'Evergreen'),
    # 龍力
    '타츠리키 토쿠베츠 쥰마이 쥰마이88 코메코도부키': ('Jun', 5, 7, '特別純米 88'),
    '타츠리키 토쿠베츠 쥰마이 쿠라다시 신슈 生': ('Jun', 5, 7, '特別純米 蔵出し 新酒 生'),
    '타츠리키 토쿠베츠 쥰마이 시보리타테 生': ('Sou', 5, 6, '特別純米 しぼりたて 生'),
    # 笑四季
    '에미시키 토쿠베츠쥰마이 센세이션 블랙 生': ('Jun', 5, 7, '笑四季 特別純米 Sensation Black'),
    '에미시키 토쿠베츠쥰마이 센세이션 화이트 生': ('Jun', 5, 7, '笑四季 特別純米 Sensation White'),
    '에미시키 토쿠베츠쥰마이 센세이션 블루 生': ('Jun', 5, 7, '笑四季 特別純米 Sensation Blue'),
    '에미시키 월드피스': ('Kun', 7, 6, '笑四季 World Peace'),
    '에미시키 퓨처리즘 쥰마이 이치고 메디테이션': ('Jun', 6, 7, 'Futurism 純米'),
    # 千代の福娘
    '쵸요후쿠무스메 야마다니시키 쥰마이 모모이로': ('Jun', 6, 6, '純米 桃色'),
    '쵸요후쿠무스메 사이토노시즈쿠 카라구치 지카구미 히이레': ('Jun', 5, 7, '純米 직급 火入'),
    # 瑞冠
    '호우쥰 쥰마이슈 즈이요': ('Jun', 5, 7, '芳醇 純米酒 瑞陽'),
    # 獺祭
    '닷사이 소노사키에': ('Kun', 9, 6, '磨きその先へ 超프리미엄 JDGJ'),
    '닷사이 쇼츄': ('Other', 5, 6, '쇼츄(粕取)'),
    # Kamotsuru
    '가모츠루 잇테키뉴콘': ('Kun', 6, 5, '一滴入魂 純米吟醸'),
    '가모츠루 소우가쿠': ('Kun', 8, 5, '双鶴 大吟醸'),
    # 小正(코마사)
    '쿠라노시콘': ('Other', 5, 6, '小正 焼酎'),
    '코즈루 PINK GOLD': ('Other', 5, 6, '小鶴 PINK GOLD'),
    '아카자루': ('Other', 5, 6, '赤猿 焼酎'),
    '사와전용 유즈레몬': ('Other', 4, 5, 'サワー専用 유즈레몬'),
    # キング醸造
    '라무네 사와노모토진저 사와노모토': ('Other', 3, 4, '사와노모토 시럽'),
    '시소 사와노모토': ('Other', 3, 4, '사와노모토 시럽'),
    '콜라 사와노모토': ('Other', 3, 4, '사와노모토 시럽'),
    # 朝日 (Kubota)
    '추구': ('Jun', 5, 6, '久保田 千寿 純米吟醸'),
    '쿠보타 만주 자사효모 에디션': ('Kun', 8, 6, '久保田 萬寿 自社酵母 JDGJ'),
    '쿠보타 유즈': ('Other', 4, 4, '久保田 ゆずリキュール'),
    # 男山
    '오토코야마 스시부스터': ('Kun', 6, 5, '寿司Booster 純米吟醸'),
    '오토코야마 하루노이자나이': ('Kun', 6, 5, '春のいざない 純米吟醸 限定'),
    '오토코야마 아키노이로도리': ('Kun', 6, 5, '秋の彩 純米吟醸 한정'),
    # 明利
    '타이야키': ('Other', 4, 5, 'たい焼き sweet sake?'),
    '소노마마 멜론': ('Other', 4, 4, '梅酒/멜론 리큐어'),
    '소노마마 망고': ('Other', 4, 4, '망고 리큐어'),
    '소노마마 살구': ('Other', 4, 4, '살구 리큐어'),
    # 宝酒造
    '미오': ('Kun', 6, 4, '澪 Sparkling Sake'),
    '미오 클리어': ('Kun', 6, 3, '澪 Clear'),
    '다카라 시즈오카 미캉': ('Other', 4, 4, '宝 미캉 사케칵테일'),
    '다카라 시마네 샤인머스켓': ('Other', 4, 4, '샤인머스켓 칵테일'),
    '다카라 야마나시 화이트피치': ('Other', 4, 4, '백도 칵테일'),
    '다카라 후라노 멜론': ('Other', 4, 4, '멜론 칵테일'),
    # 勝山
    '카츠야마 다이아몬드 아카츠키': ('Kun', 9, 7, 'DIAMOND暁 JDGJ 최고급'),
    '카츠야마 아카츠키': ('Kun', 8, 6, '暁 JDGJ 遠心しぼり'),
    '카츠야마 레이': ('Kun', 7, 6, '礼 JDGJ'),
    '카츠야마 센쇼마사무네': ('Kun', 7, 6, '仙松正宗 JDGJ'),
    '카츠야마 켄': ('Kun', 8, 6, '献 JDGJ'),
    '카츠야마 엔': ('Kun', 7, 6, '圓 JDGJ'),
    # 八海山
    '핫카이산 세이슈': ('Sou', 4, 4, '清酒(普通酒)'),
    '핫카이산 에치코데소로 생주 블루라벨': ('Sou', 6, 6, 'しぼりたて 生原酒 越後で候 청라벨 JDGJ'),
    '코메쇼츄 핫카이산 요로시쿠 센만 아루베시': ('Other', 4, 5, '米焼酎'),
    # 常山
    '죠잔 SPRARKLING 니고리 사케': ('Kun', 7, 5, 'Sparkling にごり'),
    '죠잔 후나바하츠즈메 즈이이치': ('Kun', 7, 5, '槽場初詰 純米大吟醸 瑞一'),
    # 梅乃宿
    '우메노야도 아라고시 유즈슈': ('Other', 4, 4, '柚子酒'),
    '우메노야도 아라고시 모모': ('Other', 4, 4, '桃 리큐어'),
    '우메노야도 토마토': ('Other', 4, 4, '토마토 리큐어'),
    '우메노야도 시트러스위트 Citrusweet': ('Other', 4, 4, 'Citrus liqueur'),
    # 카네타玉田
    '340': ('Kun', 7, 5, '銘柄 340 純米大吟醸'),
    # 飯沼本家
    '키노에네 쥰마이 우마카라 미가키하치와리': ('Jun', 4, 7, '甲子 純米 旨辛 磨き8割'),
    '키노에네 아키아가리': ('Jun', 5, 6, '甲子 秋上がり 純米'),
    # 二階堂
    '니카이도': ('Other', 4, 7, '麦焼酎'),
    '니카이도 킷쵸무 25도 병': ('Other', 4, 7, '麦焼酎 25도'),
    # 月山(吉田)
    '갓산 토쿠베츠 쥰마이': ('Jun', 5, 7, '月山 特別純米 出雲'),
    '갓산 토쿠베츠 쥰마이 이즈모': ('Jun', 5, 7, '月山 特別純米 出雲'),
    # 紅乙女
    '캇파 큐센보우혼류': ('Other', 5, 7, '紅乙女 焼酎'),
    '베니오토메 STANDARD25 에구치히사시VERVION': ('Other', 5, 6, '紅乙女 25도'),
    # 白鹿
    '하쿠시카 야마다니시키 카라구치 쥰마이 실크': ('Jun', 5, 6, '白鹿 山田錦 辛口 純米 シルク'),
    '하쿠시카 시보리타테': ('Sou', 5, 5, '白鹿 しぼりたて'),
    # 獺祭ブルー
    '닷사이 블루 타입 23': ('Kun', 9, 6, '獺祭BLUE TYPE23 JDGJ'),
    '닷사이 블루 타입 35': ('Kun', 8, 5, '獺祭BLUE TYPE35 JDGJ'),
    '닷사이 블루 타입 50': ('Kun', 7, 5, '獺祭BLUE TYPE50 JDGJ'),
    '닷사이 블루 타입 50 드라이(Dry)': ('Kun', 7, 4, '獺祭BLUE TYPE50 Dry'),
    # 千代むすび
    '치요무스비 애플리큐르': ('Other', 4, 4, '사과 리큐어'),
    # 黒牛
    '쿠로우시 카라구치 쥰마이슈 레드': ('Jun', 5, 7, '黒牛 辛口 純米'),
    '쥰마이슈 쿠로우시 시보리타테': ('Sou', 5, 6, '黒牛 純米 しぼりたて'),
    # 花垣
    '하나가키 쥰마이슈': ('Jun', 5, 6, '花垣 純米酒'),
    # 七田
    '시치다 510': ('Kun', 7, 6, '七田 510 純米 muscat-like'),
    '시치다 나나와리고부미가키 슌요': ('Jun', 7, 6, '七田 75% 磨 春陽 純米 lychee/grapefruit'),
    # 伊予賀儀屋
    '이요카기야 쥰마이 무로카': ('Jun', 5, 7, '伊予賀儀屋 純米 無濾過'),
    # 鶴齢
    '카쿠레이 쥰마이': ('Jun', 5, 7, '鶴齢 純米'),
    '카쿠레이 코키무라사키': ('Jun', 6, 6, '鶴齢 越淡麗 限定'),
    # 開運
    '카이운 마네키네코 히야즈메쥰마이(핑크라벨)': ('Jun', 5, 6, '開運 招き猫 ひやおろし 純米'),
    '카이운 이와이자케': ('Kun', 7, 5, '開運 祝酒 純米大吟醸 한정'),
    # 綾菊
    '아야키쿠 올리브 이스트 쥰마이 사케': ('Jun', 6, 6, '綾菊 オリーブ酵母 純米'),
    '아야키쿠 사누키올리브11': ('Jun', 6, 6, '綾菊 サヌキオリーブ11'),
    # 鳳凰美田
    '호오비덴 츠루기': ('Jun', 5, 6, '鳳凰美田 剣 辛口純米'),
    # 美湖鶴
    '미코츠루 히토고코치': ('Jun', 5, 6, '美湖鶴 純米 ヒトゴコチ'),
    # 紀土
    '킷도 무료잔': ('Kun', 8, 6, '紀土 無量山 純米大吟醸 25%/35%'),
    # 作
    '자쿠 미야비노토모 나카도리': ('Kun', 8, 6, '作 雅乃智 中取り 純米大吟醸'),
    '자쿠 호노토모': ('Jun', 6, 6, '作 穂乃智 純米'),
    # 키리시마쵸 증류소 imo
    '아카루이노우손 (고구마)': ('Other', 5, 7, '芋焼酎'),
    '아카루이노우손 실크 스위트 (고구마)': ('Other', 5, 7, '芋焼酎'),
    # 텐파이 craft
    '크래프츠맨 타다 스패니시': ('Other', 4, 5, 'sake craft blend'),
    '크래프츠맨 타다 키안티 브라운': ('Other', 4, 5, 'sake craft blend'),
    '크래프츠맨 타다 2417': ('Other', 4, 5, 'sake craft blend'),
    '크래프츠맨 타다 나츠코이': ('Other', 4, 5, 'sake craft blend'),
    'Coffee Specialite': ('Other', 5, 5, 'coffee blend'),
    'Pepper Specialite': ('Other', 5, 5, 'pepper blend'),
    # 三千櫻
    '미치자쿠라 쥰마이 R Class': ('Jun', 5, 6, '三千櫻 純米 R Class'),
    # 来福
    '라이후쿠 쥰마이슈 후쿠마루': ('Jun', 5, 6, '来福 純米 福丸'),
    '라이후쿠 엠 스페셜 에디션 퓨어': ('Kun', 7, 5, '来福 M Special Edition Pure'),
    # 出雲富士
    '이즈모후지 쥰마이': ('Jun', 5, 6, '出雲富士 純米'),
    '이즈모후지 토쿠베츠 쥰마이': ('Jun', 5, 7, '出雲富士 特別純米'),
    # 白楽星
    '하쿠라쿠세이 토쿠베츠 쥰마이': ('Jun', 5, 7, '伯楽星 特別純米'),
    '카오루코우챠슈': ('Other', 5, 4, '香 紅茶酒'),
    # G16 craft spirits
    '라스트 엘리시움': ('Other', 6, 5, 'craft spirit'),
    '라스트 엘레강트': ('Other', 6, 5, 'craft spirit'),
    '라스트 엔': ('Other', 6, 5, 'craft spirit'),
    '교토 페퍼 에티크': ('Other', 6, 5, 'craft spirit'),
    '카카오 에티크': ('Other', 6, 5, 'craft spirit'),
    # 八鹿 (G17)
    '긴자노스즈메 시로코우지': ('Other', 5, 6, '銀座のすずめ 白麹 焼酎'),
    '긴자노스즈메 코하쿠': ('Other', 5, 7, '銀座のすずめ 琥珀 樽熟成 焼酎'),
    '카보스슈': ('Other', 4, 4, 'カボス酒 리큐어'),
    '긴자노스즈메 가스라이트': ('Other', 5, 6, '銀座のすずめ Gas Light'),
    # 紀州 蜜柑
    '키슈 칸칸야 운슈미캉슈': ('Other', 4, 4, '紀州 温州蜜柑酒'),
    # 사츠마무쏘 imo
    '오토메자쿠라': ('Other', 5, 7, '芋焼酎'),
    '모구라': ('Other', 5, 7, '芋焼酎'),
    '이모노타루': ('Other', 5, 7, '芋焼酎 樽'),
    # 신자토 awamori
    '류큐 골드': ('Other', 5, 7, '泡盛 GOLD'),
    '카리유시': ('Other', 5, 7, '泡盛'),
    # 山本
    '퓨어블랙 야마모토': ('Kun', 6, 6, '山本 Pure Black 純米吟醸'),
    # 미토베 楯野川
    '시드르 마사무네 오우린': ('Other', 4, 4, '楯野川 シードル 사과'),
    # 雅山流
    '가산류 고쿠게츠 시즈쿠도리': ('Kun', 8, 5, '雅山流 極月 雫取り 大吟醸'),
    '우라가산류 코우카': ('Kun', 7, 5, '裏・雅山流 香華'),
    # 쿠메지마 久米仙 awamori
    '쿠메지마노쿠메센 브라운': ('Other', 5, 8, '泡盛 古酒 브라운'),
    '오키나와 시콰사': ('Other', 4, 4, 'シークヮーサー'),
    # 키쿠노츠카사
    '이노센트 40': ('Kun', 8, 5, '菊の司 イノセント40 純米大吟醸'),
    '이노센트 50': ('Kun', 7, 5, '菊の司 イノセント50 純米大吟醸'),
    # 山二
    '야마니 쿠모가 자아구자아구': ('Jun', 6, 7, '山二 雲がざあぐざあぐ'),
    # 豊能梅
    '토요노우메 CEL-24': ('Kun', 9, 5, '豊能梅 CEL-24 효모 strawberry-like aromatic'),
    # 세토주조
    '아즈마쵸 무츠고로상 하지메테': ('Kun', 6, 5, '東町 ムツゴロウさん 初めて'),
    # 東鶴
    '아즈마츠루 MOVIN\'': ('Kun', 7, 6, '東鶴 MOVIN\''),
    '아즈마츠루 The Origin': ('Kun', 7, 6, '東鶴 The Origin'),
    # 福海
    '쟈가타라 오하루': ('Kun', 6, 6, 'ジャガタラお春'),
    '후쿠우미 야마다니시키': ('Kun', 6, 6, '福海 山田錦'),
    # 天青
    '케센토 하루카': ('Kun', 7, 5, '天青 케센토 ハルカ 純米吟醸'),
    # 球磨焼酎
    '카와베 (쌀)': ('Other', 5, 6, '球磨 米焼酎'),
    '타루 센게츠 (쌀/오크저장)': ('Other', 6, 7, '樽 球磨 米焼酎'),
    # 福鶴 福長
    '후쿠쵸 시후도 Seafood': ('Kun', 6, 6, '福鶴 Seafood 純米吟醸'),
    # 御前酒
    '고잰슈 1859': ('Jun', 6, 8, '御前酒 1859 雄町 きもと'),
    # 大正の鶴
    '타이쇼노츠루 RISING 아사히': ('Kun', 7, 6, '大正の鶴 RISING 朝日米'),
    '타이쇼노츠루 나카도리': ('Kun', 7, 6, '大正の鶴 中取り'),
    # 麦焼酎 etc
    '킨타로 (볶은보리)': ('Other', 5, 6, '麦焼酎'),
    '츠쿠시 시로 (보리)': ('Other', 5, 6, '麦焼酎'),
    # 菊美人
    '키쿠비진 하나칸무리': ('Jun', 6, 6, '菊美人 花冠 純米吟醸'),
    # 리브롬 허브
    '리브롬 민트': ('Other', 4, 4, 'リブロム ハーブ酒 民트'),
    '리브롬 버베나': ('Other', 4, 4, 'リブロム ハーブ酒 버베나'),
    # 風の森
    '카제노모리 아키츠호 657': ('Jun', 7, 7, '風の森 秋津穂 657 無濾過生原酒 純米'),
    '카제노모리 알파 타입 2': ('Kun', 8, 6, '風の森 ALPHA TYPE2 高精白 純米'),
    # 小鼓 - 路上花 サラ etc
    '로죠 하나아리 사라': ('Kun', 7, 6, '路上花 あり SARA 純米吟醸'),
    '탐바 미야마 시로부도': ('Kun', 6, 5, '丹波 美山 白葡萄'),
    # CR L03/L04 - various
    '이비 화이트': ('Other', 5, 5, 'CR 유통'),
    '킨스즈메 플래티넘': ('Other', 5, 5, 'CR 유통'),
    '혼킨 슷핀 타이치': ('Other', 5, 5, 'CR 유통'),
    '이즈미히메 유즈': ('Other', 4, 4, '유즈 리큐어'),
    '이즈미히메 레몬': ('Other', 4, 4, '레몬 리큐어'),
    '이사다이센': ('Other', 5, 7, '쇼츄'),
    '로우': ('Other', 5, 7, '쇼츄'),
    '야키이모 쿠로세': ('Other', 5, 7, '焼芋 黒瀬'),
    '베니산고': ('Other', 5, 7, '紅珊瑚 芋焼酎'),
    '미야코자쿠라': ('Other', 5, 7, '芋焼酎'),
    '엔마': ('Other', 5, 7, '閻魔 麦焼酎'),
    '렌토': ('Other', 5, 7, 'れんと 黒糖焼酎'),
    '컬러풀': ('Other', 5, 6, 'カラフル'),
    '미타케': ('Other', 5, 7, '焼酎'),
    '케이코우토나루모': ('Other', 5, 7, '鶏口となるも 芋焼酎'),
    # 야히코
    '폰슈볼': ('Other', 4, 4, '폰슈볼(잔)'),
    # 阿部
    '아베 블랙': ('Kun', 7, 7, 'あべ Black 純米吟醸 生原酒'),
    '아베 실버': ('Kun', 6, 7, 'あべ Silver 純米吟醸 火入 sweet'),
    '아베 옐로우': ('Kun', 6, 6, 'あべ Yellow 一本〆 純米吟醸 crisp'),
    '아베 핑크': ('Kun', 7, 6, 'あべ Pink たかね錦 peach/apple aroma'),
    '아베 그린': ('Kun', 7, 7, 'あべ Green 純米吟醸 生原酒 おりがらみ'),
    '사자나미': ('Jun', 6, 7, 'さざなみ 純米生原酒'),
    '레굴루스': ('Kun', 8, 7, 'Regulus 한정 high-end'),
    '포말하우트': ('Kun', 8, 7, 'Fomalhaut 한정'),
    '베가': ('Kun', 8, 7, 'Vega 한정'),
    # 飛良泉
    '포시즌 우스니고리': ('Kun', 7, 6, '飛良泉 四季 うすにごり'),
    '히텐 히나': ('Jun', 6, 7, '飛囀 HINA 山廃純米吟醸'),
    '히텐 하쿠쵸': ('Jun', 6, 7, '飛囀 白鳥 山廃純米吟醸'),
    # 八仙
    '핫센 우라라': ('Kun', 7, 5, '八仙 麗(うらら) 純米吟醸'),
    '핫센 블라쥬': ('Kun', 7, 5, '八仙 Blasie 純米吟醸 nama'),
    # 義侠 桔梗
    '기쿄에니시': ('Jun', 5, 8, '桔梗 縁 義侠 純米'),
    '기쿄 토모가라': ('Jun', 5, 8, '桔梗 共柄 純米'),
    '기쿄 카가리비': ('Jun', 6, 8, '桔梗 篝火 純米吟醸'),
    '기쿄 요로코비': ('Jun', 5, 8, '桔梗 慶び 純米'),
    '기쿄 타헤': ('Jun', 5, 8, '桔梗 多兵衛 純米'),
    '기쿄 2001-40 (2001년 양조)': ('Juku', 8, 9, '桔梗 2001 BY 40% 25년 숙성'),
    # 中島屋
    '나카시마야 하루츠게슈': ('Kun', 6, 6, '中島屋 春告酒'),
    # 山丹正宗
    '야마탄마사무네 재즈 브루': ('Kun', 7, 5, '山丹正宗 Jazz Brew'),
    # 吉田蔵
    '에헤지 하쿠류': ('Kun', 7, 6, '吉田蔵 u 白龍'),
    '에헤지 하쿠류 TOAST': ('Kun', 7, 6, '吉田蔵 TOAST'),
    '에헤지 하쿠류 RICH': ('Jun', 6, 7, '吉田蔵 RICH 山廃'),
    '에헤지 하쿠류 JOY': ('Kun', 7, 5, '吉田蔵 JOY'),
    '에헤지 하쿠류 EDGE': ('Kun', 6, 5, '吉田蔵 EDGE'),
    # 飯沼 Flying Sugata
    'Flying Sugata': ('Kun', 8, 6, 'Flying Sugata 純米大吟醸'),
    # 十八盛
    '쥬하치자카리 에이스 켓': ('Kun', 7, 5, '十八盛 Ace Get'),
    # 蓬莱
    '히다 호라이 죠센': ('Sou', 5, 5, '飛騨 蓬莱 上撰'),
    '호라이 쿠라모토노카쿠시자케': ('Kun', 7, 6, '蓬莱 蔵元のかくし酒 限定'),
    '코마치 사쿠라': ('Kun', 6, 5, '小町桜 純米吟醸'),
    # 적토마 imo
    '적토마(세키토바)': ('Other', 5, 7, '赤兎馬 芋焼酎'),
    '적토마(세키토바) 무라사키': ('Other', 5, 7, '赤兎馬 紫'),
    '적토마(세키토바) 타마아카네': ('Other', 5, 7, '赤兎馬 タマアカネ'),
    '우카제': ('Other', 5, 7, '芋焼酎'),
    '칠그린': ('Other', 5, 6, '芋焼酎'),
    '삿슈 타마시': ('Other', 5, 7, '薩州 魂'),
    '다이야메': ('Other', 5, 6, 'ダイヤメ 前割り'),
    '적토마(세키토바) 블루': ('Other', 5, 7, '赤兎馬 Blue'),
    '적토마(세키토바) 말차': ('Other', 5, 7, '赤兎馬 抹茶'),
    '칠그린 2': ('Other', 5, 6, '芋焼酎'),
    '카쿠시구라': ('Other', 5, 7, 'かくし蔵 芋焼酎'),
    # 大口 黒伊佐錦
    '쿠로이사니시키': ('Other', 5, 7, '黒伊佐錦 芋焼酎'),
    '이사코마치': ('Other', 5, 7, '伊佐小町'),
    '쿠로이사니시키 겐슈': ('Other', 5, 8, '黒伊佐錦 原酒'),
    # 山の壽
    '재패니스사케 야마노고토부키 프릭스1': ('Kun', 7, 6, '山の壽 PRIX1'),
    '재패니스사케 야마노고토부키 프릭스2': ('Kun', 7, 6, '山の壽 PRIX2'),
    '재패니즈사케 야마노고토부키 하루노히미츠': ('Kun', 7, 5, '山の壽 春の秘密'),
    '재패니즈사케 야마노고토부키 윈터 세션': ('Kun', 7, 6, '山の壽 Winter Session'),
    # 房島屋
    '보우지마야 토코로 블랙 고햐쿠만고쿠': ('Kun', 6, 6, '房島屋 ところ Black 五百万石'),
    # 即興 R系
    '무기시루': ('Other', 5, 6, '麦汁 麦焼酎'),
    '코하쿠 무기시루': ('Other', 5, 7, '琥珀 麦汁'),
    '신콜라': ('Other', 4, 5, '新コーラ'),
    '말차캣': ('Other', 5, 5, '焼酎+말차'),
    '롱페퍼 크레인': ('Other', 5, 5, '焼酎+페퍼'),
    '스위트 포테이토 로빈': ('Other', 5, 6, '芋焼酎'),
    '발리 버니': ('Other', 5, 6, '麦焼酎'),
    '카에다': ('Other', 5, 6, '焼酎'),
    '카제노 후쿠로': ('Other', 5, 6, '焼酎'),
    '카가미즈 진저': ('Other', 4, 5, '焼酎 진저'),
    # 류스이센
    '류스이센 효준스이': ('Other', 5, 5, '流水船'),
    # 잇본기쿠보혼텐
    '긴코바이 한야토': ('Other', 5, 7, '銀紅梅 半夜兎 焼酎'),
    # 日果フロンティア whisky
    '닛카 프론티어': ('Other', 7, 7, 'NIKKA Frontier 위스키'),
    '요이치 싱글몰트': ('Other', 8, 8, 'Yoichi Single Malt'),
    '미야기쿄 싱글몰트': ('Other', 8, 8, 'Miyagikyo Single Malt'),
    '타케츠루 퓨어몰트': ('Other', 8, 8, 'Taketsuru Pure Malt'),
}

# Booth code -> brewery profile key (handle dup booth)
def brewery_key(booth, name):
    # Some shared booths
    if booth == 'B03':
        return f'B03_{name}'
    if booth == 'A11' and '하츠카메' in name: return 'A11b'
    if booth == 'A11': return 'A11'
    if booth == 'A12' and '텐료하이' in name: return 'A12b'
    if booth == 'A12': return 'A12'
    if booth == 'A13' and '오모야' in name: return 'A13b'
    if booth == 'A13': return 'A13'
    if booth == 'A14' and '요쓰야' in name: return 'A14b'
    if booth == 'A14': return 'A14'
    if booth == 'R02' and '쇼츄리퍼블릭' in name: return 'R02_쇼츄리퍼블릭'
    if booth == 'R02': return 'R02_오치아이 슈조장'
    if booth == 'R03' and '이치노야' in name: return 'R03_이치노야'
    if booth == 'R03': return 'R03_타카자와 슈조장'
    return booth

def quadrant(aroma, richness, is_aged=False):
    # Juku only with explicit aging signal
    if is_aged:
        return '熟 Juku'
    if aroma >= 6 and richness < 6:
        return '薰 Kun'
    if aroma < 6 and richness >= 6:
        return '醇 Jun'
    if aroma >= 6 and richness >= 6:
        # 高香+高맛 — bias to dominant; tie → Kun (aroma 우선 SSI standard)
        if richness - aroma >= 2: return '醇 Jun'
        return '薰 Kun'
    return '爽 Sou'

def score_product(product, booth, brewery):
    n = product.replace(' ','').replace('　','')
    # 1. Manual override
    if product in PRODUCT_OVERRIDES:
        cls, a, r, note = PRODUCT_OVERRIDES[product]
        if cls == 'Other':
            return 'Other', a, r, note
        if cls == 'Juku':
            return '熟 Juku', a, r, note
        if cls == 'Kun':
            return '薰 Kun', a, r, note
        if cls == 'Jun':
            return '醇 Jun', a, r, note
        if cls == 'Sou':
            return '爽 Sou', a, r, note
    # 2. Brewery baseline
    bkey = brewery_key(booth, brewery)
    if bkey in BREWERY_PROFILE:
        _, a_base, r_base, def_cls = BREWERY_PROFILE[bkey]
    else:
        a_base, r_base, def_cls = 5, 5, 'Kun'
    a, r = a_base, r_base
    note_parts = []
    is_aged = False
    # 3. Keyword deltas
    # Daiginjo class
    if any(k in n for k in ['다이긴죠','다이긴조','大吟']):
        if '준마이' in n or '쥰마이' in n or '純米' in n:
            a += 2; r += 1; note_parts.append('純米大吟醸')
        else:
            a += 3; r -= 1; note_parts.append('大吟醸')
    elif any(k in n for k in ['긴죠','긴조','吟釀','준긴','쥰긴']):
        if '준마이' in n or '쥰마이' in n or '純米' in n:
            a += 2; r += 1; note_parts.append('純米吟醸')
        else:
            a += 2; r -= 1; note_parts.append('吟醸')
    elif any(k in n for k in ['특별준마이','토쿠베츠쥰마이','토쿠베츠준마이','特別純米']):
        a -= 0; r += 2; note_parts.append('特別純米')
    elif any(k in n for k in ['준마이','쥰마이','純米']):
        a -= 1; r += 2; note_parts.append('純米')
    elif any(k in n for k in ['혼죠조','本醸']):
        a -= 1; r -= 1; note_parts.append('本醸造')
    # Yeast/method
    if any(k in n for k in ['키모토','生酛','야마하이','山廃']):
        r += 2; note_parts.append('生酛/山廃')
    if '무로카' in n or '無濾過' in n:
        r += 1; note_parts.append('無濾過')
    if '나마겐슈' in n or '生原酒' in n:
        r += 1; note_parts.append('生原酒')
    if '나마' in n or '生酒' in n or n.endswith('生'):
        a += 1; note_parts.append('生')
    if '시보리타테' in n:
        a -= 1; r -= 1; note_parts.append('しぼりたて')
    if '시즈쿠' in n or '雫' in n:
        a += 2; note_parts.append('雫取り')
    # Aging
    if any(k in n for k in ['숙성','古酒','貴醸','키죠슈','코우슈']) or re.search(r'\d+년', n):
        a += 2; r += 3; is_aged = True; note_parts.append('熟成/古酒')
    # Sparkling / AWA
    if any(k in n for k in ['AWA','스파클링','SPARKLING','SPRARKLING','발포','폰슈와','폰 슈와','폰슈볼','니고리']):
        a += 2; r -= 1; note_parts.append('Sparkling/にごり')
    # Karaguchi
    if '카라구치' in n or '辛口' in n:
        r -= 0; note_parts.append('辛口')
    # Cap
    a = max(0, min(10, a))
    r = max(0, min(10, r))
    # If brewery is non-sake and no sake-classification keyword matched, force Other
    sake_kw_hit = any(k in note_parts for k in ['大吟醸','吟醸','純米大吟醸','純米吟醸','純米','特別純米','本醸造','生酛/山廃']) \
                  or any(k in (note_parts+[''])[0] for k in [])  # already covered
    if def_cls == 'Other' and not sake_kw_hit:
        return 'Other', a, r, (', '.join(note_parts) if note_parts else def_cls)
    cls = quadrant(a, r, is_aged)
    note = ', '.join(note_parts) if note_parts else def_cls
    return cls, a, r, note

# Process from products_source.json (stable source of truth)
with open('/Users/user/fun/sakefes/products_source.json','r',encoding='utf-8') as fp:
    sources = json.load(fp)
entries = []
for s in sources:
    cls, a, r, note = score_product(s['product'], s['booth'], s['brewery'])
    entries.append({
        'brewery': s['brewery'], 'booth': s['booth'], 'region': s['region'],
        'product': s['product'], 'class': cls, 'aroma': a, 'richness': r, 'note': note,
    })

with open('/Users/user/fun/sakefes/scored.json','w',encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

c = Counter(e['class'] for e in entries)
print(f"총 품목: {len(entries)}")
for k,v in c.most_common():
    print(f"  {k}: {v}")
