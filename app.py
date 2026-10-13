# app.py  →  pip install streamlit  →  streamlit run app.py
import ast, difflib, html, json, operator, random, re, secrets, threading, time
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Shiblanga OS: Chicken Invaders Edition", page_icon="🐔", layout="wide")

# ----------------------------------------------------------------------------
# Themes
# ----------------------------------------------------------------------------
THEMES = {
    "Dark 🌌": dict(acc="#ffd93b", glow="#ff9800", bg1="#1b2735", bg2="#090a0f", txt="#e8f1ff", term="#7CFC9A", crt=""),
    "Neon 💜": dict(acc="#ff4de1", glow="#00e5ff", bg1="#2a0845", bg2="#050014", txt="#f3e8ff", term="#00f5ff", crt=""),
    "Retro CRT 📺": dict(acc="#39ff14", glow="#1faa00", bg1="#04170a", bg2="#000", txt="#b6ffb0", term="#39ff14",
                         crt=".stApp::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:99;"
                             "background:repeating-linear-gradient(0deg,rgba(0,0,0,.28) 0,rgba(0,0,0,.28) 1px,transparent 1px,transparent 3px)}"),
}
DIFFS = {"Easy": dict(key="Easy", name="EASY", lives=5, fire=.6, spd=.85, hp=.8),
         "Normal": dict(key="Normal", name="NORMAL", lives=3, fire=1, spd=1, hp=1),
         "Hard": dict(key="Hard", name="HARD", lives=2, fire=1.5, spd=1.2, hp=1.3)}

ss = st.session_state
qp_name = st.query_params.get("p", "")
ss.setdefault("player", re.sub(r"[^\w\s\-.]", "", qp_name, flags=re.UNICODE).strip()[:16] or None)

with st.sidebar:
    st.header("🛸 Mission Control")
    theme = THEMES[st.selectbox("🎨 Theme", list(THEMES))]
    diff_name = st.selectbox("🎚️ الصعوبة", list(DIFFS), index=1,
                             format_func=lambda d: {"Easy": "Easy 😊", "Normal": "Normal 😎", "Hard": "Hard 🔥"}[d])
    st.divider()
    if ss.player:
        st.markdown(f"👤 **{html.escape(ss.player)}**")
        if st.button("✏️ غيّر الاسم", use_container_width=True):
            ss.player = None
            st.query_params.clear()
            st.rerun()
    side_slot = st.container()   # بيتملي في آخر السكريبت عشان يبقى محدّث

CSS = """
<style>
:root{--acc:%ACC%;--glow:%GLOW%;--txt:%TXT%;--term:%TERM%}
.stApp{background:radial-gradient(ellipse at bottom,%BG1% 0%,%BG2% 100%);color:var(--txt)}
[data-testid=stSidebar]{background:rgba(5,7,13,.72);backdrop-filter:blur(10px);border-right:1px solid rgba(255,255,255,.08)}
.block-container{padding-top:1.4rem;max-width:1250px}
.stars,.stars2{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;
 background-repeat:repeat;animation:move 60s linear infinite}
.stars{background-image:radial-gradient(2px 2px at 20px 30px,#fff,transparent),
 radial-gradient(1.5px 1.5px at 120px 90px,#ffe9a8,transparent),
 radial-gradient(2px 2px at 220px 160px,#fff,transparent);background-size:250px 200px}
.stars2{background-image:radial-gradient(1px 1px at 60px 120px,#9fd3ff,transparent),
 radial-gradient(1px 1px at 180px 40px,#fff,transparent);background-size:180px 150px;animation-duration:110s}
@keyframes move{from{background-position:0 0}to{background-position:0 1000px}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes pulse{0%,100%{text-shadow:0 0 12px var(--glow),0 0 30px var(--glow)}50%{text-shadow:0 0 22px var(--acc),0 0 50px var(--glow)}}
@keyframes pop{0%{transform:scale(.8);opacity:0}100%{transform:scale(1);opacity:1}}
.title{font-size:46px;font-weight:900;text-align:center;color:var(--acc);animation:pulse 3s ease-in-out infinite;letter-spacing:2px}
.subtitle{text-align:center;opacity:.75;margin:-4px 0 14px;font-size:15px}
.chk{font-size:40px;display:inline-block;animation:float 2s ease-in-out infinite}
.glass{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:16px;
 backdrop-filter:blur(8px);box-shadow:0 6px 24px rgba(0,0,0,.35)}
.term{background:#05070dcc;border:2px solid var(--acc);border-radius:12px;padding:14px;
 font-family:monospace;color:var(--term);white-space:pre-wrap;max-height:430px;overflow:auto;
 box-shadow:0 0 18px var(--glow);direction:ltr;text-align:left}
.good{border-left:6px solid #4caf50;background:#10301a;padding:10px;border-radius:8px}
.bad{border-left:6px solid #ff3d3d;background:#3a1010;padding:10px;border-radius:8px}
.warn{background:#3a2a05;border:1px solid #ffb300;padding:10px;border-radius:8px;color:#ffe9b0}
div.stButton>button,div.stFormSubmitButton>button{background:linear-gradient(var(--acc),var(--glow));color:#111;font-weight:800;border:0;border-radius:10px;transition:.15s}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{transform:translateY(-2px) scale(1.03);box-shadow:0 0 14px var(--glow);color:#000}
.stTextInput input{border-radius:10px}
.stTabs [data-baseweb=tab-list]{gap:8px}
.stTabs [data-baseweb=tab]{font-weight:700;background:rgba(255,255,255,.05);border-radius:10px 10px 0 0;padding:8px 16px}
.stTabs [aria-selected=true]{background:rgba(255,255,255,.14);color:var(--acc)}
[data-testid=stMetric]{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:10px 14px}
/* name card */
.namecard{text-align:center;padding:26px 18px;animation:pop .4s ease}
.namecard h2{color:var(--acc);margin:0 0 6px}
/* result card */
.res{border-radius:14px;padding:14px 18px;margin:10px 0;animation:pop .4s ease;border:1px solid rgba(255,255,255,.15);
 background:linear-gradient(135deg,rgba(255,217,59,.15),rgba(255,152,0,.08))}
.res.nb{border-color:var(--acc);box-shadow:0 0 22px var(--glow)}
.res b{color:var(--acc)}
/* podium */
.podium{display:flex;justify-content:center;align-items:flex-end;gap:12px;margin:18px 0 12px;flex-wrap:wrap}
.pod{flex:1;min-width:130px;max-width:230px;text-align:center;padding:14px 10px;border-radius:16px 16px 6px 6px;
 border:1px solid rgba(255,255,255,.18);animation:pop .5s ease;backdrop-filter:blur(6px)}
.pod .medal{font-size:38px}.pod .pn{font-weight:800;font-size:18px;word-break:break-word}
.pod .ps{font-size:26px;font-weight:900;font-family:monospace}.pod .pm{font-size:12px;opacity:.75}
.pod.gold{min-height:200px;background:linear-gradient(#ffd93b55,#ffd93b11);box-shadow:0 0 24px #ffd93b66}
.pod.silver{min-height:165px;background:linear-gradient(#cfd8dc55,#cfd8dc11)}
.pod.bronze{min-height:140px;background:linear-gradient(#cd7f3255,#cd7f3211)}
.pod.you{outline:2px solid var(--acc)}
.lb{width:100%;border-collapse:collapse;margin-top:8px;direction:ltr}
.lb th{font-size:12px;text-transform:uppercase;letter-spacing:1px;opacity:.65;padding:8px;text-align:left}
.lb td{padding:9px 8px;border-top:1px solid rgba(255,255,255,.08)}
.lb tr.you td{background:rgba(255,217,59,.16);font-weight:800}
.lb td.sc{font-family:monospace;font-weight:800;color:var(--acc)}
%CRT%
</style><div class="stars"></div><div class="stars2"></div>
"""
for k, v in {"%ACC%": theme["acc"], "%GLOW%": theme["glow"], "%TXT%": theme["txt"], "%TERM%": theme["term"],
             "%BG1%": theme["bg1"], "%BG2%": theme["bg2"], "%CRT%": theme["crt"]}.items():
    CSS = CSS.replace(k, v)
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------
TAYEBAT = {
    "rice": "طيب", "رز": "طيب", "أرز": "طيب", "potato": "طيب", "بطاطس": "طيب", "beef": "طيب", "لحمة": "طيب",
    "lamb": "طيب", "كوارع": "طيب", "ghee": "طيب", "سمن": "طيب", "butter": "طيب", "زبدة": "طيب",
    "olive oil": "طيب", "زيت زيتون": "طيب", "dates": "طيب", "تمر": "طيب", "sugar": "طيب", "سكر": "طيب",
    "cheddar": "طيب", "gouda": "طيب", "mozzarella": "طيب", "parmesan": "طيب", "رومي": "طيب",
    "corn": "طيب", "درة": "طيب", "bulgur": "طيب", "freekeh": "طيب", "فريك": "طيب",
    "bran toast": "طيب", "توست نخالة": "طيب", "fruit": "طيب", "فاكهة": "طيب",
    "honey": "طيب", "عسل": "طيب", "banana": "طيب", "موز": "طيب", "apple": "طيب", "تفاح": "طيب",
    "mango": "طيب", "مانجو": "طيب", "grapes": "طيب", "عنب": "طيب", "liver": "طيب", "كبدة": "طيب",
    "chicken": "خبيث", "فراخ": "خبيث", "دجاج": "خبيث", "egg": "خبيث", "بيض": "خبيث", "milk": "خبيث",
    "لبن": "خبيث", "حليب": "خبيث", "yogurt": "خبيث", "زبادي": "خبيث", "lentils": "خبيث", "عدس": "خبيث",
    "beans": "خبيث", "فول": "خبيث", "tomato": "خبيث", "طماطم": "خبيث", "onion": "خبيث", "بصل": "خبيث",
    "salad": "خبيث", "سلطة": "خبيث", "جرجير": "خبيث", "vegetable oil": "خبيث", "زيت نباتي": "خبيث",
    "bread": "خبيث", "عيش": "خبيث", "hummus": "خبيث", "حمص": "خبيث", "cucumber": "خبيث", "خيار": "خبيث",
    "pepper": "خبيث", "فلفل": "خبيث", "lettuce": "خبيث", "خس": "خبيث", "chickpeas": "خبيث", "ترمس": "خبيث",
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
JOKES = ["ليه المبرمج بيفضل في الضلمة؟ عشان الـ light mode بتأذي الـ bugs.",
         "الفراخ دخلت الـ terminal وقالت: sudo give me rice.",
         "قالوا للـ git: إيه اللي بيحصل؟ قال: merge conflict في المطبخ.",
         "فيه مبرمجين بيعدّوا من 0، وفيه ناس بتعدّي الطيبات من 1."]
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

# ----------------------------------------------------------------------------
# Food matching: normalised, whole-word, plural-tolerant, fuzzy
# ----------------------------------------------------------------------------
_AR_DIAC = re.compile(r"[\u064B-\u0652\u0640]")


def norm(s):
    s = _AR_DIAC.sub("", s.lower().strip())
    s = re.sub("[أإآ]", "ا", s).replace("ة", "ه").replace("ى", "ي")
    words = re.findall(r"\w+", s)
    return " ".join(w[2:] if w.startswith("ال") and len(w) > 3 else w for w in words)


NORM = {norm(k): v for k, v in TAYEBAT.items()}
NORM_KEYS = sorted(NORM, key=len, reverse=True)


def check_food(q):
    """Returns (verdict, matched_key_or_None, fuzzy_flag)."""
    n = norm(q)
    if not n:
        return None, None, False
    sing = " ".join(w[:-1] if w.isascii() and w.endswith("s") and len(w) > 3 else w for w in n.split())
    for cand in dict.fromkeys([n, sing]):
        if cand in NORM:
            return NORM[cand], cand, False
        for k in NORM_KEYS:
            if re.search(rf"(?<!\w){re.escape(k)}(?!\w)", cand):
                return NORM[k], k, False
    if len(n) >= 3:
        m = difflib.get_close_matches(sing, NORM_KEYS, 1, 0.78)
        if m:
            return NORM[m[0]], m[0], True
    return None, None, False


# ----------------------------------------------------------------------------
# Terminal
# ----------------------------------------------------------------------------
COMMANDS = ["-help", "info", "shiblanga", "diaa el3awady", "diaa-wisdom", "no2ta", "nizam-el-tayebat",
            "tayebat-check", "tayebat-menu", "tayebat-meal", "hungry", "thirsty", "chicken", "rocket", "matrix",
            "weather", "fortune", "system-load", "disk-space", "cowsay", "greet", "disclaimer", "clear",
            "history", "calc", "joke", "date", "neofetch", "sudo", "konami", "whoami"]
HELP = """-help              : القائمة دي
info / neofetch    : معلومات النظام
whoami             : انت مين؟
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
calc 2+2*3         : آلة حاسبة
joke / date / history
weather / fortune / system-load / disk-space
cowsay X / greet / disclaimer / sudo / clear"""

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv, ast.USub: operator.neg}


