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
<title>GOSPEL WORLD - Le Gospel du Monde Entier</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#050505">
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
body{background:#050505;color:white;font-family:sans-serif;overflow-x:hidden}
.gold{background:linear-gradient(135deg,#FFD700,#FF8C00,#FF2D55);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-size:200% 200%;animation:grad 4s infinite}
@keyframes grad{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hero-bg{background:radial-gradient(circle at 50% 0%,#FFD70033 0%,#FF8C0022 30%,transparent 70%)}
.bar{width:4px;background:linear-gradient(#FFD700,#FF2D55);border-radius:99px;animation:eq 0.8s infinite alternate}
@keyframes eq{from{height:10px}to{height:40px}}
.tab-active{background:#FFD700!important;color:black!important}
.glow{box-shadow:0 0 40px #FFD70044}
.marquee{animation:scroll 20s linear infinite;white-space:nowrap}
@keyframes scroll{from{transform:translateX(100%)}to{transform:translateX(-100%)}}
</style></head><body class="hero-bg">

<!-- HEADER GOSPEL WORLD -->
<header class='fixed top-0 w-full bg-black/80 backdrop-blur-xl border-b border-yellow-500/20 p-4 z-50 flex justify-between items-center'>
<div class='flex items-center gap-2'><div class='w-10 h-10 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-black font-black text-xl glow'>G</div><div><b class='text-lg leading-none'>GOSPEL<span class='text-yellow-400'> WORLD</span></b><p class='text-[10px] opacity-50 leading-none'>CONAKRY • MONDE ENTIER 🌍</p></div></div>
<div class='flex gap-2'>
<button onclick="installApp()" class='bg-white text-black px-3 py-2 rounded-full font-bold text-xs md:text-sm'><i class='fa-solid fa-mobile'></i> TÉLÉCHARGER L'APP</button>
<button onclick="openModal('single')" class='bg-yellow-400 text-black px-4 py-2 rounded-full font-bold text-sm'>+ PUBLIER</button>
</div></header>

<!-- HERO IMMERSIF -->
<section class='pt-28 px-6 max-w-7xl mx-auto text-center'>
<div class='flex justify-center gap-1 items-end h-12 mb-4'><div class='bar' style='animation-delay:0s'></div><div class='bar' style='animation-delay:0.1s'></div><div class='bar' style='animation-delay:0.2s'></div><div class='bar' style='animation-delay:0.3s'></div><div class='bar' style='animation-delay:0.4s'></div><div class='bar' style='animation-delay:0.5s'></div><div class='bar' style='animation-delay:0.6s'></div></div>
<h1 class='text-6xl md:text-8xl font-black leading-[0.9]'>GOSPEL<br><span class='gold'>WORLD</span></h1>
<p class='opacity-70 mt-4 max-w-xl mx-auto'>Plus qu'une app de musique. Une expérience. Le Gospel de Guinée qui conquiert le monde. 🙏🔥</p>
<div class='mt-6 flex justify-center gap-3 flex-wrap'>
<button onclick="installApp()" class='bg-white text-black px-5 py-3 rounded-full font-black text-sm'><i class='fa-brands fa-android'></i> TÉLÉCHARGER L'APP GRATUIT</button>
<button onclick="document.getElementById('grid').scrollIntoView({behavior:'smooth'})" class='bg-yellow-400 text-black px-5 py-3 rounded-full font-black text-sm'>▶ ÉCOUTER MAINTENANT</button>
</div>
<div class='mt-6 bg-yellow-400/10 border border-yellow-500/30 rounded-full py-2 overflow-hidden'><div class='marquee text-yellow-300 text-sm font-bold'>🔥 TRENDING: AIMEZ PRECHER JESUS • GLOIRE A DIEU • JESUS REVIENT BIENTOT • CONAKRY EN FEU • GOSPEL WORLD NUMERO 1 EN GUINEE 🔥</div></div>
</section>

<!-- RECHERCHE + FILTRES -->
<section class='px-6 max-w-7xl mx-auto mt-8'>
<input id='search' oninput='render()' placeholder='🔍 Recherche artiste, titre, EP, Album...' class='w-full bg-white/5 border border-white/10 rounded-full px-5 py-3 outline-none focus:border-yellow-400'>
<div class='mt-4 flex gap-2 flex-wrap'>
<button onclick="showTab('all',this)" class='tab-btn tab-active bg-white/10 px-4 py-2 rounded-full text-sm font-bold'>Tout</button>
<button onclick="showTab('SINGLE',this)" class='tab-btn bg-white/10 px-4 py-2 rounded-full text-sm font-bold'>🎵 Singles</button>
<button onclick="showTab('EP',this)" class='tab-btn bg-white/10 px-4 py-2 rounded-full text-sm font-bold'>💿 EP</button>
<button onclick="showTab('MIXTAPE',this)" class='tab-btn bg-white/10 px-4 py-2 rounded-full text-sm font-bold'>🔥 Mixtape</button>
<button onclick="showTab('ALBUM',this)" class='tab-btn bg-white/10 px-4 py-2 rounded-full text-sm font-bold'>👑 Album</button>
<button onclick="showTab('LIKED',this)" class='tab-btn bg-white/10 px-4 py-2 rounded-full text-sm font-bold'>❤️ Mes Likes</button>
</div></section>

<section id='grid' class='px-6 max-w-7xl mx-auto mt-8 grid md:grid-cols-2 lg:grid-cols-3 gap-6 pb-48'></section>

<!-- PLAYER IMMERSIF -->
<div class='fixed bottom-0 w-full bg-black/95 backdrop-blur-xl border-t border-yellow-500/30 p-4 z-40'>
<div class='flex items-center gap-4 max-w-7xl mx-auto'>
<img id='cover' src='https://picsum.photos/seed/gospel/100' class='w-16 h-16 rounded-2xl glow'>
<div class='flex-1 min-w-0'><h4 id='ptitle' class='font-bold truncate'>Choisis un chant</h4><p id='partist' class='text-xs opacity-60'>GOSPEL WORLD</p>
<div class='w-full bg-white/10 h-1.5 rounded-full mt-1'><div id='prog' class='h-1.5 bg-gradient-to-r from-yellow-400 to-pink-500 rounded-full w-0'></div></div>
<p id='playlistInfo' class='text-[11px] text-yellow-400 mt-1'></p></div>
<div class='flex items-center gap-2'>
<button onclick="prevSong()" class='w-10 h-10 bg-white/10 rounded-full'><i class='fa-solid fa-backward'></i></button>
<button id='playBtn' class='w-14 h-14 bg-yellow-400 text-black rounded-full shrink-0 text-lg'><i class='fa-solid fa-play'></i></button>
<button onclick="nextSong()" class='w-10 h-10 bg-white/10 rounded-full'><i class='fa-solid fa-forward'></i></button>
<button onclick="shareCurrent()" class='w-10 h-10 bg-white/10 rounded-full' title='Partager'><i class='fa-solid fa-share-nodes'></i></button>
<button onclick="downloadCurrent()" class='w-10 h-10 bg-green-500 text-white rounded-full' title='Télécharger le son'><i class='fa-solid fa-download'></i></button>
</div></div><audio id='audio' class='hidden'></audio></div>

<!-- MODAL PARTAGE - TOUTES PLATEFORMES -->
<div id='shareModal' class='hidden fixed inset-0 bg-black/90 z-[120] flex items-center justify-center p-6'><div class='bg-[#111] border border-yellow-500/30 rounded-[25px] p-6 max-w-sm w-full text-center'>
<h3 class='text-xl font-black mb-1'>Partager ce chant 🔥</h3><p id='shareTitle' class='text-sm opacity-60 mb-4'></p>
<div class='grid grid-cols-3 gap-3'>
<button onclick="shareTo('whatsapp')" class='bg-[#25D366] py-3 rounded-2xl font-bold text-sm'><i class='fa-brands fa-whatsapp text-xl'></i><br>WhatsApp</button>
<button onclick="shareTo('facebook')" class='bg-[#1877F2] py-3 rounded-2xl font-bold text-sm'><i class='fa-brands fa-facebook text-xl'></i><br>Facebook</button>
<button onclick="shareTo('telegram')" class='bg-[#0088cc] py-3 rounded-2xl font-bold text-sm'><i class='fa-brands fa-telegram text-xl'></i><br>Telegram</button>
<button onclick="shareTo('x')" class='bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm'><i class='fa-brands fa-x-twitter text-xl'></i><br>X</button>
<button onclick="shareTo('tiktok')" class='bg-black border border-white/20 py-3 rounded-2xl font-bold text-sm'><i class='fa-brands fa-tiktok text-xl'></i><br>TikTok</button>
<button onclick="shareTo('copy')" class='bg-white/10 py-3 rounded-2xl font-bold text-sm'><i class='fa-solid fa-link text-xl'></i><br>Copier</button>
</div>
<p class='text-xs opacity-50 mt-4'>Partage aussi sur Instagram / Snapchat en copiant le lien</p>
<button onclick="document.getElementById('shareModal').classList.add('hidden')" class='mt-4 w-full bg-white/10 py-2 rounded-full'>Fermer</button></div></div>

<!-- MODAL PUBLIER -->
<div id='modal' class='hidden fixed inset-0 bg-black/90 z-[100] flex items-center justify-center p-4 overflow-y-auto'><div class='bg-[#111] border border-yellow-500/30 rounded-[25px] p-6 max-w-lg w-full my-8'>
<div class='flex justify-between mb-4'><h3 id='modalTitle' class='text-2xl font-black'>Publier</h3><button onclick="closeModal()" class='bg-white/10 w-8 h-8 rounded-full'>X</button></div>
<div class='flex gap-2 mb-4'>
<button onclick="openModal('single')" id='btn-single' class='flex-1 py-2 rounded-full bg-white/10 font-bold text-sm'>🎵 Single</button>
<button onclick="openModal('collection')" id='btn-collection' class='flex-1 py-2 rounded-full bg-white/10 font-bold text-sm'>💿 EP / Mixtape / Album</button>
</div>
<form id='upForm' class='space-y-3'>
<input id='artist' placeholder='Nom artiste' required class='w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3'>
<input id='titre' placeholder='Titre' required class='w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3'>
<div id='collectionFields' class='hidden space-y-3'>
<select id='type' class='w-full bg-[#222] border border-white/10 rounded-xl px-4 py-3'><option value='EP'>💿 EP - 2 à 6 sons</option><option value='MIXTAPE'>🔥 MIXTAPE - 7 à 15 sons</option><option value='ALBUM'>👑 ALBUM - 10 à 20 sons</option></select>
<textarea id='desc' placeholder='Description du projet...' class='w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3'></textarea></div>
<div class='border-2 border-dashed border-yellow-500/50 rounded-xl p-4 text-center'><label class='text-sm font-bold'>📸 COVER (Photo du projet)</label><input id='coverFile' type='file' accept='image/*' class='w-full mt-2'></div>
<div class='border-2 border-dashed border-yellow-500/50 rounded-xl p-4 text-center'><label class='text-sm font-bold'>🎵 FICHIERS AUDIO</label><input id='files' type='file' accept='.mp3,audio/*' multiple required class='w-full mt-2'><p id='fileInfo' class='text-xs opacity-60 mt-2'>Single = 1 fichier | EP / Album = plusieurs fichiers (CTRL + clic)</p></div>
<button class='w-full bg-yellow-400 text-black font-black py-3 rounded-xl'>PUBLIER SUR GOSPEL WORLD 🔥</button><p id='status' class='text-center text-sm'></p></form></div></div>

<script>
let ALL=[], CURRENT=[], CURRENT_INDEX=0, FILTER='all', LIKES=JSON.parse(localStorage.getItem('gw_likes')||'[]'), deferredPrompt=null;
const audio=document.getElementById('audio'); const playBtn=document.getElementById('playBtn');
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault(); deferredPrompt=e;});
function installApp(){ if(deferredPrompt){deferredPrompt.prompt();} else {alert('📱 Pour installer GOSPEL WORLD:\\n\\nSur Android Chrome: Menu ⋮ > Ajouter à l\\'écran d\\'accueil\\nSur iPhone Safari: Partager > Ajouter à l\\'écran d\\'accueil\\n\\nTu auras l\\'icône GOSPEL WORLD comme une vraie app!');}}
async function load(){ let r=await fetch('/api/all'); let d=await r.json(); ALL=d.items; render(); }
function showTab(f,btn){FILTER=f; document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('tab-active')); btn.classList.add('tab-active'); render();}
function toggleLike(id){ if(LIKES.includes(id)) LIKES=LIKES.filter(x=>x!==id); else LIKES.push(id); localStorage.setItem('gw_likes',JSON.stringify(LIKES)); render(); fetch('/api/like',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})}); }
function render(){
  let q=document.getElementById('search').value.toLowerCase();
  let list=ALL.filter(x=>{
    if(FILTER==='LIKED' && !LIKES.includes(x.id)) return false;
    if(FILTER!=='all' && FILTER!=='LIKED' && x.type!==FILTER) return false;
    if(q && !(x.title.toLowerCase().includes(q)||x.artist.toLowerCase().includes(q))) return false;
    return true;
  });
  document.getElementById('grid').innerHTML=list.map(item=>{
    let liked=LIKES.includes(item.id)?'❤️':'🤍';
    let shareBtn=`<button onclick="openShare('${item.id}')" class='flex-1 bg-white/10 py-2 rounded-full text-xs font-bold'>↗ PARTAGER</button>`;
    let dlBtn=`<button onclick="downloadItem('${item.id}')" class='flex-1 bg-green-500 py-2 rounded-full text-xs font-bold'>⬇ TÉLÉCHARGER</button>`;
    if(item.type==='SINGLE'){
      return `<div class='bg-[#111] rounded-[20px] p-4 border border-white/5 hover:border-yellow-500/50 transition'><img src='${item.cover}' class='w-full h-52 object-cover rounded-xl'><h3 class='font-bold mt-3 truncate'>${item.title}</h3><p class='text-xs opacity-60'>${item.artist} • 🎵 Single • ❤️ ${item.likes||0}</p><div class='flex gap-2 mt-3'><button onclick="playSingle('${item.id}')" class='flex-1 bg-yellow-400 text-black font-bold py-2 rounded-full text-sm'>▶ ÉCOUTER</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div></div>`;
    } else {
      let badge=item.type==='EP'?'💿 EP':item.type==='MIXTAPE'?'🔥 MIXTAPE':'👑 ALBUM';
      return `<div class='bg-gradient-to-br from-[#1a1500] to-[#111] rounded-[20px] p-4 border border-yellow-500/30'><img src='${item.cover}' class='w-full h-52 object-cover rounded-xl'><span class='inline-block bg-yellow-400 text-black text-[11px] font-black px-2 py-1 rounded-full mt-3'>${badge} • ${item.songs.length} TITRES</span><h3 class='font-bold mt-2 truncate'>${item.title}</h3><p class='text-xs opacity-60'>${item.artist} • ❤️ ${item.likes||0}</p><p class='text-xs opacity-50 mt-1'>${item.desc||''}</p><div class='flex gap-2 mt-3'><button onclick="playCollection('${item.id}')" class='flex-1 bg-yellow-400 text-black font-bold py-2 rounded-full text-sm'>▶ ÉCOUTER TOUT</button><button onclick="toggleLike('${item.id}')" class='w-10 bg-white/10 rounded-full'>${liked}</button></div><div class='flex gap-2 mt-2'>${shareBtn}${dlBtn}</div><div class='mt-3 space-y-1'>${item.songs.map((s,i)=>`<div onclick="playCollection('${item.id}',${i})" class='flex justify-between text-xs bg-white/5 px-3 py-2 rounded-lg cursor-pointer hover:bg-white/10'><span>${i+1}. ${s.title}</span><span>▶ ⬇</span></div>`).join('')}</div></div>`;
    }
  }).join('')||'<p class="opacity-50 col-span-full text-center py-10">Aucun résultat. Sois le premier à publier! 🙏</p>';
}
function playSingle(id){let s=ALL.find(x=>x.id===id); CURRENT=[{title:s.title,artist:s.artist,file:s.file,id:s.id}]; CURRENT_INDEX=0; playCurrent();}
function playCollection(id,start=0){let c=ALL.find(x=>x.id===id); CURRENT=c.songs.map(s=>({title:s.title,artist:c.artist,file:s.file,id:c.id})); CURRENT_INDEX=start; playCurrent(c.title);}
function playCurrent(coll=''){let s=CURRENT[CURRENT_INDEX]; if(!s) return; document.getElementById('ptitle').innerText=s.title; document.getElementById('partist').innerText=s.artist; document.getElementById('cover').src='https://picsum.photos/seed/'+encodeURIComponent(s.title)+'/100'; document.getElementById('playlistInfo').innerText=coll?`📀 ${coll} - ${CURRENT_INDEX+1}/${CURRENT.length}`:`🎵 Single`; audio.src=s.file; audio.play(); playBtn.innerHTML='<i class="fa-solid fa-pause"></i>';}
function nextSong(){if(CURRENT_INDEX<CURRENT.length-1){CURRENT_INDEX++; playCurrent();}}
function prevSong(){if(CURRENT_INDEX>0){CURRENT_INDEX--; playCurrent();}}
audio.onended=()=>nextSong();
playBtn.onclick=()=>{if(audio.paused){audio.play(); playBtn.innerHTML='<i class="fa-solid fa-pause"></i>';}else{audio.pause(); playBtn.innerHTML='<i class="fa-solid fa-play"></i>';}};
audio.ontimeupdate=()=>{if(audio.duration) document.getElementById('prog').style.width=audio.currentTime/audio.duration*100+'%';};
function downloadCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis d\\'abord un son'); let s=CURRENT[CURRENT_INDEX]; let a=document.createElement('a'); a.href=s.file; a.download=s.title+'.mp3'; a.target='_blank'; a.click(); }
function downloadItem(id){ let it=ALL.find(x=>x.id===id); if(it.type==='SINGLE'){ let a=document.createElement('a'); a.href=it.file; a.download=it.title+'.mp3'; a.target='_blank'; a.click(); } else { it.songs.forEach((s,i)=>setTimeout(()=>{let a=document.createElement('a'); a.href=s.file; a.download=s.title+'.mp3'; a.target='_blank'; a.click();}, i*800)); alert('Téléchargement de '+it.songs.length+' sons... ⬇'); } }
let SHARE_ID=null;
function openShare(id){ SHARE_ID=id; let it=ALL.find(x=>x.id===id); document.getElementById('shareTitle').innerText=it.title+' - '+it.artist; document.getElementById('shareModal').classList.remove('hidden'); }
function shareCurrent(){ if(!CURRENT[CURRENT_INDEX]) return alert('Choisis un son d\\'abord'); let s=CURRENT[CURRENT_INDEX]; let url=location.href; let txt=`🎵 ${s.title} - ${s.artist} sur GOSPEL WORLD 🔥 Ecoute ici: ${url}`; if(navigator.share){navigator.share({title:'GOSPEL WORLD',text:txt,url});} else {openShare(CURRENT[CURRENT_INDEX].id);} }
function shareTo(platform){ let it=ALL.find(x=>x.id===SHARE_ID); if(!it) return; let url=encodeURIComponent(location.href); let txt=encodeURIComponent(`🎵 ${it.title} - ${it.artist} sur GOSPEL WORLD 🔥 Ecoute ici: `+location.href); let links={whatsapp:`https://wa.me/?text=${txt}`,facebook:`https://www.facebook.com/sharer/sharer.php?u=${url}`,telegram:`https://t.me/share/url?url=${url}&text=${txt}`,x:`https://twitter.com/intent/tweet?text=${txt}`,tiktok:`https://www.tiktok.com/`}; if(platform==='copy'){ navigator.clipboard.writeText(location.href+' - '+it.title); alert('Lien copié! Colle-le sur TikTok / Instagram / Snapchat ✅'); } else if(platform==='tiktok'){ navigator.clipboard.writeText(location.href); alert('Lien copié! Ouvre TikTok et colle-le en bio / vidéo ✅'); } else { window.open(links[platform],'_blank'); } document.getElementById('shareModal').classList.add('hidden'); }
function openModal(mode){ document.getElementById('modal').classList.remove('hidden'); let isColl=mode==='collection'; document.getElementById('collectionFields').classList.toggle('hidden',!isColl); document.getElementById('modalTitle').innerText=isColl?'Créer EP / Mixtape / Album':'Publier un Single'; document.getElementById('titre').placeholder=isColl?'Nom du projet ex: Gloire Vol.1':'Titre du Single'; document.getElementById('upForm').dataset.mode=mode; }
function closeModal(){document.getElementById('modal').classList.add('hidden');}
document.getElementById('files').onchange=e=>{document.getElementById('fileInfo').innerText=e.target.files.length+' fichier(s) sélectionné(s) ✅';};
document.getElementById('upForm').onsubmit=async e=>{ e.preventDefault(); let mode=e.target.dataset.mode||'single'; let fd=new FormData(); fd.append('artist',document.getElementById('artist').value); fd.append('titre',document.getElementById('titre').value); if(mode==='collection'){fd.append('type',document.getElementById('type').value); fd.append('desc',document.getElementById('desc').value);} let cf=document.getElementById('coverFile').files[0]; if(cf) fd.append('cover',cf); for(let f of document.getElementById('files').files) fd.append('files',f); document.getElementById('status').innerText='Upload vers Cloudinary... ⏳ Ne ferme pas!'; let url=mode==='collection'?'/upload-collection':'/upload-single'; let r=await fetch(url,{method:'POST',body:fd}); let d=await r.json(); document.getElementById('status').innerText=d.message; if(d.success){load(); setTimeout(closeModal,1200);} };
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
        return jsonify({"success":True,"message":f"✅ Single '{title}' publié sur GOSPEL WORLD!"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})

@app.route("/upload-collection", methods=["POST"])
def upload_collection():
    title=request.form.get("titre","").strip(); artist=request.form.get("artist","").strip(); ptype=request.form.get("type","EP"); desc=request.form.get("desc",""); files=request.files.getlist("files")
    if not title or not artist or not files: return jsonify({"success":False,"message":"Remplis tout + choisis fichiers"})
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
