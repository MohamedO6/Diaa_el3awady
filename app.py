# app.py  →  pip install streamlit  →  streamlit run app.py
import random, time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Shiblanga OS: Chicken Invaders Edition", page_icon="🐔", layout="wide")

CSS = """
<style>
.stApp{background:radial-gradient(ellipse at bottom,#1b2735 0%,#090a0f 100%);color:#e8f1ff}
.stars,.stars2{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;
 background-repeat:repeat;animation:move 60s linear infinite}
.stars{background-image:radial-gradient(2px 2px at 20px 30px,#fff,transparent),
 radial-gradient(1.5px 1.5px at 120px 90px,#ffe9a8,transparent),
 radial-gradient(2px 2px at 220px 160px,#fff,transparent);background-size:250px 200px}
.stars2{background-image:radial-gradient(1px 1px at 60px 120px,#9fd3ff,transparent),
 radial-gradient(1px 1px at 180px 40px,#fff,transparent);background-size:180px 150px;animation-duration:110s}
@keyframes move{from{background-position:0 0}to{background-position:0 1000px}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.title{font-size:46px;font-weight:900;text-align:center;color:#ffd93b;
 text-shadow:0 0 12px #ff9800,0 0 30px #ff5722;letter-spacing:2px}
.chk{font-size:40px;display:inline-block;animation:float 2s ease-in-out infinite}
.term{background:#05070d;border:2px solid #ffd93b;border-radius:12px;padding:14px;
 font-family:monospace;color:#7CFC9A;white-space:pre-wrap;max-height:430px;overflow:auto;
 box-shadow:0 0 18px #ffd93b55;direction:ltr;text-align:left}
.good{border-left:6px solid #4caf50;background:#10301a;padding:10px;border-radius:8px}
.bad{border-left:6px solid #ff3d3d;background:#3a1010;padding:10px;border-radius:8px}
.warn{background:#3a2a05;border:1px solid #ffb300;padding:10px;border-radius:8px}
div.stButton>button{background:linear-gradient(#ffb300,#ff6f00);color:#111;font-weight:800;border:0;border-radius:10px}
</style><div class="stars"></div><div class="stars2"></div>
"""
st.markdown(CSS, unsafe_allow_html=True)

TAYEBAT = {
 "rice":"طيب","رز":"طيب","أرز":"طيب","potato":"طيب","بطاطس":"طيب","beef":"طيب","لحمة":"طيب","lamb":"طيب",
 "كوارع":"طيب","ghee":"طيب","سمن":"طيب","butter":"طيب","زبدة":"طيب","olive oil":"طيب","زيت زيتون":"طيب",
 "dates":"طيب","تمر":"طيب","sugar":"طيب","سكر":"طيب","cheddar":"طيب","gouda":"طيب","mozzarella":"طيب",
 "parmesan":"طيب","رومي":"طيب","corn":"طيب","درة":"طيب","bulgur":"طيب","freekeh":"طيب","فريك":"طيب",
 "bran toast":"طيب","توست نخالة":"طيب","fruit":"طيب","فاكهة":"طيب",
 "chicken":"خبيث","فراخ":"خبيث","دجاج":"خبيث","egg":"خبيث","بيض":"خبيث","milk":"خبيث","لبن":"خبيث",
 "حليب":"خبيث","yogurt":"خبيث","زبادي":"خبيث","lentils":"خبيث","عدس":"خبيث","beans":"خبيث","فول":"خبيث",
 "tomato":"خبيث","طماطم":"خبيث","onion":"خبيث","بصل":"خبيث","salad":"خبيث","سلطة":"خبيث","جرجير":"خبيث",
 "vegetable oil":"خبيث","زيت نباتي":"خبيث","bread":"خبيث","عيش":"خبيث",
}
LAWS = [
 "الأكل مقسّم لـ (طيبات) و(خبائث) — تصنيف النظام مش تصنيف علمي معتمد.",
 "كُل لما تجوع بجد، وقف قبل الشبع.",
 "اشرب لما تعطش، من غير مبالغة.",
 "مواعيد الوجبات الثابتة مش شرط، وقلّل عدد الوجبات.",
 "صيام الاتنين والخميس جزء من الأسلوب.",
 "فاكهة نوع واحد في المرة.",
 "المسموح: لحوم حمراء، رز، بطاطس، سمن، زبدة، زيت زيتون، تمر، جبن معيّن.",
 "الممنوع: فراخ، بيض، لبن سائل، بقوليات، خضار ورقي، طماطم، بصل، زيوت نباتية.",
]
DISCLAIMER = ("⚠️ باروديا ترفيهية. نظام الطيبات مفيهوش تجارب سريرية محكّمة تثبت إنه علاج، وجهات رسمية في مصر "
              "حذّرت منه. متوقفش أنسولين أو دوا ضغط أو علاج كيماوي بسبب أي دايت. استشر دكتورك دايماً.")