def safe_calc(expr):
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Pow) and abs(b) > 100: raise ValueError("أس كبير")
            return _OPS[type(n.op)](a, b)
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS: return _OPS[type(n.op)](ev(n.operand))
        raise ValueError("تعبير غير مسموح")
    try:
        return str(ev(ast.parse(expr.strip(), mode="eval").body))
    except Exception as e:
        return f"calc error: {e}"


def run_command(cmd, anim):
    low = cmd.lower().strip()
    if low in ("-help", "--help", "help"): return HELP
    if low == "info": return "[Shiblanga OS v5.0]\nStatus: Active\nKernel: Streamlit Simulated Shell\nTheme: Chicken Invaders Edition 🐔"
    if low == "whoami": return f"👤 {ss.get('player') or 'guest'} @ shiblanga-os"
    if low == "neofetch":
        return (f"   ,~.      shiblanga@local\n  (o o)>    ---------------\n  ( V )     OS: Shiblanga OS v5.0\n"
                f"  -\"-\"-     Shell: streamlit-sh\n            Uptime: {random.randint(1, 99)} mins\n"
                f"            Eggs: {random.randint(0, 999)}\n            Mood: {random.choice(['جعان', 'مبرمج', 'متحمس'])}")
    if low == "shiblanga": return SHIB
    if low == "diaa el3awady": return DIAA
    if low == "diaa-wisdom": return f"💡 حكمة (باروديا): \"{random.choice(WISDOM)}\""
    if low == "joke": return "😂 " + random.choice(JOKES)
    if low == "date": return datetime.now().strftime("%A %d %B %Y — %H:%M:%S")
    if low == "history":
        h = ss.get("cmds", [])
        return "\n".join(f"{i}  {c}" for i, c in enumerate(h, 1)) or "(فاضي)"
    if low.startswith("sudo"):
        return random.choice(["sudo: انت مش في ملف الـ sudoers.. الحادثة هتتبلغ للفراخ 🐔",
                              "Permission denied: الرز محجوز للمشرفين فقط 🍚",
                              "sudo make me a sandwich → خبيث! رفض."])
    if low == "konami": return "↑ ↑ ↓ ↓ ← → ← → B A  (جرّبها جوه اللعبة 😉)"
    if low.startswith("calc"):
        e = cmd[4:].strip()
        return safe_calc(e) if e else "الاستخدام: calc 2+2*3"
    if low == "no2ta":
        for i in range(1, 6):
            anim.code("." * i); time.sleep(0.35)
        return "Scan complete. One critical dot found: (.) -> Everything is in equilibrium."
    if low == "nizam-el-tayebat": return "\n".join(f"{i}. {l}" for i, l in enumerate(LAWS, 1)) + "\n\n" + DISCLAIMER
    if low.startswith("tayebat-check"):
        q = cmd[len("tayebat-check"):].strip()
        if not q: return "الاستخدام: tayebat-check <اسم الأكلة>"
        r, key, fz = check_food(q)
        if r is None: return f"'{q}': مش في القائمة المختصرة. القوائم بتختلف من مصدر لمصدر."
        note = f" (قصدك '{key}'؟)" if fz else ""
        return f"✅ '{q}' → طيّبة{note}" if r == "طيب" else f"🚫 '{q}' → خبيثة{note}\n{random.choice(FUNNY)}"
    if low == "tayebat-menu":
        g = sorted({k for k, v in TAYEBAT.items() if v == "طيب" and k.isascii()})
        b = sorted({k for k, v in TAYEBAT.items() if v == "خبيث" and k.isascii()})
        return "✅ طيبات: " + ", ".join(g) + "\n🚫 خبائث: " + ", ".join(b)
    if low == "tayebat-meal":
        return "🍽️ " + " + ".join([random.choice(["rice", "potato", "bulgur", "freekeh"]),
                                    random.choice(["beef", "lamb", "كوارع"]),
                                    random.choice(["ghee", "butter", "olive oil"]),
                                    random.choice(["dates", "fruit"])])
    if low == "hungry":
        for i in range(3):
            anim.code("." * (i + 1)); time.sleep(0.4)
        return random.choice(["✅ جعان بجد → كُل.", "❌ ده ملل مش جوع → سيب الأكل.", "🤔 اشرب مياه وبعدين قرر."])
    if low == "thirsty": return random.choice(["💧 عطشان فعلاً → اشرب.", "❌ مش عطشان → متشربش بالعافية."])
    if low == "disclaimer": return DISCLAIMER
    if low == "chicken":
        for s in ["🐔 فراخ اتكشفت في الـ buffer!", "Scanning protein source...", "Classification: خبيث", "Quarantine..."]:
            anim.code(s); time.sleep(0.6)
        return "🐔 الفراخ اتحجرت. استبدلها بـ رز وكوارع (باروديا) 🍚"
    if low == "rocket":
        for c in (3, 2, 1):
            anim.code(f"T-minus {c}..."); time.sleep(0.5)
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
            p = random.randint(15, 95)
            out.append(f"{n:<4} [{'█' * (p // 5)}{'░' * (20 - p // 5)}] {p}%")
        return "\n".join(out)
    if low == "disk-space":
        u = random.randint(40, 85)
        return f"Filesystem  Size Used Avail\n/dev/shib1  256G {u}G {256 - u}G\n/dev/shib2  1.2T 112G 1.1T"
    if low.startswith("cowsay"):
        parts = cmd.split(maxsplit=1)
        m = parts[1] if len(parts) > 1 else "Moo! Shiblanga is awesome!"
        return (f" {'_' * (len(m) + 2)}\n< {m} >\n {'-' * (len(m) + 2)}\n"
                "        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n"
                "                ||----w |\n                ||     ||")
    if low == "greet": return f"شبلنجة بترحب بيك يا {ss.get('player') or 'غريب'}! (Shiblanga welcomes you!)"
    sug = difflib.get_close_matches(low.split()[0], COMMANDS, 3, 0.5) or [c for c in COMMANDS if c.startswith(low[:2])][:3]
    hint = ("\nتقصد: " + " ، ".join(sug) + " ؟") if sug else "\nجرب -help"
    return f"{cmd}: command not found (الأوامر الخارجية متقفلة في نسخة الويب).{hint}"


