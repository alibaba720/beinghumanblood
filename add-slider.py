with open('home.html','r',encoding='utf-8') as f: h=f.read()

SH='''<section class="qs"><div class="qs-track" id="qsTrack"></div><div class="qs-dots" id="qsDots"></div></section>
'''

SC='''/* QS */
.qs{position:relative;overflow:hidden;height:180px;max-width:1100px;margin:40px auto 0;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.15)}
.qs-track{display:flex;height:100%;transition:transform 0.6s ease}
.qs-slide{min-width:100%;height:100%;display:flex;align-items:center;justify-content:center;padding:25px;text-align:center}
.qs-slide p{font-size:18px;font-weight:600;line-height:1.7;max-width:850px;margin:0;font-family:'Noto Nastaliq Urdu',serif;direction:rtl}
.qs-slide .hl{font-size:20px;font-weight:800}
.qs-dots{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:5}
.qs-dot{width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,0.4);cursor:pointer;transition:all 0.3s}
.qs-dot.active{background:white;width:24px;border-radius:5px}
.qs-1{background:linear-gradient(135deg,#8B0000,#4a0000)}.qs-1 p{color:#FFD700}.qs-1 .hl{color:#fff}
.qs-2{background:linear-gradient(135deg,#0d5c3f,#052c1d)}.qs-2 p{color:#fff}.qs-2 .hl{color:#FFD700}
.qs-3{background:linear-gradient(135deg,#1a3a6e,#0a1f3d)}.qs-3 p{color:#e8f4ff}.qs-3 .hl{color:#7ec8ff}
.qs-4{background:linear-gradient(135deg,#4a1a5c,#26102e)}.qs-4 p{color:#ffe8f4}.qs-4 .hl{color:#FFD700}
@media(max-width:700px){.qs{height:200px;margin:25px 15px 0}.qs-slide p{font-size:15px}.qs-slide .hl{font-size:17px}}
'''

SJ='''(function(){var Q=[{c:"qs-1",h:'<p><span class="hl">حقوق اللہ</span> تو شاید معاف ہو جائیں، مگر <span class="hl">حقوق العباد</span> معاف نہیں ہوں گے</p>'},{c:"qs-2",h:'<p>جو <span class="hl">لوگوں کے کام</span> آتا ہے، اللہ اسے <span class="hl">یاد رکھتا ہے</span></p>'},{c:"qs-3",h:'<p><span class="hl">ایک قطرہ خون</span>، ایک زندگی — یہ سب سے <span class="hl">بڑا صدقہ</span> ہے</p>'},{c:"qs-4",h:'<p>تم <span class="hl">بہترین انسان</span> ہو، جو دوسروں کی <span class="hl">مدد</span> کرتے ہو</p>'}];var t=document.getElementById("qsTrack"),d=document.getElementById("qsDots");if(!t)return;Q.forEach(function(q,i){var s=document.createElement("div");s.className="qs-slide "+q.c;s.innerHTML=q.h;t.appendChild(s);var dot=document.createElement("div");dot.className="qs-dot"+(i===0?" active":"");dot.onclick=function(){go(i)};d.appendChild(dot)});var idx=0;function go(i){idx=(i+Q.length)%Q.length;t.style.transform="translateX(-"+idx*100+"%)";var ds=d.querySelectorAll(".qs-dot");for(var j=0;j<ds.length;j++)ds[j].classList.toggle("active",j===idx)}setInterval(function(){go(idx+1)},4000);var sx=0;t.addEventListener("touchstart",function(e){sx=e.touches[0].clientX});t.addEventListener("touchend",function(e){var diff=e.changedTouches[0].clientX-sx;if(diff>50)go(idx-1);else if(diff<-50)go(idx+1)})})();
'''

h=h.replace('<!-- IMPACT NUMBERS -->',SH+'\n<!-- IMPACT NUMBERS -->',1)
h=h.replace('/* IMPACT NUMBERS */',SC+'\n/* IMPACT NUMBERS */',1)
h=h.replace('// MODALS',SJ+'\n// MODALS',1)

with open('home.html','w',encoding='utf-8') as f: f.write(h)
print('Done')
