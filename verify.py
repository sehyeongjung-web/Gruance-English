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