FUNNY = ["الفراخ؟ لأ يا باشا.. ده خبيث!", "سلطة؟ سيبها للأرانب.", "جعان بجد؟ كل. مش جعان؟ سيب الطبق وامشي.",
 "عطشان؟ اشرب. مش عطشان؟ متشربش.", "فاكهة نوع واحد في المرة.", "رز + كوارع = المعادلة المقدسة."]
WISDOM = ["السيستم شغال؟ متلمسهوش!", "نقطة (.) في المكان الغلط ممكن تهد architecture كامل.",
 "قبل ما تصلح الـ bug، افهم ليه اختار يعيش هنا.", "كُل لما تجوع بجد.. وارفع الكود لما يعدّي الـ tests.",
 "الـ 'خبيث' الحقيقي هو الـ global variable.", "Terminal نضيف = دماغ نضيف."]
FORTUNES = ["Great things come to those who write clean code.", "Error 404: Bad luck not found.",
 "اليوم هتلاقي bug.. بس هتحله قبل الفطار.", "In the code of life, you are the compiler."]
SHIB = """███████╗██╗  ██╗██╗██████╗ ██╗      █████╗ ███╗   ██╗ ██████╗  █████╗
██╔════╝██║  ██║██║██╔══██╗██║     ██╔══██╗████╗  ██║██╔════╝ ██╔══██╗
███████╗███████║██║██████╔╝██║     ███████║██╔██╗ ██║██║  ███╗███████║
╚════██║██╔══██║██║██╔══██╗██║     ██╔══██║██║╚██╗██║██║   ██║██╔══██║
███████║██║  ██║██║██████╔╝███████╗██║  ██║██║ ╚████║╚██████╔╝██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝"""
DIAA = """⣪⣺⣪⣺⣺⡂⡂⡂⡂⡂⡂⡂⡂⡂⡂⣂⣢⡢⣢⡢⡠⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡪⣪⡪⡪⡪
⣪⣺⣪⣺⣪⡂⡂⡂⡂⡂⡂⡂⡂⡂⣺⡻⡢⠊⠊⠊⠪⠊⡢⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡊⡪⡪⡢⡊
⣪⡺⣪⡺⣪⡂⡂⡂⡂⡂⡂⡂⡀⡢⣯⡂⡀⠀⠀⠀⠀⠀⠀⠂⡂⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡊⡢⡊⡢⡊
⣪⡺⣪⡺⣪⡂⡂⡂⡂⡂⡂⡂⡀⡊⣾⣾⣦⡂⡲⣲⣂⡂⠀⡂⡂⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡊⡢⡂⡂⡂
⣪⡺⣪⡺⣪⡂⡂⡂⡂⡂⡀⡂⡀⡂⣾⡻⣪⠂⠀⠈⠀⠀⠀⠂⡀⠂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡂⡀⡊⡂⡂⡀⡂
⣪⡪⣪⡺⣪⡂⡂⡂⡂⡂⡀⡂⡀⡊⣾⡪⣾⡦⡢⠀⡀⠀⠀⡀⡀⡂⡀⠂⡀⠂⡀⠂⡀⡂⡀⡂⡀⡊⡂⡂⡀⠂
⣪⡪⣪⡪⣪⡂⡂⡂⡀⡂⡀⡂⡀⡂⡺⣺⣾⣦⡢⡂⡂⠂⡀⣢⡀⡂⡀⠂⡀⠂⡀⠂⡀⠂⡀⠂⡀⡊⡂⠂⡀⠂
⡪⡪⣪⡪⣪⡂⡂⡂⡀⡂⡀⡂⡀⣂⣠⣾⣾⣻⡊⡀⣠⡢⡂⣺⣿⣿⣦⣦⣤⣂⣀⡂⡀⠂⡀⠂⡀⠊⡂⠂⡀⠀
⣪⡪⣪⡪⣪⡂⡂⡂⣀⣢⣤⣶⣾⣿⣿⣿⣿⣿⣾⡻⡪⡊⡀⣺⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⡂⡀⠊⡂⠂⡀⠂
⣮⡪⣪⡪⣪⡂⡂⡢⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣪⡢⡂⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡂⡀⠊⡂⠂⡀⠀
⣿⡪⣪⡪⣪⡂⡂⣪⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣾⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡂⡀⠊⡂⡂⡀⠂
⣿⣿⣪⡪⣪⡂⡂⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡪⣪⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠊⡂⡂⡀⡂
⣿⣿⣮⡪⣪⡂⡂⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣪⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠊⡂⡂⡀⡂
⣿⣿⣯⡪⣪⡂⡂⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠊⡢⡂⡂⡂"""


