# -*- coding: utf-8 -*-
import random, json, html, os
from data import *
random.seed(20261009)
L='ABCD'
esc=html.escape
names=[x[0] for x in I]
def sp(s): return s.split() if s else []

# ---------- build question model ----------
S=[]  # sections: dict(title,note,items) ; item: dict(kind,text,opts,ans,alt,ansdisp,inputs)
def sec(title,note=''):
    d=dict(title=title,note=note,items=[]); S.append(d); return d
s=sec('一、字形測驗','依注音填入正確的字')
for t,a in ZX: s['items'].append(dict(kind='fill',text=t,ans=a,ansdisp=a))
s=sec('二、綜合測驗')
for q,o,a in ZH: s['items'].append(dict(kind='mc',text=q,opts=o,ans=a,alt='',ansdisp=a))
s=sec('三、錯別字大王','請圈出錯別字，並填上正確的字（左格填錯字，右格填正字）')
for t,w,r in CW: s['items'].append(dict(kind='fill2',text=t,ans=w+'|'+r,ansdisp=w+'→'+r))
s=sec('四、成語運用')
for q,o,a in YY: s['items'].append(dict(kind='mc',text=q,opts=o,ans=a,alt='',ansdisp=a))
s=sec('五、閱讀測驗')
s['passage']=PASSAGE
for q,o,a,alt in RD: s['items'].append(dict(kind='mc',text=q,opts=o,ans=a,alt=alt,ansdisp=a+('（'+alt+' 亦可）' if alt else '')))
s=sec('六、成語接龍','填入適當的字，使成語首尾相接：伯樂相馬→馬到成功→功成不居→居安思危→危言聳聽→聽天由命')
chain=[("（　）樂相馬","伯"),("馬到成（　）","功"),("（　）成不居","功"),("居（　）思危","安"),("危（　）聳（　）","言|聽"),("（　）天由命","聽")]
for t,a in chain:
    k='fill2' if '|' in a else 'fill'
    s['items'].append(dict(kind=k,text=t,ans=a,ansdisp=a.replace('|','、')))

def shuffled(correct,wrong):
    o=wrong[:3]+[correct]; random.shuffle(o); return o,L[o.index(correct)]
# 七、例句應用題
s=sec('七、例句應用題（每個成語一題）','選出最適合填入□□□□的成語')
for n,j,l,a,b,e in I:
    wrong=random.sample([x for x in names if x!=n],3)
    o,ans=shuffled(n,wrong)
    s['items'].append(dict(kind='mc',text=l.replace(n,'□□□□'),opts=o,ans=ans,alt='',ansdisp=ans))
# 八、綜合練習題
s=sec('八、綜合練習題（每個成語一題）')
for i,(n,j,l,a,b,e) in enumerate(I):
    rel=None
    if i%2==1:
        if sp(b): rel=('相反',sp(b)[0])
        elif sp(a): rel=('相似',sp(a)[0])
    if rel:
        kind,c=rel
        bad=set(sp(a)+sp(b)+[n])
        wrong=random.sample([x for x in names if x not in bad],3)
        o,ans=shuffled(c,wrong)
        txt='下列哪一個成語，與「%s」的意思%s？'%(n,'相反' if kind=='相反' else '相近')
    else:
        wrong=[x[1] for x in random.sample([y for y in I if y[0]!=n],3)]
        o,ans=shuffled(j,wrong)
        txt='「%s」的意思是：'%n
    s['items'].append(dict(kind='mc',text=txt,opts=o,ans=ans,alt='',ansdisp=ans))
T=sum(len(x['items']) for x in S)

# ---------- extras shown on cards ----------
def card_html(i,x,star=False):
    n,j,l,a,b,e=x
    h='<div class="card%s"><h3><span>%s</span>%s</h3>'%(' star' if star else '', '★' if star else i, esc(n))
    h+='<p><b class="k">解釋</b>%s</p>'%esc(j)
    if l: h+='<p><b class="k">例句</b>%s</p>'%esc(l)
    if a: h+='<p><b class="k s">相似</b>%s</p>'%esc(a)
    if b: h+='<p><b class="k o">相反</b>%s</p>'%esc(b)
    for lab,t in e: h+='<p class="dn"><b class="k d">%s</b>%s</p>'%(lab,esc(t))
    return h+'</div>'
