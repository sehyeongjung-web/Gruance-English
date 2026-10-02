#!/bin/bash
# 그루앙스 작업 도구 설치 — 새 방을 열었을 때 한 번 실행
#   git clone https://github.com/sehyeongjung-web/Gruance-English.git /home/claude/Gruance-English
#   unzip -o /home/claude/Gruance-English/gruance_tools.zip -d /home/claude/work
#   bash /home/claude/work/setup.sh
set -e
REPO=/home/claude/Gruance-English
WORK=/home/claude/work
[ -d "$REPO/.git" ] || git clone -q https://github.com/sehyeongjung-web/Gruance-English.git "$REPO"
cd "$REPO" && git fetch -q && git reset -q --hard origin/main
mkdir -p "$WORK/out" && cd "$WORK"
cp "$REPO/index.html" out/index.html
cp "$REPO/그루앙스_작업인계문서.md" out/
cp "$REPO/verify_explain.py" out/
echo "GitHub 최신 커밋: $(git -C "$REPO" log -1 --format='%h %ci')"
echo "index.html: $(wc -c < "$REPO/index.html")바이트"
echo "인계문서 마지막 항목: $(grep '^## [0-9]*\.' "$REPO/그루앙스_작업인계문서.md" | tail -1 | cut -c1-60)"
python3 "$REPO/verify.py" "$REPO/index.html" | grep -E '^전체|검증' || true
python3 "$REPO/verify_explain.py" "$REPO/index.html" | tail -1
echo "도구 준비 끝: $WORK (README.md 참고)"