def check_food(q):
    q = q.lower().strip()
    for k, v in TAYEBAT.items():
        if q and (k in q or q in k):
            return v
    return None


HELP = """-help              : القائمة دي
info               : معلومات النظام
shiblanga          : ASCII art
diaa el3awady      : dot-art
diaa-wisdom        : حكمة (باروديا)
no2ta              : فحص النقطة
nizam-el-tayebat   : القواعد المتداولة
tayebat-check X    : طيب ولا خبيث؟
tayebat-menu       : قائمة سريعة
tayebat-meal       : وجبة عشوائية
hungry / thirsty   : فحص الجوع والعطش
chicken            : فحص الفراخ
rocket / matrix    : أنيميشن
weather / fortune / system-load / disk-space
cowsay X / greet / disclaimer / clear"""


def run_command(cmd, anim):
    low = cmd.lower().strip()
    if low in ("-help", "--help", "help"): return HELP
    if low == "info": return "[Shiblanga OS v3.0]\nStatus: Active\nKernel: Streamlit Simulated Shell\nTheme: Chicken Invaders Edition 🐔"
    if low == "shiblanga": return SHIB
    if low == "diaa el3awady": return DIAA
    if low == "diaa-wisdom": return f"💡 حكمة (باروديا): \"{random.choice(WISDOM)}\""
    if low == "no2ta":
        for i in range(1, 6): anim.code("." * i); time.sleep(0.35)
        return "Scan complete. One critical dot found: (.) -> Everything is in equilibrium."
    if low == "nizam-el-tayebat": return "\n".join(f"{i}. {l}" for i, l in enumerate(LAWS, 1)) + "\n\n" + DISCLAIMER
    if low.startswith("tayebat-check"):
        q = cmd[len("tayebat-check"):].strip(); r = check_food(q)
        if r is None: return f"'{q}': مش في القائمة المختصرة. القوائم بتختلف من مصدر لمصدر."
        return f"✅ '{q}' → طيّبة" if r == "طيب" else f"🚫 '{q}' → خبيثة\n{random.choice(FUNNY)}"
    if low == "tayebat-menu":
        g = sorted({k for k, v in TAYEBAT.items() if v == "طيب" and k.isascii()})
        b = sorted({k for k, v in TAYEBAT.items() if v == "خبيث" and k.isascii()})
        return "✅ طيبات: " + ", ".join(g) + "\n🚫 خبائث: " + ", ".join(b)
    if low == "tayebat-meal":
        return "🍽️ " + " + ".join([random.choice(["rice", "potato", "bulgur", "freekeh"]),
               random.choice(["beef", "lamb", "كوارع"]), random.choice(["ghee", "butter", "olive oil"]),
               random.choice(["dates", "fruit"])])
    if low == "hungry":
        for i in range(3): anim.code("." * (i + 1)); time.sleep(0.4)
        return random.choice(["✅ جعان بجد → كُل.", "❌ ده ملل مش جوع → سيب الأكل.", "🤔 اشرب مياه وبعدين قرر."])
    if low == "thirsty": return random.choice(["💧 عطشان فعلاً → اشرب.", "❌ مش عطشان → متشربش بالعافية."])
    if low == "disclaimer": return DISCLAIMER
    if low == "chicken":
        for s in ["🐔 فراخ اتكشفت في الـ buffer!", "Scanning protein source...", "Classification: خبيث", "Quarantine..."]:
            anim.code(s); time.sleep(0.6)
        return "🐔 الفراخ اتحجرت. استبدلها بـ رز وكوارع (باروديا) 🍚"
    if low == "rocket":
        for c in (3, 2, 1): anim.code(f"T-minus {c}..."); time.sleep(0.5)
        for h in range(8):
            anim.code("\n" * (7 - h) + "   🚀\n  🔥🔥"); time.sleep(0.25)
        return "Shiblanga-1 entered orbit! 🚀"
    if low == "matrix":
        ch = list("01xyzABC#@$%")
        for _ in range(25):
            anim.code("\n".join("".join(random.choice(ch) if random.random() > .4 else " " for _ in range(60)) for _ in range(8)))
            time.sleep(0.1)
        return "Connection secured."
    if low == "weather":
        return f"{random.choice(['☀️ Sunny', '🌧️ Rainy', '⛈️ Stormy'])} ({random.randint(18, 32)}°C) over Shiblanga Metropolis"
    if low == "fortune": return f"🔮 Oracle: \"{random.choice(FORTUNES)}\""
    if low == "system-load":
        out = []
        for n in ("CPU", "RAM", "GPU"):
            p = random.randint(15, 95); out.append(f"{n:<4} [{'█' * (p // 5)}{'░' * (20 - p // 5)}] {p}%")
        return "\n".join(out)
    if low == "disk-space":
        u = random.randint(40, 85)
        return f"Filesystem  Size Used Avail\n/dev/shib1  256G {u}G {256 - u}G\n/dev/shib2  1.2T 112G 1.1T"
    if low.startswith("cowsay"):
        m = cmd.split(maxsplit=1); m = m[1] if len(m) > 1 else "Moo! Shiblanga is awesome!"
        return f" {'_' * (len(m) + 2)}\n< {m} >\n {'-' * (len(m) + 2)}\n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||"
    if low == "greet": return "شبلنجة بترحب بيك! (Shiblanga welcomes you!)"
    return f"{cmd}: command not found (الأوامر الخارجية متقفلة في نسخة الويب).\nجرب -help"


