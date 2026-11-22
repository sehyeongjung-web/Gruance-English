# 하위 레벨 방 17차 (2026-11-22) — 43 · 44 · 45번 L5 세부 맞추기 · 45번 L5 19번째 ⑤ · 44번 L1 「하」 넷 · 43 · 44 · 45번 L1 이름 Kofi → Max
# 쓰는 법: python3 build17.py index.html   (최신본 위에 다시 돌려도 됨 — 바꿀 말이 없으면 멈춤)
# 정답 번호는 건드리지 않는다.
# ⓒ 정세형. 무단 복제 및 배포를 금지합니다.
import sys, json
sys.path.insert(0, '.')
import lib

path = sys.argv[1]
s, tb, te = lib.load(path)

def R(t, L, n, field, pairs, where='tb'):
    """t유형 L레벨 n번째(1부터)의 field에서 (old,new,몇 번)을 바꿈. field는 text/choices/ko/walk/cn."""
    box = (tb if where == 'tb' else te)[t][L][n - 1]
    for old, new, cnt in pairs:
        if field in ('choices', 'cn'):
            arr = box[field]; got = sum(x.count(old) for x in arr)
            assert got == cnt, (t, L, n, field, old, got, cnt)
            box[field] = [x.replace(old, new) for x in arr]
        else:
            got = box[field].count(old)
            assert got == cnt, (t, L, n, field, old, got, cnt)
            box[field] = box[field].replace(old, new)

def ALL(t, L, n, old, new):
    """문항 · 해설 모든 칸에서 old → new (이름 바꾸기용). 바꾼 수를 돌려줌."""
    k = 0
    for box in (tb[t][L][n - 1], te[t][L][n - 1]):
        for f, v in list(box.items()):
            if isinstance(v, str):
                k += v.count(old); box[f] = v.replace(old, new)
            elif isinstance(v, list):
                k += sum(x.count(old) for x in v if isinstance(x, str))
                box[f] = [x.replace(old, new) if isinstance(x, str) else x for x in v]
    return k

ans_before = {(t, L): [q['answer'] for q in tb[t][L]] for t in ('43', '44', '45') for L in ('1', '5')}

# ───────── ① 43 · 44 · 45번 L5 세부 맞추기 ─────────
# 5번째: 44번은 「같은 성별 두 사람」 틀이라 주인 성별을 43 · 45번(she)과 맞출 수 없음 → 44번의 신입 이름을 바꿔 다른 사람 이야기로 가르고, 둘째 토요일 시각은 43 · 45번(five past)으로 맞춤
assert ALL('44', '5', 5, '현이', '준이') > 0
assert ALL('44', '5', 5, 'Hyun', 'Jun') > 0
R('44', '5', 5, 'text', [('(b)He came at five to on the second Saturday', '(b)He came at five past on the second Saturday', 1)])
R('44', '5', 5, 'ko', [('(b)그는 둘째 토요일에 6시 55분에 와서', '(b)그는 둘째 토요일에 7시 5분에 와서', 1)], 'te')
R('44', '5', 5, 'walk', [
    ('\\"He came at five to on the second Saturday', '\\"He came at five past on the second Saturday', 0),
    ('"He came at five to on the second Saturday', '"He came at five past on the second Saturday', 1),
    ('(그는 둘째 토요일에 6시 55분에 와서', '(그는 둘째 토요일에 7시 5분에 와서', 1),
    ('준이는 정해진 시각보다 조금씩 일찍 나오는 신입이고', '준이는 7시 근무에 맞춰 나오는 신입이고', 1),
    ('도착 시각을 앞당겨 가며 테이블을 직접 정리하는 사람은', '3주째부터 도착 시각을 앞당겨 테이블을 직접 정리하는 사람은', 1),
], 'te')
R('44', '5', 5, 'cn', [('는 도착 시각을 점점 당겨 온 신입의 이야기이고', '는 도착 시각을 더 앞당긴 신입의 이야기이고', 1)], 'te')

# 6번째: 44번은 같은 성별(여동생) 틀이라 43 · 45번(남동생)과 맞출 수 없음 → 44번 주인공 이름을 바꿔 다른 집 이야기로 가름(44번 7번째에도 Yuna가 있어 겹침도 풂)
assert ALL('44', '5', 6, 'Yuna', 'Mina') > 0
assert ALL('44', '5', 6, '유나', '미나') > 0

