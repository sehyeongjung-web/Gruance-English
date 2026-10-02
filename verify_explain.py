#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그루앙스 AI 수능영어코치 — 선택지와 해설이 서로 맞는지 기계로 대조하는 도구

쓰는 법:  python3 verify_explain.py index.html
verify.py(문항 형식·길이 점검)와 따로 돌립니다. 걸리는 것이 0이면 "해설 대조 통과"라고 나옵니다.

대조하는 것 (전 유형·전 레벨)
  1. 해설의 '정답' 표시가 정답 번호 자리에 있는가
  2. 선택지를 글자 그대로 인용하는 칸에서, 해설이 지금 선택지 문구를 인용하는가
  3. 해설이 다른 번호의 선택지를 인용하고 있지 않은가
  4. 번호·기호(①~⑤, (a)~(e))로 시작하는 해설이 제자리에 있는가
  5. 순서 유형(36_37·43): 풀이가 결론으로 말하는 순서가 정답 선택지와 같은가
  6. 풀이가 "○번이 정답/일치하지 않습니다"라고 말하는 번호가 정답 번호와 같은가
  7. 일치·불일치 유형(25·26·27_28·45): 오답 해설이 '맞지 않다'고 하거나 정답 해설이 '맞다'고 하지 않는가
  8. 틀렸을 때 보여 주는 '올바른 형태/단어'(correctWord)가 정답 해설에 나오는가
  9. 해설·풀이가 큰따옴표로 옮긴 영어 문장이 지문에 그대로 있는가 (선택지를 고치다 지문 인용까지 바뀌는 사고 방지)