GAME = r"""
<style>html,body{margin:0;height:100%;background:#000;overflow:hidden}
#wrap{position:relative;width:100%;height:100vh;background:#000}
#c{width:100%;height:100%;display:block;cursor:crosshair}
#fs{position:absolute;top:8px;right:8px;z-index:5;background:#ffb300;border:0;border-radius:8px;
padding:6px 12px;font-weight:800;cursor:pointer;font-family:sans-serif}</style>
<div id="wrap"><canvas id="c"></canvas><button id="fs">⛶ Fullscreen (F)</button></div>
<script>
const cv=document.getElementById('c'),g=cv.getContext('2d'),wrap=document.getElementById('wrap');
let W,H,DPR=Math.min(window.devicePixelRatio||1,2);
function resize(){const r=cv.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*DPR;cv.height=H*DPR;g.setTransform(DPR,0,0,DPR,0,0)}
addEventListener('resize',resize);document.addEventListener('fullscreenchange',()=>setTimeout(resize,100));resize();
const R=Math.random,clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),TAU=Math.PI*2;
let AC=null,mute=false;
function snd(f,d,t='square',v=.04,sl=0){if(mute||!AC)return;try{const o=AC.createOscillator(),a=AC.createGain();o.type=t;o.frequency.value=f;
if(sl)o.frequency.exponentialRampToValueAtTime(Math.max(30,f+sl),AC.currentTime+d);a.gain.value=v;
a.gain.exponentialRampToValueAtTime(.0001,AC.currentTime+d);o.connect(a);a.connect(AC.destination);o.start();o.stop(AC.currentTime+d)}catch(e){}}
let hi=0;try{hi=+localStorage.getItem('shib_hi')||0}catch(e){}
let state='menu',score=0,wave=0,t=0,shake=0,combo=0,comboT=0,banner=0;
let P,bul,ch,eggs,items,parts,texts,boss;
let tx=0,ty=0,mx=0,my=0,mouseIn=false;const keys={};
const S=()=>clamp(W/22,30,54);
function startGame(){P={x:W/2,y:H-90,lives:3,shield:0,weapon:1,cool:0,inv:0};tx=P.x;ty=P.y;
bul=[];ch=[];eggs=[];items=[];parts=[];texts=[];boss=null;score=0;wave=0;combo=0;state='play';nextWave()}
function nextWave(){wave++;banner=120;eggs=[];
if(wave%5===0){const mx_=40+wave*12;boss={x:W/2,y:-200,ty:S()*3,hp:mx_,max:mx_,dir:1,sh:0};return}
const cols=Math.min(6+(wave>>1),11),rows=Math.min(2+(wave>>1),5),gap=S()*1.6,hp=1+(wave>>2);
for(let r=0;r<rows;r++)for(let c=0;c<cols;c++)ch.push({c,r,cols,gap,px:W/2,py:-100-r*40,hp,hit:0,diving:false})}
function shoot(){const pat=[[0],[-8,8],[-12,0,12],[-16,-6,6,16],[-22,-11,0,11,22]][P.weapon-1];
pat.forEach(a=>bul.push({x:P.x+a,y:P.y-22,vx:a*.1,vy:-13}));snd(660,.07,'square',.025,-300)}
function burst(x,y,n,cols){for(let i=0;i<n;i++){const a=R()*TAU,s=1+R()*5;
parts.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,l:30+R()*30,c:cols[R()*cols.length|0],z:2+R()*3})}}
function txt(x,y,s,c='#ffd93b'){texts.push({x,y,s,c,l:50})}
function hurt(){if(P.inv>0)return;if(P.shield>0){P.shield--;P.inv=40;snd(200,.2,'sawtooth',.05);return}
P.lives--;P.inv=110;shake=18;combo=0;burst(P.x,P.y,30,['#ff9800','#ffeb3b','#fff']);snd(120,.4,'sawtooth',.08,-60);
if(P.lives<=0){state='over';if(score>hi){hi=score;try{localStorage.setItem('shib_hi',hi)}catch(e){}}}}
function drop(x,y,force){if(!force&&R()>.14)return;const r=R();
items.push({x,y,ty:r<.35?'W':r<.55?'S':r<.7?'L':'F'})}
function kill(k,i){ch.splice(i,1);combo++;comboT=100;const m=Math.min(1+(combo/5|0),5);score+=10*m;
burst(k.px,k.py,18,['#fff','#ffd93b','#ff9800','#ff5252']);snd(300,.15,'triangle',.05,-200);
txt(k.px,k.py-20,R()<.7?'خبيث!':'×'+m);drop(k.px,k.py)}
function update(s){t+=s;
if(keys.ArrowLeft||keys.KeyA)tx-=11*s;if(keys.ArrowRight||keys.KeyD)tx+=11*s;
if(keys.ArrowUp||keys.KeyW)ty-=9*s;if(keys.ArrowDown||keys.KeyS)ty+=9*s;
if(mouseIn){tx=mx;ty=my}tx=clamp(tx,30,W-30);ty=clamp(ty,H*.4,H-50);
P.x+=(tx-P.x)*.3*s;P.y+=(ty-P.y)*.3*s;if(P.inv>0)P.inv-=s;
P.cool-=s;if(P.cool<=0){shoot();P.cool=Math.max(5,14-P.weapon*1.8)}
if(comboT>0){comboT-=s;if(comboT<=0)combo=0}
const sz=S(),ox=Math.sin(t/70)*W*.06;
ch.forEach((k,i)=>{k.hit=Math.max(0,k.hit-s);
if(k.diving){k.py+=(3.5+wave*.15)*s;k.px+=(Math.sin(k.py*.04)*3+(P.x-k.px)*.006)*s;
if(k.py>H+60){k.diving=false;k.py=-60}
if(Math.hypot(k.px-P.x,k.py-P.y)<sz*.8)hurt()}
else{const fx=W/2+(k.c-(k.cols-1)/2)*k.gap+ox,fy=90+k.r*k.gap*.85+Math.sin(t/30+k.c)*6;
k.px+=(fx-k.px)*.1*s;k.py+=(fy-k.py)*.1*s;
if(R()<.0004*(1+wave*.25)*s&&state==='play'&&k.py>40)k.diving=true}
if(R()<.0005*(1+wave*.2)*s&&k.py>30)eggs.push({x:k.px,y:k.py+10,vx:0,vy:3+wave*.1})});
if(boss){const b=boss;b.y+=(b.ty-b.y)*.04*s;b.x+=b.dir*(2+wave*.06)*s;
if(b.x>W-sz*2||b.x<sz*2)b.dir*=-1;b.sh-=s;
if(b.sh<=0&&b.y>sz){b.sh=Math.max(35,70-wave);const n=5+(wave>>2);
for(let i=0;i<n;i++){const a=Math.PI/2+(i-(n-1)/2)*.22;eggs.push({x:b.x,y:b.y+sz,vx:Math.cos(a)*3.5,vy:Math.sin(a)*3.5})}snd(150,.2,'sawtooth',.05)}}
bul.forEach(b=>{b.x+=b.vx*s;b.y+=b.vy*s});
bul=bul.filter(b=>{if(b.y<-20||b.x<-20||b.x>W+20)return false;
if(boss&&Math.hypot(b.x-boss.x,b.y-boss.y)<sz*1.8){boss.hp--;score+=2;burst(b.x,b.y,2,['#ffd93b']);
if(boss.hp<=0){burst(boss.x,boss.y,120,['#fff','#ffd93b','#ff5252','#ff9800']);score+=500;shake=30;
txt(boss.x,boss.y,'BOSS DOWN! +500','#ff5252');for(let i=0;i<4;i++)drop(boss.x+(i-1.5)*40,boss.y,true);boss=null;snd(80,.8,'sawtooth',.1,-40);setTimeout(nextWave,1500)}
return false}
for(let i=0;i<ch.length;i++){const k=ch[i];if(Math.hypot(b.x-k.px,b.y-k.py)<sz*.6){k.hp--;k.hit=5;
if(k.hp<=0)kill(k,i);else burst(b.x,b.y,3,['#fff']);return false}}return true});
eggs.forEach(e=>{e.x+=(e.vx||0)*s;e.y+=e.vy*s;if(Math.hypot(e.x-P.x,e.y-P.y)<sz*.45){hurt();e.y=H+99}});
eggs=eggs.filter(e=>e.y<H+20&&e.x>-20&&e.x<W+20);
items.forEach(it=>{it.y+=2.2*s;if(Math.hypot(it.x-P.x,it.y-P.y)<sz*.8){it.y=H+99;snd(900,.15,'sine',.06,400);
if(it.ty==='W'){P.weapon=Math.min(5,P.weapon+1);txt(P.x,P.y-40,'WEAPON '+P.weapon,'#4fc3f7')}
else if(it.ty==='S'){P.shield=Math.min(3,P.shield+1);txt(P.x,P.y-40,'SHIELD','#4fc3f7')}
else if(it.ty==='L'){P.lives=Math.min(5,P.lives+1);txt(P.x,P.y-40,'+1 LIFE','#ff5252')}
else{score+=50;txt(P.x,P.y-40,'+50 🍗')}}});
items=items.filter(i=>i.y<H+20);
parts.forEach(p=>{p.x+=p.vx*s;p.y+=p.vy*s;p.vy+=.05*s;p.l-=s});parts=parts.filter(p=>p.l>0);
texts.forEach(x=>{x.y-=.8*s;x.l-=s});texts=texts.filter(x=>x.l>0);
shake*=.9;if(banner>0)banner-=s;
if(!ch.length&&!boss&&state==='play'&&!window._wt){window._wt=1;setTimeout(()=>{window._wt=0;if(state==='play'&&!ch.length&&!boss){nextWave()}},1200)}}
const stars=[...Array(120)].map(()=>({x:R(),y:R(),z:.3+R()*2.2}));
function bg(s){const gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,'#0a0a2a');gr.addColorStop(1,'#000');g.fillStyle=gr;g.fillRect(0,0,W,H);
let n=g.createRadialGradient(W*.2,H*.3,0,W*.2,H*.3,W*.4);n.addColorStop(0,'rgba(120,40,180,.25)');n.addColorStop(1,'transparent');g.fillStyle=n;g.fillRect(0,0,W,H);
n=g.createRadialGradient(W*.85,H*.7,0,W*.85,H*.7,W*.35);n.addColorStop(0,'rgba(30,120,200,.22)');n.addColorStop(1,'transparent');g.fillStyle=n;g.fillRect(0,0,W,H);
g.fillStyle='#fff';stars.forEach(o=>{o.y+=o.z*.004*s;if(o.y>1)o.y=0;g.globalAlpha=.4+o.z*.25;g.fillRect(o.x*W,o.y*H,o.z,o.z)});g.globalAlpha=1}
function drawShip(){const k=S()/40;g.save();g.translate(P.x,P.y);g.scale(k,k);if(P.inv>0&&((P.inv/4)|0)%2)g.globalAlpha=.35;
const fl=14+R()*12;g.fillStyle='#ff9800';g.beginPath();g.moveTo(-8,16);g.lineTo(0,16+fl);g.lineTo(8,16);g.fill();
g.fillStyle='#ffeb3b';g.beginPath();g.moveTo(-4,16);g.lineTo(0,16+fl*.6);g.lineTo(4,16);g.fill();
g.fillStyle='#e53935';g.beginPath();g.moveTo(-8,-2);g.lineTo(-30,22);g.lineTo(-10,16);g.fill();g.beginPath();g.moveTo(8,-2);g.lineTo(30,22);g.lineTo(10,16);g.fill();
g.fillStyle='#cfd8dc';g.beginPath();g.moveTo(0,-32);g.lineTo(16,16);g.lineTo(0,9);g.lineTo(-16,16);g.closePath();g.fill();
g.fillStyle='#29b6f6';g.beginPath();g.ellipse(0,-8,4.5,9,0,0,TAU);g.fill();
if(P.shield>0){g.globalAlpha=.5;g.strokeStyle='#4fc3f7';g.lineWidth=3;g.shadowColor='#4fc3f7';g.shadowBlur=15;g.beginPath();g.arc(0,0,40,0,TAU);g.stroke()}
g.restore();g.globalAlpha=1}
function draw(){const sz=S();g.save();if(shake>.5)g.translate((R()-.5)*shake,(R()-.5)*shake);
g.textAlign='center';g.textBaseline='middle';
ch.forEach(k=>{g.font=sz+'px serif';g.save();if(k.hp>1){g.shadowColor='#ff3d3d';g.shadowBlur=14}if(k.hit>0)g.globalAlpha=.5;g.fillText('🐔',k.px,k.py);g.restore()});
if(boss){g.font=sz*3.4+'px serif';g.save();g.shadowColor='#ff3d3d';g.shadowBlur=30;g.fillText('🐓',boss.x,boss.y);g.restore();
const bw=W*.5;g.fillStyle='#300';g.fillRect(W/2-bw/2,50,bw,12);g.fillStyle='#ff3d3d';g.fillRect(W/2-bw/2,50,bw*boss.hp/boss.max,12);
g.strokeStyle='#fff';g.strokeRect(W/2-bw/2,50,bw,12)}
g.font=sz*.55+'px serif';eggs.forEach(e=>g.fillText('🥚',e.x,e.y));
items.forEach(i=>{g.font=sz*.8+'px serif';g.fillText({W:'⚡',S:'🛡️',L:'❤️',F:'🍗'}[i.ty],i.x,i.y)});
bul.forEach(b=>{g.fillStyle='#ff5252';g.shadowColor='#ff1744';g.shadowBlur=10;g.fillRect(b.x-2,b.y,4,16);g.shadowBlur=0});
if(state!=='menu')drawShip();
parts.forEach(p=>{g.globalAlpha=clamp(p.l/30,0,1);g.fillStyle=p.c;g.fillRect(p.x,p.y,p.z,p.z)});g.globalAlpha=1;
g.font='bold 22px sans-serif';texts.forEach(x=>{g.globalAlpha=clamp(x.l/30,0,1);g.fillStyle=x.c;g.fillText(x.s,x.x,x.y)});g.globalAlpha=1;
g.restore();
if(mouseIn){g.strokeStyle='#ffd93b';g.lineWidth=2;g.beginPath();g.arc(mx,my,14,0,TAU);g.moveTo(mx-22,my);g.lineTo(mx-8,my);g.moveTo(mx+8,my);g.lineTo(mx+22,my);g.moveTo(mx,my-22);g.lineTo(mx,my-8);g.moveTo(mx,my+8);g.lineTo(mx,my+22);g.stroke()}
g.textAlign='left';g.fillStyle='#ffd93b';g.font='bold 18px monospace';
if(state!=='menu'){g.fillText('SCORE '+score+'   HI '+hi,14,24);g.fillText('WAVE '+wave+'   WEAPON Lv'+P.weapon+(combo>4?'   COMBO x'+Math.min(1+(combo/5|0),5):''),14,48);
g.fillText('❤'.repeat(Math.max(P.lives,0))+(P.shield>0?'  🛡'.repeat(P.shield):''),14,72)}
g.textAlign='center';
if(banner>0&&state==='play'){g.globalAlpha=clamp(banner/40,0,1);g.fillStyle='#fff';g.font='bold '+W/18+'px sans-serif';g.fillText(wave%5===0?'⚠ BOSS ⚠':'WAVE '+wave,W/2,H/2);g.globalAlpha=1}
const big=(a,b)=>{g.fillStyle='rgba(0,0,0,.6)';g.fillRect(0,0,W,H);g.shadowColor='#ff9800';g.shadowBlur=25;g.fillStyle='#ffd93b';
g.font='900 '+clamp(W/14,28,80)+'px sans-serif';g.fillText(a,W/2,H*.38);g.shadowBlur=0;g.fillStyle='#fff';g.font=clamp(W/45,14,22)+'px sans-serif';
b.split('\n').forEach((l,i)=>g.fillText(l,W/2,H*.52+i*30))};
if(state==='menu')big('🐔 CHICKEN INVADERS 🐔','SHIBLANGA EDITION\nClick / Space للبدء\nماوس أو أسهم للحركة | ضرب أوتوماتيك\nP إيقاف | M صوت | F شاشة كاملة');
if(state==='pause')big('PAUSED','اضغط P أو كليك للمتابعة');
if(state==='over')big('GAME OVER','SCORE '+score+'  |  HI '+hi+'\nClick لإعادة اللعب')}
let last=performance.now();
function loop(n){const s=Math.min((n-last)/16.67,2.5);last=n;
if(state==='play')update(s);bg(state==='play'?s:.3);draw();requestAnimationFrame(loop)}
requestAnimationFrame(loop);
function act(){if(!AC){try{AC=new(window.AudioContext||window.webkitAudioContext)()}catch(e){}}
if(state==='menu'||state==='over')startGame();else if(state==='pause')state='play'}
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();mx=e.clientX-r.left;my=e.clientY-r.top;mouseIn=true});
cv.addEventListener('mouseleave',()=>mouseIn=false);cv.addEventListener('mousedown',act);
cv.addEventListener('touchstart',e=>{act();e.preventDefault()},{passive:false});
cv.addEventListener('touchmove',e=>{const r=cv.getBoundingClientRect(),q=e.touches[0];mx=q.clientX-r.left;my=q.clientY-r.top-70;mouseIn=true;e.preventDefault()},{passive:false});
function fs(){if(!document.fullscreenElement)(wrap.requestFullscreen||wrap.webkitRequestFullscreen).call(wrap);else document.exitFullscreen()}
document.getElementById('fs').onclick=fs;
addEventListener('keydown',e=>{keys[e.code]=true;if(['Space','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();
if(e.code==='KeyP'){if(state==='play')state='pause';else if(state==='pause')state='play'}
if(e.code==='KeyM')mute=!mute;if(e.code==='KeyF')fs();if(e.code==='Space'||e.code==='Enter')act()});
addEventListener('keyup',e=>keys[e.code]=false);
</script>
"""

