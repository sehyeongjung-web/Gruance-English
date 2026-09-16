#!/usr/bin/env python3
"""
25번 도표 문항 — 진술의 참·거짓 계산기

도표 문항은 "도표와 어긋나는 진술이 정확히 하나"여야 한다.
사람이 눈으로 세면 반드시 틀린다. 실제로 기존 문항의 절반 이상이
어긋난 진술을 2~4개 갖고 있었고, 정답이 참인 진술을 가리키는 경우도 있었다.

따라서 진술을 쓸 때 그 참·거짓을 수식으로 함께 정의하고,
이 파일의 ev()로 계산해 확인한 뒤에만 문항으로 조립한다.

명세 형식:
{
 "field": "재생에너지",
 "header": "The graph below shows ...",
 "labels": ["2015","2024"],
 "data": {"Denmark":[52,78], "Germany":[30,58]},
 "false_pos": 2,
 "st": [ {"s":"영문 진술", "spec":{...}}, ...5개 ]
}

사용법:
    python3 eval25.py t25_spec.json
    또는  from eval25 import ev, audit
"""

OPS = {'>':  lambda a, b: a > b,
       '<':  lambda a, b: a < b,
       '==': lambda a, b: abs(a - b) < 1e-9}


def ev(sp, D, L):
    """진술 하나의 참·거짓을 계산한다. D=자료, L=열 이름"""
    t = sp['t']
    g = lambda n: D[n]

    # 비교
    if t == 'cmp':
        return OPS[sp['op']](g(sp['a'])[sp['i']], g(sp['b'])[sp['i']])
    if t == 'cmp2':
        return all(OPS[o](g(sp['a'])[k], g(sp['b'])[k]) for k, o in enumerate(sp['ops']))
    if t == 'cmp_all':
        return all(OPS[sp['op']](v[sp['i']], v[sp['j']]) for v in D.values())
    if t == 'cmp_cross':
        return OPS[sp['op']](g(sp['a'])[sp['i']], g(sp['a'])[sp['j']])
    if t == 'cmp_cross_eq':
        return g(sp['a'])[0] == g(sp['a'])[1]
    if t == 'abs':
        return OPS[sp['op']](g(sp['a'])[sp['i']], sp['val'])

    # 변화량
    if t == 'change':
        v = g(sp['a']); return OPS[sp['op']](v[-1] - v[0], sp['val'])
    if t == 'change_all':
        return all(OPS[sp['op']](v[-1] - v[0], 0) for v in D.values())
    if t == 'diff_cmp':
        return OPS[sp['op']](g(sp['a'])[-1] - g(sp['a'])[0],
                             g(sp['b'])[-1] - g(sp['b'])[0])
    if t == 'diff_cmp_abs':
        return OPS[sp['op']](abs(g(sp['a'])[-1] - g(sp['a'])[0]),
                             abs(g(sp['b'])[-1] - g(sp['b'])[0]))
    if t == 'diff_eq':
        return abs((g(sp['a'])[-1] - g(sp['a'])[0]) -
                   (g(sp['b'])[-1] - g(sp['b'])[0])) < 1e-9

    # 배수
    if t == 'ratio':
        v = g(sp['a']); return OPS[sp['op']](v[-1], sp['k'] * v[0])
    if t in ('ratio_cross', 'ratio_cross_pair2'):
        v = g(sp['a']); return OPS[sp['op']](v[sp['i']], sp['k'] * v[sp['j']])
    if t == 'ratio_cross_pair':
        return OPS[sp['op']](g(sp['a'])[sp['i']], sp['k'] * g(sp['b'])[sp['i']])
    if t == 'ratio_cmp':
        return OPS[sp['op']](g(sp['a'])[-1] / g(sp['a'])[0],
                             g(sp['b'])[-1] / g(sp['b'])[0])

    # 격차
    if t == 'gap':
        return OPS[sp['op']](g(sp['a'])[sp['i']] - g(sp['b'])[sp['i']], sp['val'])
    if t == 'gap_abs':
        i = sp['i']; j = sp.get('j', i)
        return OPS[sp['op']](abs(g(sp['a'])[i] - g(sp['b'])[j]), sp['val'])
    if t == 'gap_narrow':
        a, b = g(sp['a']), g(sp['b'])
        return abs(a[-1] - b[-1]) < abs(a[0] - b[0])
    if t == 'gap_rank':
        gaps = {k: abs(v[0] - v[1]) for k, v in D.items()}
        tgt = (max if sp['which'] == 'max' else min)(gaps.values())
        return abs(gaps[sp['a']] - tgt) < 1e-9

    # 순위  (rank = 모든 열에서 / rank_at = 특정 열에서만)
    if t == 'rank':
        n = len(next(iter(D.values())))
        f = max if sp['which'] == 'max' else min
        return all(g(sp['a'])[i] == f(v[i] for v in D.values()) for i in range(n))
    if t == 'rank_at':
        i = sp['i']; f = max if sp['which'] == 'max' else min
        return g(sp['a'])[i] == f(v[i] for v in D.values())
    if t == 'rank_nth':
        vals = sorted(((v[sp['by']], k) for k, v in D.items()), reverse=True)
        return vals[sp['n'] - 1][1] == sp['a']
    if t == 'rank_diff':
        dif = {k: v[-1] - v[0] for k, v in D.items()}
        f = max if sp['which'] == 'max' else min
        return abs(dif[sp['a']] - f(dif.values())) < 1e-9
    if t == 'rank_diff_abs':
        dif = {k: abs(v[-1] - v[0]) for k, v in D.items()}
        f = max if sp['which'] == 'max' else min
        return abs(dif[sp['a']] - f(dif.values())) < 1e-9
    if t == 'rank_pair':
        ok = True
        if 'max_i' in sp: ok &= g(sp['a'])[sp['max_i']] == max(v[sp['max_i']] for v in D.values())
        if 'min_i' in sp: ok &= g(sp['a'])[sp['min_i']] == min(v[sp['min_i']] for v in D.values())
        if 'max_j' in sp: ok &= g(sp['a'])[sp['max_j']] == max(v[sp['max_j']] for v in D.values())
        return ok
    if t == 'rank_pair_year':
        ok = True
        if sp.get('max_year') is not None:
            i = sp['max_year']; ok &= g(sp['a'])[i] == max(v[i] for v in D.values())
        if sp.get('min_year') is not None:
            i = sp['min_year']; ok &= g(sp['a'])[i] == min(v[i] for v in D.values())
        return ok

    # 합계
    if t == 'sum_cmp':
        i = sp['i']
        return OPS[sp['op']](sum(D[x][i] for x in sp['a']), sum(D[x][i] for x in sp['b']))
    if t == 'sum_abs':
        return OPS[sp['op']](sum(D[x][sp['i']] for x in sp['a']), sp['val'])

    # 증감 방향
    if t == 'mono':
        v = g(sp['a'])
        return all(v[k+1] > v[k] for k in range(len(v)-1)) if sp['dir'] == 'up' \
          else all(v[k+1] < v[k] for k in range(len(v)-1))
    if t == 'mono_across':
        seq = [v[sp['i']] for v in D.values()]
        return all(seq[k+1] > seq[k] for k in range(len(seq)-1)) if sp['dir'] == 'up' \
          else all(seq[k+1] < seq[k] for k in range(len(seq)-1))

    raise ValueError('알 수 없는 spec 종류: ' + t)


