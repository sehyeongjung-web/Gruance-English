#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""누적본(out/index.html)을 GitHub 최신 파일과 견주어 한 번에 점검한다.

쓰는 법:  cd /home/claude/work && python3 check_all.py            (기본: out/index.html)
          python3 check_all.py out/index.html

보는 것
  1. 앱 코드(두 상수 TYPE_BANK·TYPE_EXPLAIN 밖)가 한 글자도 바뀌지 않았는가
  2. 정답 번호·발문·정답 문구·지문·선택지·해설·풀이·해석·correctWord가 몇 문항 바뀌었는가(칸별)
  3. node --check (자바스크립트 문법)
  4. verify.py (형식·길이 점검표) — 경고 목록이 바탕 파일과 같은가
  5. verify_explain.py (선택지-해설 대조)
"""
import sys, re, collections, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
REPO = '/home/claude/Gruance-English'

def outside(s):
    a, b = span(s, 'const TYPE_BANK ='); c, d = span(s, 'const TYPE_EXPLAIN =')
    return s[:c] + '§' + s[d:a] + '§' + s[b:]

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'out/index.html'
    s0, tb0, te0 = load(); s1, tb1, te1 = load(out)
    print('① 앱 코드(두 상수 밖) 동일:', outside(s0) == outside(s1))
    chg = collections.Counter(); alarm = []
    for t in tb0:
        for lv in tb0[t]:
            for n, (a, b) in enumerate(zip(tb0[t][lv], tb1[t][lv])):
                cell = '%s번 L%s' % (t, lv)
                if a['answer'] != b['answer']: alarm.append('정답 번호 변동 %s %d번째' % (cell, n + 1))
                if a.get('q') != b.get('q'): alarm.append('발문 변동 %s %d번째' % (cell, n + 1))
                if a['text'] != b['text']: chg['지문 ' + cell] += 1
                if a['choices'] != b['choices']: chg['선택지 ' + cell] += 1
                if a['choices'][a['answer']] != b['choices'][b['answer']]: chg['정답 문구 ' + cell] += 1
                if a.get('correctWord') != b.get('correctWord'): chg['correctWord ' + cell] += 1
                ea, eb = te0[t][lv][n], te1[t][lv][n]
                for f, name in (('cn', '해설'), ('walk', '풀이'), ('ko', '해석')):
                    if ea[f] != eb[f]: chg[name + ' ' + cell] += 1
    print('② 바탕(GitHub) 대비 바뀐 문항 수:')
    for k in sorted(chg): print('     %-22s %d' % (k, chg[k]))
    if not chg: print('     (없음)')
    print('   정답 번호·발문 변동:', alarm if alarm else '0건')
    print('   중복 선택지:', sum(len(set(it['choices'])) != 5 for t in tb1 for lv in tb1[t] for it in tb1[t][lv]), '/ MAINTENANCE_MODE = false:', 'MAINTENANCE_MODE = false' in s1)
    blocks = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', s1, re.S)
    open('/tmp/check.js', 'w', encoding='utf-8').write('\n;\n'.join(blocks))
    r = subprocess.run(['node', '--check', '/tmp/check.js'], capture_output=True, text=True)
    print('③ node --check:', '통과' if r.returncode == 0 else '실패\n' + r.stderr[:400])
    def verify(path):
        r = subprocess.run([sys.executable, REPO + '/verify.py', path], capture_output=True, text=True)
        return r.stdout
    va, vb = verify(REPO + '/index.html'), verify(out)
    wa = [l for l in va.splitlines() if l.strip().startswith('!')]; wb = [l for l in vb.splitlines() if l.strip().startswith('!')]
    print('④ verify.py:', [l for l in vb.splitlines() if l.startswith('전체') or '검증' in l])
    print('   경고 %d건 → %d건 / 새로 생긴 경고 %s / 사라진 경고 %s' % (len(wa), len(wb), [x.strip() for x in wb if x not in wa], [x.strip() for x in wa if x not in wb]))
    r = subprocess.run([sys.executable, REPO + '/verify_explain.py', out], capture_output=True, text=True)
    print('⑤ verify_explain.py:', r.stdout.strip().splitlines()[-1])
    print('파일 크기: %s바이트' % format(os.path.getsize(out), ','))

if __name__ == '__main__':
    main()
