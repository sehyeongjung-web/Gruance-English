# 올리기 전 안전 검사 — 다른 방이 올린 것을 지우지 않는지 GitHub 최신본과 견준다 (2026-10-20, 인계문서 376번)
# 쓰는 법:  git fetch origin main  →  python3 guard.py --allow 23:7-9 [--index index.html] [--zip gruance_tools.zip] [--doc 그루앙스_작업인계문서.md]
#   --allow  이 방이 맡은 칸. 「유형:레벨」을 쉼표로. 레벨은 7-9처럼 범위도 됨. 예) --allow 23:7-9,35:9
#   --app    앱 코드(두 상수 밖)를 일부러 고친 경우에만 붙인다.
# 통과하면 「올려도 됩니다」, 아니면 무엇이 걸렸는지 말하고 멈춘다(끝 코드 1).
import sys, os, json, subprocess, zipfile, io, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import span

REPO = os.path.dirname(os.path.abspath(__file__))

def git_show(path):
    return subprocess.run(['git', '-C', REPO, 'show', 'origin/main:' + path], capture_output=True, check=True).stdout

def parse(s):
    a, b = span(s, 'const TYPE_BANK ='); c, d = span(s, 'const TYPE_EXPLAIN =')
    rest = s[:min(a, c)] + s[min(b, d):max(a, c)] + s[max(b, d):]
    return json.loads(s[a:b]), json.loads(s[c:d]), rest

def allowed(spec):
    out = set()
    for part in filter(None, (spec or '').split(',')):
        t, lv = part.strip().split(':')
        if '-' in lv:
            x, y = lv.split('-'); out |= {(t, str(k)) for k in range(int(x), int(y) + 1)}
        else:
            out.add((t, lv))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--allow', required=True); ap.add_argument('--index', default=os.path.join(REPO, 'index.html'))
    ap.add_argument('--zip', default=os.path.join(REPO, 'gruance_tools.zip'))
    ap.add_argument('--doc', default=os.path.join(REPO, '그루앙스_작업인계문서.md'))
    ap.add_argument('--app', action='store_true')
    o = ap.parse_args(); ok = True; ALLOW = allowed(o.allow)
    head = subprocess.run(['git', '-C', REPO, 'rev-parse', '--short', 'origin/main'], capture_output=True, text=True).stdout.strip()
    print('견주는 바탕: GitHub 최신본 origin/main = %s  (먼저 git fetch origin main 을 했는지 확인)' % head)

    # 1) 문항 · 해설: 맡은 칸 밖은 한 글자도 바뀌면 안 된다
    bt, be, brest = parse(git_show('index.html').decode('utf-8'))
    nt, ne, nrest = parse(open(o.index, encoding='utf-8').read())
    changed = {}
    for t in sorted(set(bt) | set(nt)):
        for lv in sorted(set(bt.get(t, {})) | set(nt.get(t, {})), key=lambda x: int(x) if x.isdigit() else 0):
            b1, n1 = bt.get(t, {}).get(lv), nt.get(t, {}).get(lv)
            b2, n2 = be.get(t, {}).get(lv), ne.get(t, {}).get(lv)
            if b1 == n1 and b2 == n2: continue
            k = 0
            for i in range(max(len(b1 or []), len(n1 or []), len(b2 or []), len(n2 or []))):
                g = lambda L: L[i] if L and i < len(L) else None
                if g(b1) != g(n1) or g(b2) != g(n2): k += 1
            changed[(t, lv)] = k
    inside = {c: k for c, k in changed.items() if c in ALLOW}
    outside = {c: k for c, k in changed.items() if c not in ALLOW}
    print('① 바뀐 칸(맡은 칸 안): ' + (', '.join('%s번 L%s %d문항' % (t, lv, k) for (t, lv), k in inside.items()) or '없음'))
    if outside:
        ok = False
        print('   ✗ 맡은 칸 밖이 바뀜: ' + ', '.join('%s번 L%s %d문항' % (t, lv, k) for (t, lv), k in outside.items()))
        print('     → 다른 방이 올린 것을 옛 파일로 덮어쓰고 있을 수 있습니다. 파일을 복사하지 말고, 최신본에 자기 편집(build.py)을 다시 돌리세요.')
    if brest != nrest:
        if o.app: print('② 앱 코드(두 상수 밖): 바뀜 — --app 로 허락함')
        else: ok = False; print('② ✗ 앱 코드(두 상수 밖)가 GitHub 최신본과 다릅니다(일부러 고친 것이 아니면 옛 파일입니다).')
    else: print('② 앱 코드(두 상수 밖): 최신본과 같음')

    # 2) 도구 묶음: 최신본 zip에 있던 파일이 하나도 빠지면 안 되고, 공용 문서는 줄이 지워지면 알린다
    if os.path.exists(o.zip):
        bz = zipfile.ZipFile(io.BytesIO(git_show('gruance_tools.zip'))); nz = zipfile.ZipFile(o.zip)
        bn, nn = set(bz.namelist()), set(nz.namelist())
        lost = sorted(bn - nn); added = sorted(nn - bn)
        edited = sorted(n for n in bn & nn if bz.read(n) != nz.read(n))
        if lost: ok = False; print('③ ✗ 도구 묶음에서 최신본에 있던 파일 %d개가 빠짐: %s' % (len(lost), lost[:8]))
        else: print('③ 도구 묶음: 최신본 파일 모두 있음 · 새 파일 %d개 · 고친 파일 %d개 %s' % (len(added), len(edited), edited[:8]))
        for n in edited:
            if n.endswith(('.md', '.txt')):
                bl = bz.read(n).decode('utf-8', 'replace').splitlines(); nl = set(nz.read(n).decode('utf-8', 'replace').splitlines())
                gone = [x for x in bl if x.strip() and x not in nl]
                if gone: print('   ! %s: 최신본의 줄 %d개가 바뀌거나 지워짐(일부러 고친 것인지 확인) — 예: %s' % (n, len(gone), gone[0][:80]))
            elif n.endswith('.py') and n not in added:
                print('   ! %s: 최신본에 있던 도구를 고침 — 다른 방이 쓰는 도구면 이름을 바꿔 새로 넣으세요' % n)

    # 3) 인계문서: 최신본 끝에 덧붙이기만
    if os.path.exists(o.doc):
        bd = git_show('그루앙스_작업인계문서.md').decode('utf-8'); nd = open(o.doc, encoding='utf-8').read()
        if nd.startswith(bd.rstrip('\n')):
            import re
            last = max([int(x) for x in re.findall(r'^## (\d+)\.', bd, re.M)] or [0])
            new = [int(x) for x in re.findall(r'^## (\d+)\.', nd[len(bd.rstrip()):], re.M)]
            if new and min(new) != last + 1: ok = False; print('④ ✗ 인계문서 새 번호 %s — 최신본 마지막이 %d번이니 %d번부터 쓰세요' % (new, last, last + 1))
            else: print('④ 인계문서: 최신본 끝에 덧붙임만 (최신본 마지막 %d번 · 새 번호 %s)' % (last, new or '없음'))
        else: ok = False; print('④ ✗ 인계문서가 최신본 끝에 덧붙인 꼴이 아닙니다(옛 문서를 덮어썼거나 앞부분을 고침).')

    print('→ 올려도 됩니다.' if ok else '→ 멈춤: 위 ✗를 고친 뒤 다시 돌리세요.')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
