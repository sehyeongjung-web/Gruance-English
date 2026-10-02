import re
import sys, copy, importlib; sys.path.insert(0,'.')
from lib import *
def rank(ch,k): 
    L=len(ch[k]); return 1+sum(len(x)>L for i,x in enumerate(ch) if i!=k)
def gap(ch):
    ls=[len(c) for c in ch]; i=max(range(5),key=lambda k:ls[k]); o=[ls[k] for k in range(5) if k!=i]
    return ls[i]-statistics.median(o)
def flagged(ch):
    r,i=ratio(ch); return r>=1.4 and gap(ch)>=5
def cellA(items):
    a=a1=0
    for it in items:
        r=rank(it['choices'],it['answer']); a+=(r<=2); a1+=(r==1)
    return a,a1
AUTO=[0]
def apply(mods, src=SRC, out=None, verbose=True):
    s,tb,te=load(src); tb0=copy.deepcopy(tb)
    nq=nc=0; bad=[]
    for modname in mods:
        M=importlib.import_module(modname); E=M.E; autosync=getattr(M,'AUTO_SYNC',False)
        for (t,lv,n),ed in E.items():
            it=tb[t][lv][n]; ex=te[t][lv][n]; old=list(it['choices'])
            # rewrite: 문항을 통째로 새로 씀(지문·선택지·해석·풀이·해설). 정답 번호는 그대로. 선생님 승인이 있을 때만.
            if 'rewrite' in ed:
                assert ed.get('passage_ok') and ed.get('ans_ok'), ('문항 재작성은 승인 필요',t,lv,n)
                R=ed['rewrite']; assert len(R['choices'])==5==len(set(R['choices']))==len(R['cn'])
                it['text']=R['text']; it['choices']=list(R['choices']); ex['ko']=R['ko']; ex['walk']=R['walk']; ex['cn']=list(R['cn'])
                if 'cw' in R:   # 틀렸을 때 보여 주는 '올바른 형태/단어'도 새 문항에 맞춤
                    assert it.get('correctWord'), ('correctWord가 없는 문항',t,lv,n); it['correctWord']=R['cw']
                else: assert not it.get('correctWord'), ('correctWord를 함께 바꿔야 함',t,lv,n)
                old=list(it['choices']); nc+=5
            if 'text' in ed:   # 지문 수정은 선생님 승인이 있을 때만(passage_ok)
                assert ed.get('passage_ok'), ('지문 수정은 승인 필요',t,lv,n)
                x,y=ed['text']; assert it['text'].count(x)==1; it['text']=it['text'].replace(x,y)
            if 'ko' in ed:
                x,y=ed['ko']; assert ex['ko'].count(x)==1; ex['ko']=ex['ko'].replace(x,y)
            if 'walk' in ed: ex['walk']=ed['walk']
            # walk_sub: 풀이(walk) 안의 조각 바꾸기 [(옛, 새), ...] — 옛 문구는 반드시 있어야 함
            for x,y in ed.get('walk_sub',[]):
                assert x in ex['walk'], ('풀이에 그 문구가 없음',t,lv,n,x)
                ex['walk']=ex['walk'].replace(x,y)
            # cw: 틀렸을 때 보여 주는 '올바른 형태/단어'(correctWord) 바로잡기 — 그 칸이 원래 있는 문항만
            if 'cw' in ed:
                assert it.get('correctWord'), ('correctWord가 없는 문항',t,lv,n)
                it['correctWord']=ed['cw']
            for k,new in ed.get('ch',{}).items():
                assert k!=it['answer'] or ed.get('ans_ok'), ('정답 수정 금지',t,lv,n,k)
                assert new!=it['choices'][k], ('변화 없음',t,lv,n,k)
                assert new not in it['choices'], ('중복 선택지',t,lv,n,k)
                it['choices'][k]=new; nc+=1
            # 해설이 선택지를 글자 그대로 인용한 경우에는 인용도 함께 바꿈(자동)
            for k in (ed.get('ch',{}) if autosync else {}):
                if old[k] in ex['cn'][k] and not (isinstance(ed.get('cn',{}).get(k),str)):
                    ex['cn'][k]=ex['cn'][k].replace(old[k], it['choices'][k]); AUTO[0]+=1
            # kq: 해설 맨 앞의 따옴표 속 한글 해석을 통째로 바꿈 / kp: 영어 인용 뒤 첫 괄호 속 한글 해석을 바꿈
            for k,v in ed.get('kq',{}).items():
                assert re.match(r"^'[^']*'", ex['cn'][k]), ('해설이 따옴표로 시작하지 않음',t,lv,n,k,ex['cn'][k][:40])
                ex['cn'][k]=re.sub(r"^'[^']*'", lambda m: "'"+v+"'", ex['cn'][k], count=1)
            for k,v in ed.get('kp',{}).items():
                assert re.search(r"' \([^()]*\) — ", ex['cn'][k]), ('해설에 괄호 해석이 없음',t,lv,n,k,ex['cn'][k][:60])
                ex['cn'][k]=re.sub(r"(' )\([^()]*\)( — )", lambda m: m.group(1)+'('+v+')'+m.group(2), ex['cn'][k], count=1)
            for k,v in ed.get('cn',{}).items():
                if isinstance(v,tuple): v=[v]
                if isinstance(v,list):
                    for x,y in v:
                        assert x in ex['cn'][k], ('해설 조각 없음',t,lv,n,k,x,ex['cn'][k])
                        ex['cn'][k]=ex['cn'][k].replace(x,y)
                else: ex['cn'][k]=v
            nq+=1
            r0,_=ratio(old); r1,i1=ratio(it['choices'])
            f=flagged(it['choices'])
            if f: bad.append((t,lv,n))
            if verbose:
                print('%s L%s #%-2d  %s → %s   %.2f→%.2f  정답순위 %d→%d %s'%(t,lv,n,[len(c) for c in old],[len(c) for c in it['choices']],r0,r1,rank(old,it['answer']),rank(it['choices'],it['answer']),'  ◀◀ 아직 걸림' if f else ''))
    print('수정 문항 %d, 선택지 %d, 아직 걸리는 문항 %d %s / 해설 인용 자동 맞춤 %d'%(nq,nc,len(bad),bad,AUTO[0]))
    lvs=sorted({lv for mod in mods for (t,lv,n) in importlib.import_module(mod).E})
    for lv in lvs:
        print('--- 레벨%s 칸별: 남은 1.4배 문항 / 정답 1~2위(≤16) / 정답 1위(≤8)  [전→후]'%lv)
        for t in LEN_TYPES:
            c0=sum(flagged(it['choices']) for it in tb0[t][lv]); c1=sum(flagged(it['choices']) for it in tb[t][lv])
            A0=cellA(tb0[t][lv]); A1=cellA(tb[t][lv])
            warn=' ◀A' if (A1[0]>16 or A1[1]>8) else ''
            print('  %-6s %2d→%2d   %2d→%2d   %2d→%2d%s'%(t,c0,c1,A0[0],A1[0],A0[1],A1[1],warn))
    if out: save(s,tb,te,out)
    return tb,te
if __name__=='__main__':
    mods=sys.argv[1].split(','); out=sys.argv[2] if len(sys.argv)>2 else None
    apply(mods,out=out)