def qhtml(it,n):
    k=it['kind']; ans=esc(it['ans']); alt=esc(it.get('alt',''))
    base='<div class="q" data-a="%s" data-alt="%s" data-ans="%s">'%(ans,alt,esc(it['ansdisp']))
    if k=='mc':
        o=''.join('<button type="button" class="opt" data-v="%s">(%s) %s</button>'%(L[i],L[i],esc(t)) for i,t in enumerate(it['opts']))
        return base+'<p>%d. %s</p><div class="opts">%s</div><div class="fb"></div></div>'%(n,esc(it['text']),o)
    if k=='fill':
        inp='<input type="text" maxlength="2" size="3" autocomplete="off">'
        t=esc(it['text'])
        body=t.replace('（　）',inp) if '（　）' in t else t+'　'+inp
        return base+'<p>%d. %s</p><div class="fb"></div></div>'%(n,body)
    if k=='fill2':
        inp='<input type="text" maxlength="2" size="3" autocomplete="off">'
        if '（　）' in it['text']:
            body=esc(it['text']).replace('（　）',inp)
        else:
            body=esc(it['text'])+'　錯字 '+inp+' → 正字 '+inp
        return base+'<p>%d. %s</p><div class="fb"></div></div>'%(n,body)
CSS=open('style.css',encoding='utf8').read()
JS=open('app.js',encoding='utf8').read().replace('__T__',str(T))
parts=[]
parts.append('<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>成語習作 第2回｜互動版</title>\n<style>\n'+CSS+'</style></head><body><main>\n')
parts.append('<p><a href="../">← 成語典故</a>　<a href="static.html">講義版（可列印）</a></p><h1>成語習作 第2回（中學生）</h1><p>%d 個成語學習站（另有 3 個老師補充成語）、字形測驗、綜合測驗、錯別字大王、成語運用、閱讀測驗、成語接龍，以及每個成語各一題的例句應用題與綜合練習題。直接點選或輸入作答。</p>\n'%len(I))
parts.append('<nav><a href="#learn">成語學習站</a><a href="#test">實力挑戰</a><a href="#answers">參考答案</a><a href="#dl">下載 Word</a></nav>\n<p>班級：<input size="6"> 座號：<input size="4"> 姓名：<input size="8"></p>\n')
parts.append('<div class="bar"><label><input type="radio" name="m" value="live" checked> 即時對答案</label><label><input type="radio" name="m" value="sub"> 交卷模式</label>\n<span id="sc">已作答 0／%d　答對 0</span><button class="btn" id="go" type="button" hidden>交卷送出</button><button class="btn" id="rs" type="button">重新作答</button></div>\n'%T)
parts.append('<h2 id="learn">成語學習站（共 %d 個）</h2><div class="grid">'%len(I)+''.join(card_html(i+1,x) for i,x in enumerate(I))+'</div>')
parts.append('<h3>★ 老師補充成語</h3><div class="grid">'+''.join(card_html(i+1,x,True) for i,x in enumerate(X))+'</div>')
parts.append('<h2 id="test">實力挑戰</h2>')
for sc in S:
    parts.append('<h3>%s</h3>'%esc(sc['title']))
    if sc['note']: parts.append('<p class="nt">%s</p>'%esc(sc['note']))
    if sc.get('passage'): parts.append('<div class="card pass">'+''.join('<p>%s</p>'%esc(p) for p in sc['passage'])+'</div>')
    for i,it in enumerate(sc['items']): parts.append(qhtml(it,i+1))
# answers
def anstext(sc):
    return '　'.join('%d.%s'%(i+1,it['ansdisp']) for i,it in enumerate(sc['items']))
