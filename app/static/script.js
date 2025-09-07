let canvas, ctx, img=new Image();
let displayW=0, displayH=0, naturalW=0, naturalH=0;
let points=[], isClosed=false;
const imageInput=document.getElementById('image');
const canvasWrap=document.getElementById('canvas-wrap');
const form=document.getElementById('form');
const submitBtn=document.getElementById('submitBtn');
const resetBtn=document.getElementById('resetBtn');
const hiddenPoints=document.getElementById('points');
const progress=document.getElementById('progress');
const result=document.getElementById('result');
const resultImg=document.getElementById('resultImg');
const downloadLink=document.getElementById('downloadLink');
function draw(){ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(img,0,0,canvas.width,canvas.height);if(points.length){ctx.lineWidth=2;ctx.strokeStyle='#60a5fa';ctx.fillStyle='rgba(96,165,250,0.25)';ctx.beginPath();ctx.moveTo(points[0].x,points[0].y);for(let i=1;i<points.length;i++){ctx.lineTo(points[i].x,points[i].y);}if(isClosed)ctx.closePath();ctx.fill();ctx.stroke();for(const p of points){ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fillStyle='#bfdbfe';ctx.fill();}}}
function displayToNatural(p){const rx=naturalW/displayW, ry=naturalH/displayH;return {x:Math.round(p.x*rx), y:Math.round(p.y*ry)};}
function initCanvas(){canvas=document.getElementById('canvas');ctx=canvas.getContext('2d');const wrapWidth=document.querySelector('.container').clientWidth-48;const ratio=img.naturalWidth/img.naturalHeight;displayW=Math.min(wrapWidth,img.naturalWidth);displayH=Math.round(displayW/ratio);canvas.width=displayW;canvas.height=displayH;naturalW=img.naturalWidth;naturalH=img.naturalHeight;draw();canvas.addEventListener('click',onCanvasClick);canvas.addEventListener('dblclick',onCanvasDblClick);} 
function onCanvasClick(e){if(isClosed)return;const rect=canvas.getBoundingClientRect();const x=e.clientX-rect.left;const y=e.clientY-rect.top;points.push({x,y});draw();}
function onCanvasDblClick(){if(points.length>=3){isClosed=true;draw();}}
resetBtn.addEventListener('click',()=>{points=[];isClosed=false;draw();});
imageInput.addEventListener('change',(e)=>{const file=e.target.files[0];if(!file)return;const url=URL.createObjectURL(file);img.onload=()=>{canvasWrap.classList.remove('hidden');initCanvas();};img.src=url;});
form.addEventListener('submit',async(e)=>{e.preventDefault();if(!imageInput.files[0]){alert('Please choose an image.');return;}if(points.length<3||!isClosed){alert('Please draw a polygon (at least 3 points) and double‑click to close it.');return;}const originalPoints=points.map(displayToNatural);hiddenPoints.value=JSON.stringify(originalPoints);const fd=new FormData(form);progress.classList.remove('hidden');result.classList.add('hidden');submitBtn.disabled=true;try{const res=await fetch('/api/edit',{method:'POST',body:fd});const data=await res.json();if(!data.ok)throw new Error(data.detail||'Unknown error');resultImg.src=data.url+'?t='+Date.now();downloadLink.href=data.url;progress.classList.add('hidden');result.classList.remove('hidden');}catch(err){progress.classList.add('hidden');alert('Failed: '+err.message);}finally{submitBtn.disabled=false;}});
