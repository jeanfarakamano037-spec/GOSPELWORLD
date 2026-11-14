from flask import Flask, jsonify, request
import json, os, uuid
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

def get_env(*names):
    for n in names:
        v = os.getenv(n)
        if v: return v.strip()
    return None
CLOUD_NAME = get_env("CLOUDINARY_CLOUD_NAME", "cloudinary_cloud_name")
API_KEY = get_env("CLOUDINARY_API_KEY", "cloudinary_api_key")
API_SECRET = get_env("CLOUDINARY_API_SECRET", "cloudinary_api_secret")
cloudinary.config(cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET, secure=True)

def load_json(f, default):
    if not os.path.exists(f): return default
    try:
        with open(f, "r", encoding="utf-8") as x: return json.load(x)
    except: return default
def save_json(f, data):
    with open(f, "w", encoding="utf-8") as x: json.dump(data, x, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return """
<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GOSPEL WORLD - PLAFOND</title>
<link rel="manifest" href="/manifest.json">
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
body{background:#050505!important;color:#fff!important;font-family:Helvetica,Arial,sans-serif}
.sidebar{background:#000}
.card{background:#181818;color:#fff;transition:.3s}
.card:hover{background:#252525;transform:translateY(-4px) scale(1.01)}
.gold-btn{background:linear-gradient(135deg,#FFD700,#FF2D55,#8B5CF6);color:#fff;background-size:200% 200%;animation:grad 4s infinite}
@keyframes grad{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hero-grad{background:linear-gradient(180deg,#2D0A4A 0%,#1A0F00 40%,#050505 100%)}
.chip{background:#232323;color:#fff}.pill-active{background:#fff!important;color:#000!important}
input,select,textarea{background:#232323!important;color:#fff!important;border:1px solid #333!important}
.bar{width:5px;background:linear-gradient(#FFD700,#FF2D55);border-radius:99px;animation:eq .6s infinite alternate}
@keyframes eq{from{height:8px}to{height:42px}}
.marquee{animation:scroll 20s linear infinite;white-space:nowrap}
@keyframes scroll{from{transform:translateX(100%)}to{transform:translateX(-100%)}}
.play-hover{opacity:0;transition:.2s}.group:hover .play-hover{opacity:1}
.glow{box-shadow:0 20px 80px rgba(255,215,0,.4)}
.spin{animation:spin 12s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.story-ring{background:conic-gradient(#FFD700,#FF2D55,#8B5CF6,#FFD700);padding:3px;border-radius:9999px}
.viz{height:50px;display:flex;align-items:end;gap:3px}
.viz div{flex:1;background:linear-gradient(#FFD700,#FF2D55);border-radius:99px;transition:.15s}
#fullPlayer{transition:.4s}
::-webkit-scrollbar{width:6px}::-webkit-scrollbar-thumb{background:#333;border-radius:99px}
</style></head><body>

<div class="flex">
<aside class="sidebar hidden md:flex flex-col w-[250px] h-screen fixed left-0 top-0 p-4 z-50">
<div class="flex items-center gap-2 px-2"><div class="w-10 h-10 bg-gradient-to-br from-yellow-400 via-pink-500 to-purple-500 rounded-full flex items-center justify-center font-black text-xl glow">G</div><b class="text-lg">GOSPEL <span class="text-[#FFD700]">WORLD</span></b></div>
<nav class="mt-8 space-y-1 font-bold text-[15px]">
<button onclick="goHome()" class="w-full text-left flex gap-3 items-center p-3 rounded-lg bg-[#232323]"><i class="fa-solid fa-house"></i> Accueil</button>
<button onclick="document.getElementById('search').focus()" class="w-full text-left flex gap-3 items-center p-3 rounded-lg hover:bg-[#232323] text-[#B3B3B3]"><i class="fa-solid fa-magnifying-glass"></i> Rechercher</button>
<button onclick="showTab('LIKED',this)" class="w-full text-left flex gap-3 items-center p-3 rounded-lg hover:bg-[#232323] text-[#B3B3B3]"><i class="fa-solid fa-heart text-[#FF2D55]"></i> Mes Likes</button>
<button onclick="showTab('TOP',this)" class="w-full text-left flex gap-3 items-center p-3 rounded-lg hover:bg-[#232323] text-[#B3B3B3]"><i class="fa-solid fa-trophy text-[#FFD700]"></i> Top 10</button>
<button onclick="startRadio()" class="w-full text-left flex gap-3 items-center p-3 rounded-lg bg-gradient-to-r from-yellow-500/20 to-pink-500/20 border border-yellow-500/30"><i class="fa-solid fa-radio text-[#FFD700]"></i> 📻 Radio Gospel World</button>
</nav>
<div class="mt-6 bg-gradient-to-br from-[#FFD700] via-[#FF2D55] to-[#8B5CF6] text-white rounded-2xl p-4"><p class="font-black">TELECHARGE L'APP</p><p class="text-xs opacity-80">GOSPEL WORLD sur ton tel</p><button onclick="installApp()" class="mt-3 w-full bg-black py-2 rounded-full font-bold text-sm">INSTALLER - GRATUIT</button></div>
<div class="mt-auto text-[11px] text-[#B3B3B3] px-2"><p id="statsSide">...</p><p>© 2026 GOSPEL WORLD - PLAFOND</p></div>
</aside>

<main class="flex-1 md:ml-[250px] pb-44">
<header class="sticky top-0 z-40 bg-black/85 backdrop-blur-xl px-4 md:px-8 py-3 flex justify-between items-center">
<div class="flex items-center gap-2 md:hidden"><div class="w-8 h-8 bg-gradient-to-br from-yellow-400 to-pink-500 rounded-full flex items-center justify-center font-black">G</div><b>GOSPEL <span class="text-[#FFD700]">WORLD</span></b></div>
<div class="hidden md:flex gap-2"><span class="bg-red-500 px-3 py-1 rounded-full text-xs font-bold animate-pulse">🔴 LIVE - CONAKRY</span><span class="bg-white/10 px-3 py-1 rounded-full text-xs font-bold">🌍 MONDE</span></div>
<div class="flex gap-2"><button onclick="installApp()" class="bg-white text-black px-4 py-2 rounded-full font-bold text-xs">TELECHARGER L'APP</button><button onclick="openModal('single')" class="gold-btn px-4 py-2 rounded-full font-bold text-sm">+ PUBLIER</button></div></header>

<!-- STORIES -->
<section class="px-4 md:px-8 pt-5"><div id="stories" class="flex gap-4 overflow-x-auto pb-2"></div></section>

<!-- HERO PLAFOND -->
<section class="hero-grad px-4 md:px-8 pt-6 pb-8">
<div class="flex items-end gap-1 h-10"><div class="bar"></div><div class="bar" style="animation-delay:.1s"></div><div class="bar" style="animation-delay:.2s"></div><div class="bar" style="animation-delay:.3s"></div><div class="bar" style="animation-delay:.4s"></div><div class="bar" style="animation-delay:.5s"></div><div class="bar" style="animation-delay:.6s"></div></div>
<h1 class="text-[64px] md:text-[110px] font-black leading-[0.85] mt-2">GOSPEL<br><span class="bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">WORLD</span></h1>
<div id="featured" class="mt-6 bg-black/60 border border-white/10 rounded-[25px] p-4 flex gap-4 items-center max-w-2xl backdrop-blur"></div>
<div class="mt-5 flex gap-3 flex-wrap"><button onclick="startRadio()" class="gold-btn px-6 py-3 rounded-full font-black text-sm">📻 RADIO GOSPEL WORLD</button><button onclick="playFirst()" class="bg-white text-black px-6 py-3 rounded-full font-black text-sm">🔀 LECTURE ALEATOIRE</button></div>
<div class="mt-5 bg-black/40 rounded-full py-2 overflow-hidden"><div class="marquee text-[#FFD700] text-sm font-bold">🔥 PLAFOND ATTEINT - GOSPEL WORLD - L'ENTREE DU ROI - JONATHAN - N°1 EN GUINEE - PARTAGEZ MASSIVEMENT 🔥</div></div>
<div id="statsBar" class="mt-5 grid grid-cols-3 gap-3 max-w-2xl"></div>
</section>

<section class="px-4 md:px-8 mt-6">
<input id="search" oninput="render()" placeholder="🔍 Recherche artiste, titre..." class="w-full rounded-full px-5 py-3 outline-none">
<div class="mt-4 flex gap-2 flex-wrap">
<button onclick="showTab('all',this)" class="tab-btn pill-active chip px-4 py-2 rounded-full text-sm font-bold">Tout</button>
<button onclick="showTab('SINGLE',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">Singles</button>
<button onclick="showTab('EP',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">EP</button>
<button onclick="showTab('MIXTAPE',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">Mixtape</button>
<button onclick="showTab('ALBUM',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">Album</button>
<button onclick="showTab('TOP',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">🏆 Top 10</button>
<button onclick="showTab('LIKED',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">❤️ Likes</button>
</div>
<h2 id="sectionTitle" class="text-2xl font-black mt-8">Fait pour toi ✨</h2><p class="text-[#B3B3B3] text-sm">Le meilleur du Gospel de Guinée</p>
</section>
<section id="grid" class="px-4 md:px-8 mt-6 grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"></section>
<section class="px-4 md:px-8 mt-8"><h2 class="text-2xl font-black">🏆 Top 10 - Les plus aimés</h2><div id="top10" class="mt-4 space-y-2"></div></section>
<section class="px-4 md:px-8 mt-8"><h2 class="text-2xl font-black">🎤 Artistes vérifiés ✅</h2><div id="artists" class="mt-4 flex gap-3 overflow-x-auto pb-2"></div></section>
</main></div>

<!-- PLAYER -->
<div class="fixed bottom-0 w-full bg-black/95 border-t border-white/10 p-3 z-50">
<div class="flex items-center gap-3 max-w-[1400px] mx-auto">
<img id="cover" onclick="openFullPlayer()" src="https://picsum.photos/seed/gospel/100" class="w-14 h-14 rounded-xl cursor-pointer hover:scale-105 transition">
<div class="w-[160px] md:w-[220px] min-w-0"><h4 id="ptitle" class="font-bold truncate text-sm">Choisis un chant</h4><p id="partist" class="text-xs text-[#B3B3B3]">GOSPEL WORLD</p><p id="playlistInfo" class="text-[11px] text-[#FFD700]"></p></div>
<div class="flex-1 hidden md:block"><div class="flex justify-center gap-3 items-center"><button onclick="toggleShuffle()" id="shuffleBtn" class="text-[#B3B3B3]"><i class="fa-solid fa-shuffle"></i></button><button onclick="prevSong()" class="text-white"><i class="fa-solid fa-backward"></i></button><button id="playBtn" class="w-12 h-12 bg-[#FFD700] text-black rounded-full"><i class="fa-solid fa-play"></i></button><button onclick="nextSong()" class="text-white"><i class="fa-solid fa-forward"></i></button><button onclick="toggleRepeat()" id="repeatBtn" class="text-[#B3B3B3]"><i class="fa-solid fa-repeat"></i></button></div><div class="flex items-center gap-2 mt-1"><span id="curTime" class="text-[11px] text-[#B3B3B3]">0:00</span><div class="flex-1 bg-white/20 h-1 rounded-full cursor-pointer" onclick="seek(event)"><div id="prog" class="h-1 bg-gradient-to-r from-yellow-400 to-pink-500 rounded-full w-0"></div></div><span id="durTime" class="text-[11px] text-[#B3B3B3]">0:00</span></div></div>
<div class="flex items-center gap-2"><button onclick="openFullPlayer()" class="hidden md:flex w-10 h-10 bg-white/10 rounded-full items-center justify-center"><i class="fa-solid fa-expand"></i></button><button onclick="shareCurrent()" class="w-10 h-10 bg-white/10 rounded-full"><i class="fa-solid fa-share-nodes"></i></button><button onclick="downloadCurrent()" class="w-10 h-10 bg-[#1DB954] rounded-full"><i class="fa-solid fa-download"></i></button><button id="playBtnM" class="md:hidden w-11 h-11 bg-[#FFD700] text-black rounded-full"><i class="fa-solid fa-play"></i></button></div>
</div><div class="md:hidden mt-2"><div class="w-full bg-white/20 h-1 rounded-full"><div id="progM" class="h-1 bg-[#FFD700] rounded-full w-0"></div></div></div><audio id="audio" class="hidden"></audio></div>

<!-- FULLSCREEN PLAYER - LE PLAFOND -->
<div id="fullPlayer" class="hidden fixed inset-0 bg-gradient-to-b from-purple-900 via-black to-black z-[200] flex-col items-center justify-center p-6 text-center">
<button onclick="closeFullPlayer()" class="absolute top-4 right-4 w-10 h-10 bg-white/10 rounded-full text-xl">↓</button>
<p class="text-xs tracking-widest text-[#FFD700]">EN LECTURE SUR GOSPEL WORLD</p>
<img id="fullCover" src="https://picsum.photos/seed/gospel/400" class="w-[280px] h-[280px] md:w-[340px] md:h-[340px] rounded-[30px] object-cover glow spin mt-6">
<h2 id="fullTitle" class="text-3xl font-black mt-6">Choisis un chant</h2><p id="fullArtist" class="text-[#B3B3B3]">GOSPEL WORLD ✅</p>
<div class="viz w-[280px] mt-4" id="viz"></div>
<div class="w-[280px] md:w-[400px] mt-4"><div class="flex justify-between text-xs text-[#B3B3B3]"><span id="fullCur">0:00</span><span id="fullDur">0:00</span></div><div class="w-full bg-white/20 h-1.5 rounded-full mt-1 cursor-pointer" onclick="seek(event)"><div id="fullProg" class="h-1.5 bg-gradient-to-r from-yellow-400 to-pink-500 rounded-full w-0"></div></div></div>
<div class="flex items-center gap-5 mt-6"><button onclick="prevSong()" class="text-2xl"><i class="fa-solid fa-backward"></i></button><button onclick="togglePlay()" id="fullPlayBtn" class="w-16 h-16 bg-white text-black rounded-full text-2xl"><i class="fa-solid fa-play"></i></button><button onclick="nextSong()" class="text-2xl"><i class="fa-solid fa-forward"></i></button></div>
<div class="flex gap-3 mt-6"><button onclick="openLyrics()" class="bg-white/10 px-5 py-2 rounded-full text-sm font-bold">📖 Paroles</button><button onclick="openQueue()" class="bg-white/10 px-5 py-2 rounded-full text-sm font-bold">📋 File d'attente</button><button onclick="shareCurrent()" class="bg-[#FFD700] text-black px-5 py-2 rounded-full text-sm font-bold">↗ Partager</button></div>
<p class="text-xs text-[#B3B3B3] mt-6">Clique sur ↓ pour revenir • GOSPEL WORLD PLAFOND 🚀</p></div>

<!-- LYRICS + QUEUE -->
<div id="lyricsModal" class="hidden fixed inset-0 bg-black/90 z-[210] flex items-center justify-center p-6"><div class="bg-[#181818] rounded-[25px] p-6 max-w-md w-full text-center"><h3 class="font-black text-xl">📖 Paroles</h3><p id="lyricsText" class="mt-4 text-sm leading-relaxed text-[#B3B3B3]">Gloire à Dieu... 🙏<br>Chante avec tout ton coeur<br>Jesus est Roi, Il règne à jamais<br>Alleluia! Amen! 🔥<br><br><i>Paroles complètes bientôt - demande à l'artiste de les ajouter</i></p><button onclick="document.getElementById('lyricsModal').classList.add('hidden')" class="mt-4 w-full bg-white/10 py-2 rounded-full">Fermer</button></div></div>
<div id="queueModal" class="hidden fixed inset-0 bg-black/90 z-[210] flex items-center justify-center p-6"><div class="bg-[#181818] rounded-[25px] p-6 max-w-md w-full"><h3 class="font-black text-xl">📋 File d'attente</h3><div id="queueList" class="mt-3 space-y-2"></div><button onclick="document.getElementById('queueModal').classList.add('hidden')" class="mt-4 w-full bg-white/10 py-2 rounded-full">Fermer</button></div></div>

<!-- MODALS : PARTAGE / COMMENT / ARTISTE / PUBLIER -->
<div id="shareModal" class="hidden fixed inset-0 bg-black/90 z-[120] flex items-center justify-center p-6"><div class="bg-[#181818] rounded-[25px] p-6 max-w-sm w-full text-center"><h3 class="text-xl font-black">Partager 🔥</h3><p id="shareTitle" class="text-sm text-[#B3B3B3] mb-4"></p><div class="grid grid-cols-3 gap-3"><button onclick="shareTo('whatsapp')" class="bg-[#25D366] py-3 rounded-2xl font-bold text-sm">WhatsApp</button><button onclick="shareTo('facebook')" class="bg-[#1877F2] py-3 rounded-2xl font-bold text-sm">Facebook</button><button onclick="shareTo('telegram')" class="bg-[#0088cc] py-3 rounded-2xl font-bold text-sm">Telegram</button><button onclick="shareTo('x')" class="bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm">X</button><button onclick="shareTo('tiktok')" class="bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm">TikTok</button><button onclick="shareTo('copy')" class="bg-white/10 py-3 rounded-2xl font-bold text-sm">Copier</button></div><button onclick="document.getElementById('shareModal').classList.add('hidden')" class="mt-4 w-full bg-white/10 py-2 rounded-full">Fermer</button></div></div>
<div id="commentModal" class="hidden fixed inset-0 bg-black/90 z-[125] flex items-center justify-center p-6"><div class="bg-[#181818] rounded-[25px] p-6 max-w-md w-full"><h3 class="font-black text-lg">💬 Commentaires</h3><p id="commentTitle" class="text-sm text-[#B3B3B3]"></p><div id="commentList" class="mt-3 space-y-2 max-h-[200px] overflow-y-auto"></div><div class="flex gap-2 mt-3"><input id="commentInput" placeholder="Dis Amen..." class="flex-1 rounded-full px-4 py-2"><button onclick="addComment()" class="bg-[#FFD700] text-black px-4 rounded-full font-bold">Envoyer</button></div><button onclick="document.getElementById('commentModal').classList.add('hidden')" class="mt-3 w-full bg-white/10 py-2 rounded-full">Fermer</button></div></div>
<div id="artistModal" class="hidden fixed inset-0 bg-black/90 z-[130] flex items-center justify-center p-6"><div class="bg-[#181818] rounded-[25px] p-6 max-w-md w-full text-center"><div id="artistContent"></div><button onclick="document.getElementById('artistModal').classList.add('hidden')" class="mt-4 w-full bg-white/10 py-2 rounded-full">Fermer</button></div></div>
<div id="modal" class="hidden fixed inset-0 bg-black/90 z-[100] flex items-center justify-center p-4 overflow-y-auto"><div class="bg-[#181818] rounded-[25px] p-6 max-w-lg w-full my-8"><div class="flex justify-between mb-4"><h3 id="modalTitle" class="text-2xl font-black">Publier</h3><button onclick="closeModal()" class="bg-white/10 w-8 h-8 rounded-full">X</button></div><div class="flex gap-2 mb-4"><button onclick="openModal('single')" class="flex-1 py-2 rounded-full bg-white/10 font-bold text-sm">Single</button><button onclick="openModal('collection')" class="flex-1 py-2 rounded-full bg-white/10 font-bold text-sm">EP / Mixtape / Album</button></div><form id="upForm" class="space-y-3"><input id="artist" placeholder="Nom artiste" required class="w-full rounded-xl px-4 py-3"><input id="titre" placeholder="Titre" required class="w-full rounded-xl px-4 py-3"><div id="collectionFields" class="hidden space-y-3"><select id="type" class="w-full rounded-xl px-4 py-3"><option value="EP">EP</option><option value="MIXTAPE">MIXTAPE</option><option value="ALBUM">ALBUM</option></select><textarea id="desc" placeholder="Description..." class="w-full rounded-xl px-4 py-3"></textarea></div><div class="border-2 border-dashed border-[#FFD700]/50 rounded-xl p-4 text-center"><label class="text-sm font-bold">COVER</label><input id="coverFile" type="file" accept="image/*" class="w-full mt-2"></div><div class="border-2 border-dashed border-[#FFD700]/50 rounded-xl p-4 text-center"><label class="text-sm font-bold">FICHIERS AUDIO</label><input id="files" type="file" accept=".mp3,audio/*" multiple required class="w-full mt-2"></div><button class="w-full bg-[#FFD700] text-black font-black py-3 rounded-xl">PUBLIER SUR GOSPEL WORLD</button><p id="status" class="text-center text-sm"></p></form></div></div>

<script>
let ALL=[], CURRENT=[], CURRENT_INDEX=0, FILTER='all', LIKES=JSON.parse(localStorage.getItem('gw_likes')||'[]'), COMMENTS=JSON.parse(localStorage.getItem('gw_comments')||'{}'), deferredPrompt=null, SHUFFLE=false, REPEAT=false, RADIO=false;
const audio=document.getElementById('audio'); const playBtn=document.getElementById('playBtn'); const playBtnM=document.getElementById('playBtnM');
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault(); deferredPrompt=e;});
function installApp(){ if(deferredPrompt) deferredPrompt.prompt(); else alert("Android: Menu > Ajouter a l'ecran d'accueil\\niPhone: Partager > Ajouter"); }
function goHome(){ FILTER='all'; document.getElementById('search').value=''; render(); window.scrollTo({top:0,behavior:'smooth'}); }
function toggleShuffle(){ SHUFFLE=!SHUFFLE; document.getElementById('shuffleBtn').style.color=SHUFFLE?'#FFD700':'#B3B3B3'; }
function toggleRepeat(){ REPEAT=!REPEAT; document.getElementById('repeatBtn').style.color=REPEAT?'#FFD700':'#B3B3B3'; }
function fmt(s){ if(!s) return '0:00'; return Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0'); }
function seek(e){ let r=e.currentTarget.getBoundingClientRect(); audio.currentTime=(e.clientX-r.left)/r.width*audio.duration; }
async function load(){ let r=await fetch('/api/all'); let d=await r.json(); ALL=d.items; render(); renderTop(); renderArtists(); renderFeatured(); renderStats(); renderStories(); }
function startRadio(){ if(!ALL.length) return alert('Pas encore de sons'); RADIO=true; CURRENT=ALL.flatMap(x=>x.type==='SINGLE'?[{title:x.title,artist:x.artist,file:x.file,id:x.id}]:x.songs.map(s=>({title:s.title,artist:x.artist,file:s.file,id:x.id}))); CURRENT_INDEX=Math.floor(Math.random()*CURRENT.length); playCurrent('📻 RADIO GOSPEL WORLD'); alert('📻 Radio lancée! Ca joue sans s\'arreter!'); }
function openFullPlayer(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son d\\'abord'); let fp=document.getElementById('fullPlayer'); fp.classList.remove('hidden'); fp.classList.add('flex'); }
function closeFullPlayer(){ let fp=document.getElementById('fullPlayer'); fp.classList.add('hidden'); fp.classList.remove('flex'); }
function openLyrics(){ let s=CURRENT[CURRENT_INDEX]; if(!s) return; document.getElementById('lyricsText').innerHTML=`<b>${s.title} - ${s.artist}</b><br><br>Gloire à Dieu... 🙏<br>Chante avec tout ton coeur<br>Jésus est Roi, Il règne à jamais<br>Alléluia! Amen! 🔥<br><br><i>Paroles complètes bientôt</i>`; document.getElementById('lyricsModal').classList.remove('hidden'); }
function openQueue(){ document.getElementById('queueList').innerHTML=CURRENT.map((s,i)=>`<div class='flex gap-3 bg-white/5 p-2 rounded-xl ${i===CURRENT_INDEX?'border border-yellow-400':''}'><span>${i+1}.</span><div><b class='text-sm block'>${s.title}</b><span class='text-xs text-[#B3B3B3]'>${s.artist} ${i===CURRENT_INDEX?'▶ EN COURS':''}</span></div></div>`).join('')||'File vide'; document.getElementById('queueModal').classList.remove('hidden'); }
function showTab(f,btn){ FILTER=f; document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('pill-active')); if(btn && btn.classList.contains('tab-btn')) btn.classList.add('pill-active'); document.getElementById('sectionTitle').innerText=f==='TOP'?'🏆 Top 10':f==='LIKED'?'❤️ Mes Likes':'Fait pour toi ✨'; render(); }
function toggleLike(id){ if(LIKES.includes(id)) LIKES=LIKES.filter(x=>x!==id); else LIKES.push(id); localStorage.setItem('gw_likes',JSON.stringify(LIKES)); render(); renderTop(); fetch('/api/like',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})}); }
function renderStats(){ let artists=new Set(ALL.map(x=>x.artist)).size; let likes=ALL.reduce((a,x)=>a+(x.likes||0),0); document.getElementById('statsBar').innerHTML=`<div class='bg-white/5 rounded-2xl p-3 text-center'><b class='text-xl text-[#FFD700]'>${ALL.length}</b><p class='text-xs text-[#B3B3B3]'>Sons</p></div><div class='bg-white/5 rounded-2xl p-3 text-center'><b class='text-xl text-[#FFD700]'>${artists}</b><p class='text-xs text-[#B3B3B3]'>Artistes ✅</p></div><div class='bg-white/5 rounded-2xl p-3 text-center'><b class='text-xl text-[#FFD700]'>${likes}</b><p class='text-xs text-[#B3B3B3]'>Likes</p></div>`; document.getElementById('statsSide').innerText=`${ALL.length} sons - ${artists} artistes`; }
function renderStories(){ let map={}; ALL.forEach(x=>{ if(!map[x.artist]) map[x.artist]=x.cover; }); document.getElementById('stories').innerHTML=Object.entries(map).map(([n,c])=>`<div onclick="openArtist('${n}')" class='shrink-0 text-center cursor-pointer'><div class='story-ring w-[68px] h-[68px]'><img src='${c}' class='w-full h-full rounded-full object-cover border-2 border-black'></div><p class='text-[11px] mt-1 truncate w-[68px]'>${n} ✅</p></div>`).join('')||''; }
function renderFeatured(){ if(!ALL.length) return; let f=ALL[0]; document.getElementById('featured').innerHTML=`<img src='${f.cover}' class='w-20 h-20 md:w-24 md:h-24 rounded-2xl object-cover glow'><div class='flex-1 min-w-0'><span class='bg-[#FFD700] text-black text-[10px] font-black px-2 py-1 rounded-full'>🔥 A LA UNE - PLAFOND</span><h3 class='font-black text-lg truncate mt-1'>${f.title}</h3><p class='text-sm text-[#B3B3B3]'>${f.artist} ✅ - ${f.type}</p></div><button onclick="playSingle('${f.id}')" class='w-14 h-14 bg-[#FFD700] text-black rounded-full shrink-0 text-xl'><i class='fa-solid fa-play'></i></button>`; }
function renderTop(){ let top=[...ALL].sort((a,b)=>(b.likes||0)-(a.likes||0)).slice(0,10); document.getElementById('top10').innerHTML=top.map((x,i)=>`<div class='flex items-center gap-3 bg-[#181818] p-3 rounded-2xl'><span class='w-8 text-center font-black text-[#FFD700] text-lg'>${i+1}</span><img src='${x.cover}' class='w-12 h-12 rounded-lg object-cover'><div class='flex-1 min-w-0'><b class='truncate block'>${x.title}</b><span class='text-xs text-[#B3B3B3]'>${x.artist} ✅ - ❤️ ${x.likes||0}</span></div><button onclick="playSingle('${x.id}')" class='w-10 h-10 bg-[#FFD700] text-black rounded-full'><i class='fa-solid fa-play'></i></button></div>`).join(''); }
function renderArtists(){ let map={}; ALL.forEach(x=>{ if(!map[x.artist]) map[x.artist]={cover:x.cover,count:0}; map[x.artist].count++; }); document.getElementById('artists').innerHTML=Object.entries(map).map(([name,info])=>`<div onclick="openArtist('${name}')" class='shrink-0 w-[120px] text-center cursor-pointer'><img src='${info.cover}' class='w-[120px] h-[120px] rounded-full object-cover border-2 border-[#FFD700]'><b class='block mt-2 truncate'>${name} ✅</b><span class='text-xs text-[#B3B3B3]'>${info.count} son(s)</span></div>`).join(''); }
function openArtist(name){ let list=ALL.filter(x=>x.artist===name); document.getElementById('artistContent').innerHTML=`<img src='${list[0].cover}' class='w-24 h-24 rounded-full mx-auto object-cover border-2 border-[#FFD700]'><h3 class='font-black text-2xl mt-2'>${name} ✅</h3><p class='text-[#B3B3B3] text-sm'>Artiste vérifié - ${list.length} son(s)</p><div class='mt-4 space-y-2 text-left'>${list.map(x=>`<div onclick="document.getElementById('artistModal').classList.add('hidden');playSingle('${x.id}')" class='flex gap-3 bg-white/5 p-2 rounded-xl cursor-pointer'><img src='${x.cover}' class='w-10 h-10 rounded-lg'><div><b class='text-sm block'>${x.title}</b><span class='text-xs text-[#B3B3B3]'>${x.type} - ❤️ ${x.likes||0}</span></div></div>`).join('')}</div>`; document.getElementById('artistModal').classList.remove('hidden'); }
function render(){
  let q=(document.getElementById('search').value||'').toLowerCase();
  let list=ALL.filter(x=>{ if(FILTER==='LIKED' && !LIKES.includes(x.id)) return false; if(FILTER==='TOP') return true; if(FILTER!=='all' && FILTER!=='LIKED' && x.type!==FILTER) return false; if(q && !(x.title.toLowerCase().includes(q)||x.artist.toLowerCase().includes(q))) return false; return true; });
  if(FILTER==='TOP') list=[...list].sort((a,b)=>(b.likes||0)-(a.likes||0)).slice(0,10);
  document.getElementById('grid').innerHTML=list.map(item=>{
    let liked=LIKES.includes(item.id)?'❤️':'🤍'; let cmt=(COMMENTS[item.id]||[]).length;
    let shareBtn=`<button onclick="openShare('${item.id}')" class='flex-1 bg-white/10 py-2 rounded-full text-xs font-bold'>PARTAGER</button>`;
    let dlBtn=`<button onclick="downloadItem('${item.id}')" class='flex-1 bg-[#1DB954] py-2 rounded-full text-xs font-bold'>TELECHARGER</button>`;
    let cmtBtn=`<button onclick="openComments('${item.id}')" class='w-full bg-white/5 py-1.5 rounded-full text-xs mt-2'>💬 ${cmt} - Laisser un Amen</button>`;
    if(item.type==='SINGLE') return `<div class='card group rounded-[20px] p-4'><div class='relative'><img src='${item.cover}' class='w-full aspect-square object-cover rounded-xl'><button onclick="playSingle('${item.id}')" class='play-hover absolute bottom-3 right-3 w-12 h-12 bg-[#FFD700] text-black rounded-full'><i class='fa-solid fa-play'></i></button></div><h3 class='font-bold mt-3 truncate'>${item.title}</h3><p class='text-xs text-[#B3B3B3]'>${item.artist} ✅ - Single - ❤️ ${item.likes||0}</p><div class='flex gap-2 mt-3'><button onclick="playSingle('${item.id}')" class='flex-1 bg-[#FFD700] text-black font-bold py-2 rounded-full text-sm'>ECOUTER</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div>${cmtBtn}</div>`;
    else return `<div class='card rounded-[20px] p-4 border border-[#FFD700]/20'><img src='${item.cover}' class='w-full aspect-square object-cover rounded-xl'><span class='inline-block bg-[#FFD700] text-black text-[11px] font-black px-2 py-1 rounded-full mt-3'>${item.type} - ${item.songs.length} TITRES</span><h3 class='font-bold mt-2 truncate'>${item.title}</h3><p class='text-xs text-[#B3B3B3]'>${item.artist} ✅ - ❤️ ${item.likes||0}</p><div class='flex gap-2 mt-3'><button onclick="playCollection('${item.id}')" class='flex-1 bg-[#FFD700] text-black font-bold py-2 rounded-full text-sm'>ECOUTER TOUT</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div>${cmtBtn}</div>`;
  }).join('')||'<p class="col-span-full text-center py-10 text-[#B3B3B3]">Aucun resultat</p>';
}
function playFirst(){ if(!ALL.length) return; playSingle(ALL[Math.floor(Math.random()*ALL.length)].id); }
function playSingle(id){let s=ALL.find(x=>x.id===id); CURRENT=[{title:s.title,artist:s.artist,file:s.file,id:s.id}]; CURRENT_INDEX=0; playCurrent();}
function playCollection(id,start=0){let c=ALL.find(x=>x.id===id); CURRENT=c.songs.map(s=>({title:s.title,artist:c.artist,file:s.file,id:c.id})); CURRENT_INDEX=start; playCurrent(c.title);}
function playCurrent(coll=''){let s=CURRENT[CURRENT_INDEX]; if(!s) return; document.getElementById('ptitle').innerText=s.title; document.getElementById('partist').innerText=s.artist; document.getElementById('cover').src='https://picsum.photos/seed/'+encodeURIComponent(s.title)+'/100'; document.getElementById('fullCover').src='https://picsum.photos/seed/'+encodeURIComponent(s.title)+'/400'; document.getElementById('fullTitle').innerText=s.title; document.getElementById('fullArtist').innerText=s.artist+' ✅'; document.getElementById('playlistInfo').innerText=coll||'Single'; audio.src=s.file; audio.play(); setPlayIcon(true); startViz();}
function setPlayIcon(p){ let h=p?'<i class="fa-solid fa-pause"></i>':'<i class="fa-solid fa-play"></i>'; playBtn.innerHTML=h; playBtnM.innerHTML=h; document.getElementById('fullPlayBtn').innerHTML=h; }
function nextSong(){ if(SHUFFLE){ CURRENT_INDEX=Math.floor(Math.random()*CURRENT.length); } else if(CURRENT_INDEX<CURRENT.length-1){ CURRENT_INDEX++; } else if(RADIO||REPEAT){ CURRENT_INDEX=0; } else return; playCurrent(RADIO?'📻 RADIO GOSPEL WORLD':''); }
function prevSong(){ if(CURRENT_INDEX>0){ CURRENT_INDEX--; playCurrent(); } }
audio.onended=()=>{ if(REPEAT){ audio.currentTime=0; audio.play(); } else nextSong(); };
function togglePlay(){ if(audio.paused){audio.play(); setPlayIcon(true);} else {audio.pause(); setPlayIcon(false);} }
playBtn.onclick=togglePlay; playBtnM.onclick=togglePlay;
audio.ontimeupdate=()=>{ if(audio.duration){ let p=audio.currentTime/audio.duration*100+'%'; document.getElementById('prog').style.width=p; let pm=document.getElementById('progM'); if(pm) pm.style.width=p; document.getElementById('fullProg').style.width=p; document.getElementById('curTime').innerText=fmt(audio.currentTime); document.getElementById('fullCur').innerText=fmt(audio.currentTime); document.getElementById('durTime').innerText=fmt(audio.duration); document.getElementById('fullDur').innerText=fmt(audio.duration); } };
function startViz(){ let v=document.getElementById('viz'); v.innerHTML=''; for(let i=0;i<28;i++){ let d=document.createElement('div'); d.style.height=(Math.random()*40+10)+'px'; v.appendChild(d); } setInterval(()=>{ if(audio.paused) return; [...v.children].forEach(d=>d.style.height=(Math.random()*45+5)+'px'); },150); }
function downloadCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son'); let s=CURRENT[CURRENT_INDEX]; let a=document.createElement('a'); a.href=s.file; a.download=s.title+'.mp3'; a.target='_blank'; a.click(); }
function downloadItem(id){ let it=ALL.find(x=>x.id===id); if(it.type==='SINGLE'){ let a=document.createElement('a'); a.href=it.file; a.download=it.title+'.mp3'; a.target='_blank'; a.click(); } else { it.songs.forEach((s,i)=>setTimeout(()=>{let a=document.createElement('a'); a.href=s.file; a.download=s.title+'.mp3'; a.target='_blank'; a.click();}, i*800)); } }
let SHARE_ID=null, COMMENT_ID=null;
function openShare(id){ SHARE_ID=id; let it=ALL.find(x=>x.id===id); document.getElementById('shareTitle').innerText=it.title+' - '+it.artist; document.getElementById('shareModal').classList.remove('hidden'); }
function shareCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son'); if(navigator.share){let s=CURRENT[CURRENT_INDEX]; navigator.share({title:'GOSPEL WORLD',text:`${s.title} - ${s.artist} sur GOSPEL WORLD`,url:location.href});} else openShare(CURRENT[CURRENT_INDEX].id); }
function shareTo(p){ let it=ALL.find(x=>x.id===SHARE_ID); if(!it) return; let url=encodeURIComponent(location.href); let txt=encodeURIComponent(`${it.title} - ${it.artist} sur GOSPEL WORLD Ecoute ici: `+location.href); let links={whatsapp:`https://wa.me/?text=${txt}`,facebook:`https://www.facebook.com/sharer/sharer.php?u=${url}`,telegram:`https://t.me/share/url?url=${url}&text=${txt}`,x:`https://twitter.com/intent/tweet?text=${txt}`,tiktok:`https://www.tiktok.com/`}; if(p==='copy'){navigator.clipboard.writeText(location.href+' - '+it.title); alert('Lien copie!');} else if(p==='tiktok'){navigator.clipboard.writeText(location.href); alert('Lien copie! Colle-le sur TikTok');} else window.open(links[p],'_blank'); document.getElementById('shareModal').classList.add('hidden'); }
function openComments(id){ COMMENT_ID=id; let it=ALL.find(x=>x.id===id); document.getElementById('commentTitle').innerText=it.title+' - '+it.artist; renderComments(); document.getElementById('commentModal').classList.remove('hidden'); }
function renderComments(){ let list=COMMENTS[COMMENT_ID]||[]; document.getElementById('commentList').innerHTML=list.map(c=>`<div class='bg-white/5 p-2 rounded-xl text-sm'>${c}</div>`).join('')||'<p class="text-[#B3B3B3] text-sm">Sois le premier 🙏</p>'; }
function addComment(){ let v=document.getElementById('commentInput').value.trim(); if(!v) return; if(!COMMENTS[COMMENT_ID]) COMMENTS[COMMENT_ID]=[]; COMMENTS[COMMENT_ID].push(v); localStorage.setItem('gw_comments',JSON.stringify(COMMENTS)); document.getElementById('commentInput').value=''; renderComments(); render(); }
function openModal(mode){ document.getElementById('modal').classList.remove('hidden'); let isColl=mode==='collection'; document.getElementById('collectionFields').classList.toggle('hidden',!isColl); document.getElementById('modalTitle').innerText=isColl?'Creer EP / Mixtape / Album':'Publier un Single'; document.getElementById('upForm').dataset.mode=mode; }
function closeModal(){document.getElementById('modal').classList.add('hidden');}
document.getElementById('files').onchange=e=>{document.getElementById('fileInfo');};
document.getElementById('upForm').onsubmit=async e=>{ e.preventDefault(); let mode=e.target.dataset.mode||'single'; let fd=new FormData(); fd.append('artist',document.getElementById('artist').value); fd.append('titre',document.getElementById('titre').value); if(mode==='collection'){fd.append('type',document.getElementById('type').value); fd.append('desc',document.getElementById('desc').value);} let cf=document.getElementById('coverFile').files[0]; if(cf) fd.append('cover',cf); for(let f of document.getElementById('files').files) fd.append('files',f); document.getElementById('status').innerText='Upload... Ne ferme pas!'; let url=mode==='collection'?'/upload-collection':'/upload-single'; let r=await fetch(url,{method:'POST',body:fd}); let d=await r.json(); document.getElementById('status').innerText=d.message; if(d.success){load(); setTimeout(closeModal,1200);} };
load();
</script></body></html>
    """
@app.route("/manifest.json")
def manifest():
    return jsonify({"name":"GOSPEL WORLD","short_name":"GOSPEL WORLD","start_url":"/","display":"standalone","background_color":"#050505","theme_color":"#FFD700","icons":[{"src":"https://picsum.photos/seed/gospel/512","sizes":"512x512","type":"image/png"}]})
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
    title=request.form.get("titre","").strip(); artist=request.form.get("artist","").strip(); files=request.files.getlist("files")
    if not title or not artist or not files: return jsonify({"success":False,"message":"Remplis tout"})
    try:
        cover_url=f"https://picsum.photos/seed/{uuid.uuid4().hex[:6]}/400/400"
        if "cover" in request.files and request.files["cover"].filename:
            c=cloudinary.uploader.upload(request.files["cover"], folder="gospelworld/covers"); cover_url=c["secure_url"]
        res=cloudinary.uploader.upload(files[0], resource_type="video", folder="gospelworld/singles")
        songs=load_json("songs.json",[]); songs.insert(0,{"id":uuid.uuid4().hex[:8],"title":title,"artist":artist,"file":res["secure_url"],"cover":cover_url,"likes":0,"created":uuid.uuid4().hex}); save_json("songs.json",songs)
        return jsonify({"success":True,"message":f"Single '{title}' publie!"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})
@app.route("/upload-collection", methods=["POST"])
def upload_collection():
    title=request.form.get("titre","").strip(); artist=request.form.get("artist","").strip(); ptype=request.form.get("type","EP"); desc=request.form.get("desc",""); files=request.files.getlist("files")
    if not title or not artist or not files: return jsonify({"success":False,"message":"Remplis tout"})
    try:
        cover_url=f"https://picsum.photos/seed/{uuid.uuid4().hex[:6]}/400/400"
        if "cover" in request.files and request.files["cover"].filename:
            c=cloudinary.uploader.upload(request.files["cover"], folder="gospelworld/covers"); cover_url=c["secure_url"]
        songs_list=[]
        for f in files:
            st=os.path.splitext(f.filename)[0].replace("_"," ").replace("-"," ")
            res=cloudinary.uploader.upload(f, resource_type="video", folder=f"gospelworld/{ptype.lower()}")
            songs_list.append({"title":st,"file":res["secure_url"]})
        colls=load_json("collections.json",[]); colls.insert(0,{"id":uuid.uuid4().hex[:8],"type":ptype,"title":title,"artist":artist,"desc":desc,"cover":cover_url,"songs":songs_list,"likes":0,"created":uuid.uuid4().hex}); save_json("collections.json",colls)
        return jsonify({"success":True,"message":f"{ptype} '{title}' publie avec {len(songs_list)} titres!"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
