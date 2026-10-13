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
        return "🍽️ " + " + ".join([random.choice(["rice","potato","bulgur","freekeh"]),
               random.choice(["beef","lamb","كوارع"]), random.choice(["ghee","butter","olive oil"]),
               random.choice(["dates","fruit"])])
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
        return f"{random.choice(['☀️ Sunny','🌧️ Rainy','⛈️ Stormy'])} ({random.randint(18,32)}°C) over Shiblanga Metropolis"
    if low == "fortune": return f"🔮 Oracle: \"{random.choice(FORTUNES)}\""
    if low == "system-load":
        out = []
        for n in ("CPU", "RAM", "GPU"):
            p = random.randint(15, 95); out.append(f"{n:<4} [{'█'*(p//5)}{'░'*(20-p//5)}] {p}%")
        return "\n".join(out)
    if low == "disk-space":
        u = random.randint(40, 85)
        return f"Filesystem  Size Used Avail\n/dev/shib1  256G {u}G {256-u}G\n/dev/shib2  1.2T 112G 1.1T"
    if low.startswith("cowsay"):
        m = cmd.split(maxsplit=1); m = m[1] if len(m) > 1 else "Moo! Shiblanga is awesome!"
        return f" {'_'*(len(m)+2)}\n< {m} >\n {'-'*(len(m)+2)}\n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||"
    if low == "greet": return "شبلنجة بترحب بيك! (Shiblanga welcomes you!)"
    return f"{cmd}: command not found (الأوامر الخارجية متقفلة في نسخة الويب).\nجرب -help"

GAME = """
<canvas id="c" width="720" height="460" style="background:#05070d;border:3px solid #ffd93b;border-radius:12px;width:100%;cursor:none"></canvas>
<script>
const c=document.getElementById('c'),x=c.getContext('2d');let ship=360,bul=[],ch=[],eggs=[],score=0,lives=3,wave=1,over=false,fire=0;
function spawn(){ch=[];for(let r=0;r<3+Math.min(wave,3);r++)for(let i=0;i<8;i++)ch.push({x:60+i*80,y:40+r*50,dx:1+wave*0.2,hp:1})}
spawn();
c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect();ship=(e.clientX-r.left)*c.width/r.width});
c.addEventListener('mousedown',()=>{if(over){score=0;lives=3;wave=1;over=false;eggs=[];spawn()}else bul.push({x:ship,y:410})});
document.addEventListener('keydown',e=>{if(e.code=='Space'){bul.push({x:ship,y:410});e.preventDefault()}if(e.code=='ArrowLeft')ship-=25;if(e.code=='ArrowRight')ship+=25});
let stars=[...Array(70)].map(()=>({x:Math.random()*720,y:Math.random()*460,s:Math.random()*2+.5}));
function loop(){x.clearRect(0,0,720,460);x.fillStyle='#fff';stars.forEach(s=>{s.y=(s.y+s.s)%460;x.fillRect(s.x,s.y,s.s,s.s)});
x.font='30px serif';x.textAlign='center';
let edge=false;ch.forEach(k=>{k.x+=k.dx;if(k.x>690||k.x<30)edge=true});
if(edge)ch.forEach(k=>{k.dx*=-1;k.y+=14});
ch.forEach(k=>{x.fillText('🐔',k.x,k.y);if(Math.random()<0.0007*wave)eggs.push({x:k.x,y:k.y});if(k.y>400&&!over){lives=0}});
bul.forEach(b=>{b.y-=9;x.fillStyle='#ff5252';x.fillRect(b.x-2,b.y,4,14)});
bul=bul.filter(b=>{let hit=false;ch=ch.filter(k=>{if(!hit&&Math.abs(k.x-b.x)<20&&Math.abs(k.y-b.y)<20){hit=true;score+=10;x.fillText('🍗',k.x,k.y);return false}return true});return !hit&&b.y>0});
eggs.forEach(e=>{e.y+=4;x.fillText('🥚',e.x,e.y);if(Math.abs(e.x-ship)<20&&e.y>400){lives--;e.y=999}});eggs=eggs.filter(e=>e.y<460);
x.fillText('🚀',ship,435);
if(!ch.length&&!over){wave++;spawn()}
if(lives<=0)over=true;
x.fillStyle='#ffd93b';x.font='16px monospace';x.textAlign='left';x.fillText('SCORE '+score+'   LIVES '+'❤'.repeat(Math.max(lives,0))+'   WAVE '+wave,10,22);
if(over){x.textAlign='center';x.font='34px monospace';x.fillText('GAME OVER - click to restart',360,230)}
requestAnimationFrame(loop)}loop();
</script>
<p style="color:#ccc;font-family:sans-serif;direction:rtl">الماوس: حرّك وكليك للضرب | Space: ضرب | الأسهم: حركة</p>
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
        if col.button(q, use_container_width=True): clicked = q
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
    st.markdown('<div class="term">' + "\n\n".join(st.session_state.hist).replace("<", "&lt;") + "</div>", unsafe_allow_html=True)

with t2:
    st.subheader("🔬 طيب ولا خبيث؟")
    food = st.text_input("اكتب الأكلة (عربي أو English)")
    if food:
        st.session_state.score += 1
        r = check_food(food)
        if r == "طيب": st.markdown(f'<div class="good">✅ <b>{food}</b> → طيّبة (حسب القوائم المتداولة)</div>', unsafe_allow_html=True)
        elif r == "خبيث": st.markdown(f'<div class="bad">🚫 <b>{food}</b> → خبيثة<br>{random.choice(FUNNY)}</div>', unsafe_allow_html=True)
        else: st.info("مش في القائمة المختصرة.")
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
    st.subheader("🚀 Chicken Invaders (نسخة مصغّرة)")
    components.html(GAME, height=560)
