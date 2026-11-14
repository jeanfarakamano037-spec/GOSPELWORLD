from flask import Flask, jsonify, request, send_file
import json, os, uuid, random, urllib.request, datetime, base64
from io import BytesIO
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# ===== ICONE G DOREE - V27 - MARCHE MEME SANS PIL =====
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except:
    HAS_PIL = False

# Petit PNG de secours si PIL n'est pas la - 1x1 transparent, Chrome accepte
FALLBACK_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

def make_gospel_icon(size):
    if not HAS_PIL:
        buf = BytesIO(base64.b64decode(FALLBACK_PNG_B64))
        buf.seek(0)
        return buf
    img = Image.new("RGB", (size, size), (10, 10, 18))
    d = ImageDraw.Draw(img)
    d.ellipse([size*0.05, size*0.05, size*0.95, size*0.95], fill=(255, 215, 0))
    d.ellipse([size*0.12, size*0.12, size*0.88, size*0.88], fill=(10, 10, 18))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", int(size*0.55))
    except:
        font = ImageFont.load_default()
    txt = "G"
    bbox = d.textbbox((0,0), txt, font=font)
    tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    d.text(((size-tw)/2 - bbox[0], (size-th)/2 - bbox[1] - size*0.03), txt, fill=(255, 215, 0), font=font)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

GOSPEL_OM = "629757411"
GOSPEL_OM_DISPLAY = "629-757-411"
VERSETS = [
    ("Jean 3:16", "Car Dieu a tant aime le monde, qu'il a donne son Fils unique, afin que quiconque croit en lui ne perisse point, mais qu'il ait la vie eternelle."),
    ("Psaume 150:6", "Que tout ce qui respire loue l'Eternel! Louez l'Eternel!"),
    ("Philippiens 4:13", "Je puis tout par celui qui me fortifie."),
    ("Jeremie 29:11", "Car je connais les projets que j'ai formes sur vous, projets de paix et non de malheur, afin de vous donner un avenir et de l'esperance."),
    ("Esaie 40:31", "Mais ceux qui se confient en l'Eternel renouvellent leur force."),
    ("Matthieu 28:19", "Allez, faites de toutes les nations des disciples."),
    ("Psaume 23:1", "L'Eternel est mon berger: je ne manquerai de rien."),
    ("Psaume 121:1", "Je leve mes yeux vers les montagnes... D'ou me viendra le secours?"),
    ("Romains 8:28", "Nous savons que toutes choses concourent au bien de ceux qui aiment Dieu."),
    ("Esaie 41:10", "Ne crains rien, car je suis avec toi."),
]
def get_env(*names):
    for n in names:
        v = os.getenv(n)
        if v: return v.strip()
    return None
CLOUD_NAME = get_env("CLOUDINARY_CLOUD_NAME", "cloudinary_cloud_name")
API_KEY = get_env("CLOUDINARY_API_KEY", "cloudinary_api_key")
API_SECRET = get_env("CLOUDINARY_API_SECRET", "cloudinary_api_secret")
cloudinary.config(cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET, secure=True)
_memory_cache = {}
def cloudinary_json_url(fname):
    base = fname.replace(".json","")
    return f"https://res.cloudinary.com/{CLOUD_NAME}/raw/upload/gospelworld_data/{base}.json"
