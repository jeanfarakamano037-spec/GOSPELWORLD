from flask import Flask, jsonify, request
import json, os, uuid
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

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
<title>GOSPEL WORLD</title>
<link rel="manifest" href="/manifest.json">
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{-webkit-tap-highlight-color:transparent}
body{background:#121212!important;color:#FFFFFF!important;font-family:'Circular',Helvetica,Arial,sans-serif}
.sidebar{background:#000000}
.card{background:#181818!important;color:#fff!important}
.card:hover{background:#282828!important}
.text-dim{color:#B3B3B3!important}
.gold-btn{background:#FFD700;color:#000}
.gold-btn:hover{background:#FFE44D;transform:scale(1.03)}
.hero-grad{background:linear-gradient(180deg,#3a2a00 0%,#1a1200 40%,#121212 100%)}
.pill-active{background:#fff!important;color:#000!important}
.chip{background:#232323;color:#fff}
.chip:hover{background:#2e2e2e}
input,select,textarea{background:#232323!important;color:#fff!important;border:1px solid #333!important}
input::placeholder{color:#8a8a8a!important}
.bar{width:5px;background:#FFD700;border-radius:99px;animation:eq 0.7s infinite alternate}
@keyframes eq{from{height:8px}to{height:36px}}
.marquee{animation:scroll 22s linear infinite;white-space:nowrap}
@keyframes scroll{from{transform:translateX(100%)}to{transform:translateX(-100%)}}
.play-hover{opacity:0;transition:0.2s}
.group:hover .play-hover{opacity:1}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-thumb{background:#333;border-radius:99px}
</style></head>
<body class="bg-[#121212] text-white">

<!-- LAYOUT SPOTIFY -->
<div class="flex">

<!-- SIDEBAR GAUCHE COMME SPOTIFY -->
<aside class="sidebar hidden md:flex flex-col w-[240px] h-screen fixed left-0 top-0 p-4 z-50">
<div class="flex items-center gap-2 px-2"><div class="w-10 h-10 bg-[#FFD700] rounded-full flex items-center justify-center text-black font-black text-xl">G</div><b class="text-lg">GOSPEL <span class="text-[#FFD700]">WORLD</span></b></div>
<nav class="mt-8 space-y-1 font-bold text-[15px]">
<a href="#" onclick="showTab('all',this)" class="flex gap-3 items-center p-3 rounded-lg bg-[#232323]"><i class="fa-solid fa-house"></i> Accueil</a>
<a href="#" onclick="document.getElementById('search').focus()" class="flex gap-3 items-center p-3 rounded-lg hover:bg-[#232323] text-[#B3B3B3]"><i class="fa-solid fa-magnifying-glass"></i> Rechercher</a>
<a href="#" onclick="showTab('LIKED',this)" class="flex gap-3 items-center p-3 rounded-lg hover:bg-[#232323] text-[#B3B3B3]"><i class="fa-solid fa-heart text-[#FFD700]"></i> Mes Likes</a>
</nav>
<div class="mt-6 bg-gradient-to-br from-[#FFD700] to-[#FF8C00] text-black rounded-2xl p-4">
<p class="font-black text-sm">TÉLÉCHARGE L'APP</p><p class="text-xs font-bold opacity-80 mt-1">GOSPEL WORLD sur ton téléphone</p>
<button onclick="installApp()" class="mt-3 w-full bg-black text-white py-2 rounded-full font-bold text-sm">⬇ INSTALLER</button>
</div>
<div class="mt-auto text-[11px] text-[#B3B3B3] px-2"><p>© 2026 GOSPEL WORLD</p><p>Conakry • Guinée • Monde</p></div>
</aside>

<!-- CONTENU PRINCIPAL -->
<main class="flex-1 md:ml-[240px] pb-40">

<!-- TOP BAR -->
<header class="sticky top-0 z-40 bg-black/80 backdrop-blur-xl px-4 md:px-8 py-3 flex justify-between items-center">
<div class="flex items-center gap-2 md:hidden"><div class="w-8 h-8 bg-[#FFD700] rounded-full flex items-center justify-center text-black font-black">G</div><b>GOSPEL <span class="text-[#FFD700]">WORLD</span></b></div>
<div class="hidden md:block"></div>
<div class="flex gap-2">
<button onclick="installApp()" class="bg-white text-black px-4 py-2 rounded-full font-bold text-xs md:text-sm">⬇ TÉLÉCHARGER L'APP</button>
<button onclick="openModal('single')" class="gold-btn px-4 py-2 rounded-full font-bold text-sm">+ PUBLIER</button>
</div></header>

<!-- HERO - SANS LA PHRASE, JUSTE LE TITRE -->
<section class="hero-grad px-4 md:px-8 pt-10 pb-8 rounded-b-[30px]">
<div class="flex items-end gap-1 h-10"><div class="bar"></div><div class="bar" style="animation-delay:.1s"></div><div class="bar" style="animation-delay:.2s"></div><div class="bar" style="animation-delay:.3s"></div><div class="bar" style="animation-delay:.4s"></div></div>
<h1 class="text-[64px] md:text-[110px] font-black leading-[0.85] tracking-tight mt-2">GOSPEL<br><span class="text-[#FFD700]">WORLD</span></h1>
<!-- PHRASE ENLEVÉE COMME DEMANDÉ -->
<div class="mt-6 flex gap-3 flex-wrap">
<button onclick="document.getElementById('grid').scrollIntoView({behavior:'smooth'})" class="gold-btn px-6 py-3 rounded-full font-black text-sm">▶ ÉCOUTER MAINTENANT</button>
<button onclick="installApp()" class="bg-white text-black px-6 py-3 rounded-full font-black text-sm">⬇ TÉLÉCHARGER L'APP GRATUIT</button>
</div>
<div class="mt-6 bg-black/40 border border-white/10 rounded-full py-2 overflow-hidden"><div class="marquee text-[#FFD700] text-sm font-bold">🔥 TRENDING : AIMEZ PRECHER JESUS • GLOIRE A DIEU • JESUS REVIENT BIENTOT • CONAKRY EN FEU • GOSPEL WORLD N°1 EN GUINEE 🔥</div></div>
</section>

<!-- RECHERCHE + FILTRES -->
<section class="px-4 md:px-8 mt-6">
<input id="search" oninput="render()" placeholder="🔍 Recherche artiste, titre, EP, Album..." class="w-full rounded-full px-5 py-3 outline-none text-white placeholder-gray-400">
<div class="mt-4 flex gap-2 flex-wrap">
<button onclick="showTab('all',this)" class="tab-btn pill-active chip px-4 py-2 rounded-full text-sm font-bold">Tout</button>
<button onclick="showTab('SINGLE',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">🎵 Singles</button>
<button onclick="showTab('EP',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">💿 EP</button>
<button onclick="showTab('MIXTAPE',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">🔥 Mixtape</button>
<button onclick="showTab('ALBUM',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">👑 Album</button>
<button onclick="showTab('LIKED',this)" class="tab-btn chip px-4 py-2 rounded-full text-sm font-bold">❤️ Mes Likes</button>
</div>
<h2 class="text-2xl font-black mt-8">Fait pour toi</h2><p class="text-dim text-sm">Les derniers sons de Guinée, en exclusivité sur GOSPEL WORLD</p>
</section>

<section id="grid" class="px-4 md:px-8 mt-6 grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"></section>
</main></div>

<!-- PLAYER SPOTIFY EN BAS -->
<div class="fixed bottom-0 w-full bg-[#000] border-t border-white/10 p-3 md:p-4 z-50">
<div class="flex items-center gap-3 md:gap-4 max-w-[1400px] mx-auto">
<img id="cover" src="https://picsum.photos/seed/gospel/100" class="w-14 h-14 md:w-16 md:h-16 rounded-xl">
<div class="flex-1 min-w-0"><h4 id="ptitle" class="font-bold truncate text-white text-sm md:text-base">Choisis un chant</h4><p id="partist" class="text-xs text-[#B3B3B3]">GOSPEL WORLD</p>
<div class="w-full bg-white/20 h-1 rounded-full mt-2"><div id="prog" class="h-1 bg-[#FFD700] rounded-full w-0"></div></div><p id="playlistInfo" class="text-[11px] text-[#FFD700] mt-1"></p></div>
<div class="flex items-center gap-1 md:gap-2">
<button onclick="prevSong()" class="w-10 h-10 bg-white/10 rounded-full text-white"><i class="fa-solid fa-backward"></i></button>
<button id="playBtn" class="w-12 h-12 md:w-14 md:h-14 bg-[#FFD700] text-black rounded-full shrink-0"><i class="fa-solid fa-play"></i></button>
<button onclick="nextSong()" class="w-10 h-10 bg-white/10 rounded-full text-white"><i class="fa-solid fa-forward"></i></button>
<button onclick="shareCurrent()" class="hidden md:flex w-10 h-10 bg-white/10 rounded-full items-center justify-center text-white"><i class="fa-solid fa-share-nodes"></i></button>
<button onclick="downloadCurrent()" class="w-10 h-10 bg-[#1DB954] text-white rounded-full"><i class="fa-solid fa-download"></i></button>
</div></div><audio id="audio" class="hidden"></audio></div>

<!-- MODAL PARTAGE -->
<div id="shareModal" class="hidden fixed inset-0 bg-black/90 z-[120] flex items-center justify-center p-6"><div class="bg-[#181818] border border-white/10 rounded-[25px] p-6 max-w-sm w-full text-center">
<h3 class="text-xl font-black text-white">Partager ce chant 🔥</h3><p id="shareTitle" class="text-sm text-[#B3B3B3] mb-4"></p>
<div class="grid grid-cols-3 gap-3">
<button onclick="shareTo('whatsapp')" class="bg-[#25D366] py-3 rounded-2xl font-bold text-sm text-white"><i class="fa-brands fa-whatsapp text-xl"></i><br>WhatsApp</button>
<button onclick="shareTo('facebook')" class="bg-[#1877F2] py-3 rounded-2xl font-bold text-sm text-white"><i class="fa-brands fa-facebook text-xl"></i><br>Facebook</button>
<button onclick="shareTo('telegram')" class="bg-[#0088cc] py-3 rounded-2xl font-bold text-sm text-white"><i class="fa-brands fa-telegram text-xl"></i><br>Telegram</button>
<button onclick="shareTo('x')" class="bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm text-white"><i class="fa-brands fa-x-twitter text-xl"></i><br>X</button>
<button onclick="shareTo('tiktok')" class="bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm text-white"><i class="fa-brands fa-tiktok text-xl"></i><br>TikTok</button>
<button onclick="shareTo('copy')" class="bg-white/10 py-3 rounded-2xl font-bold text-sm text-white"><i class="fa-solid fa-link text-xl"></i><br>Copier</button>
</div><button onclick="document.getElementById('shareModal').classList.add('hidden')" class="mt-4 w-full bg-white/10 py-2 rounded-full text-white">Fermer</button></div></div>

<!-- MODAL PUBLIER -->
<div id="modal" class="hidden fixed inset-0 bg-black/90 z-[100] flex items-center justify-center p-4 overflow-y-auto"><div class="bg-[#181818] border border-white/10 rounded-[25px] p-6 max-w-lg w-full my-8">
<div class="flex justify-between mb-4"><h3 id="modalTitle" class="text-2xl font-black text-white">Publier</h3><button onclick="closeModal()" class="bg-white/10 w-8 h-8 rounded-full text-white">X</button></div>
<div class="flex gap-2 mb-4"><button onclick="openModal('single')" class="flex-1 py-2 rounded-full bg-white/10 font-bold text-sm text-white">🎵 Single</button><button onclick="openModal('collection')" class="flex-1 py-2 rounded-full bg-white/10 font-bold text-sm text-white">💿 EP / Mixtape / Album</button></div>
<form id="upForm" class="space-y-3">
<input id="artist" placeholder="Nom artiste" required class="w-full rounded-xl px-4 py-3 text-white">
<input id="titre" placeholder="Titre" required class="w-full rounded-xl px-4 py-3 text-white">
<div id="collectionFields" class="hidden space-y-3"><select id="type" class="w-full rounded-xl px-4 py-3 text-white"><option value="EP">💿 EP - 2 à 6 sons</option><option value="MIXTAPE">🔥 MIXTAPE - 7 à 15 sons</option><option value="ALBUM">👑 ALBUM - 10 à 20 sons</option></select><textarea id="desc" placeholder="Description du projet..." class="w-full rounded-xl px-4 py-3 text-white"></textarea></div>
<div class="border-2 border-dashed border-[#FFD700]/50 rounded-xl p-4 text-center"><label class="text-sm font-bold text-white">📸 COVER</label><input id="coverFile" type="file" accept="image/*" class="w-full mt-2 text-white"></div>
<div class="border-2 border-dashed border-[#FFD700]/50 rounded-xl p-4 text-center"><label class="text-sm font-bold text-white">🎵 FICHIERS AUDIO</label><input id="files" type="file" accept=".mp3,audio/*" multiple required class="w-full mt-2 text-white"><p id="fileInfo" class="text-xs text-[#B3B3B3] mt-2">Single = 1 fichier | EP / Album = plusieurs fichiers</p></div>
<button class="w-full bg-[#FFD700] text-black font-black py-3 rounded-xl">PUBLIER SUR GOSPEL WORLD 🔥</button><p id="status" class="text-center text-sm text-white"></p></form></div></div>

<script>
let ALL=[], CURRENT=[], CURRENT_INDEX=0, FILTER='all', LIKES=JSON.parse(localStorage.getItem('gw_likes')||'[]'), deferredPrompt=null;
const audio=document.getElementById('audio'); const playBtn=document.getElementById('playBtn');
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault(); deferredPrompt=e;});
function installApp(){ if(deferredPrompt){deferredPrompt.prompt();} else {alert("📱 Pour installer GOSPEL WORLD:\\nAndroid Chrome: Menu ⋮ > Ajouter à l'écran d'accueil\\niPhone Safari: Partager > Ajouter à l'écran d'accueil");}}
async function load(){ let r=await fetch('/api/all'); let d=await r.json(); ALL=d.items; render(); }
function showTab(f,btn){FILTER=f; document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('pill-active')); if(btn) btn.classList.add('pill-active'); render();}
function toggleLike(id){ if(LIKES.includes(id)) LIKES=LIKES.filter(x=>x!==id); else LIKES.push(id); localStorage.setItem('gw_likes',JSON.stringify(LIKES)); render(); fetch('/api/like',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})}); }
function render(){
  let q=(document.getElementById('search').value||'').toLowerCase();
  let list=ALL.filter(x=>{
    if(FILTER==='LIKED' && !LIKES.includes(x.id)) return false;
    if(FILTER!=='all' && FILTER!=='LIKED' && x.type!==FILTER) return false;
    if(q && !(x.title.toLowerCase().includes(q)||x.artist.toLowerCase().includes(q))) return false;
    return true;
  });
  document.getElementById('grid').innerHTML=list.map(item=>{
    let liked=LIKES.includes(item.id)?'❤️':'🤍';
    let shareBtn=`<button onclick="openShare('${item.id}')" class='flex-1 bg-white/10 py-2 rounded-full text-xs font-bold text-white'>↗ PARTAGER</button>`;
    let dlBtn=`<button onclick="downloadItem('${item.id}')" class='flex-1 bg-[#1DB954] py-2 rounded-full text-xs font-bold text-white'>⬇ TÉLÉCHARGER</button>`;
    if(item.type==='SINGLE'){
      return `<div class='card group rounded-[20px] p-4'><div class='relative'><img src='${item.cover}' class='w-full aspect-square object-cover rounded-xl'><button onclick="playSingle('${item.id}')" class='play-hover absolute bottom-3 right-3 w-12 h-12 bg-[#FFD700] text-black rounded-full shadow-xl'><i class='fa-solid fa-play'></i></button></div><h3 class='font-bold mt-3 truncate text-white'>${item.title}</h3><p class='text-xs text-[#B3B3B3]'>${item.artist} • 🎵 Single • ❤️ ${item.likes||0}</p><div class='flex gap-2 mt-3'><button onclick="playSingle('${item.id}')" class='flex-1 bg-[#FFD700] text-black font-bold py-2 rounded-full text-sm'>▶ ÉCOUTER</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full text-white'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div></div>`;
    } else {
      let badge=item.type==='EP'?'💿 EP':item.type==='MIXTAPE'?'🔥 MIXTAPE':'👑 ALBUM';
      return `<div class='card rounded-[20px] p-4 border border-[#FFD700]/20'><div class='relative'><img src='${item.cover}' class='w-full aspect-square object-cover rounded-xl'><button onclick="playCollection('${item.id}')" class='play-hover absolute bottom-3 right-3 w-12 h-12 bg-[#FFD700] text-black rounded-full'><i class='fa-solid fa-play'></i></button></div><span class='inline-block bg-[#FFD700] text-black text-[11px] font-black px-2 py-1 rounded-full mt-3'>${badge} • ${item.songs.length} TITRES</span><h3 class='font-bold mt-2 truncate text-white'>${item.title}</h3><p class='text-xs text-[#B3B3B3]'>${item.artist} • ❤️ ${item.likes||0}</p><p class='text-xs text-[#B3B3B3] mt-1'>${item.desc||''}</p><div class='flex gap-2 mt-3'><button onclick="playCollection('${item.id}')" class='flex-1 bg-[#FFD700] text-black font-bold py-2 rounded-full text-sm'>▶ ÉCOUTER TOUT</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div><div class='mt-3 space-y-1'>${item.songs.map((s,i)=>`<div onclick="playCollection('${item.id}',${i})" class='flex justify-between text-xs bg-white/5 px-3 py-2 rounded-lg cursor-pointer hover:bg-white/10 text-white'><span>${i+1}. ${s.title}</span><span>▶</span></div>`).join('')}</div></div>`;
    }
  }).join('')||'<p class="col-span-full text-center py-10 text-[#B3B3B3]">Aucun résultat. Sois le premier à publier! 🙏</p>';
}
function playSingle(id){let s=ALL.find(x=>x.id===id); CURRENT=[{title:s.title,artist:s.artist,file:s.file,id:s.id}]; CURRENT_INDEX=0; playCurrent();}
function playCollection(id,start=0){let c=ALL.find(x=>x.id===id); CURRENT=c.songs.map(s=>({title:s.title,artist:c.artist,file:s.file,id:c.id})); CURRENT_INDEX=start; playCurrent(c.title);}
function playCurrent(coll=''){let s=CURRENT[CURRENT_INDEX]; if(!s) return; document.getElementById('ptitle').innerText=s.title; document.getElementById('partist').innerText=s.artist; document.getElementById('cover').src='https://picsum.photos/seed/'+encodeURIComponent(s.title)+'/100'; document.getElementById('playlistInfo').innerText=coll?`📀 ${coll} - ${CURRENT_INDEX+1}/${CURRENT.length}`:`🎵 Single`; audio.src=s.file; audio.play(); playBtn.innerHTML='<i class="fa-solid fa-pause"></i>';}
function nextSong(){if(CURRENT_INDEX<CURRENT.length-1){CURRENT_INDEX++; playCurrent();}}
function prevSong(){if(CURRENT_INDEX>0){CURRENT_INDEX--; playCurrent();}}
audio.onended=()=>nextSong();
playBtn.onclick=()=>{if(audio.paused){audio.play(); playBtn.innerHTML='<i class="fa-solid fa-pause"></i>';}else{audio.pause(); playBtn.innerHTML='<i class="fa-solid fa-play"></i>';}};
audio.ontimeupdate=()=>{if(audio.duration) document.getElementById('prog').style.width=audio.currentTime/audio.duration*100+'%';};
function downloadCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son'); let s=CURRENT[CURRENT_INDEX]; let a=document.createElement('a'); a.href=s.file; a.download=s.title+'.mp3'; a.target='_blank'; a.click(); }
function downloadItem(id){ let it=ALL.find(x=>x.id===id); if(it.type==='SINGLE'){ let a=document.createElement('a'); a.href=it.file; a.download=it.title+'.mp3'; a.target='_blank'; a.click(); } else { it.songs.forEach((s,i)=>setTimeout(()=>{let a=document.createElement('a'); a.href=s.file; a.download=s.title+'.mp3'; a.target='_blank'; a.click();}, i*800)); alert('Téléchargement de '+it.songs.length+' sons... ⬇'); } }
let SHARE_ID=null;
function openShare(id){ SHARE_ID=id; let it=ALL.find(x=>x.id===id); document.getElementById('shareTitle').innerText=it.title+' - '+it.artist; document.getElementById('shareModal').classList.remove('hidden'); }
function shareCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son'); if(navigator.share){let s=CURRENT[CURRENT_INDEX]; navigator.share({title:'GOSPEL WORLD',text:`🎵 ${s.title} - ${s.artist} sur GOSPEL WORLD 🔥`,url:location.href});} else {openShare(CURRENT[CURRENT_INDEX].id);} }
function shareTo(platform){ let it=ALL.find(x=>x.id===SHARE_ID); if(!it) return; let url=encodeURIComponent(location.href); let txt=encodeURIComponent(`🎵 ${it.title} - ${it.artist} sur GOSPEL WORLD 🔥 Ecoute ici: `+location.href); let links={whatsapp:`https://wa.me/?text=${txt}`,facebook:`https://www.facebook.com/sharer/sharer.php?u=${url}`,telegram:`https://t.me/share/url?url=${url}&text=${txt}`,x:`https://twitter.com/intent/tweet?text=${txt}`,tiktok:`https://www.tiktok.com/`}; if(platform==='copy'){ navigator.clipboard.writeText(location.href+' - '+it.title); alert('Lien copié! ✅'); } else if(platform==='tiktok'){ navigator.clipboard.writeText(location.href); alert('Lien copié! Colle-le sur TikTok ✅'); } else { window.open(links[platform],'_blank'); } document.getElementById('shareModal').classList.add('hidden'); }
function openModal(mode){ document.getElementById('modal').classList.remove('hidden'); let isColl=mode==='collection'; document.getElementById('collectionFields').classList.toggle('hidden',!isColl); document.getElementById('modalTitle').innerText=isColl?'Créer EP / Mixtape / Album':'Publier un Single'; document.getElementById('titre').placeholder=isColl?'Nom du projet ex: Gloire Vol.1':'Titre du Single'; document.getElementById('upForm').dataset.mode=mode; }
function closeModal(){document.getElementById('modal').classList.add('hidden');}
document.getElementById('files').onchange=e=>{document.getElementById('fileInfo').innerText=e.target.files.length+' fichier(s) sélectionné(s) ✅';};
document.getElementById('upForm').onsubmit=async e=>{ e.preventDefault(); let mode=e.target.dataset.mode||'single'; let fd=new FormData(); fd.append('artist',document.getElementById('artist').value); fd.append('titre',document.getElementById('titre').value); if(mode==='collection'){fd.append('type',document.getElementById('type').value); fd.append('desc',document.getElementById('desc').value);} let cf=document.getElementById('coverFile').files[0]; if(cf) fd.append('cover',cf); for(let f of document.getElementById('files').files) fd.append('files',f); document.getElementById('status').innerText='Upload vers Cloudinary... ⏳'; let url=mode==='collection'?'/upload-collection':'/upload-single'; let r=await fetch(url,{method:'POST',body:fd}); let d=await r.json(); document.getElementById('status').innerText=d.message; if(d.success){load(); setTimeout(closeModal,1200);} };
load();
</script></body></html>
    """

@app.route("/manifest.json")
def manifest():
    return jsonify({"name":"GOSPEL WORLD","short_name":"GOSPEL WORLD","start_url":"/","display":"standalone","background_color":"#121212","theme_color":"#FFD700","icons":[{"src":"https://picsum.photos/seed/gospel/512","sizes":"512x512","type":"image/png"}]})

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
        return jsonify({"success":True,"message":f"✅ Single '{title}' publié!"})
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
        return jsonify({"success":True,"message":f"✅ {ptype} '{title}' publié avec {len(songs_list)} titres!"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
