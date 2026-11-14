from flask import Flask, jsonify, request
import json, os, uuid, urllib.request
import cloudinary, cloudinary.uploader
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
GW="629757411"
CLOUD=os.getenv("CLOUDINARY_CLOUD_NAME")
cloudinary.config(cloud_name=CLOUD, api_key=os.getenv("CLOUDINARY_API_KEY"), api_secret=os.getenv("CLOUDINARY_API_SECRET"), secure=True)
cache={}
def load(f,d=[]):
    try:
        u=f"https://res.cloudinary.com/{CLOUD}/raw/upload/gospelworld_data/{f.replace('.json','')}.json"
        with urllib.request.urlopen(urllib.request.Request(u,headers={"Cache-Control":"no-cache"}),timeout=8) as r:
            cache[f]=json.loads(r.read()); return cache[f]
    except: return cache.get(f,d)
def save(f,data):
    cache[f]=data
    try:
        open("/tmp/"+f,"w").write(json.dumps(data))
        cloudinary.uploader.upload("/tmp/"+f, resource_type="raw", public_id="gospelworld_data/"+f.replace(".json",""), overwrite=True, invalidate=True)
    except: pass

@app.route("/")
def home():
    return open(__file__).read().split('HTML="""')[1].split('"""')[0] if False else """<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GOSPEL WORLD</title><script src="https://cdn.tailwindcss.com"></script><style>
body{background:#000;color:#fff;font-family:Arial}input{background:#222!important;color:#fff!important;border:1px solid #333!important}
.chip{background:#222}.pill-active{background:#fff!important;color:#000!important}
.spot-row{display:flex;gap:10px;overflow-x:auto;padding:0 12px 4px;scrollbar-width:none}.spot-row::-webkit-scrollbar{display:none}
.spot-card{flex:0 0 148px;cursor:pointer}.spot-card img{width:148px;height:148px;object-fit:cover;border-radius:8px}
.spot-card.artist img{border-radius:9999px}.spot-card p{font-weight:700;margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.spot-card span{font-size:12px;color:#aaa;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.spot-title{font-size:20px;font-weight:800;padding:18px 12px 10px}
.hrow{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:4px}.hrow::-webkit-scrollbar{display:none}.hrow>*{flex-shrink:0;white-space:nowrap}
@media(min-width:769px){.spot-card{flex:0 0 180px}.spot-card img{width:180px;height:180px}}
</style></head><body>
<header class="sticky top-0 z-40 bg-black/90 p-3 flex justify-between items-center"><b>GOSPEL <span class="text-yellow-400">WORLD</span> 👑</b><div class="flex gap-2"><button onclick="installApp()" class="bg-green-600 px-3 py-2 rounded-full text-xs font-bold">📥 TELECHARGER L'APP</button><button onclick="openModal()" class="bg-yellow-400 text-black px-3 py-2 rounded-full text-xs font-black">➕ PUBLIER</button></div></header>

<div class="p-3"><div class="bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-400 rounded-xl p-3 flex justify-between items-center gap-2"><div><b class="text-black text-sm">🎤 TU ES ARTISTE? BALANCE TON SON!</b><p class="text-black text-[11px] font-bold">Reste pour toujours 🔒 Gratuit</p></div><button onclick="openModal()" class="bg-black text-white px-4 py-2 rounded-full text-xs font-black shrink-0">➕ PUBLIER</button></div></div>

<div class="px-3"><h1 class="text-[32px] font-black leading-none">GOSPEL<br><span class="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-400">WORLD</span></h1><p class="font-bold text-sm mt-1">👑 ROYAUME DE DIEU</p>
<div class="bg-white/5 rounded-xl p-3 mt-3"><p class="text-[11px] text-yellow-400 font-black">📖 VERSET DU JOUR</p><p id="verse" class="text-xs italic mt-1">Chargement...</p></div>
<div class="hrow mt-3"><button onclick="startRadio()" class="bg-gradient-to-r from-yellow-400 to-pink-500 px-4 py-2 rounded-full text-xs font-black">📻 RADIO ROYAUME</button><button onclick="playFirst()" class="bg-white text-black px-4 py-2 rounded-full text-xs font-black">🔀 ALEATOIRE</button><button onclick="openDonateGW()" class="bg-yellow-400 text-black px-4 py-2 rounded-full text-xs font-black">💛 SOUTENIR GW - 629-757-411</button><button onclick="openModal()" class="bg-yellow-400 text-black px-4 py-2 rounded-full text-xs font-black">➕ PUBLIER MON SON</button></div>
<div id="stats" class="hrow mt-3"></div></div>

<div class="px-3 mt-4"><input id="search" oninput="renderSpotify()" placeholder="🔍 Recherche artiste, titre..." class="w-full rounded-full px-4 py-2.5 text-sm outline-none">
<div class="hrow mt-3" id="filters">
<button onclick="showTab('all',this)" class="tab-btn pill-active chip px-3 py-1.5 rounded-full text-xs font-bold">Tout</button>
<button onclick="showTab('SINGLE',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">🎵 Single</button>
<button onclick="showTab('EP',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">📀 EP</button>
<button onclick="showTab('MIXTAPE',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">🔥 Mixtape</button>
<button onclick="showTab('ALBUM',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">💿 Album</button>
<button onclick="showTab('LIVE SESSION',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">🔴 Live</button>
<button onclick="showTab('ACAPELLA',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">🎤 Acapella</button>
<button onclick="showTab('WORSHIP NIGHT',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">🙏 Worship</button>
<button onclick="showTab('TOP',this)" class="tab-btn chip px-3 py-1.5 rounded-full text-xs font-bold">🌍 Top</button>
</div></div>

<div><div class="spot-title">Titres tendance 🔥</div><div id="spotTrending" class="spot-row"></div>
<div class="spot-title">Artistes populaires 🎤</div><div id="spotArtists" class="spot-row"></div>
<div class="spot-title">Albums et singles populaires 💿</div><div id="spotAlbums" class="spot-row"></div>
<div class="spot-title">Nouveautés du Royaume ✨</div><div id="spotNew" class="spot-row"></div></div>

<div class="fixed bottom-[118px] w-full bg-black border-t border-yellow-500/20 p-3 z-50 flex items-center gap-3"><img id="cover" onclick="openFull()" src="https://picsum.photos/seed/gospel/100" class="w-12 h-12 rounded-lg"><div class="flex-1 min-w-0"><b id="ptitle" class="text-sm truncate block">Choisis un chant</b><span id="partist" class="text-xs text-gray-400 truncate block">GOSPEL WORLD</span></div><button onclick="downloadCurrent()" class="w-10 h-10 bg-green-600 rounded-full">⬇️</button><button id="playBtn" onclick="togglePlay()" class="w-11 h-11 bg-yellow-400 text-black rounded-full">▶️</button></div>
<div class="fixed bottom-0 w-full bg-black border-t border-white/10 z-[60] flex justify-around py-2"><button onclick="goHome()" class="text-xs text-center">🏠<br>Accueil</button><button onclick="document.getElementById('search').focus()" class="text-xs text-center">🔍<br>Rechercher</button><button onclick="openModal()" class="text-center -mt-6"><span class="w-14 h-14 bg-yellow-400 text-black rounded-full flex items-center justify-center text-2xl font-black border-4 border-black">+</span><span class="text-[11px] font-black text-yellow-400">PUBLIER</span></button><button onclick="showTab('TOP',null)" class="text-xs text-center">🏆<br>Top</button><button onclick="openDonateGW()" class="text-xs text-center">💛<br>Soutenir</button></div>

<div id="full" class="hidden fixed inset-0 z-[200] bg-black p-4 text-center overflow-y-auto"><button onclick="closeFull()" class="absolute top-3 right-3 bg-white/10 w-10 h-10 rounded-full">X</button><p class="text-[11px] text-yellow-400 font-black mt-6">👑 ROYAUME DE DIEU</p><img id="fullCover" class="w-[260px] h-[260px] rounded-[30px] object-cover mx-auto mt-4 border-4 border-yellow-400"><h2 id="fullTitle" class="text-2xl font-black mt-4">Choisis un chant</h2><p id="fullArtist" class="text-yellow-400 font-bold">GOSPEL WORLD</p><div class="flex justify-center gap-4 mt-5"><button onclick="prevSong()" class="w-12 h-12 bg-white/10 rounded-full">⏮️</button><button onclick="togglePlay()" id="fullPlay" class="w-[70px] h-[70px] bg-yellow-400 text-black rounded-full text-2xl">▶️</button><button onclick="nextSong()" class="w-12 h-12 bg-white/10 rounded-full">⏭️</button></div><div class="flex gap-2 justify-center mt-5 flex-wrap"><button onclick="downloadCurrent()" class="bg-green-600 px-4 py-2 rounded-full text-sm font-bold">⬇️ TELECHARGER HD</button><button onclick="donateCurrent()" class="bg-green-600 px-4 py-2 rounded-full text-sm font-bold">🙏 Soutenir l'artiste</button><button onclick="openDonateGW()" class="bg-yellow-400 text-black px-4 py-2 rounded-full text-sm font-bold">💛 Soutenir GW - 629-757-411</button></div><div class="w-full bg-white/20 h-1.5 rounded-full mt-5"><div id="prog" class="h-1.5 bg-yellow-400 rounded-full" style="width:0%"></div></div><p class="text-xs text-gray-400 mt-2"><span id="cur">0:00</span> / <span id="dur">0:00</span></p></div>
<audio id="audio" class="hidden"></audio>

<div id="donate" class="hidden fixed inset-0 bg-black/90 z-[220] flex items-center justify-center p-6"><div class="bg-[#181818] rounded-2xl p-5 w-full max-w-sm text-center"><h3 id="donateTitle" class="font-black">💛 Soutenir</h3><p id="donateDesc" class="text-xs text-gray-400 mt-2"></p><p id="donateNum" class="text-xl font-black text-yellow-400 mt-2"></p><div class="grid grid-cols-3 gap-2 mt-3"><button onclick="doDonate(5000)" class="bg-white/10 py-2 rounded-lg text-sm">5.000</button><button onclick="doDonate(10000)" class="bg-yellow-400 text-black py-2 rounded-lg text-sm font-bold">10.000</button><button onclick="doDonate(20000)" class="bg-white/10 py-2 rounded-lg text-sm">20.000</button></div><button onclick="document.getElementById('donate').classList.add('hidden')" class="mt-4 w-full bg-white/10 py-2 rounded-full text-sm">Fermer</button></div></div>

<div id="modal" class="hidden fixed inset-0 bg-black/90 z-[100] flex items-center justify-center p-4 overflow-y-auto"><div class="bg-[#181818] rounded-2xl p-5 w-full max-w-md"><div class="flex justify-between"><h3 class="font-black text-lg">🎤 PUBLIER</h3><button onclick="closeModal()" class="bg-white/10 w-8 h-8 rounded-full">X</button></div><p class="text-xs text-yellow-400 mt-1">Ton son reste pour toujours 🔒 Gratuit</p><form id="upForm" class="space-y-2 mt-3"><div class="flex gap-2"><button type="button" onclick="setType('SINGLE')" id="bSingle" class="flex-1 bg-yellow-400 text-black py-2 rounded-lg text-xs font-black">🎵 SINGLE</button><button type="button" onclick="setType('EP')" id="bEP" class="flex-1 bg-white/10 py-2 rounded-lg text-xs font-bold">📀 EP / ALBUM</button></div><input id="artist" placeholder="Nom artiste - Ex: Jonathan" required class="w-full rounded-xl px-3 py-2.5 text-sm"><input id="titre" placeholder="Titre - Ex: Mon Chant" required class="w-full rounded-xl px-3 py-2.5 text-sm"><input id="artistOM" placeholder="Ton Orange Money / Wave - Ex: 622123456" required class="w-full rounded-xl px-3 py-2.5 text-sm"><label class="text-xs font-bold block">📸 Cover (photo)</label><input id="coverFile" type="file" accept="image/*" class="w-full text-sm"><label class="text-xs font-bold block">🎵 Fichiers MP3 (1 pour Single, plusieurs pour EP/Album)</label><input id="files" type="file" accept=".mp3,audio/*" multiple required class="w-full text-sm"><button class="w-full bg-yellow-400 text-black font-black py-3 rounded-xl">🚀 PUBLIER - CA RESTE POUR TOUJOURS 🔒</button><p id="status" class="text-center text-xs"></p></form></div></div>

<script>
let ALL=[],CUR=[],IDX=0,FLT='all',TYPE='SINGLE',DON={name:'GOSPEL WORLD',num:'629-757-411'};
const audio=document.getElementById('audio');
function installApp(){alert("📥 Android: Menu ⋮ > Ajouter a l'ecran d'accueil\\niPhone: Partager > Ajouter a l'ecran d'accueil")}
function setType(t){TYPE=t;document.getElementById('bSingle').className=t=='SINGLE'?'flex-1 bg-yellow-400 text-black py-2 rounded-lg text-xs font-black':'flex-1 bg-white/10 py-2 rounded-lg text-xs font-bold';document.getElementById('bEP').className=t!='SINGLE'?'flex-1 bg-yellow-400 text-black py-2 rounded-lg text-xs font-black':'flex-1 bg-white/10 py-2 rounded-lg text-xs font-bold'}
function goHome(){FLT='all';document.getElementById('search').value='';renderSpotify();window.scrollTo({top:0,behavior:'smooth'})}
function showTab(f,b){FLT=f;document.querySelectorAll('.tab-btn').forEach(x=>x.classList.remove('pill-active'));if(b)b.classList.add('pill-active');renderSpotify()}
function fmt(s){return s?Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0'):'0:00'}
async function load(){let d=await(await fetch('/api/all')).json();ALL=d.items;let v=await(await fetch('/api/verse')).json();document.getElementById('verse').innerText='"'+v.text+'" - '+v.ref;renderSpotify();let a=new Set(ALL.map(x=>x.artist)).size;document.getElementById('stats').innerHTML=`<span class="bg-white/10 px-3 py-1.5 rounded-full text-xs">${ALL.length} Projets</span><span class="bg-white/10 px-3 py-1.5 rounded-full text-xs">${a} Artistes ✅</span><span class="bg-yellow-400 text-black px-3 py-1.5 rounded-full text-xs font-black">🌍 +120 Pays</span>`}
function renderSpotify(){let q=(document.getElementById('search').value||'').toLowerCase();let list=ALL.filter(x=>{if(FLT=='TOP')return true;if(FLT!='all'&&FLT!='TOP'){if(FLT=='EP'&&['EP','MIXTAPE','ALBUM'].includes(x.type))return true;if(x.type!=FLT)return false}if(q&&!(x.title.toLowerCase().includes(q)||x.artist.toLowerCase().includes(q)))return false;return true});if(FLT=='TOP')list=[...list].sort((a,b)=>(b.likes||0)-(a.likes||0)).slice(0,20);let card=x=>`<div class="spot-card" onclick="playSingle('${x.id}')"><img src="${x.cover}"><p>${x.title}</p><span>${x.artist} ✅ - ${x.type}</span></div>`;document.getElementById('spotTrending').innerHTML=[...list].sort((a,b)=>(b.likes||0)-(a.likes||0)).map(card).join('')||'Pas encore - Publie!';let m={};ALL.forEach(x=>{if(!m[x.artist])m[x.artist]=x});document.getElementById('spotArtists').innerHTML=Object.entries(m).map(([n,i])=>`<div class="spot-card artist" onclick="openArtist('${n}')"><img src="${i.cover}"><p>${n}</p><span>Artiste ✅</span></div>`).join('');document.getElementById('spotAlbums').innerHTML=list.map(card).join('')||'Pas encore';document.getElementById('spotNew').innerHTML=[...list].reverse().map(card).join('')}
function openArtist(n){let l=ALL.filter(x=>x.artist==n);alert(n+' ✅\\n'+l.length+' projet(s)\\n\\nClique sur sa cover pour écouter!')}
function playSingle(id){let s=ALL.find(x=>x.id==id);CUR=s.type=='SINGLE'?[{title:s.title,artist:s.artist,file:s.file,id:s.id,cover:s.cover}]:s.songs.map(x=>({title:x.title,artist:s.artist,file:x.file,id:s.id,cover:s.cover}));IDX=0;playCur()}
function playFirst(){if(!ALL.length)return alert('Pas encore de son');playSingle(ALL[Math.floor(Math.random()*ALL.length)].id)}
function playCur(){let s=CUR[IDX];if(!s)return;document.getElementById('ptitle').innerText=s.title;document.getElementById('partist').innerText=s.artist;document.getElementById('cover').src=s.cover;document.getElementById('fullCover').src=s.cover;document.getElementById('fullTitle').innerText=s.title;document.getElementById('fullArtist').innerText=s.artist+' ✅';audio.src=s.file;audio.play();setIcon(true)}
function setIcon(p){document.getElementById('playBtn').innerText=p?'⏸️':'▶️';document.getElementById('fullPlay').innerText=p?'⏸️':'▶️'}
function togglePlay(){if(audio.paused){audio.play();setIcon(true)}else{audio.pause();setIcon(false)}}
function nextSong(){IDX=(IDX+1)%CUR.length;playCur()}function prevSong(){IDX=IDX>0?IDX-1:0;playCur()}
function startRadio(){if(!ALL.length)return alert('Pas encore');CUR=ALL.flatMap(x=>x.type=='SINGLE'?[{title:x.title,artist:x.artist,file:x.file,id:x.id,cover:x.cover}]:x.songs.map(s=>({title:s.title,artist:x.artist,file:s.file,id:x.id,cover:x.cover})));IDX=Math.floor(Math.random()*CUR.length);playCur()}
audio.onended=()=>nextSong();audio.ontimeupdate=()=>{if(audio.duration){document.getElementById('prog').style.width=audio.currentTime/audio.duration*100+'%';document.getElementById('cur').innerText=fmt(audio.currentTime);document.getElementById('dur').innerText=fmt(audio.duration)}}
function openFull(){if(!CUR[IDX])return alert('Choisis un son');document.getElementById('full').classList.remove('hidden')}function closeFull(){document.getElementById('full').classList.add('hidden')}
function downloadCurrent(){if(!CUR[IDX])return alert('Choisis un son');let a=document.createElement('a');a.href=CUR[IDX].file;a.download=CUR[IDX].title+'.mp3';a.target='_blank';a.click()}
function openDonateGW(){DON={name:'GOSPEL WORLD',num:'629-757-411'};document.getElementById('donateTitle').innerText='💛 Soutenir GOSPEL WORLD';document.getElementById('donateDesc').innerText='Aide a payer le serveur et faire grandir FLASH EVANGILE WORLD. Dieu te benisse!';document.getElementById('donateNum').innerText='Orange Money: 629-757-411';document.getElementById('donate').classList.remove('hidden')}
function donateCurrent(){let s=CUR[IDX];if(!s)return alert('Choisis un son');let it=ALL.find(x=>x.id==s.id);DON={name:it.artist,num:it.artist_om};document.getElementById('donateTitle').innerText='🙏 Soutenir '+it.artist;document.getElementById('donateDesc').innerText='Don DIRECT a 100% a '+it.artist;document.getElementById('donateNum').innerText='Orange Money / Wave: '+(it.artist_om||'');document.getElementById('donate').classList.remove('hidden')}
function doDonate(m){navigator.clipboard.writeText(DON.num);alert('Numero copie: '+DON.num+'\\nEnvoie '+m+' GNF a '+DON.name)}
function openModal(){document.getElementById('modal').classList.remove('hidden')}function closeModal(){document.getElementById('modal').classList.add('hidden')}
document.getElementById('upForm').onsubmit=async e=>{e.preventDefault();let fd=new FormData();fd.append('artist',document.getElementById('artist').value);fd.append('titre',document.getElementById('titre').value);fd.append('artist_om',document.getElementById('artistOM').value);fd.append('type',TYPE);let c=document.getElementById('coverFile').files[0];if(c)fd.append('cover',c);for(let f of document.getElementById('files').files)fd.append('files',f);document.getElementById('status').innerText='Upload... Ne ferme pas! 🔒';let r=await fetch(TYPE=='SINGLE'?'/upload-single':'/upload-collection',{method:'POST',body:fd});let d=await r.json();document.getElementById('status').innerText=d.message;if(d.success){load();setTimeout(closeModal,1000)}};
load();
</script></body></html>"""