"""
import json, re, sys
from collections import defaultdict, Counter

def span(s, key):
    i = s.find(key); st = s.find('{', i); d = 0; j = st; instr = False; esc = False
    while j < len(s):
        ch = s[j]
        if instr:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': instr = False
        else:
            if ch == '"': instr = True
            elif ch == '{': d += 1
            elif ch == '}':
                d -= 1
                if d == 0: break
        j += 1
    return st, j + 1

def load(path):
    s = open(path, encoding='utf-8').read()
    a, b = span(s, 'const TYPE_BANK ='); tb = json.loads(s[a:b])
    c, d = span(s, 'const TYPE_EXPLAIN ='); te = json.loads(s[c:d])
    return tb, te

CIRC = '①②③④⑤'
LET = ['(a)', '(b)', '(c)', '(d)', '(e)']
POS = re.compile(r'정답(이에요|입니다|이야)|번이 정답|\)가 정답')
NEG = re.compile(r'정답이 아니|정답은 아니|정답이 될 수 없')

def _norm(x):
    return re.sub(r'\s+', ' ', re.sub(r'[①②③④⑤]|\([a-e]\)|\([A-D]\)|<[^>]+>', '', x)).strip()

def bad_quotes(passage, texts):
    P = _norm(passage); out = []
    for txt in texts:
        for q in re.findall(r'"([^"\n]{12,})"', txt):
            if not re.search(r'[A-Za-z]{3,} [A-Za-z]{2,} [A-Za-z]{2,}', q) or re.search(r'[가-힣]', q):
                continue
            if '…' in q or '...' in q:
                parts = [p.strip().rstrip('.') for p in re.split(r'…|\.\.\.', _norm(q)) if p.strip()]
                if not all(p.lower() in P.lower() for p in parts): out.append(q)
            elif q.endswith('.'):
                if _norm(q) not in P: out.append(q)
            elif _norm(q).lower().rstrip(',') not in P.lower():
                out.append(q)
    return out

def check(tb, te):
    F = defaultdict(list)
    for t in tb:
        for lv in sorted(tb[t]):
            items = tb[t][lv]; exs = te[t][lv]
            textual = not all(c in CIRC or c in LET for c in items[0]['choices'])
            # 이 칸이 선택지를 그대로 인용하는 형식인지(오답 해설 / 정답 해설 따로)
            q = {'ans': [0, 0], 'non': [0, 0]}
            for n, it in enumerate(items):
                for k, c in enumerate(it['choices']):
                    g = 'ans' if k == it['answer'] else 'non'
                    q[g][1] += 1; q[g][0] += (c in exs[n]['cn'][k])
            quoted = {g: textual and v[1] and v[0] / v[1] >= 0.8 for g, v in q.items()}
            for n, it in enumerate(items):
                ex = exs[n]; cn = ex['cn']; a = it['answer']; ch = it['choices']; walk = str(ex.get('walk', ''))
                where = '%s번 레벨%s %d번째' % (t, lv, n + 1)
                if len(cn) != 5 or len(ch) != 5:
                    F['선택지·해설 개수'].append(where); continue
                marks = [k for k, c in enumerate(cn) if POS.search(c) and not NEG.search(c)]
                if marks and marks != [a]:
                    F['1 정답 표시 위치'].append('%s: 정답 %s, 표시된 자리 %s' % (where, CIRC[a], ''.join(CIRC[k] for k in marks)))
                if textual and t not in ('36_37', '43'):
                    for k, c in enumerate(ch):
                        g = 'ans' if k == a else 'non'
                        if quoted[g] and c not in cn[k]:
                            F['2 인용 불일치'].append('%s %s: 선택지 "%s" / 해설 "%s…"' % (where, CIRC[k], c, cn[k][:40]))
                        for j, cj in enumerate(ch):
                            if j != k and len(cj) >= 6 and cj in cn[k] and c not in cn[k]:
                                F['3 다른 선택지 인용'].append('%s %s: 해설이 %s의 문구를 인용' % (where, CIRC[k], CIRC[j]))
                labs = list(CIRC) if ch[0] in CIRC else (LET if ch[0] in LET else None)
                if labs:
                    for k in range(5):
                        first = None
                        for x in labs:
                            i = cn[k].find(x)
                            if i != -1 and i < 12 and (first is None or i < first[1]): first = (x, i)
                        if first and first[0] != labs[k]:
                            F['4 번호·기호 어긋남'].append('%s %s: 해설이 %s로 시작' % (where, labs[k], first[0]))
                if t in ('36_37', '43'):
                    seqs = re.findall(r'\([A-D]\)\s*[-–→]\s*\([A-D]\)\s*[-–→]\s*\([A-D]\)', walk + ' ' + cn[a])
                    norm = [re.sub(r'\s*[-–→]\s*', '-', x) for x in seqs]
                    if norm and ch[a] not in norm:
                        F['5 순서 결론'].append('%s: 정답 %s, 풀이 %s' % (where, ch[a], norm[-1]))
                else:
                    if ch[0] in LET:
                        said = ['(' + x + ')' for x in re.findall(r'\(([a-e])\)(?:가|이)? ?(?:정답|문맥에 맞지|문맥과 어긋)', walk)]
                        lab = LET[a]
                    else:
                        said = re.findall(r'([①②③④⑤])번?(?:이|가)? ?(?:정답|답입니다|답이에요|어법상 틀|문맥과 반대|문맥에 맞지|도표와 일치하지|일치하지 않|들어갈 자리)', walk)
                        said += re.findall(r'정답은 ([①②③④⑤])', walk)
                        lab = CIRC[a]
                    if said and lab not in said:
                        F['6 풀이의 정답 번호'].append('%s: 정답 %s, 풀이가 말한 번호 %s' % (where, lab, ''.join(said)))
                if t in ('25', '26', '27_28', '45'):
                    for k in range(5):
                        if k != a and re.search(r'(본문|안내문|도표|표)(과|와|의 내용과)? ?(맞지 않|일치하지 않)', cn[k]):
                            F['7 일치 방향'].append('%s %s: 오답 해설이 "맞지 않다"고 함' % (where, CIRC[k]))
                    if re.search(r'(본문|안내문|도표|표)(과|와) (맞아요|일치합니다|일치해요)', cn[a]) and not re.search(r'맞지 않|일치하지 않|어긋|틀렸|틀립|다릅니다|달라요', cn[a]):
                        F['7 일치 방향'].append('%s: 정답 해설이 "맞다"고 함' % where)
                for q in bad_quotes(it['text'], list(cn) + [walk]):
                    F['9 지문 인용'].append('%s: 해설·풀이가 옮긴 "%s"가 지문에 그대로 없음' % (where, q))
                cw = it.get('correctWord')
                if cw and str(cw).lower() not in cn[a].lower():
                    F['8 correctWord'].append('%s: 화면에 보여 주는 말 "%s"가 정답 해설에 없음 — "%s…"' % (where, cw, cn[a][:50]))
    return F

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
    tb, te = load(path)
    F = check(tb, te)
    n_items = sum(len(tb[t][lv]) for t in tb for lv in tb[t])
    print('대조한 문항: %d개 (%d개 유형)' % (n_items, len(tb)))
    total = 0
    for name in sorted(F):
        v = F[name]; total += len(v)
        print('\n[%s] %d건' % (name, len(v)))
        for line in v[:15]: print('  -', line)
        if len(v) > 15: print('  … 외 %d건' % (len(v) - 15))
    print()
    print('해설 대조 통과.' if total == 0 else '해설 대조에서 %d건이 걸렸습니다.' % total)
    return 0 if total == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