def audit(spec_list, verbose=True):
    """명세 전체를 검사하고 문제 문항 수를 반환한다."""
    bad = []
    for it in spec_list:
        vals = []
        for st in it['st']:
            try:
                vals.append(ev(st['spec'], it['data'], it['labels']))
            except Exception as e:
                vals.append('ERR: %s' % e)
        f = [k for k, v in enumerate(vals) if v is False]
        err = [v for v in vals if not isinstance(v, bool)]
        if err:
            bad.append((it['field'], '계산 실패', vals))
        elif len(f) != 1:
            bad.append((it['field'], '어긋나는 진술이 %d개 (1개여야 함)' % len(f), vals))
        elif f[0] != it['false_pos']:
            bad.append((it['field'], '오답 위치 불일치: 실제 %d, 명세 %d' % (f[0], it['false_pos']), vals))
    if verbose:
        if bad:
            print('[오류] %d문항' % len(bad))
            for fld, msg, vals in bad:
                print('  X %s — %s  %s' % (fld, msg, vals))
        else:
            print('전 문항 통과 — 어긋나는 진술이 정확히 1개이고 위치가 명세와 일치')
    return len(bad)


if __name__ == '__main__':
    import json, sys
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    sys.exit(1 if audit(json.load(open(sys.argv[1], encoding='utf-8'))) else 0)