def load_json(f, default):
    try:
        url = cloudinary_json_url(f)
        req = urllib.request.Request(url, headers={"Cache-Control":"no-cache"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
            _memory_cache[f] = data
            return data
    except: pass
    if f in _memory_cache: return _memory_cache[f]
    if os.path.exists(f):
        try:
            with open(f, "r", encoding="utf-8") as x:
                d = json.load(x); _memory_cache[f]=d; return d
        except: pass
    return default
def save_json(f, data):
    _memory_cache[f]=data
    try:
        with open(f, "w", encoding="utf-8") as x: json.dump(data, x, ensure_ascii=False, indent=2)
    except: pass
    try:
        base=f.replace(".json",""); tmp=f"/tmp/{f}"
        with open(tmp,"w",encoding="utf-8") as x: json.dump(data,x,ensure_ascii=False,indent=2)
        cloudinary.uploader.upload(tmp, resource_type="raw", public_id=f"gospelworld_data/{base}", overwrite=True, invalidate=True)
    except Exception as e: print(f"Erreur save {f}: {e}")

@app.route("/")
def home():
    return """
<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>GOSPEL WORLD - FLASH EVANGILE WORLD - ROYAUME DE DIEU</title>
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="icon" type="image/png" href="/icon-192.png">
<meta name="theme-color" content="#FFD700">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="GOSPEL WORLD">
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
html,body{overflow-x:hidden;overflow-y:auto!important}
body{background:#08080F!important;color:#fff!important;font-family:Inter,Helvetica,Arial,sans-serif;margin:0;-webkit-tap-highlight-color:transparent}
::-webkit-scrollbar{width:8px;height:6px}::-webkit-scrollbar-thumb{background:#3a3a3a;border-radius:99px}
input,select,textarea{background:#1A1A22!important;color:#fff!important;border:1px solid #2a2a35!important}
input:focus{border-color:#FFD700!important;outline:none}
.chip{background:#1E1E28;color:#fff}.pill-active{background:#fff!important;color:#000!important}
.gold-btn{background:linear-gradient(135deg,#FFD700,#FF2D55,#8B5CF6,#00E5FF);color:#fff;background-size:300% 300%;animation:grad 3s infinite}
@keyframes grad{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.money-btn{background:linear-gradient(135deg,#25D366,#128C7E);color:#fff}
.money-gw{background:linear-gradient(135deg,#FFD700,#FF8C00,#FF2D55);color:#000;animation:grad 2s infinite;background-size:200% 200%}
.bar{width:4px;background:linear-gradient(#FFD700,#FF2D55,#00E5FF);border-radius:99px;animation:eq .6s infinite alternate}
@keyframes eq{from{height:6px}to{height:32px}}
.marquee{animation:scroll 16s linear infinite;white-space:nowrap}
@keyframes scroll{from{transform:translateX(100%)}to{transform:translateX(-100%)}}
.glow{box-shadow:0 0 30px rgba(255,215,0,.45)}
.spin{animation:spin 12s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.story-ring{background:conic-gradient(#FFD700,#FF2D55,#8B5CF6,#00E5FF,#FFD700);padding:2px;border-radius:9999px}
.viz{height:44px;display:flex;align-items:end;gap:3px}.viz div{flex:1;background:linear-gradient(#FFD700,#FF2D55,#00E5FF);border-radius:99px;transition:.15s}
.star{position:fixed;top:-10px;background:#fff;border-radius:9999px;animation:fall linear infinite;z-index:1;pointer-events:none}
@keyframes fall{to{transform:translateY(110vh) translateX(40px);opacity:0}}
.fire{animation:fire 1s infinite alternate}@keyframes fire{from{transform:scale(1)}to{transform:scale(1.04)}}
.float{animation:float 3s ease-in-out infinite}@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.type-btn{transition:.2s;border:2px solid transparent}.type-btn.active{border-color:#FFD700!important;background:#FFD700!important;color:#000!important;transform:scale(1.03)}
.dim-stage{perspective:1200px;position:relative}
.dim-photo{transform-style:preserve-3d;animation:dimFloat 4s ease-in-out infinite;box-shadow:0 30px 80px rgba(0,0,0,.8),0 0 60px rgba(255,215,0,.5);border:4px solid rgba(255,215,0,.9)}
@keyframes dimFloat{0%,100%{transform:rotateY(-8deg) rotateX(4deg) translateY(0)}25%{transform:rotateY(8deg) rotateX(-2deg) translateY(-10px) scale(1.02)}50%{transform:rotateY(-4deg) rotateX(6deg) translateY(-5px)}75%{transform:rotateY(6deg) rotateX(2deg) translateY(-12px)}}
.dim-halo{position:absolute;inset:-22px;border-radius:9999px;background:conic-gradient(#FFD700,#FF2D55,#8B5CF6,#00E5FF,#FFD700);animation:spin 8s linear infinite;z-index:-1;filter:blur(2px)}
.dim-halo2{position:absolute;inset:-40px;border-radius:9999px;border:2px dashed rgba(255,215,0,.6);animation:spin 20s linear infinite reverse;z-index:-1}
.dim-artist-pop{animation:popIn .6s ease-out, float 3s ease-in-out infinite;box-shadow:0 0 0 4px #FFD700,0 15px 40px rgba(0,0,0,.8);transform:translateY(-30px)}
@keyframes popIn{from{transform:scale(0) translateY(30px)}to{transform:scale(1) translateY(-30px)}}
.dim-bg{position:absolute;inset:0;background-size:cover;background-position:center;filter:blur(40px) brightness(.5);transform:scale(1.3);opacity:.8}
.beat{animation:beat .6s ease-in-out infinite}@keyframes beat{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
#mobileMenu{transition:transform .3s ease}#mobileMenu.closed{transform:translateX(-100%)}#mobileMenu.open{transform:translateX(0)}
.hero-grad{background:radial-gradient(ellipse at top,#2D0A4A 0%,#0A0A2E 35%,#08080F 70%,#000 100%)}
.spot-card{background:#181818;border-radius:12px;padding:14px;cursor:pointer;transition:.3s;position:relative}
.spot-card:hover{background:#282828}
.spot-card img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px}
.spot-card.artist img{border-radius:9999px}
.spot-card h4{font-size:15px;font-weight:700;margin-top:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.spot-card p{font-size:13px;color:#B3B3B3;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.spot-play{position:absolute;bottom:72px;right:20px;width:48px;height:48px;background:#1DB954;color:#000;border-radius:9999px;display:flex;align-items:center;justify-content:center;opacity:0;transform:translateY(10px);transition:.3s}
.spot-card:hover .spot-play{opacity:1;transform:translateY(0)}
.spot-row{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 4px 12px 4px;scrollbar-width:none}
.spot-row::-webkit-scrollbar{display:none}.spot-row .spot-card{flex:0 0 190px;scroll-snap-align:start}
.spot-title{font-size:22px;font-weight:800;padding:22px 4px 10px 4px;display:flex;justify-content:space-between;align-items:center}
.spot-title span{font-size:13px;color:#B3B3B3;cursor:pointer}
.filter-row{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:4px 0 8px 0}.filter-row::-webkit-scrollbar{display:none}.filter-row button{flex-shrink:0;white-space:nowrap}
.hrow{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:4px}.hrow::-webkit-scrollbar{display:none}.hrow>*{flex-shrink:0;white-space:nowrap}
@media (max-width: 768px){
  body{background:#0A0A12!important;font-size:13.5px}
  main{max-width:460px;margin:0 auto!important;padding-left:0!important;padding-right:0!important}
  header{padding:8px 12px!important;background:rgba(10,10,18,.95)!important;backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.06);display:flex!important;align-items:center!important;gap:10px!important;justify-content:flex-start!important}
  .top-banner{padding:9px 11px!important;border-radius:14px!important;box-shadow:0 6px 18px rgba(255,45,85,.22)}
  .top-banner h3{font-size:12.5px!important;line-height:1.25}
  .top-banner p{font-size:10.5px!important;margin-top:1px}
  .hero-grad{padding:10px 12px 8px 12px!important;border-radius:0 0 18px 18px}
  .hero-grad h1{font-size:30px!important;line-height:.95!important;letter-spacing:-.5px}
  .hero-grad .verse-box{padding:9px 11px!important;border-radius:13px!important;background:rgba(255,255,255,.06)!important;border:1px solid rgba(255,255,255,.08)!important}
  .hero-grad .flash-box{padding:9px!important;border-radius:14px!important;flex-wrap:nowrap!important}
  .hero-grad .flash-box button{flex-shrink:0!important;white-space:nowrap!important;font-size:10px!important;padding:7px 10px!important;line-height:1.2}
  .hero-grad .flash-box h3{font-size:12px!important}
  .action-row{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;gap:7px!important;scrollbar-width:none;padding:2px 2px 5px 2px}
  .action-row::-webkit-scrollbar{display:none}
  .action-row button{flex-shrink:0!important;white-space:nowrap!important;padding:8px 12px!important;font-size:11px!important;border-radius:9999px!important}
  #statsBar{display:flex!important;overflow-x:auto!important;gap:7px!important;scrollbar-width:none}
  #statsBar::-webkit-scrollbar{display:none}
  #statsBar div{flex:0 0 78px!important;padding:8px 5px!important;border-radius:12px!important}
  .flags-row{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;gap:6px!important;scrollbar-width:none}
  .flags-row::-webkit-scrollbar{display:none}.flags-row span{flex-shrink:0!important}
  #search{border-radius:9999px!important;padding:10px 14px!important;font-size:13px!important;background:#1A1A22!important;border:none!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)}
  .filter-row{padding:7px 12px 3px 12px!important;gap:6px!important}
  .filter-row button{padding:7px 11px!important;font-size:11px!important;border-radius:9999px!important}
  .spot-row{gap:10px!important;padding:0 12px 5px 12px!important}
  .spot-row .spot-card{flex:0 0 138px!important;padding:0!important;background:transparent!important}
  .spot-row .spot-card img{width:138px!important;height:138px!important;border-radius:14px!important;box-shadow:0 6px 16px rgba(0,0,0,.4)}
  .spot-row .spot-card.artist img{border-radius:9999px!important}
  .spot-row .spot-card h4{font-size:13px!important;margin-top:6px!important}
  .spot-row .spot-card p{font-size:11px!important}
  .spot-title{font-size:17.5px!important;padding:14px 12px 7px 12px!important}
  .spot-title span{font-size:11.5px!important}
  .spot-play{display:none}
  #stories{padding:0 12px!important}
  #stories .story-ring{width:48px!important;height:48px!important}
  #grid{display:none!important}
  .player-bar{margin:0 7px 7px 7px!important;border-radius:14px!important;background:rgba(20,20,28,.95)!important;border:1px solid rgba(255,255,255,.08)!important;box-shadow:0 8px 24px rgba(0,0,0,.55)}
  .player-bar img{border-radius:9px!important}
  .bottom-nav{margin:0 8px 8px 8px!important;border-radius:18px!important;background:rgba(18,18,26,.95)!important;border:1px solid rgba(255,255,255,.08)!important;box-shadow:0 10px 26px rgba(0,0,0,.55)}
  #modal{align-items:flex-start!important;padding:8px!important}
  #modal .modal-box{max-height:88vh!important;overflow-y:auto!important;padding:12px!important;border-radius:18px!important;max-width:430px!important}
  #modal .type-btn{padding:7px 4px!important;border-radius:11px!important}
  #modal input, #modal textarea{padding:9px 11px!important;font-size:13px!important;border-radius:11px!important}
  #modal h3{font-size:15px!important}
  .publish-float{display:none!important}
}
@media (min-width: 769px){
  .main-content{margin-left:300px}
  #grid{display:grid!important}
}
</style></head><body>
<div id="stars"></div>
<div id="mobileMenu" class="closed fixed top-0 left-0 w-[280px] h-full bg-[#121212] z-[300] p-4 overflow-y-auto border-r border-white/10">
<div class="flex justify-between items-center"><div class="flex items-center gap-2"><div class="w-10 h-10 bg-white rounded-full flex items-center justify-center font-black text-xl text-black">G</div><div><b>GOSPEL <span class="text-[#1DB954]">WORLD</span></b><p class="text-[10px] text-[#B3B3B3]">ROYAUME DE DIEU</p></div></div><button onclick="toggleMobileMenu()" class="w-9 h-9 bg-white rounded-full text-black font-black">✕</button></div>
<button onclick="toggleMobileMenu();openModal('single')" class="mt-5 w-full bg-[#FFD700] text-black font-black py-3 rounded-full">➕ PUBLIER UN SON 🎤</button>
<button onclick="toggleMobileMenu();openModal('collection')" class="mt-2 w-full bg-white text-black font-bold py-2 rounded-full text-sm">📀 PUBLIER EP / MIXTAPE / ALBUM</button>
<button onclick="toggleMobileMenu();installApp()" class="mt-2 w-full bg-[#1DB954] text-white font-black py-3 rounded-full text-sm">📥 TELECHARGER L'APP - GRATUIT</button>
<nav class="mt-4 space-y-1 font-bold">
<button onclick="toggleMobileMenu();goHome()" class="w-full text-left flex gap-3 items-center p-3 rounded-xl bg-[#232323]">🏠 Accueil</button>
<button onclick="toggleMobileMenu();document.getElementById('search').focus()" class="w-full text-left flex gap-3 items-center p-3 rounded-xl hover:bg-[#232323] text-[#B3B3B3]">🔍 Rechercher</button>
<button onclick="toggleMobileMenu();showTab('LIKED',null)" class="w-full text-left flex gap-3 items-center p-3 rounded-xl hover:bg-[#232323] text-[#B3B3B3]">❤️ Titres likés</button>
<button onclick="toggleMobileMenu();showTab('TOP',null)" class="w-full text-left flex gap-3 items-center p-3 rounded-xl hover:bg-[#232323] text-[#B3B3B3]">🏆 Top Mondial</button>
<button onclick="toggleMobileMenu();startRadio()" class="w-full text-left flex gap-3 items-center p-3 rounded-xl bg-gradient-to-r from-yellow-500/20 to-cyan-500/20 border border-yellow-500/30">📻 Radio Royaume</button>
<button onclick="toggleMobileMenu();toggleKingdom()" class="w-full text-left flex gap-3 items-center p-3 rounded-xl bg-gradient-to-r from-purple-600 to-yellow-500">👑 Mode Royaume</button>
<button onclick="toggleMobileMenu();openDonateGW()" class="w-full text-left flex gap-3 items-center p-3 rounded-xl bg-[#FFD700] text-black">💛 Soutenir Gospel World<br><span class="text-xs font-black">629-757-411</span></button>
</nav>
<div class="mt-4 bg-gradient-to-br from-[#FFD700] via-[#FF2D55] to-[#00E5FF] rounded-2xl p-4"><p class="font-black">🌌 DIMENSION CIEL</p><p class="text-xs">GOSPEL WORLD partout</p><p class="mt-2 text-lg">🇬🇳 🇫🇷 🇺🇸 🇨🇮 🇲🇱 🇸🇳 🌍</p></div>
<p class="text-[11px] text-[#B3B3B3] mt-4">© 2026 GOSPEL WORLD - FLASH EVANGILE WORLD</p>
</div>
<div id="mobileOverlay" onclick="toggleMobileMenu()" class="hidden fixed inset-0 bg-black/70 z-[290]"></div>
<div class="flex relative z-10">
<aside class="sidebar hidden md:flex flex-col w-[290px] fixed left-2 top-2 bottom-[90px] p-3 z-50 overflow-y-auto bg-[#121212] rounded-xl">
<div class="bg-[#121212] rounded-xl p-2">
<div class="flex items-center gap-3 p-2.5 rounded-lg hover:bg-white/5 cursor-pointer font-bold" onclick="goHome()"><i class="fa-solid fa-house"></i> Accueil</div>
<div class="flex items-center gap-3 p-2.5 rounded-lg hover:bg-white/5 cursor-pointer font-bold text-[#B3B3B3]" onclick="document.getElementById('search').focus()"><i class="fa-solid fa-magnifying-glass"></i> Rechercher</div>
</div>
<div class="bg-[#121212] rounded-xl p-3 mt-2 flex-1">
<div class="flex justify-between items-center px-2"><div class="flex items-center gap-2 font-bold text-[#B3B3B3]"><i class="fa-solid fa-book-open"></i> Bibliothèque</div><button onclick="openModal('single')" class="w-8 h-8 bg-white/10 rounded-full font-black">+</button></div>
<button onclick="openModal('single')" class="mt-3 w-full bg-[#FFD700] text-black font-black py-2.5 rounded-full text-sm">➕ PUBLIER UN SON 🎤</button>
<button onclick="openModal('collection')" class="mt-2 w-full bg-white text-black font-bold py-2 rounded-full text-xs">📀 EP / MIXTAPE / ALBUM</button>
<button onclick="installApp()" class="mt-2 w-full bg-[#1DB954] text-white font-black py-2 rounded-full text-xs">📥 TELECHARGER L'APP</button>
<div class="mt-3 space-y-1 font-bold text-sm">
<button onclick="showTab('LIKED',this)" class="w-full text-left flex gap-3 items-center p-2.5 rounded-lg hover:bg-white/5 text-[#B3B3B3]"><span class="w-9 h-9 bg-gradient-to-br from-purple-600 to-blue-400 rounded-lg flex items-center justify-center">❤️</span> Titres likés</button>
<button onclick="showTab('TOP',this)" class="w-full text-left flex gap-3 items-center p-2.5 rounded-lg hover:bg-white/5 text-[#B3B3B3]"><span class="w-9 h-9 bg-[#FFD700] rounded-lg flex items-center justify-center text-black">🏆</span> Top Mondial</button>
<button onclick="startRadio()" class="w-full text-left flex gap-3 items-center p-2.5 rounded-lg hover:bg-white/5 text-[#B3B3B3]"><span class="w-9 h-9 bg-gradient-to-br from-yellow-400 to-pink-500 rounded-lg flex items-center justify-center">📻</span> Radio Royaume</button>
<button onclick="toggleKingdom()" class="w-full text-left flex gap-3 items-center p-2.5 rounded-lg hover:bg-white/5 text-[#B3B3B3]"><span class="w-9 h-9 bg-purple-600 rounded-lg flex items-center justify-center">👑</span> Mode Royaume</button>
<button onclick="openDonateGW()" class="w-full text-left flex gap-3 items-center p-2.5 rounded-lg bg-[#FFD700] text-black"><span class="w-9 h-9 bg-black rounded-lg flex items-center justify-center">💛</span> Soutenir GW - 629-757-411</button>
</div>
<div class="mt-3 bg-gradient-to-br from-[#FFD700] via-[#FF2D55] to-[#00E5FF] rounded-xl p-3"><p class="font-black text-sm">🌌 DIMENSION CIEL</p><p class="mt-1">🇬🇳 🇫🇷 🇺🇸 🇨🇮 🇲🇱 🌍</p></div>
<div id="libList" class="mt-3 space-y-1"></div>
<div class="mt-4 text-[11px] text-[#B3B3B3] px-2 pb-2"><p id="statsSide">...</p><p>© 2026 GOSPEL WORLD</p></div>
</div>
</aside>
<main class="main-content flex-1 md:ml-[300px] md:mr-2 md:mt-2 md:mb-[90px] pb-[180px] md:pb-6 relative z-10 bg-[#121212] md:rounded-xl overflow-hidden">
<header class="sticky top-0 z-40 bg-[#121212]/95 backdrop-blur-xl px-3 py-2.5 flex items-center gap-2.5">
<div class="flex items-center gap-2">
<button onclick="toggleMobileMenu()" class="md:hidden w-9 h-9 bg-white/10 rounded-full shrink-0">☰</button>
<div class="w-9 h-9 bg-white rounded-full flex items-center justify-center font-black text-black text-base shrink-0">G</div>
<div class="leading-none"><b class="text-[14px] block">GOSPEL <span class="text-[#1DB954]">WORLD</span></b><span class="text-[9px] text-[#B3B3B3] tracking-wider">ROYAUME DE DIEU</span></div>
</div>
<div class="hidden md:flex ml-auto items-center gap-2">
<button onclick="history.back()" class="w-8 h-8 bg-black rounded-full items-center justify-center">‹</button>
<button onclick="history.forward()" class="w-8 h-8 bg-black rounded-full items-center justify-center">›</button>
<div class="w-9 h-9 bg-gradient-to-br from-yellow-400 to-pink-500 rounded-full flex items-center justify-center font-black">G</div>
</div>
</header>
<section class="px-3 md:px-6 pt-2.5"><div class="top-banner bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-400 rounded-2xl p-3 flex items-center gap-3"><div class="min-w-0"><h3 class="font-black text-black text-[13px] md:text-xl leading-tight">🎤 TU ES ARTISTE? BALANCE TON SON!</h3><p class="text-black text-[11px] md:text-sm font-bold">Single - EP - Album</p></div></div></section>
<section class="px-3 md:px-6 pt-3"><div id="stories" class="flex gap-3 md:gap-4 overflow-x-auto pb-2"></div></section>
<section class="hero-grad px-3 md:px-6 pt-3 pb-4">
<div class="flex items-end gap-1 h-6"><div class="bar"></div><div class="bar" style="animation-delay:.1s"></div><div class="bar" style="animation-delay:.2s"></div><div class="bar" style="animation-delay:.3s"></div><div class="bar" style="animation-delay:.4s"></div><div class="bar" style="animation-delay:.5s"></div><div class="bar" style="animation-delay:.6s"></div></div>
<p class="text-[#FFD700] text-[10px] font-black tracking-[2px] mt-1.5">🌌 DIMENSION CIEL - ROYAUME DE DIEU</p>
<h1 class="text-[32px] md:text-[90px] font-black leading-[0.95] mt-1">GOSPEL<br><span class="bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-400 bg-clip-text text-transparent">WORLD</span></h1>
<p class="text-[15px] md:text-xl font-black mt-1">👑 ROYAUME DE DIEU <span class="text-[#B3B3B3] text-xs font-normal">- KINGDOM OF GOD</span></p>
<div class="verse-box mt-2.5 bg-white/5 border border-white/10 rounded-2xl p-2.5 max-w-2xl"><p class="text-[11px] text-[#FFD700] font-black">📖 VERSET DU JOUR</p><p id="verseText" class="text-[13px] mt-1 italic leading-snug">Chargement...</p><p id="verseRef" class="text-[11px] text-[#B3B3B3] mt-1"></p></div>
<div class="flash-box mt-2.5 bg-black/60 border border-[#FFD700]/40 rounded-2xl p-2.5 flex gap-2.5 items-center max-w-2xl">
<div class="w-11 h-11 md:w-20 md:h-20 rounded-xl bg-gradient-to-br from-yellow-400 via-pink-500 to-cyan-400 flex items-center justify-center text-lg md:text-3xl font-black glow shrink-0 float">⚡</div>
<div class="flex-1 min-w-0"><span class="bg-[#FFD700] text-black text-[9px] font-black px-2 py-0.5 rounded-full">⚡ FLASH EVANGILE WORLD</span><h3 class="font-black text-[12px] md:text-base truncate mt-0.5">FLASH EVANGILE WORLD</h3><p class="text-[11px] md:text-sm text-[#B3B3B3] truncate">La voix du Gospel dans le monde entier</p></div>
<button onclick="openDonateGW()" class="bg-[#FFD700] text-black px-2.5 py-2 rounded-full font-black text-[10px] md:text-sm shrink-0 fire">💛 SOUTENIR<br>629-757-411</button>
</div>
<div class="action-row mt-2.5 flex gap-2 flex-wrap"><button onclick="startRadio()" class="gold-btn px-3.5 py-2.5 rounded-full font-black text-[11px] fire">📻 RADIO ROYAUME</button><button onclick="playFirst()" class="bg-white text-black px-3.5 py-2.5 rounded-full font-black text-[11px]">🔀 ALEATOIRE</button><button onclick="openDonateGW()" class="bg-[#FFD700] text-black px-3.5 py-2.5 rounded-full font-black text-[11px]">💛 SOUTENIR GW - 629-757-411</button><button onclick="toggleKingdom()" class="bg-purple-600 px-3.5 py-2.5 rounded-full font-black text-[11px]">👑 MODE ROYAUME</button></div>
<div class="mt-2.5 bg-black/40 rounded-full py-1.5 overflow-hidden"><div class="marquee text-[#FFD700] text-[11px] md:text-sm font-bold">⚡ FLASH EVANGILE WORLD - 👑 ROYAUME DE DIEU - KINGDOM OF GOD - 🌍 GOSPEL WORLD GLOBAL - 💛 SOUTENIR GOSPEL WORLD - ORANGE MONEY 629-757-411 - TELECHARGEMENT HD - 👑 ROYAUME DE DIEU ⚡</div></div>
<div id="statsBar" class="mt-2.5 grid grid-cols-4 gap-2 max-w-3xl"></div>
<div class="flags-row mt-2.5 flex gap-2 flex-wrap"><span class="bg-white/10 px-2.5 py-1 rounded-full text-[11px]">🇬🇳 Guinée</span><span class="bg-white/10 px-2.5 py-1 rounded-full text-[11px]">🇫🇷 France</span><span class="bg-white/10 px-2.5 py-1 rounded-full text-[11px]">🇺🇸 USA</span><span class="bg-white/10 px-2.5 py-1 rounded-full text-[11px]">🇨🇮 Côte d'Ivoire</span><span class="bg-white/10 px-2.5 py-1 rounded-full text-[11px]">🇨🇦 Canada</span><span class="bg-[#FFD700] text-black px-2.5 py-1 rounded-full text-[11px] font-black">🌍 + 120 PAYS</span></div>
</section>
<section class="px-3 md:px-6 mt-3">
<input id="search" oninput="render();renderSpotify()" placeholder="🔍 Que veux-tu écouter ? Artiste, titre..." class="w-full rounded-full px-4 py-2.5 outline-none text-sm">
<div class="filter-row mt-2.5 flex gap-2 flex-wrap">
<button onclick="showTab('all',this)" class="tab-btn pill-active chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">Tout</button>
<button onclick="showTab('SINGLE',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">🎵 Single</button>
<button onclick="showTab('EP',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">📀 EP</button>
<button onclick="showTab('MIXTAPE',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">🔥 Mixtape</button>
<button onclick="showTab('ALBUM',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">💿 Album</button>
<button onclick="showTab('LIVE SESSION',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">🔴 Live</button>
<button onclick="showTab('ACAPELLA',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">🎤 Acapella</button>
<button onclick="showTab('WORSHIP NIGHT',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">🙏 Worship</button>
<button onclick="showTab('TOP',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">🌍 Top Mondial</button>
<button onclick="showTab('LIKED',this)" class="tab-btn chip px-3.5 py-1.5 rounded-full text-xs md:text-sm font-bold">❤️ Likes</button>
</div>
<h2 id="sectionTitle" class="text-[17px] md:text-2xl font-black mt-2.5">⚡ FLASH ÉVANGILE WORLD</h2>
</section>
<div class="px-1 md:px-4">
<div class="spot-title">Titres tendance 🔥 <span onclick="showTab('TOP',null)">Tout afficher</span></div><div id="spotTrending" class="spot-row"></div>
<div class="spot-title">Artistes populaires 🎤 <span>Tout afficher</span></div><div id="spotArtists" class="spot-row"></div>
<div class="spot-title">Albums et singles populaires 💿 <span>Tout afficher</span></div><div id="spotAlbums" class="spot-row"></div>
<div class="spot-title">Nouveautés du Royaume ✨ <span>Tout afficher</span></div><div id="spotNew" class="spot-row"></div>
<div class="spot-title">Radio Royaume 📻 - Pour toi <span onclick="startRadio()">Ecouter</span></div><div id="spotRadio" class="spot-row"></div>
<div class="spot-title">Worship & Adoration 🙏 <span onclick="showTab('WORSHIP NIGHT',null)">Tout afficher</span></div><div id="spotWorship" class="spot-row"></div>
<div class="spot-title">Live Sessions 🔴 <span onclick="showTab('LIVE SESSION',null)">Tout afficher</span></div><div id="spotLive" class="spot-row"></div>
</div>
<section id="grid" class="px-4 md:px-6 mt-6 grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4"></section>
<section class="px-4 md:px-6 mt-8 hidden md:block"><h2 class="text-2xl font-black">🌍 Top Mondial</h2><div id="top10" class="mt-4 space-y-2"></div></section>
<section class="px-4 md:px-6 mt-8 hidden md:block"><h2 class="text-2xl font-black">🎤 Artistes du Royaume ✅</h2><div id="artists" class="mt-4 flex gap-3 overflow-x-auto pb-2"></div></section>
<footer class="px-4 md:px-6 mt-8 pb-4 text-xs text-[#B3B3B3]"><div class="grid grid-cols-2 md:grid-cols-4 gap-4"><div><b class="text-white">GOSPEL WORLD</b><p class="mt-2">A propos</p><p>Presse</p></div><div><b class="text-white">Communautés</b><p class="mt-2">Artistes</p><p>Publicité</p></div><div><b class="text-white">Liens utiles</b><p class="mt-2">Aide</p><p>App mobile</p></div><div><b class="text-white">👑 ROYAUME DE DIEU</b><p class="mt-2">💛 629-757-411</p><p>© 2026 GOSPEL WORLD</p></div></div></footer>
</main></div>
<div class="player-bar fixed bottom-[68px] md:bottom-0 left-0 md:left-auto right-0 md:right-0 w-full md:w-full bg-black border-t border-white/10 p-3 z-50 md:rounded-none">
<div class="flex items-center gap-3 max-w-[1500px] mx-auto">
<div class="flex items-center gap-3 w-[35%] min-w-[130px]"><img id="cover" onclick="openFullPlayer()" src="https://picsum.photos/seed/gospel/100" class="w-11 h-11 md:w-14 md:h-14 rounded-lg cursor-pointer shrink-0"><div class="min-w-0"><h4 id="ptitle" class="font-bold truncate text-[13px] md:text-sm">Choisis un chant</h4><p id="partist" class="text-[11px] md:text-xs text-[#B3B3B3] truncate">GOSPEL WORLD</p><p id="playlistInfo" class="text-[10px] text-[#1DB954]"></p></div></div>
<div class="flex-1 hidden md:block max-w-[600px] mx-auto"><div class="flex justify-center gap-4 items-center"><button onclick="toggleShuffle()" id="shuffleBtn" class="text-[#B3B3B3]"><i class="fa-solid fa-shuffle"></i></button><button onclick="prevSong()" class="text-[#B3B3B3] hover:text-white"><i class="fa-solid fa-backward-step"></i></button><button id="playBtn" class="w-9 h-9 bg-white text-black rounded-full"><i class="fa-solid fa-play"></i></button><button onclick="nextSong()" class="text-[#B3B3B3] hover:text-white"><i class="fa-solid fa-forward-step"></i></button><button onclick="toggleRepeat()" id="repeatBtn" class="text-[#B3B3B3]"><i class="fa-solid fa-repeat"></i></button></div><div class="flex items-center gap-2 mt-1"><span id="curTime" class="text-[11px] text-[#B3B3B3]">0:00</span><div class="flex-1 bg-white/20 h-1 rounded-full cursor-pointer" onclick="seek(event)"><div id="prog" class="h-1 bg-white rounded-full w-0"></div></div><span id="durTime" class="text-[11px] text-[#B3B3B3]">0:00</span></div></div>
<div class="flex items-center gap-2 ml-auto"><button onclick="openQueue()" class="hidden md:block w-8 h-8 text-[#B3B3B3]"><i class="fa-solid fa-list"></i></button><button onclick="openFullPlayer()" class="hidden md:flex w-8 h-8 text-[#B3B3B3] items-center justify-center"><i class="fa-solid fa-expand"></i></button><button onclick="shareCurrent()" class="w-9 h-9 bg-white/10 rounded-full"><i class="fa-solid fa-share-nodes"></i></button><button onclick="downloadCurrent()" class="w-9 h-9 bg-[#1DB954] rounded-full"><i class="fa-solid fa-download"></i></button><button id="playBtnM" class="md:hidden w-11 h-11 bg-white text-black rounded-full shrink-0"><i class="fa-solid fa-play"></i></button></div>
</div><div class="md:hidden mt-2"><div class="w-full bg-white/20 h-1 rounded-full"><div id="progM" class="h-1 bg-white rounded-full w-0"></div></div></div><audio id="audio" class="hidden"></audio></div>
<div class="bottom-nav md:hidden fixed bottom-0 left-0 right-0 bg-black border-t border-white/10 z-[60] flex justify-around py-2.5 pb-3">
<button onclick="goHome()" class="flex flex-col items-center text-[11px] font-bold gap-0.5"><span class="text-lg">🏠</span>Accueil</button>
<button onclick="document.getElementById('search').focus();window.scrollTo({top:650,behavior:'smooth'})" class="flex flex-col items-center text-[11px] gap-0.5"><span class="text-lg">🔍</span>Rechercher</button>
<button onclick="openModal('single')" class="flex flex-col items-center -mt-6"><span class="w-14 h-14 bg-[#FFD700] text-black rounded-full flex items-center justify-center text-2xl font-black border-4 border-[#0A0A12] shadow-lg">+</span><span class="text-[11px] font-black text-[#FFD700]">PUBLIER</span></button>
<button onclick="showTab('TOP',null)" class="flex flex-col items-center text-[11px] gap-0.5"><span class="text-lg">🏆</span>Top</button>
<button onclick="toggleMobileMenu()" class="flex flex-col items-center text-[11px] gap-0.5"><span class="text-lg">☰</span>Menu</button>
</div>
<div id="fullPlayer" class="hidden fixed inset-0 z-[200] flex-col items-center justify-center p-4 text-center overflow-hidden overflow-y-auto">
<div id="fullBg" class="dim-bg"></div><div class="absolute inset-0 bg-gradient-to-b from-purple-900/80 via-black/70 to-black/95"></div>
<button onclick="closeFullPlayer()" class="absolute top-4 right-4 z-20 w-11 h-11 bg-white text-black rounded-full text-lg font-black">✕</button>
<button onclick="closeFullPlayer()" class="absolute top-4 left-4 z-20 bg-white/10 px-4 py-2 rounded-full text-xs font-bold">← RETOUR</button>
<p class="relative z-10 text-[11px] tracking-[3px] text-[#FFD700] font-black mt-8">⚡ FLASH EVANGILE WORLD - 👑 ROYAUME DE DIEU</p>
<div class="relative z-10 dim-stage mt-5"><div class="dim-halo"></div><div class="dim-halo2"></div><img id="fullCover" src="https://picsum.photos/seed/gospel/400" class="dim-photo w-[260px] h-[260px] md:w-[380px] md:h-[380px] rounded-[35px] object-cover relative"><img id="fullArtistPhoto" src="https://picsum.photos/seed/gospel/200" class="dim-artist-pop absolute -bottom-8 -right-2 md:-right-8 w-[100px] h-[100px] md:w-[130px] md:h-[130px] rounded-full object-cover"><div class="absolute -top-3 -left-3 bg-[#FFD700] text-black text-xs font-black px-3 py-1 rounded-full rotate-[-8deg]">👑 ROYAUME</div><div class="absolute -bottom-2 left-4 bg-red-500 text-white text-xs font-black px-3 py-1 rounded-full animate-pulse">🔴 LIVE</div></div>
<div class="relative z-10 mt-10"><h2 id="fullTitle" class="text-2xl md:text-4xl font-black">Choisis un chant</h2><p class="mt-1"><span id="fullArtist" class="text-[#FFD700] font-black">GOSPEL WORLD ✅</span> <span class="text-[#B3B3B3] text-sm">- Artiste du Royaume</span></p><p id="fullType" class="text-xs text-white/70 mt-1">🎵 SINGLE - 🌍 Mondial</p></div>
<div class="viz w-[280px] md:w-[380px] mt-4 relative z-10" id="viz"></div>
<div class="w-[280px] md:w-[420px] mt-3 relative z-10"><div class="flex justify-between text-xs text-white/80"><span id="fullCur">0:00</span><span id="fullDur">0:00</span></div><div class="w-full bg-white/20 h-2 rounded-full mt-1 cursor-pointer" onclick="seek(event)"><div id="fullProg" class="h-2 bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-400 rounded-full w-0"></div></div></div>
<div class="flex items-center gap-4 mt-5 relative z-10"><button onclick="prevSong()" class="w-12 h-12 bg-white/10 rounded-full text-xl"><i class="fa-solid fa-backward"></i></button><button onclick="togglePlay()" id="fullPlayBtn" class="w-[76px] h-[76px] bg-[#FFD700] text-black rounded-full text-3xl glow beat"><i class="fa-solid fa-play"></i></button><button onclick="nextSong()" class="w-12 h-12 bg-white/10 rounded-full text-xl"><i class="fa-solid fa-forward"></i></button></div>
<div class="flex gap-2 mt-5 flex-wrap justify-center relative z-10 pb-8"><button onclick="openLyrics()" class="bg-white/10 px-4 py-2 rounded-full text-sm font-bold">📖 Paroles</button><button onclick="openArtistFromPlayer()" class="bg-white text-black px-4 py-2 rounded-full text-sm font-bold">🎤 Voir l'artiste</button><button onclick="donateCurrentArtist()" class="money-btn px-4 py-2 rounded-full text-sm font-bold">🙏 Soutenir l'artiste</button><button onclick="openDonateGW()" class="money-gw px-4 py-2 rounded-full text-sm font-bold">💛 Soutenir GW - 629-757-411</button></div>
</div>
<div id="donateModal" class="hidden fixed inset-0 bg-black/90 z-[220] flex items-center justify-center p-4"><div class="bg-[#181818] rounded-[20px] p-5 max-w-sm w-full text-center border border-[#FFD700]/30"><div class="flex justify-between"><h3 id="donateTitle" class="font-black text-lg">🙏 Soutenir</h3><button onclick="document.getElementById('donateModal').classList.add('hidden')" class="w-8 h-8 bg-white text-black rounded-full font-black">✕</button></div><p id="donateDesc" class="text-sm text-[#B3B3B3] mt-2"></p><p id="donateNumber" class="text-xl font-black text-[#FFD700] mt-3"></p><div class="grid grid-cols-3 gap-2 mt-4"><button onclick="doDonate(5000)" class="bg-white/10 py-3 rounded-xl font-bold">5.000 GNF</button><button onclick="doDonate(10000)" class="bg-[#FFD700] text-black py-3 rounded-xl font-bold">10.000 GNF</button><button onclick="doDonate(20000)" class="bg-white/10 py-3 rounded-xl font-bold">20.000 GNF</button></div><p class="text-xs text-[#B3B3B3] mt-3">Don DIRECT, sans intermediaire.<br><span class="text-[#FFD700]">🎁 Bonus Ciel: Dieu te benisse!</span></p></div></div>
<div id="lyricsModal" class="hidden fixed inset-0 bg-black/90 z-[210] flex items-center justify-center p-4"><div class="bg-[#181818] rounded-[20px] p-5 max-w-md w-full text-center"><div class="flex justify-between"><h3 class="font-black">📖 Paroles</h3><button onclick="document.getElementById('lyricsModal').classList.add('hidden')" class="w-8 h-8 bg-white text-black rounded-full font-black">✕</button></div><p id="lyricsText" class="mt-4 text-sm leading-relaxed text-[#B3B3B3]"></p></div></div>
<div id="queueModal" class="hidden fixed inset-0 bg-black/90 z-[210] flex items-center justify-center p-4"><div class="bg-[#181818] rounded-[20px] p-5 max-w-md w-full"><div class="flex justify-between"><h3 class="font-black">📋 File d'attente</h3><button onclick="document.getElementById('queueModal').classList.add('hidden')" class="w-8 h-8 bg-white text-black rounded-full font-black">✕</button></div><div id="queueList" class="mt-3 space-y-2 max-h-[300px] overflow-y-auto"></div></div></div>
<div id="shareModal" class="hidden fixed inset-0 bg-black/90 z-[120] flex items-center justify-center p-4"><div class="bg-[#181818] rounded-[20px] p-5 max-w-sm w-full text-center"><div class="flex justify-between"><h3 class="font-black">Partager 🌍</h3><button onclick="document.getElementById('shareModal').classList.add('hidden')" class="w-8 h-8 bg-white text-black rounded-full font-black">✕</button></div><p id="shareTitle" class="text-sm text-[#B3B3B3] mb-4"></p><div class="grid grid-cols-3 gap-3"><button onclick="shareTo('whatsapp')" class="bg-[#25D366] py-3 rounded-2xl font-bold text-sm">WhatsApp</button><button onclick="shareTo('facebook')" class="bg-[#1877F2] py-3 rounded-2xl font-bold text-sm">Facebook</button><button onclick="shareTo('telegram')" class="bg-[#0088cc] py-3 rounded-2xl font-bold text-sm">Telegram</button><button onclick="shareTo('x')" class="bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm">X</button><button onclick="shareTo('tiktok')" class="bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm">TikTok</button><button onclick="shareTo('copy')" class="bg-white/10 py-3 rounded-2xl font-bold text-sm">Copier</button></div></div></div>
<div id="commentModal" class="hidden fixed inset-0 bg-black/90 z-[125] flex items-center justify-center p-4"><div class="bg-[#181818] rounded-[20px] p-5 max-w-md w-full"><div class="flex justify-between"><h3 class="font-black">💬 Commentaires</h3><button onclick="document.getElementById('commentModal').classList.add('hidden')" class="w-8 h-8 bg-white text-black rounded-full font-black">✕</button></div><p id="commentTitle" class="text-sm text-[#B3B3B3]"></p><div id="commentList" class="mt-3 space-y-2 max-h-[200px] overflow-y-auto"></div><div class="flex gap-2 mt-3"><input id="commentInput" placeholder="Dis Amen..." class="flex-1 rounded-full px-4 py-2"><button onclick="addComment()" class="bg-[#FFD700] text-black px-4 rounded-full font-bold">Envoyer</button></div></div></div>
<div id="artistModal" class="hidden fixed inset-0 bg-black/90 z-[130] flex items-center justify-center p-4"><div class="bg-[#181818] rounded-[20px] p-5 max-w-md w-full text-center max-h-[90vh] overflow-y-auto"><div class="flex justify-end"><button onclick="document.getElementById('artistModal').classList.add('hidden')" class="w-8 h-8 bg-white text-black rounded-full font-black">✕</button></div><div id="artistContent"></div></div></div>
<div id="modal" class="hidden fixed inset-0 bg-black/80 z-[100] flex items-start md:items-center justify-center p-2 md:p-4 overflow-y-auto"><div class="modal-box bg-[#181818] rounded-[18px] p-3 md:p-6 w-full max-w-2xl my-2 md:my-8 relative">
<div class="sticky top-0 z-10 flex justify-between items-center bg-[#181818] pb-2 -mx-1 px-1"><h3 id="modalTitle" class="text-base md:text-2xl font-black">🎤 STUDIO - Publier</h3><button onclick="closeModal()" class="w-9 h-9 min-w-[36px] bg-white text-black rounded-full font-black text-lg leading-none shrink-0 shadow-lg">✕</button></div>
<p class="text-[11px] md:text-sm text-[#FFD700] mb-2">👉 CHOISIS TON TYPE, PUIS BALANCE TES SONS!</p>
<p class="font-black text-[11px] md:text-sm mb-1.5">1 - CHOISIS TON TYPE 👇</p>
<div class="grid grid-cols-3 gap-1.5 md:gap-2 mb-2">
<button type="button" onclick="selectType('SINGLE','🎵 SINGLE - 1 Son','single')" class="type-btn active bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="SINGLE"><span class="block text-base md:text-xl">🎵</span><b class="text-[11px] md:text-sm block">SINGLE</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">1 Son</span></button>
<button type="button" onclick="selectType('EP','📀 EP - 3 a 6 Sons','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="EP"><span class="block text-base md:text-xl">📀</span><b class="text-[11px] md:text-sm block">EP</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">3-6 Sons</span></button>
<button type="button" onclick="selectType('MIXTAPE','🔥 MIXTAPE - 7 a 12 Sons','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="MIXTAPE"><span class="block text-base md:text-xl">🔥</span><b class="text-[11px] md:text-sm block">MIXTAPE</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">7-12 Sons</span></button>
<button type="button" onclick="selectType('ALBUM','💿 ALBUM - 13 Sons et +','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="ALBUM"><span class="block text-base md:text-xl">💿</span><b class="text-[11px] md:text-sm block">ALBUM</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">13+ Sons</span></button>
<button type="button" onclick="selectType('LIVE SESSION','🔴 LIVE SESSION - 5 a 10 Sons','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="LIVE SESSION"><span class="block text-base md:text-xl">🔴</span><b class="text-[11px] md:text-sm block">LIVE</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">5-10 Sons</span></button>
<button type="button" onclick="selectType('ACAPELLA','🎤 ACAPELLA - 1 a 5 Sons','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="ACAPELLA"><span class="block text-base md:text-xl">🎤</span><b class="text-[11px] md:text-sm block">ACAPELLA</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">1-5 Sons</span></button>
<button type="button" onclick="selectType('WORSHIP NIGHT','🙏 WORSHIP NIGHT - 8 a 15 Sons','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="WORSHIP NIGHT"><span class="block text-base md:text-xl">🙏</span><b class="text-[11px] md:text-sm block">WORSHIP</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">8-15 Sons</span></button>
<button type="button" onclick="selectType('COMPILATION ROYAUME','🌍 COMPILATION - 10 a 20 Sons','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="COMPILATION ROYAUME"><span class="block text-base md:text-xl">🌍</span><b class="text-[11px] md:text-sm block">COMPILATION</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">10-20 Sons</span></button>
<button type="button" onclick="selectType('SPOKEN WORD','📖 SPOKEN WORD - 1 a 3 Sons','collection')" class="type-btn bg-white/10 py-2 md:py-3 rounded-lg md:rounded-xl text-center" data-type="SPOKEN WORD"><span class="block text-base md:text-xl">📖</span><b class="text-[11px] md:text-sm block">SPOKEN</b><span class="text-[9px] md:text-[11px] text-[#B3B3B3]">1-3 Sons</span></button>
</div>
<div id="typeInfo" class="bg-[#FFD700] text-black rounded-lg p-2 text-[11px] md:text-sm font-bold mb-2">🎵 SINGLE - 1 Son - 1 fichier MP3</div>
<form id="upForm" class="space-y-2"><input id="artist" placeholder="2 - Nom artiste - Ex: Jonathan" required class="w-full rounded-lg px-3 py-2 text-sm"><input id="titre" placeholder="3 - Titre - Ex: Mon Chant" required class="w-full rounded-lg px-3 py-2 text-sm"><input id="artistOM" placeholder="4 - Ton Orange Money / Wave - Ex: 622123456" required class="w-full rounded-lg px-3 py-2 text-sm border !border-yellow-500/50"><p class="text-[10px] md:text-xs text-[#FFD700]">💰 C'est sur ce numero que les fans vont t'envoyer les dons. 100% pour toi.</p><div id="collectionFields" class="hidden space-y-2"><textarea id="desc" placeholder="Description de ton projet..." class="w-full rounded-lg px-3 py-2 text-sm"></textarea></div><div class="border-2 border-dashed border-[#FFD700]/50 rounded-lg p-2.5 text-center"><label class="text-[11px] md:text-sm font-bold">5 - COVER (photo) 📸</label><input id="coverFile" type="file" accept="image/*" class="w-full mt-1 text-xs"></div><div class="border-2 border-dashed border-[#1DB954] rounded-lg p-2.5 text-center"><label class="text-[11px] md:text-sm font-bold">6 - FICHIERS AUDIO MP3 🎵</label><input id="files" type="file" accept=".mp3,audio/*" multiple required class="w-full mt-1 text-xs"><p id="fileInfo" class="text-[10px] text-[#FFD700] mt-1">Pour SINGLE: choisis 1 seul MP3.</p><p id="fileCount" class="text-[10px] font-black mt-1 text-white"></p></div><button class="w-full bg-[#FFD700] text-black font-black py-2.5 rounded-xl text-sm md:text-lg">🚀 PUBLIER</button><p id="status" class="text-center text-xs"></p><button type="button" onclick="closeModal()" class="w-full bg-white/10 py-2 rounded-full text-xs font-bold">❌ ANNULER / SORTIR</button></form></div></div>
<script>
// V27 - INSTALLATION DIRECTE SANS CHROME
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', {scope: '/'}).then(() => {
      console.log('GOSPEL WORLD installee - Service Worker OK');
    }).catch(() => {});
  });
}
let ALL=[], CURRENT=[], CURRENT_INDEX=0, FILTER='all', LIKES=JSON.parse(localStorage.getItem('gw_likes')||'[]'), COMMENTS=JSON.parse(localStorage.getItem('gw_comments')||'{}'), deferredPrompt=null, SHUFFLE=false, REPEAT=false, RADIO=false, KINGDOM=false, DONATE_TARGET={type:'gw',name:'GOSPEL WORLD',number:''}, SELECTED_TYPE='SINGLE', SELECTED_MODE='single', CURRENT_COVER='', FOLLOWED=JSON.parse(localStorage.getItem('gw_follow')||'[]');
const audio=document.getElementById('audio'); const playBtn=document.getElementById('playBtn'); const playBtnM=document.getElementById('playBtnM');
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault(); deferredPrompt=e;});
function installApp(){
  if(deferredPrompt){
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choice) => {
      if(choice.outcome === 'accepted'){
        alert('✅ MERCI! GOSPEL WORLD est en train de s installer sur ton téléphone! Regarde ton écran d accueil dans 5 secondes!');
      }
      deferredPrompt = null;
    });
  } else {
    alert("📥 Pour installer GOSPEL WORLD comme TikTok:\\n\\n1. Clique sur les 3 points ⋮ en haut à droite de Chrome\\n2. Clique sur 'Installer l'application' ou 'Ajouter à l'écran d'accueil'\\n3. Clique sur 'Installer'\\n\\nL'icône GOSPEL WORLD va apparaître sur ton écran d'accueil!");
  }
}
function toggleKingdom(){ KINGDOM=!KINGDOM; document.body.style.background=KINGDOM?'linear-gradient(180deg,#1A0F00,#2D0A4A,#000)':'#08080F'; alert(KINGDOM?'👑 MODE ROYAUME ACTIVE - Bienvenue dans le Royaume de Dieu!':'Mode normal'); }
function createStars(){ let c=document.getElementById('stars'); for(let i=0;i<30;i++){ let s=document.createElement('div'); s.className='star'; let sz=Math.random()*3+1; s.style.width=sz+'px'; s.style.height=sz+'px'; s.style.left=Math.random()*100+'vw'; s.style.animationDuration=(Math.random()*4+3)+'s'; s.style.animationDelay=Math.random()*4+'s'; s.style.opacity=Math.random(); c.appendChild(s); } }
createStars();
function toggleMobileMenu(){ let m=document.getElementById('mobileMenu'); let o=document.getElementById('mobileOverlay'); if(m.classList.contains('closed')){ m.classList.remove('closed'); m.classList.add('open'); o.classList.remove('hidden'); } else { m.classList.add('closed'); m.classList.remove('open'); o.classList.add('hidden'); } }
function selectType(type, label, mode){
  SELECTED_TYPE=type; SELECTED_MODE=mode;
  document.querySelectorAll('.type-btn').forEach(b=>b.classList.remove('active'));
  document.querySelector(`[data-type="${type}"]`).classList.add('active');
  document.getElementById('typeInfo').innerText=label;
  document.getElementById('modalTitle').innerText='🎤 STUDIO - Publier '+type;
  document.getElementById('collectionFields').classList.toggle('hidden', mode==='single');
  let fi=document.getElementById('fileInfo');
  if(type==='SINGLE') fi.innerText='Pour SINGLE: choisis 1 seul MP3.';
  else if(type==='EP') fi.innerText='Pour EP: choisis 3 a 6 MP3 en meme temps.';
  else if(type==='MIXTAPE') fi.innerText='Pour MIXTAPE: choisis 7 a 12 MP3 en meme temps.';
  else if(type==='ALBUM') fi.innerText='Pour ALBUM: choisis 13 MP3 et + en meme temps.';
  else if(type==='LIVE SESSION') fi.innerText='Pour LIVE SESSION: choisis 5 a 10 MP3 enregistres en live.';
  else if(type==='ACAPELLA') fi.innerText='Pour ACAPELLA: choisis 1 a 5 MP3 voix seule.';
  else if(type==='WORSHIP NIGHT') fi.innerText='Pour WORSHIP NIGHT: choisis 8 a 15 MP3 d adoration.';
  else if(type==='COMPILATION ROYAUME') fi.innerText='Pour COMPILATION: choisis 10 a 20 MP3.';
  else fi.innerText='Pour SPOKEN WORD: choisis 1 a 3 fichiers audio.';
  document.getElementById('upForm').dataset.mode=mode;
  document.getElementById('upForm').dataset.ptype=type;
}
document.getElementById('files').addEventListener('change', function(){ let n=this.files.length; document.getElementById('fileCount').innerText='✅ Tu as choisi '+n+' fichier(s) pour '+SELECTED_TYPE+' - Parfait!'; });
function goHome(){ FILTER='all'; document.getElementById('search').value=''; render(); renderSpotify(); window.scrollTo({top:0,behavior:'smooth'}); }
function toggleShuffle(){ SHUFFLE=!SHUFFLE; document.getElementById('shuffleBtn').style.color=SHUFFLE?'#1DB954':'#B3B3B3'; }
function toggleRepeat(){ REPEAT=!REPEAT; document.getElementById('repeatBtn').style.color=REPEAT?'#1DB954':'#B3B3B3'; }
function fmt(s){ if(!s) return '0:00'; return Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0'); }
function seek(e){ let r=e.currentTarget.getBoundingClientRect(); audio.currentTime=(e.clientX-r.left)/r.width*audio.duration; }
function openDonateGW(){ fetch('/api/gw-number').then(r=>r.json()).then(d=>{ DONATE_TARGET={type:'gw',name:'GOSPEL WORLD',number:d.display}; document.getElementById('donateTitle').innerText='💛 Soutenir GOSPEL WORLD - ROYAUME DE DIEU'; document.getElementById('donateDesc').innerText='Ton don aide a payer le serveur, l\\'app et a faire grandir FLASH EVANGILE WORLD dans le monde entier. Merci! Dieu te benisse! 🙏👑'; document.getElementById('donateNumber').innerText='Orange Money: '+d.display; document.getElementById('donateModal').classList.remove('hidden'); }); }
function donateArtist(id){ let it=ALL.find(x=>x.id===id); if(!it) return; DONATE_TARGET={type:'artist',name:it.artist,number:it.artist_om||'Non renseigne'}; document.getElementById('donateTitle').innerText='🙏 Soutenir '+it.artist; document.getElementById('donateDesc').innerText='Ton don va DIRECT a '+it.artist+' a 100%. Gospel World ne prend rien.'; document.getElementById('donateNumber').innerText='Orange Money / Wave: '+(it.artist_om||'Non renseigne'); document.getElementById('donateModal').classList.remove('hidden'); }
function donateCurrentArtist(){ let s=CURRENT[CURRENT_INDEX]; if(!s) return alert('Choisis un son'); let it=ALL.find(x=>x.id===s.id)||ALL.find(x=>x.artist===s.artist); if(it) donateArtist(it.id); }
function openArtistFromPlayer(){ let s=CURRENT[CURRENT_INDEX]; if(!s) return; closeFullPlayer(); setTimeout(()=>openArtist(s.artist),300); }
function doDonate(amount){ navigator.clipboard.writeText(DONATE_TARGET.number||''); alert('Numero copie: '+(DONATE_TARGET.number||'')+'\\n\\nEnvoie '+amount.toLocaleString()+' GNF par Orange Money / Wave a '+DONATE_TARGET.name+'\\n\\n🎁 Bonus Ciel: Dieu te benisse abondamment!'); }
async function load(){ let r=await fetch('/api/all'); let d=await r.json(); ALL=d.items; let v=await fetch('/api/verse').then(x=>x.json()); document.getElementById('verseText').innerText='"'+v.text+'"'; document.getElementById('verseRef').innerText='- '+v.ref+' - FLASH EVANGILE WORLD'; render(); renderTop(); renderArtists(); renderStats(); renderStories(); renderSpotify(); renderLibrary(); }
function startRadio(){ if(!ALL.length) return alert('Pas encore de sons - Publie sur FLASH EVANGILE WORLD'); RADIO=true; CURRENT=ALL.flatMap(x=>x.type==='SINGLE'?[{title:x.title,artist:x.artist,file:x.file,id:x.id,cover:x.cover,type:x.type}]:x.songs.map(s=>({title:s.title,artist:x.artist,file:s.file,id:x.id,cover:x.cover,type:x.type}))); CURRENT_INDEX=Math.floor(Math.random()*CURRENT.length); playCurrent('📻 RADIO ROYAUME DE DIEU'); }
function openFullPlayer(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son'); let fp=document.getElementById('fullPlayer'); fp.classList.remove('hidden'); fp.classList.add('flex'); }
function closeFullPlayer(){ let fp=document.getElementById('fullPlayer'); fp.classList.add('hidden'); fp.classList.remove('flex'); }
function openLyrics(){ let s=CURRENT[CURRENT_INDEX]; if(!s) return; document.getElementById('lyricsText').innerHTML=`<b>${s.title} - ${s.artist}</b><br><br>Gloire a Dieu... 🙏<br>Chante avec tout ton coeur<br>Jesus est Roi, Il regne a jamais<br>Dans le Royaume de Dieu! Alleluia! Amen! 🔥👑`; document.getElementById('lyricsModal').classList.remove('hidden'); }
function openQueue(){ document.getElementById('queueList').innerHTML=CURRENT.map((s,i)=>`<div class='flex gap-3 bg-white/5 p-2 rounded-xl ${i===CURRENT_INDEX?'border border-green-400':''}'><span>${i+1}.</span><div><b class='text-sm block'>${s.title}</b><span class='text-xs text-[#B3B3B3]'>${s.artist} ${i===CURRENT_INDEX?'▶ EN COURS':''}</span></div></div>`).join('')||'File vide'; document.getElementById('queueModal').classList.remove('hidden'); }
function showTab(f,btn){ FILTER=f; document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('pill-active')); if(btn && btn.classList.contains('tab-btn')) btn.classList.add('pill-active'); document.getElementById('sectionTitle').innerText=f==='TOP'?'🌍 Top Mondial':f==='LIKED'?'❤️ Titres likés':'⚡ FLASH ÉVANGILE WORLD'; render(); renderSpotify(); window.scrollTo({top:600,behavior:'smooth'}); }
function toggleLike(id){ if(LIKES.includes(id)) LIKES=LIKES.filter(x=>x!==id); else LIKES.push(id); localStorage.setItem('gw_likes',JSON.stringify(LIKES)); render(); renderTop(); renderSpotify(); fetch('/api/like',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})}); }
function likeCurrent(){ let s=CURRENT[CURRENT_INDEX]; if(!s) return; toggleLike(s.id); }
function toggleFollow(name){ if(FOLLOWED.includes(name)) FOLLOWED=FOLLOWED.filter(x=>x!==name); else FOLLOWED.push(name); localStorage.setItem('gw_follow',JSON.stringify(FOLLOWED)); renderSpotify(); renderLibrary(); }
function renderLibrary(){ let el=document.getElementById('libList'); if(!el) return; let map={}; ALL.forEach(x=>{ if(!map[x.artist]) map[x.artist]=x; }); el.innerHTML=Object.entries(map).slice(0,8).map(([n,info])=>`<div onclick="openArtist('${n}')" class='flex gap-2 items-center p-2 rounded-lg hover:bg-white/5 cursor-pointer'><img src='${info.cover}' class='w-10 h-10 rounded-lg object-cover'><div class='min-w-0'><b class='text-sm truncate block'>${n}</b><span class='text-xs text-[#B3B3B3]'>Artiste ✅</span></div></div>`).join(''); }
function renderStats(){ let artists=new Set(ALL.map(x=>x.artist)).size; let likes=ALL.reduce((a,x)=>a+(x.likes||0),0); document.getElementById('statsBar').innerHTML=`<div class='bg-white/5 rounded-xl p-2 md:p-3 text-center border border-yellow-500/20'><b class='text-lg md:text-xl text-[#FFD700]'>${ALL.length}</b><p class='text-[10px] md:text-xs text-[#B3B3B3]'>Projets</p></div><div class='bg-white/5 rounded-xl p-2 md:p-3 text-center border border-yellow-500/20'><b class='text-lg md:text-xl text-[#FFD700]'>${artists}</b><p class='text-[10px] md:text-xs text-[#B3B3B3]'>Artistes ✅</p></div><div class='bg-white/5 rounded-xl p-2 md:p-3 text-center border border-yellow-500/20'><b class='text-lg md:text-xl text-[#FFD700]'>${likes}</b><p class='text-[10px] md:text-xs text-[#B3B3B3]'>Likes</p></div><div class='bg-gradient-to-br from-yellow-500 to-pink-500 rounded-xl p-2 md:p-3 text-center'><b class='text-base md:text-xl text-black'>🌍 120+</b><p class='text-[10px] md:text-xs text-black font-bold'>Pays</p></div>`; let ss=document.getElementById('statsSide'); if(ss) ss.innerText=`${ALL.length} projets - ${artists} artistes - 🌍 Mondial`; }
function renderStories(){ let map={}; ALL.forEach(x=>{ if(!map[x.artist]) map[x.artist]=x.cover; }); document.getElementById('stories').innerHTML=Object.entries(map).map(([n,c])=>`<div onclick="openArtist('${n}')" class='shrink-0 text-center cursor-pointer'><div class='story-ring w-[48px] h-[48px] md:w-[68px] md:h-[68px]'><img src='${c}' class='w-full h-full rounded-full object-cover border-2 border-black'></div><p class='text-[11px] mt-1 truncate w-[48px] md:w-[68px]'>${n} ✅</p></div>`).join(''); }
function renderSpotify(){
  let q=(document.getElementById('search').value||'').toLowerCase();
  let list=ALL.filter(x=>{ if(FILTER==='LIKED' && !LIKES.includes(x.id)) return false; if(FILTER!=='all' && FILTER!=='LIKED' && FILTER!=='TOP' && x.type!==FILTER) return false; if(q && !(x.title.toLowerCase().includes(q)||x.artist.toLowerCase().includes(q))) return false; return true; });
  if(FILTER==='TOP') list=[...list].sort((a,b)=>(b.likes||0)-(a.likes||0)).slice(0,20);
  let card = (x)=>`<div class="spot-card" onclick="playSingle('${x.id}')"><img src="${x.cover}"><div class="spot-play">▶</div><h4>${x.title}</h4><p>${x.artist} ✅ - ${x.type}</p></div>`;
  let artistCard = (name,info)=>`<div class="spot-card artist" onclick="openArtist('${name}')"><img src="${info.cover}"><div class="spot-play">▶</div><h4>${name}</h4><p>Artiste ✅</p></div>`;
  let set=(id,html)=>{let e=document.getElementById(id); if(e) e.innerHTML=html||'<p style="padding:0 12px;color:#888">Pas encore - Publie le premier!</p>'};
  set('spotTrending', [...list].sort((a,b)=>(b.likes||0)-(a.likes||0)).map(card).join(''));
  set('spotAlbums', list.map(card).join(''));
  set('spotNew', [...list].reverse().map(card).join(''));
  set('spotRadio', [...list].sort(()=>Math.random()-0.5).map(card).join(''));
  set('spotWorship', list.filter(x=>x.type==='WORSHIP NIGHT'||x.type==='ACAPELLA').map(card).join(''));
  set('spotLive', list.filter(x=>x.type==='LIVE SESSION').map(card).join(''));
  let map={}; ALL.forEach(x=>{ if(!map[x.artist]) map[x.artist]=x; });
  set('spotArtists', Object.entries(map).map(([n,i])=>artistCard(n,i)).join(''));
}
function renderTop(){ let top=[...ALL].sort((a,b)=>(b.likes||0)-(a.likes||0)).slice(0,10); let el=document.getElementById('top10'); if(!el) return; el.innerHTML=top.map((x,i)=>`<div class='flex items-center gap-3 bg-[#181818] p-3 rounded-xl border border-white/5'><span class='w-8 text-center font-black text-[#FFD700] text-lg'>${i+1}</span><img src='${x.cover}' class='w-12 h-12 rounded-lg object-cover'><div class='flex-1 min-w-0'><b class='truncate block'>${x.title}</b><span class='text-xs text-[#B3B3B3]'>${x.artist} ✅ - ${x.type} - ❤️ ${x.likes||0}</span></div><button onclick="playSingle('${x.id}')" class='w-10 h-10 bg-[#1DB954] text-black rounded-full'>▶</button></div>`).join(''); }
function renderArtists(){ let map={}; ALL.forEach(x=>{ if(!map[x.artist]) map[x.artist]={cover:x.cover,count:0}; map[x.artist].count++; }); let el=document.getElementById('artists'); if(!el) return; el.innerHTML=Object.entries(map).map(([name,info])=>`<div onclick="openArtist('${name}')" class='shrink-0 w-[120px] text-center cursor-pointer'><img src='${info.cover}' class='w-[120px] h-[120px] rounded-full object-cover border-2 border-[#FFD700]'><b class='block mt-2 truncate'>${name} ✅</b><span class='text-xs text-[#B3B3B3]'>${info.count} projet(s)</span></div>`).join(''); }
function openArtist(name){ let list=ALL.filter(x=>x.artist===name); let om=list[0].artist_om||''; let isF=FOLLOWED.includes(name); document.getElementById('artistContent').innerHTML=`<div class='relative inline-block'><img src='${list[0].cover}' class='w-32 h-32 rounded-full mx-auto object-cover border-4 border-[#FFD700] glow'><span class='absolute -bottom-1 -right-1 bg-[#FFD700] text-black text-xs font-black px-2 py-1 rounded-full'>✅ VERIFIE</span></div><h3 class='font-black text-2xl mt-3'>${name} ✅</h3><p class='text-[#B3B3B3] text-sm'>Artiste du Royaume - ${list.length} projet(s) - 🌍 Mondial</p><div class='flex gap-2 mt-3'><button onclick="toggleFollow('${name}');openArtist('${name}')" class='flex-1 ${isF?'bg-white/10':'bg-[#1DB954] text-black'} py-2 rounded-full font-bold text-sm'>${isF?'✅ Suivi':'➕ Suivre'}</button><button onclick="document.getElementById('artistModal').classList.add('hidden');donateArtist('${list[0].id}')" class='flex-1 money-btn py-2 rounded-full font-bold text-sm'>🙏 Soutenir - ${om}</button></div><div class='mt-4 space-y-2 text-left'>${list.map(x=>`<div onclick="document.getElementById('artistModal').classList.add('hidden');playSingle('${x.id}')" class='flex gap-3 bg-white/5 p-2 rounded-xl cursor-pointer'><img src='${x.cover}' class='w-10 h-10 rounded-lg'><div><b class='text-sm block'>${x.title}</b><span class='text-xs text-[#B3B3B3]'>${x.type} - ❤️ ${x.likes||0}</span></div></div>`).join('')}</div>`; document.getElementById('artistModal').classList.remove('hidden'); }
function render(){
  let q=(document.getElementById('search').value||'').toLowerCase();
  let list=ALL.filter(x=>{ if(FILTER==='LIKED' && !LIKES.includes(x.id)) return false; if(FILTER==='TOP') return true; if(FILTER!=='all' && FILTER!=='LIKED' && x.type!==FILTER) return false; if(q && !(x.title.toLowerCase().includes(q)||x.artist.toLowerCase().includes(q))) return false; return true; });
  if(FILTER==='TOP') list=[...list].sort((a,b)=>(b.likes||0)-(a.likes||0)).slice(0,10);
  document.getElementById('grid').innerHTML=list.map(item=>{
    let liked=LIKES.includes(item.id)?'❤️':'🤍'; let cmt=(COMMENTS[item.id]||[]).length;
    let shareBtn=`<button onclick="openShare('${item.id}')" class='flex-1 bg-white/10 py-2 rounded-full text-xs font-bold'>PARTAGER 🌍</button>`;
    let dlBtn=`<button onclick="downloadItem('${item.id}')" class='flex-1 bg-[#1DB954] py-2 rounded-full text-xs font-bold'>⬇ HD</button>`;
    let donateArtistBtn=`<button onclick="donateArtist('${item.id}')" class='w-full money-btn py-2 rounded-full text-xs font-bold mt-2'>🙏 SOUTENIR ${item.artist.toUpperCase()} - Orange Money</button>`;
    let donateGWBtn=`<button onclick="openDonateGW()" class='w-full money-gw py-2 rounded-full text-xs font-bold mt-1'>💛 SOUTENIR GOSPEL WORLD - 629-757-411</button>`;
    let cmtBtn=`<button onclick="openComments('${item.id}')" class='w-full bg-white/5 py-1.5 rounded-full text-xs mt-2'>💬 ${cmt} - Laisser un Amen 👑</button>`;
    let countTxt=item.type==='SINGLE'?'1 Son':(item.songs?item.songs.length+' Sons':'');
    if(item.type==='SINGLE') return `<div class='spot-card'><div class='relative'><img src='${item.cover}'><span class='absolute top-2 left-2 bg-[#FFD700] text-black text-[10px] font-black px-2 py-1 rounded-full'>🎵 SINGLE</span><button onclick="playSingle('${item.id}')" class='spot-play !opacity-100' style='opacity:1;transform:none'>▶</button></div><h4>${item.title}</h4><p>${item.artist} ✅ - ❤️ ${item.likes||0}</p><div class='flex gap-2 mt-3'><button onclick="playSingle('${item.id}')" class='flex-1 bg-white text-black font-bold py-2 rounded-full text-sm'>ECOUTER</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div>${donateArtistBtn}${donateGWBtn}${cmtBtn}</div>`;
    else return `<div class='spot-card border border-[#FFD700]/20'><div class='relative'><img src='${item.cover}'><span class='absolute top-2 left-2 bg-[#FFD700] text-black text-[10px] font-black px-2 py-1 rounded-full'>${item.type} - ${countTxt}</span></div><h4>${item.title}</h4><p>${item.artist} ✅ - ❤️ ${item.likes||0}</p><div class='flex gap-2 mt-3'><button onclick="playCollection('${item.id}')" class='flex-1 bg-white text-black font-bold py-2 rounded-full text-sm'>ECOUTER TOUT (${countTxt})</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div>${donateArtistBtn}${donateGWBtn}${cmtBtn}</div>`;
  }).join('')||'<p class="col-span-full text-center py-10 text-[#B3B3B3]">Aucun resultat - Publie le premier projet sur FLASH EVANGILE WORLD 🌍👑</p>';
}
function playFirst(){ if(!ALL.length) return alert('Pas encore de sons - Publie sur FLASH EVANGILE WORLD'); playSingle(ALL[Math.floor(Math.random()*ALL.length)].id); }
function playSingle(id){let s=ALL.find(x=>x.id===id); if(s.type==='SINGLE'){ CURRENT=[{title:s.title,artist:s.artist,file:s.file,id:s.id,cover:s.cover,type:s.type}]; } else { CURRENT=s.songs.map(x=>({title:x.title,artist:s.artist,file:x.file,id:s.id,cover:x.cover,type:s.type})); } CURRENT_INDEX=0; playCurrent();}
function playCollection(id,start=0){let c=ALL.find(x=>x.id===id); if(c.type==='SINGLE'){ CURRENT=[{title:c.title,artist:c.artist,file:c.file,id:c.id,cover:c.cover,type:c.type}]; } else { CURRENT=c.songs.map(s=>({title:s.title,artist:c.artist,file:s.file,id:c.id,cover:c.cover,type:c.type})); } CURRENT_INDEX=start; playCurrent(c.title);}
function playCurrent(coll=''){let s=CURRENT[CURRENT_INDEX]; if(!s) return; let it=ALL.find(x=>x.id===s.id); let cover=s.cover||(it?it.cover:''); CURRENT_COVER=cover; document.getElementById('ptitle').innerText=s.title; document.getElementById('partist').innerText=s.artist; document.getElementById('cover').src=cover; document.getElementById('fullCover').src=cover; document.getElementById('fullArtistPhoto').src=cover; document.getElementById('fullBg').style.backgroundImage=`url(${cover})`; document.getElementById('fullTitle').innerText=s.title; document.getElementById('fullArtist').innerText=s.artist+' ✅'; document.getElementById('fullType').innerText='🎵 '+(s.type||'SINGLE')+' - 🌍 Mondial - 👑 Royaume de Dieu'; document.getElementById('playlistInfo').innerText=coll||'Single'; audio.src=s.file; audio.play(); setPlayIcon(true); startViz();}
function setPlayIcon(p){ let h=p?'<i class="fa-solid fa-pause"></i>':'<i class="fa-solid fa-play"></i>'; playBtn.innerHTML=h; playBtnM.innerHTML=h; document.getElementById('fullPlayBtn').innerHTML=h; }
function nextSong(){ if(SHUFFLE){ CURRENT_INDEX=Math.floor(Math.random()*CURRENT.length); } else if(CURRENT_INDEX<CURRENT.length-1){ CURRENT_INDEX++; } else if(RADIO||REPEAT){ CURRENT_INDEX=0; } else return; playCurrent(RADIO?'📻 RADIO ROYAUME DE DIEU':''); }
function prevSong(){ if(CURRENT_INDEX>0){ CURRENT_INDEX--; playCurrent(); } }
audio.onended=()=>{ if(REPEAT){ audio.currentTime=0; audio.play(); } else nextSong(); };
function togglePlay(){ if(audio.paused){audio.play(); setPlayIcon(true);} else {audio.pause(); setPlayIcon(false);} }
playBtn.onclick=togglePlay; playBtnM.onclick=togglePlay;
audio.ontimeupdate=()=>{ if(audio.duration){ let p=audio.currentTime/audio.duration*100+'%'; document.getElementById('prog').style.width=p; let pm=document.getElementById('progM'); if(pm) pm.style.width=p; document.getElementById('fullProg').style.width=p; document.getElementById('curTime').innerText=fmt(audio.currentTime); document.getElementById('fullCur').innerText=fmt(audio.currentTime); document.getElementById('durTime').innerText=fmt(audio.duration); document.getElementById('fullDur').innerText=fmt(audio.duration); } };
function startViz(){ let v=document.getElementById('viz'); v.innerHTML=''; for(let i=0;i<28;i++){ let d=document.createElement('div'); d.style.height=(Math.random()*40+10)+'px'; v.appendChild(d); } setInterval(()=>{ if(audio.paused) return; [...v.children].forEach(d=>d.style.height=(Math.random()*45+5)+'px'); },150); }
function downloadCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son'); let s=CURRENT[CURRENT_INDEX]; let a=document.createElement('a'); a.href=s.file; a.download=s.title+'_HD_GOSPEL_WORLD.mp3'; a.target='_blank'; a.click(); }
function downloadItem(id){ let it=ALL.find(x=>x.id===id); if(it.type==='SINGLE'){ let a=document.createElement('a'); a.href=it.file; a.download=it.title+'_HD_GOSPEL_WORLD.mp3'; a.target='_blank'; a.click(); } else { it.songs.forEach((s,i)=>setTimeout(()=>{let a=document.createElement('a'); a.href=s.file; a.download=s.title+'_HD.mp3'; a.target='_blank'; a.click();}, i*800)); } }
let SHARE_ID=null, COMMENT_ID=null;
function openShare(id){ SHARE_ID=id; let it=ALL.find(x=>x.id===id); document.getElementById('shareTitle').innerText=it.title+' - '+it.artist; document.getElementById('shareModal').classList.remove('hidden'); }
function shareCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son'); if(navigator.share){let s=CURRENT[CURRENT_INDEX]; navigator.share({title:'GOSPEL WORLD',text:`${s.title} - ${s.artist} sur FLASH EVANGILE WORLD - ROYAUME DE DIEU`,url:location.href});} else openShare(CURRENT[CURRENT_INDEX].id); }
function shareTo(p){ let it=ALL.find(x=>x.id===SHARE_ID); if(!it) return; let url=encodeURIComponent(location.href); let txt=encodeURIComponent(`${it.title} - ${it.artist} sur FLASH EVANGILE WORLD - ROYAUME DE DIEU Ecoute ici: `+location.href); let links={whatsapp:`https://wa.me/?text=${txt}`,facebook:`https://www.facebook.com/sharer/sharer.php?u=${url}`,telegram:`https://t.me/share/url?url=${url}&text=${txt}`,x:`https://twitter.com/intent/tweet?text=${txt}`,tiktok:`https://www.tiktok.com/`}; if(p==='copy'){navigator.clipboard.writeText(location.href+' - '+it.title); alert('Lien copie! Partage dans le monde! 🌍');} else if(p==='tiktok'){navigator.clipboard.writeText(location.href); alert('Lien copie! Colle-le sur TikTok');} else window.open(links[p],'_blank'); document.getElementById('shareModal').classList.add('hidden'); }
function openComments(id){ COMMENT_ID=id; let it=ALL.find(x=>x.id===id); document.getElementById('commentTitle').innerText=it.title+' - '+it.artist; renderComments(); document.getElementById('commentModal').classList.remove('hidden'); }
function renderComments(){ let list=COMMENTS[COMMENT_ID]||[]; document.getElementById('commentList').innerHTML=list.map(c=>`<div class='bg-white/5 p-2 rounded-xl text-sm'>${c}</div>`).join('')||'<p class="text-[#B3B3B3] text-sm">Sois le premier dans le Royaume 🙏👑</p>'; }
function addComment(){ let v=document.getElementById('commentInput').value.trim(); if(!v) return; if(!COMMENTS[COMMENT_ID]) COMMENTS[COMMENT_ID]=[]; COMMENTS[COMMENT_ID].push(v); localStorage.setItem('gw_comments',JSON.stringify(COMMENTS)); document.getElementById('commentInput').value=''; renderComments(); render(); }
function openModal(mode){ document.getElementById('modal').classList.remove('hidden'); document.body.classList.add('modal-open'); if(mode==='single') selectType('SINGLE','🎵 SINGLE - 1 Son','single'); else selectType('EP','📀 EP - 3 a 6 Sons','collection'); }
function closeModal(){document.getElementById('modal').classList.add('hidden'); document.body.classList.remove('modal-open');}
document.getElementById('upForm').onsubmit=async e=>{ e.preventDefault(); let mode=document.getElementById('upForm').dataset.mode||SELECTED_MODE; let ptype=document.getElementById('upForm').dataset.ptype||SELECTED_TYPE; let fd=new FormData(); fd.append('artist',document.getElementById('artist').value); fd.append('titre',document.getElementById('titre').value); fd.append('artist_om',document.getElementById('artistOM').value); fd.append('type',ptype); fd.append('desc',document.getElementById('desc')?document.getElementById('desc').value:''); let cf=document.getElementById('coverFile').files[0]; if(cf) fd.append('cover',cf); for(let f of document.getElementById('files').files) fd.append('files',f); document.getElementById('status').innerText='Upload de '+ptype+' vers le coffre Cloudinary... Ne ferme pas! 🔒'; let url=mode==='single'?'/upload-single':'/upload-collection'; let r=await fetch(url,{method:'POST',body:fd}); let d=await r.json(); document.getElementById('status').innerText=d.message; if(d.success){load(); setTimeout(closeModal,1200);} };
load();
</script></body></html>
    """
@app.route("/icon-192.png")
def icon192():
    resp = send_file(make_gospel_icon(192), mimetype="image/png")
    resp.headers["Cache-Control"] = "public, max-age=86400"
    return resp
@app.route("/icon-512.png")
def icon512():
    resp = send_file(make_gospel_icon(512), mimetype="image/png")
    resp.headers["Cache-Control"] = "public, max-age=86400"
    return resp
@app.route("/manifest.json")
def manifest():
    resp = jsonify({
        "id": "/",
        "name": "GOSPEL WORLD - ROYAUME DE DIEU",
        "short_name": "GOSPEL WORLD",
        "description": "FLASH EVANGILE WORLD - ROYAUME DE DIEU - KINGDOM OF GOD",
        "start_url": "/?source=pwa",
        "scope": "/",
        "display": "standalone",
        "display_override": ["window-controls-overlay", "standalone"],
        "orientation": "portrait",
        "background_color": "#0A0A12",
        "theme_color": "#FFD700",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
        ]
    })
    resp.headers["Cache-Control"] = "no-cache"
    return resp
@app.route("/sw.js")
def sw():
    js = """
const CACHE = 'gospel-world-v27';
self.addEventListener('install', e => { self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).then(res => {
      const copy = res.clone();
      if (e.request.url.startsWith(self.location.origin)) {
        caches.open(CACHE).then(c => c.put(e.request, copy));
      }
      return res;
    }).catch(() => caches.match(e.request))
  );
});
"""
    return js, 200, {'Content-Type': 'application/javascript', 'Cache-Control': 'no-cache'}
@app.route("/api/gw-number")
def gw_number():
    return jsonify({"number": GOSPEL_OM, "display": GOSPEL_OM_DISPLAY})
@app.route("/api/verse")
def verse():
    idx = datetime.date.today().toordinal() % len(VERSETS)
    ref, text = VERSETS[idx]
    return jsonify({"ref": ref, "text": text})
@app.route("/api/all")
def api_all():
    singles=load_json("songs.json",[]); colls=load_json("collections.json",[]); items=[]
    for s in singles: s["type"]="SINGLE"; items.append(s)
    for c in colls: items.append(c)
    items.sort(key=lambda x: x.get("created",""), reverse=True)
    return jsonify({"items":items})
@app.route("/api/like", methods=["POST"])
def like():
    d=request.get_json(); id=d.get("id")
    for f in ["songs.json","collections.json"]:
        items=load_json(f,[])
        for it in items:
            if it.get("id")==id: it["likes"]=it.get("likes",0)+1; save_json(f,items); return jsonify({"ok":True})
    return jsonify({"ok":False})
@app.route("/upload-single", methods=["POST"])
def upload_single():
    title=request.form.get("titre","").strip(); artist=request.form.get("artist","").strip(); artist_om=request.form.get("artist_om","").strip(); files=request.files.getlist("files")
    if not title or not artist or not files: return jsonify({"success":False,"message":"Remplis tout"})
    try:
        cover_url=f"https://picsum.photos/seed/{uuid.uuid4().hex[:6]}/400/400"
        if "cover" in request.files and request.files["cover"].filename:
            c=cloudinary.uploader.upload(request.files["cover"], folder="gospelworld/covers"); cover_url=c["secure_url"]
        res=cloudinary.uploader.upload(files[0], resource_type="video", folder="gospelworld/singles")
        songs=load_json("songs.json",[]); songs.insert(0,{"id":uuid.uuid4().hex[:8],"title":title,"artist":artist,"artist_om":artist_om,"file":res["secure_url"],"cover":cover_url,"likes":0,"created":uuid.uuid4().hex}); save_json("songs.json",songs)
        return jsonify({"success":True,"message":f"SINGLE '{title}' sauvegarde pour toujours! 🔒 Dons vers {artist_om}"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})
@app.route("/upload-collection", methods=["POST"])
def upload_collection():
    title=request.form.get("titre","").strip(); artist=request.form.get("artist","").strip(); artist_om=request.form.get("artist_om","").strip(); ptype=request.form.get("type","EP"); desc=request.form.get("desc",""); files=request.files.getlist("files")
    if not title or not artist or not files: return jsonify({"success":False,"message":"Remplis tout"})
    try:
        cover_url=f"https://picsum.photos/seed/{uuid.uuid4().hex[:6]}/400/400"
        if "cover" in request.files and request.files["cover"].filename:
            c=cloudinary.uploader.upload(request.files["cover"], folder="gospelworld/covers"); cover_url=c["secure_url"]
        songs_list=[]
        for f in files:
            st=os.path.splitext(f.filename)[0].replace("_"," ").replace("-"," ")
            res=cloudinary.uploader.upload(f, resource_type="video", folder=f"gospelworld/{ptype.lower().replace(' ','_')}")
            songs_list.append({"title":st,"file":res["secure_url"]})
        colls=load_json("collections.json",[]); colls.insert(0,{"id":uuid.uuid4().hex[:8],"type":ptype,"title":title,"artist":artist,"artist_om":artist_om,"desc":desc,"cover":cover_url,"songs":songs_list,"likes":0,"created":uuid.uuid4().hex}); save_json("collections.json",colls)
        return jsonify({"success":True,"message":f"{ptype} '{title}' sauvegarde avec {len(songs_list)} Sons! 🔒"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