# 8번째: 44번 이름 · 날을 43 · 45번(Mr. Kang · 폭설 내린 날)으로 맞춤
R('44', '5', 8, 'text', [
    ('Mr. Oyelaran opened his shop on the morning after the storm had passed and walked there, which took forty minutes.',
     'Mr. Kang opened his store on the morning of the heavy snow and walked there, which took forty minutes.', 1),
    ('in front of his shop and then', 'in front of his store and then', 1),
    ('since the storm passed,', 'since the heavy snow,', 1),
])
assert ALL('44', '5', 8, '오예라란 씨', '강 씨') > 0
for f, pairs in {
    'ko': [('폭풍이 지나간 다음 날 아침 가게를 열었는데', '폭설이 내린 날 아침 가게를 열었는데', 1),
           ('폭풍이 지나간 뒤로', '폭설이 내린 뒤로', 1)],
    'walk': [('폭풍이 지난 다음 날 40분을 걸어서', '폭설이 내린 날 40분을 걸어서', 1),
             ('폭풍이 지난 아침 일부러', '폭설이 내린 아침 일부러', 1),
             ('in front of his shop and then', 'in front of his store and then', 1),
             ('since the storm passed,', 'since the heavy snow,', 1),
             ('(그는 폭풍이 지나간 뒤로', '(그는 폭설이 내린 뒤로', 1),
             ('강 씨는 폭풍 다음 날부터', '강 씨는 폭설이 내린 날부터', 1),
             ('storm 폭풍 /', 'heavy snow 폭설 /', 1)],
    'cn': [('폭풍 다음 날 걸어서', '폭설이 내린 날 걸어서', 1),
           ('폭풍 다음 날 처음 가게를 연', '폭설이 내린 날 처음 가게를 연', 1)],
}.items():
    R('44', '5', 8, f, pairs, 'te')

# 8번째: 45번 「여덟 시 전」을 43번 「그날 늦은 오후」로 맞춤(43번은 순서 단서라 45번을 바꿈)
R('45', '5', 8, 'text', [('Three people came in before eight, all of them surprised to find the lights on.',
                          'Late that afternoon three people came in, all of them surprised to find him still there with the lights on.', 1)])
R('45', '5', 8, 'choices', [('여덟 시 전에 세 사람이 왔다', '그날 오후 늦게 세 사람이 왔다', 1)])
R('45', '5', 8, 'ko', [('8시 전에 세 사람이 들어왔는데, 모두 불이 켜져 있는 것을 보고 놀랐다.',
                        '그날 늦은 오후 세 사람이 들어왔는데, 모두 그가 여태 불을 켜 놓고 가게에 있는 것을 보고 놀랐다.', 1)], 'te')
R('45', '5', 8, 'walk', [
    ('숫자(여섯 시 · 40분 · 세 사람 · 여덟 시)와', '숫자(여섯 시 · 40분 · 세 사람)와 때(늦은 오후),', 1),
    ("▸ ①번 '여덟 시 전에 세 사람이 왔다'\n\"Three people came in before eight\"(여덟 시 전에 세 사람이 들어왔다)",
     "▸ ①번 '그날 오후 늦게 세 사람이 왔다'\n\"Late that afternoon three people came in\"(그날 늦은 오후 세 사람이 들어왔다)", 1),
], 'te')
R('45', '5', 8, 'cn', [("'여덟 시 전에 세 사람이 왔다' — 본문 내용과 일치합니다. \"Three people came in before eight\"(여덟 시 전에 세 사람이 들어왔다)와 숫자까지 같습니다.",
                        "'그날 오후 늦게 세 사람이 왔다' — 본문 내용과 일치합니다. \"Late that afternoon three people came in\"(그날 늦은 오후 세 사람이 들어왔다)와 때 · 사람 수가 같습니다.", 1)], 'te')

# 7번째: 45번 「including Do-yun」(도윤이 앉아 있던 듯 읽힘 — 뒤의 「양보할 자리를 마련하려고 한 정거장 일찍」과 부딪힘)을 43번 문장으로 맞춤
R('45', '5', 7, 'text', [('Nobody offered a seat, including Do-yun, who was fifteen and looked at his phone.',
                          'Nobody from the terminal offered a seat, and Do-yun, who was fifteen and standing too, looked at his phone.', 1)])
R('45', '5', 7, 'ko', [('아무도 자리를 양보하지 않았는데, 휴대폰을 보고 있던 열다섯 살 도윤이도 마찬가지였다.',
                        '종점부터 타고 온 사람들은 아무도 자리를 양보하지 않았고, 열다섯 살로 역시 서 있던 도윤이는 휴대폰을 보았다.', 1)], 'te')
R('45', '5', 7, 'walk', [('"Nobody offered a seat, including Do-yun"(아무도 자리를 양보하지 않았고 도윤도 그랬다)과',
                          '"Do-yun, who was fifteen and standing too, looked at his phone"(열다섯 살로 역시 서 있던 도윤은 휴대폰을 보았다)과', 1)], 'te')

