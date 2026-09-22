#!/usr/bin/env python3
"""
그루앙스 AI 수능영어코치 — 문항 전수 검증
사용법:  python3 verify.py index.html [--level 8] [--type 43]

검증을 통과하지 못하면 종료 코드 1을 반환한다.
문항을 index.html에 적용하기 전에 반드시 통과시킬 것.
"""
import json, re, sys, argparse
from collections import Counter

MARK = ['①', '②', '③', '④', '⑤']
ABC  = ['(a)', '(b)', '(c)', '(d)', '(e)']

# 유형별 지문 길이 기준 (레벨9=수능 실전, 레벨8=80%, 레벨7=64%)
LEN9 = {'18':160,'19':136,'20':124,'21':89,'22':101,'23':112,'24':98,'25':136,
        '26':134,'27_28':139,'29':134,'30':140,'31':104,'32':98,'33':87,'34':90,
        '35':128,'36_37':126,'38_39':136,'40':139,'41':236,'42':266,'43':280,
        '44':257,'45':264}
RATIO = {9:1.00, 8:0.80, 7:0.64, 6:0.52, 5:0.42, 4:0.34, 3:0.27, 2:0.22, 1:0.18}
TOLERANCE = 0.35   # 목표치 대비 허용 오차

# 순서 배열 유형의 수능 표준 선택지 (나열 순서 그대로인 배열은 제외되어야 함)
STD_ORDER = {
    '36_37': ['(A)-(C)-(B)','(B)-(A)-(C)','(B)-(C)-(A)','(C)-(A)-(B)','(C)-(B)-(A)'],
    '43':    ['(B)-(D)-(C)','(C)-(B)-(D)','(C)-(D)-(B)','(D)-(B)-(C)','(D)-(C)-(B)'],
}
TRIVIAL_ORDER = {'36_37': '(A)-(B)-(C)', '43': '(B)-(C)-(D)'}


def load_bank(path):
    c = open(path, encoding='utf-8').read()
    i = c.find('const TYPE_BANK =')
    if i < 0:
        raise SystemExit('TYPE_BANK를 찾을 수 없습니다: ' + path)
    st = c.find('{', i); d = 0; j = st
    while j < len(c):
        if c[j] == '{': d += 1
        elif c[j] == '}':
            d -= 1
            if d == 0: break
        j += 1
    return json.loads(c[st:j+1]), c