@app.route("/api/verse")
def verse():
    import datetime
    v=[("Jean 3:16","Car Dieu a tant aime le monde..."),("Psaume 150:6","Que tout ce qui respire loue l'Eternel!"),("Philippiens 4:13","Je puis tout par celui qui me fortifie."),("Psaume 23:1","L'Eternel est mon berger, je ne manquerai de rien.")]
    i=datetime.date.today().toordinal()%len(v)
    return jsonify({"ref":v[i][0],"text":v[i][1]})
@app.route("/api/all")
def api_all():
    s=load("songs.json"); c=load("collections.json"); items=[]
    for x in s: x["type"]="SINGLE"; items.append(x)
    for x in c: items.append(x)
    return jsonify({"items":items})
@app.route("/upload-single", methods=["POST"])
def up_single():
    t=request.form.get("titre",""); a=request.form.get("artist",""); om=request.form.get("artist_om",""); f=request.files.getlist("files")
    if not t or not a or not f: return jsonify({"success":False,"message":"Remplis tout"})
    try:
        cov=f"https://picsum.photos/seed/{uuid.uuid4().hex[:6]}/400/400"
        if "cover" in request.files and request.files["cover"].filename:
            cov=cloudinary.uploader.upload(request.files["cover"], folder="gospelworld/covers")["secure_url"]
        r=cloudinary.uploader.upload(f[0], resource_type="video", folder="gospelworld/singles")
        s=load("songs.json"); s.insert(0,{"id":uuid.uuid4().hex[:8],"title":t,"artist":a,"artist_om":om,"file":r["secure_url"],"cover":cov,"likes":0}); save("songs.json",s)
        return jsonify({"success":True,"message":f"✅ SINGLE '{t}' sauvegarde pour toujours! 🔒"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})
