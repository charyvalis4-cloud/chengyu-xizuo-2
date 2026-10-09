const Q=[...document.querySelectorAll('.q')],T=__T__;
const val=q=>{const ins=[...q.querySelectorAll('input[type=text]')];if(ins.length){const v=ins.map(i=>i.value.trim());return v.every(x=>x)?v.join('|'):''}const o=q.querySelector('.opt.sel');return o?o.dataset.v:''};
const good=(q,v)=>v===q.dataset.a||(q.dataset.alt&&v===q.dataset.alt);
function mark(q){const v=val(q);if(!v){q.classList.remove('ok','bad');q.querySelector('.fb').textContent='';return}const ok=good(q,v);q.classList.toggle('ok',ok);q.classList.toggle('bad',!ok);q.querySelector('.fb').textContent=ok?'✔ 答對了':'✘ 正確答案：'+q.dataset.ans}
const mode=()=>document.querySelector('[name=m]:checked').value;
function stat(){const d=Q.filter(q=>val(q)).length;const r=Q.filter(q=>q.classList.contains('ok')).length;document.getElementById('sc').textContent='已作答 '+d+'／'+T+'　答對 '+(mode()=='live'?r:'—')}
function upd(q){if(mode()=='live')mark(q);stat()}
Q.forEach(q=>{q.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{q.querySelectorAll('.opt').forEach(x=>x.classList.remove('sel'));b.classList.add('sel');upd(q)});q.querySelectorAll('input').forEach(e=>e.addEventListener('input',()=>upd(q)))});
document.querySelectorAll('[name=m]').forEach(r=>r.onchange=()=>{document.getElementById('go').hidden=mode()=='live';Q.forEach(q=>{q.classList.remove('ok','bad');q.querySelector('.fb').textContent=''});if(mode()=='live')Q.forEach(mark);stat()});
document.getElementById('go').onclick=()=>{Q.forEach(q=>{if(val(q))mark(q);else{q.classList.add('bad');q.querySelector('.fb').textContent='未作答，正確答案：'+q.dataset.ans}});const r=Q.filter(q=>q.classList.contains('ok')).length;document.getElementById('sc').textContent='已作答 '+Q.filter(q=>val(q)).length+'／'+T+'　答對 '+r+'　（'+Math.round(r*100/T)+' 分）'};
document.getElementById('rs').onclick=()=>{Q.forEach(q=>{q.classList.remove('ok','bad');q.querySelector('.fb').textContent='';q.querySelectorAll('.opt').forEach(x=>x.classList.remove('sel'));q.querySelectorAll('input').forEach(e=>e.value='')});stat()};