st.markdown('<div class="title"><span class="chk">🐔</span> SHIBLANGA OS <span class="chk">🐔</span></div>', unsafe_allow_html=True)
st.markdown(f'<div class="warn">{DISCLAIMER}</div>', unsafe_allow_html=True)

if "hist" not in st.session_state:
    st.session_state.hist = ["Welcome to Shiblanga OS v3.0 — اكتب -help"]
if "score" not in st.session_state:
    st.session_state.score = 0

with st.sidebar:
    st.header("🛸 Mission Control")
    st.metric("🍗 Chicken checks", st.session_state.score)
    st.caption("الباروديا ترفيهية، والرسومات emoji بس.")

t1, t2, t3, t4 = st.tabs(["💻 Terminal", "🍽️ Tayebat Lab", "📜 القواعد", "🎮 Chicken Invaders"])

with t1:
    anim = st.empty()
    qc = st.columns(6)
    quick = ["-help", "shiblanga", "diaa el3awady", "diaa-wisdom", "chicken", "rocket"]
    clicked = None
    for col, q in zip(qc, quick):
        if col.button(q, use_container_width=True):
            clicked = q
    with st.form("f", clear_on_submit=True):
        typed = st.text_input("shiblanga@local:~$", placeholder="tayebat-check chicken")
        st.form_submit_button("Run ▶")
    cmd = clicked or typed.strip()
    if cmd:
        if cmd.lower() == "clear":
            st.session_state.hist = ["Terminal cleared."]
        else:
            out = run_command(cmd, anim)
            anim.empty()
            st.session_state.hist.append(f"shiblanga@local:~$ {cmd}\n{out}")
            st.session_state.hist = st.session_state.hist[-25:]
    st.markdown('<div class="term">' + "\n\n".join(st.session_state.hist).replace("<", "&lt;") + "</div>",
                unsafe_allow_html=True)