# 45번 L5 19번째 ⑤: 글은 「지호의 어머니가 9월부터 덧붙였다」뿐 → 보기를 글 그대로
R('45', '5', 19, 'choices', [('9월부터 지호의 키를 적기 시작했다', '9월부터 지호의 어머니가 표시를 보탰다', 1)])
R('45', '5', 19, 'walk', [
    ("▸ ⑤번 '9월부터 지호의 키를 적기 시작했다'", "▸ ⑤번 '9월부터 지호의 어머니가 표시를 보탰다'", 1),
    ('it은 키를 잰 자국이고, 마지막 표시보다 아래에서 시작했다는 것은 새로 이사 온 지호의 키를 잰다는 뜻이므로 보기와 같은 내용입니다.',
     'it은 키를 잰 자국이고, 9월부터 그 자국에 표시를 보탠 사람은 지호의 어머니이므로 보기와 같은 내용입니다.', 1),
], 'te')
R('45', '5', 19, 'cn', [("'9월부터 지호의 키를 적기 시작했다' — 본문 내용과 일치합니다. 마지막 문장의 \"Ji-ho's mother began adding to it in September\"(지호의 어머니는 9월에 거기에 덧붙이기 시작했다)가 근거입니다. 어머니가 덧붙인 것은 키를 잰 자국이고, 지난 아이의 마지막 표시 아래에서 시작했으니 지호의 키를 잰 것입니다.",
                         "'9월부터 지호의 어머니가 표시를 보탰다' — 본문 내용과 일치합니다. 마지막 문장의 \"Ji-ho's mother began adding to it in September\"(지호의 어머니는 9월에 거기에 덧붙이기 시작했다)가 근거입니다. 어머니가 덧붙인 것은 키를 잰 자국의 표시입니다.", 1)], 'te')

# ───────── ② 44번 L1 「하」 넷(643번 표) ─────────
R('44', '1', 28, 'text', [('over the door of (e)her own house.', 'over (e)her own bedroom door.', 1)])
R('44', '1', 28, 'ko', [('(e)그녀 자신의 집 문 위에 걸었다', '(e)그녀 자신의 침실 문 위에 걸었다', 1)], 'te')
R('44', '1', 28, 'walk', [('over the door of her own house.', 'over her own bedroom door.', 1),
                          ('그녀 자신의 집 문 위에 걸었다', '그녀 자신의 침실 문 위에 걸었다', 1)], 'te')
R('44', '1', 28, 'cn', [('over the door of her own house.', 'over her own bedroom door.', 1),
                        ('그녀 자신의 집 문 위에 걸었다', '그녀 자신의 침실 문 위에 걸었다', 1)], 'te')

R('44', '1', 13, 'text', [('around the whole rink again on (e)his', 'around the whole rink for the first time on (e)his', 1)])
R('44', '1', 13, 'ko', [('링크 전체를 다시 돌았다', '링크 전체를 처음으로 돌았다', 1)], 'te')
for f in ('walk', 'cn'):
    R('44', '1', 13, f, [('around the whole rink again on his', 'around the whole rink for the first time on his', 1),
                         ('링크 전체를 다시 돌았다', '링크 전체를 처음으로 돌았다', 1),
                         ('링크를 다시 돈 사람은', '링크 전체를 처음으로 돈 사람은', 1),
                         ('손을 받은 him은 샘이에요', '잭이 손을 내민 상대인 him은 샘이에요', 1)], 'te')

R('44', '1', 21, 'text', [('with (b)his free hand.', 'with (b)his right hand.', 1)])
R('44', '1', 21, 'ko', [('(b)그의 비어 있는 다른 손으로', '(b)그의 오른손으로', 1)], 'te')
for f in ('walk', 'cn'):
    R('44', '1', 21, f, [('with his free hand.', 'with his right hand.', 1),
                         ('그의 비어 있는 다른 손으로', '그의 오른손으로', 1)], 'te')

# ───────── ③ 43 · 44 · 45번 L1 29번째 이름 Kofi(코피) → Max(맥스) ─────────
for t in ('43', '44', '45'):
    a = ALL(t, '1', 29, 'Kofi', 'Max'); b = ALL(t, '1', 29, '코피', '맥스')
    assert a > 0 and b > 0, (t, a, b)
    print(t, 'Kofi→Max', a, '코피→맥스', b)

# 감수 「하」 반영: 44번 L1 29번째 「소풍」 → 43 · 45번과 같은 「여행」 · 43 · 45번 L5 8번째 「강씨」 띄어 씀
assert ALL('44', '1', 29, '소풍', '여행') == 1
for t in ('43', '45'):
    R(t, '5', 8, 'ko', [('강씨는', '강 씨는', 1)], 'te')

for k, v in ans_before.items():
    assert [q['answer'] for q in tb[k[0]][k[1]]] == v, k
lib.save(s, tb, te, path)
print('ok — 정답 번호 그대로')