@app.route("/upload-collection", methods=["POST"])
def up_coll():
    t=request.form.get("titre",""); a=request.form.get("artist",""); om=request.form.get("artist_om",""); tp=request.form.get("type","EP"); f=request.files.getlist("files")
    if not t or not a or not f: return jsonify({"success":False,"message":"Remplis tout"})
    try:
        cov=f"https://picsum.photos/seed/{uuid.uuid4().hex[:6]}/400/400"
        if "cover" in request.files and request.files["cover"].filename:
            cov=cloudinary.uploader.upload(request.files["cover"], folder="gospelworld/covers")["secure_url"]
        lst=[]
        for x in f:
            st=os.path.splitext(x.filename)[0].replace("_"," ").replace("-"," ")
            r=cloudinary.uploader.upload(x, resource_type="video", folder="gospelworld/collections")
            lst.append({"title":st,"file":r["secure_url"]})
        c=load("collections.json"); c.insert(0,{"id":uuid.uuid4().hex[:8],"type":tp,"title":t,"artist":a,"artist_om":om,"cover":cov,"songs":lst,"likes":0}); save("collections.json",c)
        return jsonify({"success":True,"message":f"✅ {tp} '{t}' sauvegarde avec {len(lst)} sons! 🔒"})
    except Exception as e: return jsonify({"success":False,"message":f"Erreur: {e}"})
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