with t2:
    st.subheader("🔬 طيب ولا خبيث؟")
    food = st.text_input("اكتب الأكلة (عربي أو English)")
    if food:
        st.session_state.score += 1
        r = check_food(food)
        if r == "طيب":
            st.markdown(f'<div class="good">✅ <b>{food}</b> → طيّبة (حسب القوائم المتداولة)</div>', unsafe_allow_html=True)
        elif r == "خبيث":
            st.markdown(f'<div class="bad">🚫 <b>{food}</b> → خبيثة<br>{random.choice(FUNNY)}</div>', unsafe_allow_html=True)
        else:
            st.info("مش في القائمة المختصرة.")
    c1, c2 = st.columns(2)
    c1.success("✅ " + "، ".join(sorted({k for k, v in TAYEBAT.items() if v == "طيب" and not k.isascii()})))
    c2.error("🚫 " + "، ".join(sorted({k for k, v in TAYEBAT.items() if v == "خبيث" and not k.isascii()})))
    if st.button("🍽️ وجبة عشوائية"):
        st.write(run_command("tayebat-meal", st.empty()))
    h = st.radio("فحص سريع", ["🤤 جعان؟", "💧 عطشان؟"], horizontal=True)
    if st.button("افحص"):
        st.write(run_command("hungry" if "جعان" in h else "thirsty", st.empty()))

with t3:
    st.subheader("📜 قواعد نظام الطيبات (المتداولة)")
    for i, l in enumerate(LAWS, 1):
        st.markdown(f"**{i}.** {l}")
    st.markdown(f'<div class="warn">{DISCLAIMER}</div>', unsafe_allow_html=True)
    st.code(DIAA, language=None)

with t4:
    st.subheader("🚀 Chicken Invaders: Shiblanga Edition")
    components.html(GAME, height=780)
