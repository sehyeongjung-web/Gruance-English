import json, statistics, sys
SRC='/home/claude/Gruance-English/index.html'
def span(s,key):
    i=s.find(key); st=s.find('{',i); d=0; j=st; instr=False; esc=False
    while j<len(s):
        ch=s[j]
        if instr:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"': instr=False
        else:
            if ch=='"': instr=True
            elif ch=='{': d+=1
            elif ch=='}':
                d-=1
                if d==0: break
        j+=1
    return st,j+1
def load(path=SRC):
    s=open(path,encoding='utf-8').read()
    a,b=span(s,'const TYPE_BANK =');  tb=json.loads(s[a:b])
    c,d=span(s,'const TYPE_EXPLAIN ='); te=json.loads(s[c:d])
    return s,tb,te
def dump(o): return json.dumps(o,ensure_ascii=False)
def save(s,tb,te,path):
    # EXPLAIN은 BANK보다 앞에 있으므로 뒤(BANK)부터 교체
    a,b=span(s,'const TYPE_BANK ='); s=s[:a]+dump(tb)+s[b:]
    c,d=span(s,'const TYPE_EXPLAIN ='); s=s[:c]+dump(te)+s[d:]
    open(path,'w',encoding='utf-8').write(s)
LEN_TYPES=['18','19','20','21','22','23','24','26','27_28','31','32','33','34','40','41','45']
def ratio(ch):
    ls=[len(c) for c in ch]; i=max(range(5),key=lambda k:ls[k]); o=[ls[k] for k in range(5) if k!=i]
    m=statistics.median(o)
    return (ls[i]/m if m else 0), i