def boot(anim):
    lines = ["[ OK ] Loading kernel: shiblanga-5.0", "[ OK ] Mounting /dev/rice", "[ OK ] Starting egg-daemon",
             "[ OK ] Quarantining chickens 🐔", "[ OK ] Warming up spaceship 🚀", "Welcome to Shiblanga OS v5.0"]
    for i in range(1, len(lines) + 1):
        anim.code("\n".join(lines[:i])); time.sleep(0.25)


# ----------------------------------------------------------------------------
# Leaderboard: best score per (player, difficulty), saved automatically
# ----------------------------------------------------------------------------
SC_FILE = Path(__file__).with_name("scores.json")
_LOCK = threading.Lock()


def load_scores():
    try:
        d = json.loads(SC_FILE.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _write_scores(data):
    tmp = SC_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(SC_FILE)


def submit_score(name, score, wave, diff):
    """Keeps only the player's best per difficulty. Returns (record, is_new_best, previous_best)."""
    key = name.casefold()
    now = datetime.now().strftime("%Y-%m-%d")
    with _LOCK:
        data = load_scores()
        rec = next((r for r in data if r["name"].casefold() == key and r["diff"] == diff), None)
        prev = rec["score"] if rec else 0
        new_best = False
        if rec is None:
            rec = dict(name=name, diff=diff, score=score, wave=wave, games=1, date=now)
            data.append(rec)
            new_best = True
        else:
            rec["games"] = rec.get("games", 1) + 1
            if score > rec["score"]:
                rec.update(score=score, wave=wave, date=now)
                new_best = True
        try:
            _write_scores(data)
        except Exception:
            st.warning("مقدرتش أحفظ الملف (مفيش صلاحية كتابة).")
    return rec, new_best, prev


def board(diff="All"):
    best = {}
    for r in load_scores():
        if diff != "All" and r.get("diff") != diff:
            continue
        k = r["name"].casefold()
        if k not in best or r["score"] > best[k]["score"]:
            best[k] = r
    return sorted(best.values(), key=lambda r: (-r["score"], r.get("date", "")))


def player_stats(name):
    k = (name or "").casefold()
    recs = [r for r in load_scores() if r["name"].casefold() == k]
    return recs


def board_html(rows, me):
    me_k = (me or "").casefold()
    top, rest = rows[:3], rows[3:15]
    pod = ""
    for idx in (1, 0, 2):
        if idx < len(top):
            r = top[idx]
            cls = ["gold", "silver", "bronze"][idx]
            you = " you" if r["name"].casefold() == me_k else ""
            pod += (f'<div class="pod {cls}{you}"><div class="medal">{["🥇", "🥈", "🥉"][idx]}</div>'
                    f'<div class="pn">{html.escape(r["name"])}</div><div class="ps">{r["score"]:,}</div>'
                    f'<div class="pm">{html.escape(r["diff"])} · Wave {r.get("wave", 0)}</div></div>')
    out = f'<div class="podium">{pod}</div>'
    if rest:
        trs = ""
        for i, r in enumerate(rest, 4):
            you = ' class="you"' if r["name"].casefold() == me_k else ""
            trs += (f'<tr{you}><td>{i}</td><td>{html.escape(r["name"])}</td><td class="sc">{r["score"]:,}</td>'
                    f'<td>{html.escape(r["diff"])}</td><td>{r.get("wave", 0)}</td><td>{html.escape(str(r.get("date", "")))}</td></tr>')
        out += ('<div class="glass"><table class="lb"><tr><th>#</th><th>Player</th><th>Score</th><th>Mode</th>'
                f'<th>Wave</th><th>Date</th></tr>{trs}</table></div>')
    return out


# ----------------------------------------------------------------------------
# Game component: HTML5 canvas that reports the score back to Python by itself
# ----------------------------------------------------------------------------
GAME = r"""
<style>
html,body{margin:0;height:100%;background:#000;overflow:hidden;font-family:sans-serif}
#wrap{position:relative;width:100%;height:100vh;min-height:300px;background:#000}
#c{position:absolute;inset:0;width:100%;height:100%;display:block;cursor:crosshair;outline:none}
.btn{position:absolute;z-index:5;border:0;border-radius:8px;padding:6px 12px;font-weight:800;cursor:pointer;background:#ffb300}
#fs{top:8px;right:8px}#bb{bottom:10px;right:10px;font-size:18px}
#err{position:absolute;left:0;right:0;top:0;z-index:9;background:#7a0000;color:#fff;font:12px monospace;padding:8px;display:none;white-space:pre-wrap}
#toast{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);z-index:6;background:#000a;color:#ffd93b;padding:6px 14px;border-radius:8px;font-size:14px;display:none}
</style>
<div id="wrap"><canvas id="c" tabindex="0"></canvas>
<button id="fs" class="btn">⛶ Fullscreen (F)</button><button id="bb" class="btn">💣 (B)</button>
<div id="err"></div><div id="toast"></div></div>
<script>
(function(){
// ---------- Streamlit component protocol ----------
function send(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data||{}),'*')}
let DIFF={key:'Normal',name:'NORMAL',lives:3,fire:1,spd:1,hp:1},NEXT=DIFF,NAME='Player',BEST=0,NONCE='',RUN='',playT=0,newBest=false;
window.addEventListener('message',e=>{
  const d=e.data;if(!d||d.type!=='streamlit:render')return;const a=d.args||{};
  if(a.diff)NEXT=a.diff;
  if(a.name!==undefined){if(a.name!==NAME)BEST=0;NAME=a.name}
  BEST=Math.max(BEST,+a.best||0);NONCE=a.nonce||NONCE});
send('streamlit:componentReady',{apiVersion:1});
send('streamlit:setFrameHeight',{height:720});

const cv=document.getElementById('c'),g=cv.getContext('2d'),wrap=document.getElementById('wrap');
const errBox=document.getElementById('err'),toastBox=document.getElementById('toast');
window.addEventListener('error',e=>{errBox.style.display='block';errBox.textContent='JS error: '+e.message+' (line '+e.lineno+')'});
function toast(m){toastBox.textContent=m;toastBox.style.display='block';clearTimeout(toast._t);toast._t=setTimeout(()=>toastBox.style.display='none',2200)}
const R=Math.random,clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),TAU=Math.PI*2;
let W=0,H=0,DPR=1,P=null,tx=0,ty=0;
function resize(){const r=wrap.getBoundingClientRect(),w=Math.floor(r.width),h=Math.floor(r.height);
  if(w<20||h<20)return false;if(w===W&&h===H)return true;
  W=w;H=h;DPR=Math.min(window.devicePixelRatio||1,2);cv.width=Math.floor(W*DPR);cv.height=Math.floor(H*DPR);g.setTransform(DPR,0,0,DPR,0,0);
  if(P){P.x=clamp(P.x,30,W-30);P.y=clamp(P.y,H*.4,H-50);tx=P.x;ty=P.y}return true}
if(window.ResizeObserver)new ResizeObserver(()=>resize()).observe(wrap);
addEventListener('resize',resize);document.addEventListener('fullscreenchange',()=>setTimeout(resize,100));

// ---------- audio ----------
let AC=null,mute=false,musicT=null;
function snd(f,d,t,v,sl){t=t||'square';v=v||.04;sl=sl||0;if(mute||!AC)return;
  try{const o=AC.createOscillator(),a=AC.createGain();o.type=t;o.frequency.value=f;
  if(sl)o.frequency.exponentialRampToValueAtTime(Math.max(30,f+sl),AC.currentTime+d);
  a.gain.value=v;a.gain.exponentialRampToValueAtTime(.0001,AC.currentTime+d);o.connect(a);a.connect(AC.destination);o.start();o.stop(AC.currentTime+d)}catch(e){}}
function startMusic(){if(musicT||!AC)return;const n=[110,110,165,131,110,110,196,165],m=[440,523,659,523,440,392,440,523];let i=0;
  musicT=setInterval(()=>{if(state==='play'){const k=boss?1.5:1;snd(n[i%8]*k,.2,'triangle',.035);if(i%2===0)snd(m[(i>>1)%8]*k,.1,'square',.008)}i++},230)}
const WSND=['square','square','sawtooth','sawtooth','triangle'];

// ---------- state ----------
let state='menu',score=0,wave=0,t=0,shake=0,flash=0,combo=0,comboT=0,banner=0,overAt=0,waveTimer=0;
let bul=[],ch=[],eggs=[],items=[],parts=[],texts=[],boss=null,mx=0,my=0,mouseIn=false;const keys={};
const S=()=>clamp(W/22,30,54);
const T={n:{e:'🐔',hp:0,fire:1,dive:1},f:{e:'🐤',hp:0,fire:.5,dive:3},t:{e:'🦃',hp:2,fire:1.6,dive:.4}};

function startGame(){
  DIFF=NEXT;RUN=Date.now().toString(36)+R().toString(36).slice(2,10);playT=0;newBest=false;
  P={x:W/2,y:H-90,lives:DIFF.lives,shield:0,weapon:1,cool:0,inv:60,bombs:2,freeze:0,magnet:0,laser:0};tx=P.x;ty=P.y;
  bul=[];ch=[];eggs=[];items=[];parts=[];texts=[];boss=null;score=0;wave=0;combo=0;waveTimer=0;state='play';startMusic();nextWave()}
function finish(){
  state='over';overAt=performance.now();newBest=score>BEST;if(newBest)BEST=score;
  // الاسكور بيتبعت تلقائي لبايثون: مفيش إدخال يدوي
  send('streamlit:setComponentValue',{dataType:'json',value:{run:RUN,name:NAME,score:score,wave:wave,secs:Math.round(playT*10)/10,nonce:NONCE,diff:DIFF.key}})}
function nextWave(){
  wave++;banner=120;eggs=[];waveTimer=0;
  if(wave%5===0){const m=Math.round((40+wave*12)*DIFF.hp);boss={x:W/2,y:-200,ty:S()*3,hp:m,max:m,dir:1,sh:0,ph:1};return}
  const cols=Math.min(6+(wave>>1),11),rows=Math.min(2+(wave>>1),5),gap=S()*1.6,hp=1+(wave>>2);
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){
    const ty_=(r===0&&wave>2)?'t':(c%3===0&&wave>1)?'f':'n';
    ch.push({c,r,cols,gap,ty:ty_,px:W/2,py:-100-r*40,hp:hp+T[ty_].hp,hit:0,diving:false})}}
function shoot(){
  const pat=[[0],[-8,8],[-12,0,12],[-16,-6,6,16],[-22,-11,0,11,22]][P.weapon-1],L=P.laser>0;
  pat.forEach(a=>bul.push({x:P.x+a,y:P.y-22,vx:a*.1,vy:L?-18:-13,n:L?3:1,L}));
  snd(500+P.weapon*70+(L?200:0),.07,L?'sawtooth':WSND[P.weapon-1],.025,-250)}
function burst(x,y,n,cols){for(let i=0;i<n;i++){const a=R()*TAU,s=1+R()*5;
  parts.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,l:30+R()*30,c:cols[R()*cols.length|0],z:2+R()*3})}}
function txt(x,y,s,c){texts.push({x,y,s,c:c||'#ffd93b',l:50})}
function hurt(){
  if(P.inv>0)return;
  if(P.shield>0){P.shield--;P.inv=40;snd(200,.2,'sawtooth',.05);return}
  P.lives--;P.inv=110;shake=18;combo=0;burst(P.x,P.y,30,['#ff9800','#ffeb3b','#fff']);snd(120,.4,'sawtooth',.08,-60);
  if(P.lives<=0)finish()}
function drop(x,y,force){
  if(!force&&R()>.15)return;const r=R();
  items.push({x,y,ty:r<.22?'W':r<.37?'S':r<.46?'L':r<.58?'B':r<.7?'Z':r<.8?'M':r<.9?'X':'F'})}
function kill(k,i){
  ch.splice(i,1);combo++;comboT=100;const m=Math.min(1+(combo/5|0),5);score+=({n:10,f:20,t:30}[k.ty])*m;
  burst(k.px,k.py,18,['#fff','#ffd93b','#ff9800','#ff5252']);snd(300,.15,'triangle',.05,-200);
  txt(k.px,k.py-20,R()<.7?'خبيث!':'×'+m);drop(k.px,k.py)}
function bomb(){
  if(state!=='play'||P.bombs<=0)return;
  P.bombs--;eggs=[];shake=26;flash=14;snd(70,.7,'sawtooth',.1,-30);
  for(let i=ch.length-1;i>=0;i--){const k=ch[i];k.hp-=3;if(k.hp<=0)kill(k,i)}
  if(boss){boss.hp-=25;burst(boss.x,boss.y,40,['#fff','#ffd93b']);if(boss.hp<=0)killBoss()}
  txt(W/2,H/2,'💣 BOOM!','#ff9800')}
function killBoss(){
  burst(boss.x,boss.y,120,['#fff','#ffd93b','#ff5252','#ff9800']);score+=500;shake=30;
  txt(boss.x,boss.y,'BOSS DOWN! +500','#ff5252');for(let i=0;i<4;i++)drop(boss.x+(i-1.5)*40,boss.y,true);
  boss=null;snd(80,.8,'sawtooth',.1,-40)}
function egg(x,y,vx,vy){eggs.push({x,y,vx,vy})}

function update(s){
  t+=s;playT+=s/60;const sz=S();
  if(keys.ArrowLeft||keys.KeyA)tx-=11*s;if(keys.ArrowRight||keys.KeyD)tx+=11*s;
  if(keys.ArrowUp||keys.KeyW)ty-=9*s;if(keys.ArrowDown||keys.KeyS)ty+=9*s;
  if(mouseIn){tx=mx;ty=my}
  tx=clamp(tx,30,W-30);ty=clamp(ty,H*.4,H-50);
  const f=Math.min(.3*s,1);P.x+=(tx-P.x)*f;P.y+=(ty-P.y)*f;if(P.inv>0)P.inv-=s;
  ['freeze','magnet','laser'].forEach(k=>{if(P[k]>0)P[k]-=s});
  P.cool-=s;if(P.cool<=0){shoot();P.cool=P.laser>0?4:Math.max(5,14-P.weapon*1.8)}
  if(comboT>0){comboT-=s;if(comboT<=0)combo=0}
  const ox=Math.sin(t/70)*W*.06,fr=P.freeze>0;

  if(!fr)ch.forEach(k=>{
    const ty_=T[k.ty];k.hit=Math.max(0,k.hit-s);
    if(k.diving){k.py+=(3.5+wave*.15)*DIFF.spd*s;k.px+=(Math.sin(k.py*.04)*3+(P.x-k.px)*.006)*s;
      if(k.py>H+60){k.diving=false;k.py=-60}if(Math.hypot(k.px-P.x,k.py-P.y)<sz*.8)hurt()}
    else{const zz=k.ty==='f'?Math.sin(t/12+k.c)*k.gap*.35:0;
      const fx=W/2+(k.c-(k.cols-1)/2)*k.gap+ox+zz,fy=90+k.r*k.gap*.85+Math.sin(t/30+k.c)*6;
      k.px+=(fx-k.px)*Math.min(.1*s,1);k.py+=(fy-k.py)*Math.min(.1*s,1);
      if(R()<.0004*ty_.dive*(1+wave*.25)*DIFF.spd*s&&k.py>40)k.diving=true}
    if(R()<.0005*ty_.fire*(1+wave*.2)*DIFF.fire*s&&k.py>30)egg(k.px,k.py+10,0,3+wave*.1)});

  if(boss&&!fr){
    const b=boss;b.ph=b.hp/b.max>.66?1:b.hp/b.max>.33?2:3;
    b.y+=(b.ty-b.y)*Math.min(.04*s,1);b.x+=b.dir*(2+wave*.06+b.ph)*s;
    if(b.x>W-sz*2||b.x<sz*2)b.dir*=-1;b.sh-=s;
    if(b.sh<=0&&b.y>sz){
      b.sh=Math.max(30,(75-wave)/(b.ph*.7+.3))/DIFF.fire;const n=5+(wave>>2)+b.ph;
      for(let i=0;i<n;i++){const a=Math.PI/2+(i-(n-1)/2)*.22;egg(b.x,b.y+sz,Math.cos(a)*3.5,Math.sin(a)*3.5)}
      if(b.ph>=2){const a=Math.atan2(P.y-b.y,P.x-b.x);egg(b.x,b.y+sz,Math.cos(a)*5,Math.sin(a)*5)}
      snd(150,.2,'sawtooth',.05)}
    if(Math.hypot(b.x-P.x,b.y-P.y)<sz*1.6)hurt()}

  bul.forEach(b=>{b.x+=b.vx*s;b.y+=b.vy*s});
  bul=bul.filter(b=>{
    if(b.y<-20||b.x<-20||b.x>W+20)return false;
    if(boss&&Math.hypot(b.x-boss.x,b.y-boss.y)<sz*1.8){boss.hp--;score+=2;burst(b.x,b.y,2,['#ffd93b']);if(boss.hp<=0)killBoss();return false}
    for(let i=0;i<ch.length;i++){const k=ch[i];
      if(Math.hypot(b.x-k.px,b.y-k.py)<sz*.6){k.hp--;k.hit=5;
        if(k.hp<=0)kill(k,i);else burst(b.x,b.y,3,['#fff']);b.n--;return b.n>0}}
    return true});

  eggs.forEach(e=>{e.x+=(e.vx||0)*s;e.y+=e.vy*s;if(Math.hypot(e.x-P.x,e.y-P.y)<sz*.45){hurt();e.y=H+99}});
  eggs=eggs.filter(e=>e.y<H+20&&e.x>-20&&e.x<W+20);

  items.forEach(it=>{
    if(P.magnet>0){const d=Math.hypot(P.x-it.x,P.y-it.y)||1;it.x+=(P.x-it.x)/d*7*s;it.y+=(P.y-it.y)/d*7*s}else it.y+=2.2*s;
    if(Math.hypot(it.x-P.x,it.y-P.y)<sz*.8){
      it.y=H+99;snd(900,.15,'sine',.06,400);
      if(it.ty==='W'){P.weapon=Math.min(5,P.weapon+1);txt(P.x,P.y-40,'WEAPON '+P.weapon,'#4fc3f7')}
      else if(it.ty==='S'){P.shield=Math.min(3,P.shield+1);txt(P.x,P.y-40,'SHIELD','#4fc3f7')}
      else if(it.ty==='L'){P.lives=Math.min(5,P.lives+1);txt(P.x,P.y-40,'+1 LIFE','#ff5252')}
      else if(it.ty==='B'){P.bombs=Math.min(5,P.bombs+1);txt(P.x,P.y-40,'+1 BOMB','#ff9800')}
      else if(it.ty==='Z'){P.freeze=240;txt(P.x,P.y-40,'FREEZE ❄️','#80deea')}
      else if(it.ty==='M'){P.magnet=480;txt(P.x,P.y-40,'MAGNET 🧲','#ce93d8')}
      else if(it.ty==='X'){P.laser=360;txt(P.x,P.y-40,'LASER 🔱','#ff5252')}
      else{score+=50;txt(P.x,P.y-40,'+50 🍗')}}});
  items=items.filter(i=>i.y<H+20&&i.y>-50);
  parts.forEach(p=>{p.x+=p.vx*s;p.y+=p.vy*s;p.vy+=.05*s;p.l-=s});parts=parts.filter(p=>p.l>0);
  texts.forEach(x=>{x.y-=.8*s;x.l-=s});texts=texts.filter(x=>x.l>0);
  shake*=.9;if(flash>0)flash-=s;if(banner>0)banner-=s;
  if(!ch.length&&!boss){waveTimer+=s;if(waveTimer>75)nextWave()}else waveTimer=0}

const stars=[...Array(120)].map(()=>({x:R(),y:R(),z:.3+R()*2.2}));
function bg(s){
  const gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,'#0a0a2a');gr.addColorStop(1,'#000');g.fillStyle=gr;g.fillRect(0,0,W,H);
  let n=g.createRadialGradient(W*.2,H*.3,0,W*.2,H*.3,W*.4);n.addColorStop(0,'rgba(120,40,180,.25)');n.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=n;g.fillRect(0,0,W,H);
  n=g.createRadialGradient(W*.85,H*.7,0,W*.85,H*.7,W*.35);n.addColorStop(0,'rgba(30,120,200,.22)');n.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=n;g.fillRect(0,0,W,H);
  g.fillStyle='#fff';stars.forEach(o=>{o.y+=o.z*.004*s;if(o.y>1)o.y=0;g.globalAlpha=.4+o.z*.25;g.fillRect(o.x*W,o.y*H,o.z,o.z)});g.globalAlpha=1}
function drawShip(){
  const k=S()/40;g.save();g.translate(P.x,P.y);g.scale(k,k);
  if(P.inv>0&&((P.inv/4)|0)%2)g.globalAlpha=.35;
  const fl=14+R()*12;
  g.fillStyle='#ff9800';g.beginPath();g.moveTo(-8,16);g.lineTo(0,16+fl);g.lineTo(8,16);g.fill();
  g.fillStyle='#ffeb3b';g.beginPath();g.moveTo(-4,16);g.lineTo(0,16+fl*.6);g.lineTo(4,16);g.fill();
  g.fillStyle='#e53935';g.beginPath();g.moveTo(-8,-2);g.lineTo(-30,22);g.lineTo(-10,16);g.fill();
  g.beginPath();g.moveTo(8,-2);g.lineTo(30,22);g.lineTo(10,16);g.fill();
  g.fillStyle='#cfd8dc';g.beginPath();g.moveTo(0,-32);g.lineTo(16,16);g.lineTo(0,9);g.lineTo(-16,16);g.closePath();g.fill();
  g.fillStyle='#29b6f6';g.beginPath();g.ellipse(0,-8,4.5,9,0,0,TAU);g.fill();
  if(P.shield>0){g.globalAlpha=.5;g.strokeStyle='#4fc3f7';g.lineWidth=3;g.shadowColor='#4fc3f7';g.shadowBlur=15;g.beginPath();g.arc(0,0,40,0,TAU);g.stroke()}
  g.restore();g.globalAlpha=1}
function big(a,b){
  g.fillStyle='rgba(0,0,0,.6)';g.fillRect(0,0,W,H);g.shadowColor='#ff9800';g.shadowBlur=25;g.fillStyle='#ffd93b';
  g.font='900 '+clamp(W/14,28,80)+'px sans-serif';g.fillText(a,W/2,H*.34);g.shadowBlur=0;g.fillStyle='#fff';
  g.font=clamp(W/45,14,22)+'px sans-serif';b.split('\n').forEach((l,i)=>g.fillText(l,W/2,H*.47+i*30))}
function draw(){
  const sz=S();g.save();if(shake>.5)g.translate((R()-.5)*shake,(R()-.5)*shake);
  g.textAlign='center';g.textBaseline='middle';
  const fr=P&&P.freeze>0;
  ch.forEach(k=>{g.font=sz*(k.ty==='t'?1.2:1)+'px serif';g.save();
    if(fr){g.shadowColor='#80deea';g.shadowBlur=16}else if(k.hp>1){g.shadowColor='#ff3d3d';g.shadowBlur=14}
    if(k.hit>0)g.globalAlpha=.5;g.fillText(T[k.ty].e,k.px,k.py);g.restore()});
  if(boss){
    g.font=sz*3.4+'px serif';g.save();g.shadowColor=['','#ff3d3d','#ff9800','#d500f9'][boss.ph];g.shadowBlur=30;g.fillText('🐓',boss.x,boss.y);g.restore();
    const bw=W*.5;g.fillStyle='#300';g.fillRect(W/2-bw/2,50,bw,12);g.fillStyle=['','#ff3d3d','#ff9800','#d500f9'][boss.ph];
    g.fillRect(W/2-bw/2,50,bw*clamp(boss.hp/boss.max,0,1),12);g.strokeStyle='#fff';g.strokeRect(W/2-bw/2,50,bw,12)}
  g.font=sz*.55+'px serif';eggs.forEach(e=>g.fillText('🥚',e.x,e.y));
  items.forEach(i=>{g.font=sz*.8+'px serif';g.fillText({W:'⚡',S:'🛡️',L:'❤️',F:'🍗',B:'💣',Z:'❄️',M:'🧲',X:'🔱'}[i.ty],i.x,i.y)});
  bul.forEach(b=>{g.fillStyle=b.L?'#00e5ff':'#ff5252';g.shadowColor=b.L?'#00e5ff':'#ff1744';g.shadowBlur=10;g.fillRect(b.x-(b.L?3:2),b.y,b.L?6:4,b.L?26:16);g.shadowBlur=0});
  if(state!=='menu'&&P)drawShip();
  parts.forEach(p=>{g.globalAlpha=clamp(p.l/30,0,1);g.fillStyle=p.c;g.fillRect(p.x,p.y,p.z,p.z)});g.globalAlpha=1;
  g.font='bold 22px sans-serif';texts.forEach(x=>{g.globalAlpha=clamp(x.l/30,0,1);g.fillStyle=x.c;g.fillText(x.s,x.x,x.y)});g.globalAlpha=1;
  g.restore();
  if(flash>0){g.fillStyle='rgba(255,255,255,'+clamp(flash/14,0,1)*.6+')';g.fillRect(0,0,W,H)}
  if(mouseIn&&state==='play'){g.strokeStyle='#ffd93b';g.lineWidth=2;g.beginPath();g.arc(mx,my,14,0,TAU);
    g.moveTo(mx-22,my);g.lineTo(mx-8,my);g.moveTo(mx+8,my);g.lineTo(mx+22,my);g.moveTo(mx,my-22);g.lineTo(mx,my-8);g.moveTo(mx,my+8);g.lineTo(mx,my+22);g.stroke()}
  g.textAlign='left';g.fillStyle='#ffd93b';g.font='bold 18px monospace';
  if(state!=='menu'&&P){
    g.fillText('SCORE '+score+'   BEST '+BEST+'   '+DIFF.name,14,24);
    g.fillText('WAVE '+wave+'   WEAPON Lv'+P.weapon+'   💣 x'+P.bombs+(combo>4?'   COMBO x'+Math.min(1+(combo/5|0),5):''),14,48);
    g.fillText('❤'.repeat(Math.max(P.lives,0))+'  🛡'.repeat(P.shield),14,72);
    let y=96;[['freeze','❄️'],['magnet','🧲'],['laser','🔱']].forEach(q=>{if(P[q[0]]>0){g.fillText(q[1]+' '+(P[q[0]]/60).toFixed(1)+'s',14,y);y+=24}});
    g.font='bold 15px sans-serif';g.fillStyle='#fff9';g.fillText('👤 '+NAME,14,H-16)}
  g.textAlign='center';
  if(banner>0&&state==='play'){g.globalAlpha=clamp(banner/40,0,1);g.fillStyle='#fff';g.font='bold '+W/18+'px sans-serif';g.fillText(wave%5===0?'⚠ BOSS ⚠':'WAVE '+wave,W/2,H/2);g.globalAlpha=1}
  if(state==='menu')big('🐔 CHICKEN INVADERS 🐔','👤 '+NAME+'  —  '+NEXT.name+'\nClick / Space للبدء\nماوس أو أسهم للحركة | ضرب أوتوماتيك\nB قنبلة | P إيقاف | M صوت | F شاشة كاملة\n🏆 BEST: '+BEST);
  if(state==='pause')big('PAUSED','اضغط P أو كليك للمتابعة');
  if(state==='over')big('GAME OVER',(newBest?'🏆 NEW PERSONAL BEST! 🏆\n':'')+'SCORE '+score+'  |  BEST '+BEST+'\n✅ السكور اتسجّل تلقائي في الـ Leaderboard\nClick لإعادة اللعب')}

let last=performance.now(),errShown=false;
function loop(n){
  requestAnimationFrame(loop);
  try{if(!resize()){last=n;return}
    const s=Math.min((n-last)/16.67,2.5);last=n;
    if(state==='play')update(s);bg(state==='play'?s:.3);draw()}
  catch(e){if(!errShown){errShown=true;errBox.style.display='block';errBox.textContent='Game error: '+e.message+'\n'+(e.stack||'')}console.error(e)}}
requestAnimationFrame(loop);

function act(){
  if(!AC){try{AC=new(window.AudioContext||window.webkitAudioContext)()}catch(e){}}
  if(state==='menu')startGame();
  else if(state==='over'){if(performance.now()-overAt>700)startGame()}
  else if(state==='pause')state='play'}
function pos(e){const r=cv.getBoundingClientRect();return[e.clientX-r.left,e.clientY-r.top]}
cv.addEventListener('mousemove',e=>{[mx,my]=pos(e);mouseIn=true});
cv.addEventListener('mouseleave',()=>mouseIn=false);
cv.addEventListener('mousedown',()=>{cv.focus();act()});
cv.addEventListener('touchstart',e=>{act();const p=pos(e.touches[0]);mx=p[0];my=p[1]-70;mouseIn=true;e.preventDefault()},{passive:false});
cv.addEventListener('touchmove',e=>{const p=pos(e.touches[0]);mx=p[0];my=p[1]-70;mouseIn=true;e.preventDefault()},{passive:false});
cv.addEventListener('touchend',()=>mouseIn=false);
function fs(){try{if(!document.fullscreenElement){const p=(wrap.requestFullscreen||wrap.webkitRequestFullscreen).call(wrap);
  if(p&&p.catch)p.catch(()=>toast('المتصفح منع الـ Fullscreen هنا'))}else document.exitFullscreen()}catch(e){toast('الـ Fullscreen مش مدعوم هنا')}}
document.getElementById('fs').onclick=fs;
document.getElementById('bb').onclick=()=>{act();bomb()};

const KON=['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','KeyB','KeyA'];let kp=0;
addEventListener('keydown',e=>{
  keys[e.code]=true;
  if(['Space','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();
  if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','KeyA','KeyD','KeyW','KeyS'].includes(e.code))mouseIn=false;
  kp=(e.code===KON[kp])?kp+1:(e.code===KON[0]?1:0);
  if(kp===KON.length){kp=0;if(P&&state==='play'){P.lives=5;P.bombs=5;P.weapon=5;P.shield=3;txt(W/2,H/2,'🥚 KONAMI! FULL POWER','#ffd93b');snd(1000,.4,'sine',.08,600)}}
  if(e.code==='KeyP'){if(state==='play')state='pause';else if(state==='pause')state='play'}
  if(e.code==='KeyM')mute=!mute;
  if(e.code==='KeyF')fs();
  if(e.code==='KeyB')bomb();
  if(e.code==='Space'||e.code==='Enter')act()});
addEventListener('keyup',e=>keys[e.code]=false);
addEventListener('blur',()=>{if(state==='play')state='pause';for(const k in keys)keys[k]=false});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&state==='play')state='pause'});
})();
</script>
"""

COMP_DIR = Path(__file__).with_name("shiblanga_game_component")
COMP_DIR.mkdir(exist_ok=True)
_page = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
         '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + GAME + "</body></html>")
_idx = COMP_DIR / "index.html"
if not _idx.exists() or _idx.read_text(encoding="utf-8") != _page:
    _idx.write_text(_page, encoding="utf-8")
game_component = components.declare_component("shiblanga_game", path=str(COMP_DIR))


def clean_name(s):
    return re.sub(r"[^\w\s\-.]", "", s or "", flags=re.UNICODE).strip()[:16]


def validate_run(res):
    """Basic sanity checks: nonce, difficulty, and a plausible score for the time played."""
    try:
        score, wave, secs = int(res["score"]), int(res["wave"]), float(res["secs"])
    except Exception:
        return False, "بيانات غير صالحة"
    if res.get("diff") not in DIFFS:
        return False, "صعوبة غير معروفة"
    if res.get("nonce") != ss.nonce:
        return False, "الجلسة منتهية، العب تاني"
    if res.get("name") != ss.player:
        return False, "الاسم مش مطابق"
    if score < 0 or wave < 1 or secs < 3:
        return False, "محاولة قصيرة جداً"
    if score > secs * 450 + 300 or wave > secs / 2 + 2:
        return False, "السكور مش منطقي بالنسبة لوقت اللعب"
    return True, ""


# ----------------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------------
st.markdown('<div class="title"><span class="chk">🐔</span> SHIBLANGA OS <span class="chk">🐔</span></div>'
            '<div class="subtitle">Terminal · Tayebat Lab · Chicken Invaders — كله في مكان واحد 🚀</div>',
            unsafe_allow_html=True)
st.markdown(f'<div class="warn">{DISCLAIMER}</div>', unsafe_allow_html=True)

ss.setdefault("hist", ["Welcome to Shiblanga OS v5.0 — اكتب -help"])
ss.setdefault("cmds", [])
ss.setdefault("score", 0)
ss.setdefault("log", {"طيب": 0, "خبيث": 0})
ss.setdefault("quiz", None)
ss.setdefault("quiz_score", [0, 0])
ss.setdefault("booted", False)
ss.setdefault("nonce", secrets.token_hex(8))
ss.setdefault("done_runs", set())
ss.setdefault("last_result", None)
ss.setdefault("lb_diff", "All")


def _count_check():
    if ss.get("food_input", "").strip():
        ss.score += 1


def new_quiz():
    ss.quiz = random.choice(list(TAYEBAT))


def answer_quiz(ans):
    ss.quiz_score[1] += 1
    if TAYEBAT[ss.quiz] == ans:
        ss.quiz_score[0] += 1
        ss.quiz_msg = ("good", f"✅ صح! {ss.quiz} → {ans}")
    else:
        ss.quiz_msg = ("bad", f"🚫 غلط! {ss.quiz} → {TAYEBAT[ss.quiz]}")
    new_quiz()


t1, t2, t3, t4 = st.tabs(["💻 Terminal", "🍽️ Tayebat Lab", "📜 القواعد", "🎮 Chicken Invaders"])

with t1:
    anim = st.empty()
    if not ss.booted:
        boot(anim)
        ss.booted = True
        anim.empty()
    qc = st.columns(6)
    quick = ["-help", "shiblanga", "diaa el3awady", "diaa-wisdom", "chicken", "rocket"]
    clicked = None
    for col, q in zip(qc, quick):
        if col.button(q, use_container_width=True):
            clicked = q
    with st.form("f", clear_on_submit=True):
        typed = st.text_input("shiblanga@local:~$", placeholder="tayebat-check chicken | calc 2+2 | joke | neofetch")
        st.form_submit_button("Run ▶")
    cmd = clicked or typed.strip()
    if cmd:
        if cmd.lower() == "clear":
            ss.hist = ["Terminal cleared."]
        else:
            ss.cmds.append(cmd)
            out = run_command(cmd, anim)
            anim.empty()
            ss.hist.append(f"shiblanga@local:~$ {cmd}\n{out}")
            ss.hist = ss.hist[-25:]
            ss.cmds = ss.cmds[-50:]
    st.markdown('<div class="term">' + html.escape("\n\n".join(ss.hist)) + "</div>", unsafe_allow_html=True)
    st.caption("الأوامر: " + " · ".join(COMMANDS[:14]) + " …")

with t2:
    st.subheader("🔬 طيب ولا خبيث؟")
    food = st.text_input("اكتب الأكلة (عربي أو English)", key="food_input", on_change=_count_check)
    if food:
        r, key, fz = check_food(food)
        safe = html.escape(food)
        note = f"<br><small>قصدك «{html.escape(key)}»؟</small>" if fz else ""
        if r == "طيب":
            st.markdown(f'<div class="good">✅ <b>{safe}</b> → طيّبة (حسب القوائم المتداولة){note}</div>', unsafe_allow_html=True)
        elif r == "خبيث":
            st.markdown(f'<div class="bad">🚫 <b>{safe}</b> → خبيثة{note}<br>{random.choice(FUNNY)}</div>', unsafe_allow_html=True)
        else:
            st.info("مش في القائمة المختصرة.")
        if r and st.button("➕ سجّلتها في وجباتي النهاردة"):
            ss.log[r] += 1
    c1, c2 = st.columns(2)
    c1.success("✅ " + "، ".join(sorted({k for k, v in TAYEBAT.items() if v == "طيب" and not k.isascii()})))
    c2.error("🚫 " + "، ".join(sorted({k for k, v in TAYEBAT.items() if v == "خبيث" and not k.isascii()})))

    st.markdown("### 📊 عداد وجبات اليوم")
    st.bar_chart({"عدد": {"طيب ✅": ss.log["طيب"], "خبيث 🚫": ss.log["خبيث"]}}, height=200)
    if st.button("🗑️ صفّر العداد"):
        ss.log = {"طيب": 0, "خبيث": 0}
        st.rerun()

    st.markdown("### 🧠 Quiz: طيب ولا خبيث؟")
    if ss.quiz is None:
        new_quiz()
    msg = ss.pop("quiz_msg", None)
    if msg:
        st.markdown(f'<div class="{msg[0]}">{msg[1]}</div>', unsafe_allow_html=True)
    st.markdown(f"### 🍽️ **{ss.quiz}**")
    q1, q2 = st.columns(2)
    q1.button("✅ طيب", key="qa", on_click=answer_quiz, args=("طيب",), use_container_width=True)
    q2.button("🚫 خبيث", key="qb", on_click=answer_quiz, args=("خبيث",), use_container_width=True)

    st.markdown("### 🎲 أدوات سريعة")
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

    if not ss.player:
        # ---- أول مرة: اسأل عن الاسم قبل اللعب ----
        st.markdown('<div class="glass namecard"><h2>👋 أهلاً يا بطل!</h2>'
                    '<div>قبل ما تبدأ، قولنا اسمك عشان نسجّل أحسن محاولة ليك في الـ Leaderboard تلقائياً 🏆</div></div>',
                    unsafe_allow_html=True)
        with st.form("name_form"):
            nm = st.text_input("اسمك (٢ – ١٦ حرف)", max_chars=16, placeholder="مثلاً: Shiblanga")
            go = st.form_submit_button("🚀 يلا نلعب", use_container_width=True)
        if go:
            nm = clean_name(nm)
            if len(nm) < 2:
                st.error("الاسم لازم يكون حرفين على الأقل (حروف وأرقام بس).")
            else:
                ss.player = nm
                st.query_params["p"] = nm
                st.rerun()
    else:
        st.caption("اضغط جوه اللعبة الأول عشان الكيبورد يشتغل. 💣 B | إيقاف P | صوت M | Fullscreen F | "
                   "Power-ups: ❄️ تجميد · 🧲 مغناطيس · 🔱 ليزر | جرّب Konami Code 😉")
        my_best = max([r["score"] for r in player_stats(ss.player) if r["diff"] == diff_name] or [0])
        res = game_component(diff=DIFFS[diff_name], name=ss.player, best=my_best, nonce=ss.nonce,
                             key="shib_game", default=None)

        # ---- استقبال السكور تلقائياً من اللعبة ----
        if isinstance(res, dict) and res.get("run") and res["run"] not in ss.done_runs:
            ss.done_runs.add(res["run"])
            ok, why = validate_run(res)
            if ok:
                rec, nb, prev = submit_score(ss.player, int(res["score"]), int(res["wave"]), res["diff"])
                rank = next((i for i, r in enumerate(board(res["diff"]), 1) if r["name"].casefold() == ss.player.casefold()), None)
                ss.last_result = dict(ok=True, score=int(res["score"]), wave=int(res["wave"]), nb=nb, prev=prev,
                                      rank=rank, diff=res["diff"])
                ss.nonce = secrets.token_hex(8)
                st.rerun()
            else:
                ss.last_result = dict(ok=False, why=why)

        lr = ss.last_result
        if lr:
            if lr["ok"]:
                head = "🏆 <b>رقم قياسي جديد!</b>" if lr["nb"] else "✅ اتسجّلت المحاولة"
                extra = (f" (كان {lr['prev']:,})" if lr["nb"] and lr["prev"] else "")
                tail = "" if lr["nb"] else f"<br><small>أحسن سكور ليك لسه أعلى، المحاولة دي مغيّرتش الترتيب.</small>"
                st.markdown(f'<div class="res {"nb" if lr["nb"] else ""}">{head} — سكور <b>{lr["score"]:,}</b>{extra} · '
                            f'Wave {lr["wave"]} · {lr["diff"]} · ترتيبك الحالي: <b>#{lr["rank"]}</b>{tail}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad">⚠️ المحاولة اتر��ضت: {html.escape(lr["why"])}</div>', unsafe_allow_html=True)

    # ---- Leaderboard ----
    st.markdown("### 🏆 Leaderboard")
    ss.lb_diff = st.radio("المستوى", ["All", "Easy", "Normal", "Hard"], horizontal=True,
                          index=["All", "Easy", "Normal", "Hard"].index(ss.lb_diff), label_visibility="collapsed")
    rows = board(ss.lb_diff)
    if rows:
        st.markdown(board_html(rows, ss.player), unsafe_allow_html=True)
    else:
        st.info("لسه مفيش سكورات في المستوى ده. كن أول واحد! 🐔")

    if ss.player:
        recs = player_stats(ss.player)
        if recs:
            mine = [r for r in recs if ss.lb_diff in ("All", r["diff"])]
            if mine:
                best_rec = max(mine, key=lambda r: r["score"])
                my_rank = next((i for i, r in enumerate(rows, 1) if r["name"].casefold() == ss.player.casefold()), "-")
                st.markdown(f"#### 👤 إحصائيات {html.escape(ss.player)}")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("🏅 أحسن سكور", f"{best_rec['score']:,}")
                m2.metric("📍 ترتيبك", f"#{my_rank}")
                m3.metric("🌊 أعلى Wave", max(r.get("wave", 0) for r in mine))
                m4.metric("🎮 محاولات", sum(r.get("games", 1) for r in mine))
    st.caption("السكور بيتسجّل تلقائياً من اللعبة نفسها، ومفيش إدخال يدوي. بيتحفظ لكل لاعب أحسن محاولة بس في كل مستوى صعوبة.")

# ----------------------------------------------------------------------------
# Sidebar stats (بتتحدّث بعد معالجة السكور)
# ----------------------------------------------------------------------------
with side_slot:
    st.metric("🍗 Chicken checks", ss.score)
    st.metric("🧠 Quiz", f"{ss.quiz_score[0]}/{ss.quiz_score[1]}")
    top = board("All")[:1]
    if top:
        st.metric("🏆 أعلى سكور", f"{top[0]['score']:,}", top[0]["name"])
    st.caption("الباروديا ترفيهية، والرسومات emoji بس.")