def check_set(code, lv, items, errors, warnings):
    tag = '%s번 L%s' % (code, lv)

    # 1) 문항 수 ─ 31개를 쓰고 한 개가 잘려 나가는 사고가 반복되었음
    if len(items) != 30:
        errors.append('%s: 문항 수가 %d개 (30개여야 함)' % (tag, len(items)))
        return

    # 2) 필수 필드
    for n, it in enumerate(items):
        if 'text' not in it or 'choices' not in it or 'answer' not in it:
            errors.append('%s #%d: 필수 필드 누락' % (tag, n))
            return

    # 3) 선택지 5개, 중복 없음
    for n, it in enumerate(items):
        if len(it['choices']) != 5:
            errors.append('%s #%d: 선택지가 %d개' % (tag, n, len(it['choices'])))
        if len(set(it['choices'])) != 5:
            errors.append('%s #%d: 선택지 중복' % (tag, n))
        if not (0 <= it['answer'] < 5):
            errors.append('%s #%d: answer 범위 밖 (%s)' % (tag, n, it['answer']))

    # 4) 정답 위치 균등 ─ 한 번호만 찍어서 풀리면 안 됨
    dist = Counter(it['answer'] for it in items)
    counts = [dist.get(k, 0) for k in range(5)]
    if max(counts) > 9:
        errors.append('%s: 정답 편중 %s (각 6개 권장, 9개 초과는 불가)' % (tag, counts))
    elif counts != [6, 6, 6, 6, 6]:
        warnings.append('%s: 정답 분포 %s (6/6/6/6/6 권장)' % (tag, counts))

    # 5) 위치표시형 ─ ①~⑤ 또는 (a)~(e)가 본문에 각 1회
    ch0 = items[0]['choices']
    if all(x in MARK for x in ch0):
        for n, it in enumerate(items):
            for m in MARK:
                if it['text'].count(m) != 1:
                    errors.append('%s #%d: 본문의 %s 표시가 %d개' % (tag, n, m, it['text'].count(m)))
    if all(x in ABC for x in ch0):
        for n, it in enumerate(items):
            for m in ABC:
                if it['text'].count(m) != 1:
                    errors.append('%s #%d: 본문의 %s 표시가 %d개' % (tag, n, m, it['text'].count(m)))

    # 6) 순서 배열형 ─ 나열 순서 그대로가 정답이면 지문을 읽지 않고 풀 수 있음
    if code in STD_ORDER:
        triv = TRIVIAL_ORDER[code]
        bad = sum(1 for it in items if it['choices'][it['answer']] == triv)
        if bad:
            errors.append('%s: 나열 순서 그대로가 정답인 문항 %d개 (%s)' % (tag, bad, triv))
        off = sum(1 for it in items if sorted(it['choices']) != sorted(STD_ORDER[code]))
        if off:
            warnings.append('%s: 수능 표준 배열이 아닌 선택지를 쓴 문항 %d개' % (tag, off))
        labels = ['(A)','(B)','(C)'] if code == '36_37' else ['(B)','(C)','(D)']
        for n, it in enumerate(items):
            for m in labels:
                if it['text'].count(m) != 1:
                    errors.append('%s #%d: 문단 표시 %s가 %d개' % (tag, n, m, it['text'].count(m)))

    # 7) 빈칸 유형 ─ 빈칸이 정확히 하나
    if any('______' in it['text'] for it in items):
        for n, it in enumerate(items):
            k = it['text'].count('______')
            if k != 1 and not (code == '40' and k == 2):
                errors.append('%s #%d: 빈칸이 %d개' % (tag, n, k))

    # 8) 지문 중복
    dup = len(items) - len(set(it['text'] for it in items))
    if dup:
        errors.append('%s: 지문 중복 %d건' % (tag, dup))

    # 9) 지문 길이 ─ 레벨 간 계단이 뒤집히지 않았는지
    if code in LEN9:
        target = LEN9[code] * RATIO.get(int(lv), 1.0)
        avg = sum(len(it['text'].split()) for it in items) / len(items)
        if abs(avg - target) / target > TOLERANCE:
            warnings.append('%s: 평균 %.0f단어 (목표 약 %.0f단어)' % (tag, avg, target))



