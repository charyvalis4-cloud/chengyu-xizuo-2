const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,PageBreak,AlignmentType,BorderStyle}=require('docx');
const d=JSON.parse(fs.readFileSync('content.json','utf8'));
const L='ABCD';
function build(color,out){
  const C=color?{h:'1F5C5A',jie:'1F4E9E',li:'2E7D32',si:'00838F',fan:'D9622B',ex:'7B3FA0',ttl:'B23A48'}:{h:'000000',jie:'000000',li:'000000',si:'000000',fan:'000000',ex:'000000',ttl:'000000'};
  const F={ascii:'Microsoft JhengHei',eastAsia:'Microsoft JhengHei',hAnsi:'Microsoft JhengHei'};
  const r=(t,o={})=>new TextRun({text:t,font:F,...o});
  const P=(runs,o={})=>new Paragraph({children:Array.isArray(runs)?runs:[r(runs)],spacing:{after:80,line:340},...o});
  const H=(t,lvl)=>new Paragraph({heading:lvl,children:[r(t,{bold:true,color:C.h,size:lvl===HeadingLevel.HEADING_1?32:26})],spacing:{before:240,after:120}});
  const kids=[];
  kids.push(new Paragraph({alignment:AlignmentType.CENTER,children:[r('成語習作 第2回（中學生）',{bold:true,size:40,color:C.ttl})],spacing:{after:120}}));
  kids.push(P('班級：＿＿＿＿　座號：＿＿＿＿　姓名：＿＿＿＿＿＿　得分：＿＿＿＿'));
  kids.push(H('壹、成語學習站',HeadingLevel.HEADING_1));
  const card=(num,x)=>{
    const [n,j,l,a,b,e]=x;
    kids.push(new Paragraph({keepNext:true,spacing:{before:160,after:40},border:{top:{style:BorderStyle.SINGLE,size:4,color:'BBBBBB',space:4}},children:[r(num+' '+n,{bold:true,size:28,color:C.ttl})]}));
    const line=(lab,t,col)=>kids.push(P([r(lab+'：',{bold:true,color:col}),r(t)],{indent:{left:240}}));
    line('解釋',j,C.jie); if(l)line('例句',l,C.li); if(a)line('相似',a,C.si); if(b)line('相反',b,C.fan);
    e.forEach(([lab,t])=>line(lab,t,C.ex));
  };
  d.I.forEach((x,i)=>card(String(i+1),x));
  kids.push(H('★ 老師補充成語',HeadingLevel.HEADING_2));
  d.X.forEach(x=>card('★',x));
  kids.push(new Paragraph({children:[new PageBreak()]}));
  kids.push(H('貳、實力挑戰',HeadingLevel.HEADING_1));
  d.S.forEach(sc=>{
    kids.push(H(sc.title,HeadingLevel.HEADING_2));
    if(sc.note)kids.push(P(sc.note,{}));
    if(sc.passage)sc.passage.forEach(p=>kids.push(P(p,{indent:{firstLine:480}})));
    sc.items.forEach((it,i)=>{
      const n=i+1;
      if(it.kind==='mc'){
        kids.push(new Paragraph({keepNext:true,spacing:{before:100,after:20},children:[r(n+'. （　）'+it.text)]}));
        kids.push(P(it.opts.map((o,k)=>'('+L[k]+') '+o).join('　'),{indent:{left:480}}));
      }else{
        let t=it.text; if(t.indexOf('（　）')<0) t+= it.kind==='fill2'?'：（　　）→（　　）':'：（　　）';
        kids.push(P(n+'. '+t));
      }
    });
  });
  kids.push(new Paragraph({children:[new PageBreak()]}));
  kids.push(H('參考答案',HeadingLevel.HEADING_1));
  d.S.forEach(sc=>{
    const nm=sc.title.split('、')[1].split('（')[0];
    kids.push(P([r(nm+'：',{bold:true,color:C.h}),r(sc.items.map((it,i)=>(i+1)+'.'+it.ansdisp).join('　'))]));
  });
  kids.push(P('註：講義本身沒有附答案，以上為編者依題意解答，請老師核對；閱讀測驗第 3 題「百發百中」與「百步穿楊」皆可。七、八兩節為仿第 1 回自動產生的延伸練習。',{}));
  const doc=new Document({styles:{default:{document:{run:{font:F,size:24}}}},sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1134,bottom:1134,left:1134,right:1134}}},children:kids}]});
  return Packer.toBuffer(doc).then(b=>fs.writeFileSync(out,b));
}
Promise.all([build(false,'out/xizuo-2-handout.docx'),build(true,'out/xizuo-2-handout-color.docx')]).then(()=>console.log('docx ok'));
