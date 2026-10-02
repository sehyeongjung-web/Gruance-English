# 그루앙스 AI 수능영어코치 — 작업 도구 묶음

문항(index.html 안의 `TYPE_BANK`·`TYPE_EXPLAIN` 두 상수)을 고칠 때 쓰는 도구입니다.
방이 바뀌면 작업 폴더가 사라지므로, 이 묶음을 GitHub에 올려 두고 새 방에서 풀어 씁니다.

## 새 방에서 시작하는 법

```bash
git clone https://github.com/sehyeongjung-web/Gruance-English.git /home/claude/Gruance-English
unzip -o /home/claude/Gruance-English/gruance_tools.zip -d /home/claude/work
bash /home/claude/work/setup.sh
```

`setup.sh`가 저장소를 최신으로 맞추고, `out/`에 index.html·인계문서를 복사하고, 두 검증 도구를 돌려 현재 상태를 보여 줍니다.
그다음 **인계문서의 마지막 항목**을 읽고 이어서 작업합니다.

## 폴더 구조

| 자리 | 내용 |
|---|---|
| `/home/claude/Gruance-English/` | GitHub 복사본(바탕). 직접 고치지 않음 |
| `/home/claude/work/` | 이 도구들과 수정안 파일(`edits_*.py`) |
| `/home/claude/work/out/` | 만들어진 누적본(index.html)과 인계문서 |
| `/mnt/user-data/outputs/` | 선생님께 전달하는 파일 |

## 도구

| 파일 | 하는 일 |
|---|---|
| `lib.py` | index.html에서 두 상수를 읽고(`load`) 다시 써넣음(`save`). `span`은 상수의 범위 |
| `apply.py` | 수정안 파일을 바탕 파일에 적용. 정답·지문을 건드리면 멈춤(승인 표시가 있어야 통과) |
| `build.py` | **누적본 만들기**: `python3 build.py edits_A,edits_B out/index.html` — 바탕(GitHub) 위에 수정안들을 차례로 적용 |
| `check_all.py` | **한 번에 점검**: 앱 코드 불변, 바뀐 문항 수, node --check, verify.py, verify_explain.py |
| `dump.py` | 문항 읽기: `python3 dump.py 24 3 200 all 60` (유형, 레벨, 지문 길이, all=전체, 해설 길이) |
| `qcheck.py` | 길이 작업용 인용 대조(레벨별): `python3 qcheck.py out/index.html 3` |
| `examples/` | 실제로 쓴 수정안 파일 4개(형식 참고용) |

`verify.py`(형식·길이 점검표)와 `verify_explain.py`(선택지-해설 대조)는 저장소에 있는 것을 씁니다.

## 표준 절차

1. `git fetch`로 GitHub 최신 커밋을 확인한다. 지난번 파일이 올라갔으면 바탕을 그 커밋으로 옮긴다(`git reset --hard origin/main`). 안 올라갔으면 지난 수정안 파일들을 계속 함께 적용한다.
2. 고칠 칸을 **전부 읽는다**(`dump.py` 또는 직접 출력). 범위가 예상과 다르면 먼저 선생님께 말씀드린다.
3. 수정안 파일 `edits_이름.py`를 쓴다(아래 형식).
4. `python3 build.py (아직 안 올라간 수정안들),edits_이름 out/index.html`
5. `python3 check_all.py` — 다섯 항목이 모두 깨끗해야 한다.
6. 인계문서(`out/그루앙스_작업인계문서.md`) 끝에 새 번호 항목을 덧붙인다.
7. `out/index.html`과 인계문서를 `/mnt/user-data/outputs/`로 복사해 전달한다.

## 수정안 파일 형식

```python
AUTO_SYNC = True      # 해설이 선택지를 글자 그대로 인용한 곳을 함께 바꿈 (주의: 아래 '교훈' 참고)
E = {}
# 열쇠는 (유형, 레벨, 문항 번호) — 문항 번호는 0부터 센다(1번째 문항 = 0)
E[('24','3',5)] = {
    'ch': {1: '새 선택지', 3: '새 선택지'},          # 선택지 바꾸기(0~4 자리). 정답 자리는 'ans_ok': True가 있어야 함
    'kp': {1: '새 한글 해석'},                        # 해설의 "'영어' (한글 해석) — 설명"에서 괄호 속 해석
    'kq': {3: '새 한글 해석'},                        # 해설 맨 앞 따옴표 속 한글 해석 통째로
    'cn': {1: ('옛 조각', '새 조각'),                 # 해설의 한 조각 바꾸기(튜플 또는 튜플 목록)
           3: '해설 전체를 이 글로 바꿈'},            # 문자열이면 통째로 바꿈
    'walk_sub': [('옛 조각', '새 조각')],             # 풀이(walk)의 조각 바꾸기
    'ko': ('옛 조각', '새 조각'),                     # 해석(ko)의 조각 바꾸기
    'cw': 'smiled',                                   # 틀렸을 때 보여 주는 correctWord 바로잡기
    'text': ('옛 조각', '새 조각'), 'passage_ok': True,   # 지문 수정 — 선생님 승인이 있을 때만
}
# 문항을 통째로 새로 쓸 때(승인 필요): 정답 번호는 그대로, correctWord가 있는 문항은 'cw'도 함께
E[('44','3',7)] = {'passage_ok': True, 'ans_ok': True,
    'rewrite': {'text': '...', 'choices': [...5개...], 'ko': '...', 'walk': '...', 'cn': [...5개...]}}
```

## 지켜야 할 규칙

- **정답 번호·발문은 절대 바꾸지 않는다.** 지문과 정답 문구는 선생님 승인이 있을 때만(코드에서 `passage_ok`·`ans_ok`).
- 한 유형에서 10문항 이상 고칠 때, 지문을 고칠 때는 먼저 승인을 받는다.
- 길이 점검표(verify.py)의 다섯 조건 — A 정답이 긴 쪽에 과다(칸마다 정답 1~2위 ≤16문항, 1위 ≤8문항) · B 혼자 튀게 긴 선택지 · C 나머지보다 1.4배 이상 긴 선택지 · D 정답이 긴 쪽에 거의 안 옴(1~2위 ≥5문항) · E 정답만 혼자 짧음. 지금은 144칸 전부 ✅.
- 지문 길이는 칸 평균이 `LEN9 × RATIO`의 ±35% 안이어야 경고가 없다(verify.py 안에 표가 있음).
- 레벨1~3 해설은 "~어요" 말투, 레벨4 이상은 "~입니다" 말투.
- 선생님께 드리는 말은 쉬운 말로, 결론부터, 올릴 파일과 바이트 수를 밝힌다.

## 교훈 (같은 사고를 되풀이하지 않기 위해)

1. **자동 맞춤(AUTO_SYNC)은 해설 안의 '지문 인용'까지 바꿀 수 있다.** 선택지가 지문 문장과 글자까지 같은 칸(45번 레벨1·2)에서 일어났다 → 선택지를 고친 뒤 반드시 `verify_explain.py`를 돌린다(검사 9번이 잡아냄).
2. **정답 문구를 바꾸면 풀이(walk)도 본다.** 풀이가 옛 정답 문구를 인용하고 있으면 `walk_sub`으로 함께 고친다.
3. **correctWord**는 29번·30번 레벨1에만 있다. 문항을 다시 쓰면 함께 바꾼다(`rewrite`가 빠뜨리면 멈춤).
4. 틀 문제(같은 구조의 문항 반복)는 칸 전체를 읽어야 보인다. 견본 몇 개만 보고 범위를 말하지 않는다.