ah=''.join('<p>%s：%s</p>'%(esc(sc['title'].split('、',1)[1].split('（')[0]),esc(anstext(sc))) for sc in S)
parts.append('<h2 id="answers">參考答案</h2><details><summary>顯示參考答案（老師用）</summary>'+ah+'<p class="nt">註：講義本身沒有附答案，以上為編者依題意解答，請老師核對；閱讀測驗第 3 題「百發百中」與「百步穿楊」皆可，系統兩者都算對。七、八兩節為仿第 1 回自動產生的延伸練習。</p></details>')
parts.append('<h2 id="dl">下載 Word 檔</h2><div class="dl"><a href="xizuo-2-handout.docx">📄 標準版 Word 檔（黑白，適合列印）</a><a href="xizuo-2-handout-color.docx">🎨 彩色版 Word 檔（內容相同，依單元上色）</a></div>\n</main>\n<script>\n'+JS+'</script></body></html>')
os.makedirs('out',exist_ok=True)
open('out/index.html','w',encoding='utf8').write(''.join(parts))

# ---------- static ----------
st=[]
st.append('<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>成語習作 第2回｜講義版</title>\n<style>body{font:15px/1.7 "Noto Sans TC","Microsoft JhengHei",sans-serif;color:#000;background:#fff;max-width:820px;margin:auto;padding:16px}h1,h2{color:#1f5c5a}.c{break-inside:avoid;margin:8px 0;padding:6px 0;border-bottom:1px solid #ccc}.q{break-inside:avoid;margin:6px 0}.o{margin:0 0 4px 1.5em}.pb{break-before:page}@media print{.np{display:none}}</style></head><body>\n')
st.append('<p class="np"><a href="../">← 成語典故</a>　<a href="./">互動版</a>　<a href="xizuo-2-handout.docx">Word 講義</a>　<a href="xizuo-2-handout-color.docx">Word 講義（彩色版）</a></p>\n<h1>成語習作 第2回（中學生）</h1><p>班級：＿＿＿＿　座號：＿＿＿＿　姓名：＿＿＿＿＿＿　得分：＿＿＿＿</p>\n<h2>壹、成語學習站</h2>')
def sc_card(i,x):
    n,j,l,a,b,e=x
    h='<div class="c"><b>%s %s</b><br>解釋：%s'%(i,esc(n),esc(j))
    if l: h+='<br>例句：'+esc(l)
    if a: h+='<br>相似：'+esc(a)
    if b: h+='<br>相反：'+esc(b)
    for lab,t in e: h+='<br>%s：%s'%(lab,esc(t))
    return h+'</div>'
st.append(''.join(sc_card(str(i+1),x) for i,x in enumerate(I)))
st.append('<h3>★ 老師補充成語</h3>'+''.join(sc_card('★',x) for x in X))
st.append('<h2 class="pb">貳、實力挑戰</h2>')
for sc in S:
    st.append('<h3>%s</h3>'%esc(sc['title']))
    if sc['note']: st.append('<p>%s</p>'%esc(sc['note']))
    if sc.get('passage'): st.append(''.join('<p>%s</p>'%esc(p) for p in sc['passage']))
    for i,it in enumerate(sc['items']):
        n=i+1
        if it['kind']=='mc':
            st.append('<div class="q"><p>%d. （　）%s</p><p class="o">%s</p></div>'%(n,esc(it['text']),'　'.join('(%s) %s'%(L[k],esc(t)) for k,t in enumerate(it['opts']))))
        elif it['kind']=='fill':
            t=esc(it['text']); st.append('<p>%d. %s</p>'%(n,t if '（　）' in t else t+'：（　　）'))
        else:
            t=esc(it['text']); st.append('<p>%d. %s</p>'%(n,t if '（　）' in t else t+'：（　　）→（　　）'))
st.append('<h2 class="pb">參考答案</h2>'+ah+'</body></html>')
open('out/static.html','w',encoding='utf8').write(''.join(st))
json.dump(dict(I=I,X=X,S=S,T=T),open('content.json','w',encoding='utf8'),ensure_ascii=False)
print('T=',T,[len(x['items']) for x in S])