# ───────── 레벨테스트(진단) 문항 검사 — 2026-09-21 추가 ─────────
# 배경: shuffleSingle이 q.answer를 무시하고 첫 선택지를 정답으로 채점해,
# 레벨5~9 진단 101문항이 정답·오답이 뒤바뀌어 채점된 사고가 있었다.
def check_diagnostic(c, errors, warns):
    import json as _j, re as _r
    def grab(name):
        i=c.find('const '+name+' ='); st=c.find('{',i); d=0; j=st
        while j<len(c):
            if c[j]=='{': d+=1
            elif c[j]=='}':
                d-=1
                if d==0: break
            j+=1
        return _j.loads(c[st:j+1])
    if 'Number.isInteger(q.answer)' not in c:
        errors.append('진단 채점: shuffleSingle이 q.answer를 따르지 않음 (정답이 첫 자리가 아닌 문항이 오답 처리됨)')
    TAIL=_r.compile(r'(는|은) 점(이|을) .{2,20}(확인된다|드러난다|밝히고 있다)$|이번 결과의 핵심이다$')
    for name in ['REASON_BANK','REASON_CONFIRM','SYNTAX_BANK','SYNTAX_CONFIRM']:
        B=grab(name)
        for lv,items in B.items():
            for n,x in enumerate(items):
                tag='%s L%s #%d'%(name,lv,n)
                ch=x.get('choices',[]); a=x.get('answer',0)
                if len(ch)!=5: errors.append(tag+': 선택지 %d개'%len(ch))
                if len(set(ch))!=len(ch): errors.append(tag+': 선택지 중복')
                if not (isinstance(a,int) and 0<=a<len(ch)): errors.append(tag+': 정답 번호 범위 밖')
                for k,t in enumerate(ch):
                    if TAIL.search(t): errors.append(tag+': %d번 선택지에 길이 늘리기용 꼬리 문구'%(k+1))
    V=grab('VOCAB_BANK')
    for lv,items in V.items():
        for n,(w,s,chs) in enumerate(items):
            opts=[o.strip() for o in _r.split(r'[①②③④⑤]',chs) if o.strip()]
            if len(opts)!=5 or len(set(opts))!=5: errors.append('VOCAB_BANK L%s #%d (%s): 뜻 선택지 형식 오류'%(lv,n,w))

    # ── 길이 단서 검사 (2026-09-22 추가) ──
    # 문제를 읽지 않고 「가장 긴 것」「두 번째로 긴 것」「가장 짧은 것」만 골라도 통과하는 일이 없도록 한다.
    def strat_rate(opts_ans):
        out={}
        for key in ('가장 긴 것','두 번째로 긴 것','가장 짧은 것'):
            tot=0.0
            for o,a in opts_ans:
                L=[len(x) for x in o]; u=sorted(set(L),reverse=True)
                t={'가장 긴 것':u[0],'두 번째로 긴 것':u[1] if len(u)>1 else u[0],'가장 짧은 것':u[-1]}[key]
                cand=[i for i,l in enumerate(L) if l==t]; tot+=(1.0/len(cand) if a in cand else 0)
            out[key]=100*tot/len(opts_ans)
        return out
    def rank_of(o,a): return 1+sum(1 for k,z in enumerate(o) if k!=a and len(z)>len(o[a]))
    for name in ['REASON_CONFIRM','SYNTAX_CONFIRM']:
        B=grab(name)
        for lv,items in B.items():
            for key,r in strat_rate([(x['choices'],x.get('answer',0)) for x in items]).items():
                if r>40: errors.append('%s L%s: 「%s」만 골라도 %.0f%% 정답 (40%% 이하여야 함)'%(name,lv,key,r))
    for name in ['REASON_BANK','SYNTAX_BANK']:
        B=grab(name)
        for lv,items in B.items():
            rk=[rank_of(x['choices'],x.get('answer',0)) for x in items]
            if len(rk)>1 and len(set(rk))==1: errors.append('%s L%s: 첫 시도 문항의 정답 길이 순위가 모두 %d위 (같은 요령으로 항상 통과)'%(name,lv,rk[0]))
    for lv,items in V.items():
        oa=[([o.strip() for o in _r.split(r'[①②③④⑤]',chs) if o.strip()],0) for w,s,chs in items]
        for key,r in strat_rate(oa).items():
            if r>40: errors.append('VOCAB_BANK L%s: 「%s」만 골라도 %.0f%% 정답 (40%% 이하여야 함)'%(lv,key,r))
    if '문항 ${vocabSub+1}/3<' in c:
        errors.append('어휘 진단 화면: 문항 번호가 「/3」으로 표시됨 (VOCAB_TOTAL을 써야 함)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--level', help='특정 레벨만 검사')
    ap.add_argument('--type', help='특정 유형만 검사')
    ap.add_argument('--quiet-warnings', action='store_true')
    a = ap.parse_args()

    tb, raw = load_bank(a.path)
    errors, warnings = [], []

    if len(tb) != 25:
        errors.append('유형 수가 %d개 (25개여야 함)' % len(tb))

    total = 0
    for code in sorted(tb):
        if a.type and code != a.type: continue
        for lv in sorted(tb[code], key=int):
            if a.level and lv != a.level: continue
            items = tb[code][lv]
            total += len(items)
            check_set(code, lv, items, errors, warnings)

    print('검사한 문항 수: %d' % total)
    if not a.quiet_warnings and warnings:
        print('\n[경고] %d건 — 확인 권장' % len(warnings))
        for w in warnings: print('  ! ' + w)
    check_diagnostic(raw, errors, warnings)
    if errors:
        print('\n[오류] %d건 — 적용 불가' % len(errors))
        for e in errors: print('  X ' + e)
        print('\n검증 실패. 위 오류를 고치기 전에 index.html에 적용하지 말 것.')
        sys.exit(1)
    print('\n검증 통과.')
    m = re.search(r'MAINTENANCE_MODE\s*=\s*(\w+)', raw)
    if m: print('MAINTENANCE_MODE = %s' % m.group(1))


if __name__ == '__main__':
    main()
