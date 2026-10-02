import sys,re,statistics; sys.path.insert(0,'.')
from lib import *
from apply import flagged, rank
def E(ch,a):
    ls=[len(c) for c in ch]; L=ls[a]; o=sorted(ls[k] for k in range(5) if k!=a)
    return L<o[0] and (o[1]+o[2])/2/L>=1.4 and (o[1]+o[2])/2-L>=5
def dump(t,lv,path='/home/claude/work/out/index.html',tlen=230,all_items=False,cnlen=70):
    s,tb,te=load(path)
    for n,it in enumerate(tb[t][lv]):
        c=flagged(it['choices']); e=E(it['choices'],it['answer'])
        if not (c or e or all_items): continue
        ex=te[t][lv][n]; tx=it['text'].replace('\n',' ')
        print('=== %s #%d %s%s정답 %d위 | %s'%(t,n,'C ' if c else '','E ' if e else '',rank(it['choices'],it['answer']),tx if len(tx)<=tlen else tx[:tlen]+'…'))
        for k,ch in enumerate(it['choices']):
            cn=ex['cn'][k]
            if ch in cn: cn2='「」'+cn.replace("'"+ch+"'",'').replace('정답입니다.','').strip(' —')[:cnlen]
            else: cn2=cn[:cnlen]
            print('  %s%d [%2d] %s ‖ %s'%('*' if k==it['answer'] else ' ',k,len(ch),ch,cn2))
if __name__=='__main__':
    a=sys.argv; dump(a[1],a[2],tlen=int(a[3]) if len(a)>3 else 230, all_items=(len(a)>4 and a[4]=='all'), cnlen=int(a[5]) if len(a)>5 else 70)
