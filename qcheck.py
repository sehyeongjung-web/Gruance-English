import sys, re, importlib; sys.path.insert(0,'.')
from lib import *
def frag(c):
    m=re.match(r"^'(.+?)'(?= \(| —|\(|$)", c)
    if not m: return None
    q=m.group(1)
    if '→' in q and '(' in q: q=q.split('(')[0]
    return q
def run(out, lv):
    s0,tb0,te0=load(); s1,tb1,te1=load(out); bad=0; n=0
    for t in LEN_TYPES:
        for i,(a,b) in enumerate(zip(tb0[t][lv],tb1[t][lv])):
            if a==b and te0[t][lv][i]==te1[t][lv][i]: continue
            for k in range(5):
                q0=frag(te0[t][lv][i]['cn'][k]); q1=frag(te1[t][lv][i]['cn'][k])
                if q0 and q0 in a['choices'][k]:
                    n+=1
                    if not (q1 and q1 in b['choices'][k]):
                        bad+=1; print('인용 어긋남',t,lv,i,k,'|',q1,'|',b['choices'][k])
    print('레벨%s 인용 대조 %d건, 어긋남 %d건'%(lv,n,bad))
if __name__=='__main__': run(sys.argv[1], sys.argv[2])
