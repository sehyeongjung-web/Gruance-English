# 누적본 만들기: 수정안 적용 → 해설의 기계적 결함 고치기
import sys, re; sys.path.insert(0,'.')
from lib import *
import apply as A
DUP_CELLS=[('20','6'),('20','5'),('22','5')]   # 해설에 '정답입니다'가 두 번 들어간 칸(148번에서 발견)
def fix_dup(path):
    s,tb,te=load(path); n=0
    for t,lv in DUP_CELLS:
        for e in te[t][lv]:
            for k,c in enumerate(e['cn']):
                if c.count('정답입니다')>=2:
                    new=re.sub(r"^(정답입니다\. '.*?') 정답입니다\. ", r"\1 ", c, count=1)
                    assert new!=c and new.count('정답입니다')==1, c
                    e['cn'][k]=new; n+=1
    save(s,tb,te,path); return n
if __name__=='__main__':
    mods=sys.argv[1].split(','); out=sys.argv[2]
    A.apply(mods,out=out)
    print('해설 「정답입니다」 중복 고침:', fix_dup(out))
