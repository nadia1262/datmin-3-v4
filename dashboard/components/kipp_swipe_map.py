# dashboard/components/kipp_swipe_map.py
"""
Dual-layer Leaflet swipe-map:
  • Layer MAKRO  — seluruh Kalimantan, Majority Voting 500 m (~1,5 juta sel)
  • Layer MIKRO  — KIPP IKN, klasifikasi LightGBM 10 m (~198 ribu piksel)

Includes a floating toggle to fly between Kalimantan-wide and KIPP IKN views.
"""
import os, base64, hashlib, json
import streamlit as st
import streamlit.components.v1 as components

_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'cache')

_KAL19 = os.path.join(_CACHE, 'kalimantan_2019_overlay.png')
_KAL24 = os.path.join(_CACHE, 'kalimantan_2024_overlay.png')
_META  = os.path.join(_CACHE, 'kalimantan_overlay_meta.json')
_IKN19 = os.path.join(_CACHE, 'kipp_10m_2019_overlay.png')
_IKN24 = os.path.join(_CACHE, 'kipp_10m_2024_overlay.png')


def _md5(path):
    if not os.path.exists(path):
        return "MISSING"
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(8192), b''):
            h.update(blk)
    return h.hexdigest()


def _b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


@st.cache_data(show_spinner=False)
def _load_all(_h1, _h2, _h3, _h4, _h5):
    meta = {}
    if os.path.exists(_META):
        with open(_META) as f:
            meta = json.load(f)
    return (_b64(_KAL19), _b64(_KAL24),
            _b64(_IKN19), _b64(_IKN24), meta)


def render_kipp_swipe_map(split_pct=50, height=620, overlay_opacity=0.78):
    hashes = [_md5(p) for p in [_KAL19, _KAL24, _IKN19, _IKN24, _META]]
    b_kal19, b_kal24, b_ikn19, b_ikn24, meta = _load_all(*hashes)

    if not b_kal19 or not b_kal24:
        st.error("Overlay Kalimantan tidak ditemukan. Jalankan "
                 "`python scripts/build_kalimantan_overlays.py`.")
        return

    KAL_S = meta.get('south', -4.201)
    KAL_N = meta.get('north',  4.408)
    KAL_W = meta.get('west', 108.657)
    KAL_E = meta.get('east', 119.006)
    KAL_CL = (KAL_S + KAL_N) / 2
    KAL_CN = (KAL_W + KAL_E) / 2

    IKN_S, IKN_N = -0.979927, -0.940042
    IKN_W, IKN_E =  116.680061, 116.719946
    IKN_CL = (IKN_S + IKN_N) / 2
    IKN_CN = (IKN_W + IKN_E) / 2

    has_ikn = bool(b_ikn19 and b_ikn24)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
      *{{box-sizing:border-box}}
      html,body{{margin:0;padding:0;height:100%;width:100%;overflow:hidden;
        font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
      #wrap{{position:relative;width:100%;height:100%;background:#0A1612;
        border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.2)}}
      .mv{{position:absolute;top:0;left:0;width:100%;height:100%}}
      #mL{{z-index:1}}
      #mR{{z-index:2;clip-path:inset(0 0 0 {split_pct}%)}}

      /* slider */
      #bar{{position:absolute;top:0;bottom:0;left:{split_pct}%;width:4px;
        background:#fff;box-shadow:0 0 16px rgba(0,0,0,.85);z-index:9999;
        cursor:ew-resize;transform:translateX(-50%)}}
      #handle{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
        width:48px;height:48px;background:#1E482D;border:2.5px solid #fff;
        border-radius:50%;box-shadow:0 4px 16px rgba(0,0,0,.65);
        display:flex;align-items:center;justify-content:center;
        color:#fff;font-size:16px;font-weight:800;user-select:none;cursor:grab;
        transition:background .15s,transform .1s}}
      #handle:hover{{background:#2D6A4F;transform:translate(-50%,-50%) scale(1.1)}}
      #handle:active{{cursor:grabbing;background:#52B788}}

      /* badges */
      .badge{{position:absolute;top:14px;padding:8px 18px;
        background:rgba(14,26,18,.93);backdrop-filter:blur(8px);color:#fff;
        border-radius:22px;font-size:12px;font-weight:700;letter-spacing:.04em;
        z-index:9000;box-shadow:0 3px 12px rgba(0,0,0,.5);
        border:1px solid rgba(255,255,255,.25);pointer-events:none}}
      #bL{{left:14px;border-left:4px solid #52B788}}
      #bR{{right:14px;border-right:4px solid #E63946}}

      /* legend */
      .leg{{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);
        background:rgba(255,255,255,.96);backdrop-filter:blur(10px);
        padding:8px 20px;border-radius:26px;box-shadow:0 4px 20px rgba(0,0,0,.3);
        z-index:9000;display:flex;gap:16px;align-items:center;
        font-size:11px;font-weight:600;color:#1F2937;
        border:1px solid rgba(220,228,216,.8);flex-wrap:wrap;justify-content:center}}
      .li{{display:flex;align-items:center;gap:5px;white-space:nowrap}}
      .ld{{width:10px;height:10px;border-radius:50%;display:inline-block}}

      /* ===== VIEW TOGGLE BUTTONS ===== */
      #view-toggle{{
        position:absolute; top:14px; left:50%; transform:translateX(-50%);
        z-index:9500; display:flex; gap:0;
        border-radius:24px; overflow:hidden;
        box-shadow:0 3px 14px rgba(0,0,0,.45);
        border:1.5px solid rgba(255,255,255,.3);
      }}
      .vt-btn{{
        padding:8px 18px;
        font-size:11.5px; font-weight:700; letter-spacing:.03em;
        border:none; cursor:pointer;
        transition:background .2s,color .2s;
        display:flex; align-items:center; gap:6px;
        white-space:nowrap;
      }}
      .vt-btn.active{{
        background:#1E482D; color:#fff;
        pointer-events:none;
      }}
      .vt-btn:not(.active){{
        background:rgba(255,255,255,.92); color:#1E482D;
      }}
      .vt-btn:not(.active):hover{{
        background:#D8F3DC; color:#1E482D;
      }}
    </style>
    </head>
    <body>
    <div id="wrap">
      <div id="bL" class="badge">2019 — PRA-PERUBAHAN</div>
      <div id="bR" class="badge">2024 — PASCA-PERUBAHAN</div>

      <!-- VIEW TOGGLE -->
      <div id="view-toggle">
        <button class="vt-btn active" id="btn-ikn" onclick="flyIKN()">
          KIPP IKN (Mikro 10m)
        </button>
        <button class="vt-btn" id="btn-kal" onclick="flyKAL()">
          Seluruh Kalimantan (Makro 500m)
        </button>
      </div>

      <div id="mL" class="mv"></div>
      <div id="mR" class="mv"></div>
      <div id="bar"><div id="handle">&lsaquo;&#10073;&rsaquo;</div></div>
      <div class="leg">
        <div class="li"><span class="ld" style="background:#2D6A4F"></span> Hutan</div>
        <div class="li"><span class="ld" style="background:#6E9A2E"></span> Semak / Pertanian</div>
        <div class="li"><span class="ld" style="background:#C6371F"></span> Terbangun</div>
        <div class="li"><span class="ld" style="background:#D97706"></span> Lahan Terbuka / Tambang</div>
        <div class="li"><span class="ld" style="background:#1B5FA8"></span> Air</div>
      </div>
    </div>

    <script>
    (function(){{
      /* ---- BOUNDS ---- */
      var kalBounds = [[{KAL_S},{KAL_W}],[{KAL_N},{KAL_E}]];
      var iknBounds = [[{IKN_S},{IKN_W}],[{IKN_N},{IKN_E}]];
      var hasIkn = {'true' if has_ikn else 'false'};

      /* ---- PRESET VIEWS ---- */
      var VIEW_IKN = {{ center:[{IKN_CL},{IKN_CN}], zoom:13 }};
      var VIEW_KAL = {{ center:[{KAL_CL},{KAL_CN}], zoom:6  }};

      var esri = 'https://server.arcgisonline.com/ArcGIS/rest/services/'
               + 'World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}';

      /* ---- TWO MAPS — default ke IKN ---- */
      var mL = L.map('mL', {{center:VIEW_IKN.center, zoom:VIEW_IKN.zoom,
                             zoomControl:false, attributionControl:false}});
      var mR = L.map('mR', {{center:VIEW_IKN.center, zoom:VIEW_IKN.zoom,
                             zoomControl:false, attributionControl:false}});
      L.tileLayer(esri,{{maxZoom:18}}).addTo(mL);
      L.tileLayer(esri,{{maxZoom:18}}).addTo(mR);
      L.control.zoom({{position:'topleft'}}).addTo(mL);

      var opa = {overlay_opacity};

      /* ---- LAYER MAKRO ---- */
      L.imageOverlay("data:image/png;base64,{b_kal19}",kalBounds,{{opacity:opa}}).addTo(mL);
      L.imageOverlay("data:image/png;base64,{b_kal24}",kalBounds,{{opacity:opa}}).addTo(mR);

      /* ---- LAYER MIKRO ---- */
      if(hasIkn){{
        L.imageOverlay("data:image/png;base64,{b_ikn19}",iknBounds,{{opacity:opa}}).addTo(mL);
        L.imageOverlay("data:image/png;base64,{b_ikn24}",iknBounds,{{opacity:opa}}).addTo(mR);
      }}

      /* ---- SYNC ---- */
      var syncing=false;
      function sync(s,d){{
        s.on('move zoom',function(){{
          if(!syncing){{syncing=true;d.setView(s.getCenter(),s.getZoom(),{{animate:false}});syncing=false}}
        }});
      }}
      sync(mL,mR); sync(mR,mL);

      /* ---- CITY MARKERS ---- */
      var pts=[
        [[-0.960,116.700],"KIPP IKN","Kawasan Inti Pusat Pemerintahan IKN",true],
        [[-1.240,116.852],"Balikpapan","Kota Balikpapan, Kaltim",false],
        [[-0.495,117.146],"Samarinda","Ibukota Provinsi Kaltim",false],
        [[-3.324,114.591],"Banjarmasin","Ibukota Provinsi Kalsel",false],
        [[-0.026,109.343],"Pontianak","Ibukota Provinsi Kalbar",false],
        [[0.135,117.489],"Bontang","Kota Industri LNG, Kaltim",false],
        [[-1.681,116.082],"Penajam","Penajam Paser Utara",false],
        [[1.480,110.350],"Singkawang","Kota Singkawang, Kalbar",false]
      ];
      pts.forEach(function(p){{
        var ik=p[3];
        [mL,mR].forEach(function(m){{
          L.circleMarker(p[0],{{
            radius:ik?9:5, fillColor:ik?"#E63946":"#FFF",
            color:ik?"#FFF":"#1E482D", weight:ik?3:2,
            opacity:1, fillOpacity:.95
          }}).addTo(m).bindPopup('<b>'+p[1]+'</b><br><span style="font-size:11px;color:#555">'+p[2]+'</span>');
        }});
      }});

      /* ======== FLY-TO TOGGLE ======== */
      var btnIkn = document.getElementById('btn-ikn');
      var btnKal = document.getElementById('btn-kal');

      function setActive(btn){{
        btnIkn.classList.remove('active');
        btnKal.classList.remove('active');
        btn.classList.add('active');
      }}

      window.flyIKN = function(){{
        setActive(btnIkn);
        mL.flyTo(VIEW_IKN.center, VIEW_IKN.zoom, {{duration:1.5}});
      }};
      window.flyKAL = function(){{
        setActive(btnKal);
        mL.flyTo(VIEW_KAL.center, VIEW_KAL.zoom, {{duration:1.5}});
      }};

      /* auto-highlight button based on manual zoom */
      mL.on('zoomend',function(){{
        var z=mL.getZoom();
        if(z>=11) setActive(btnIkn);
        else if(z<=8) setActive(btnKal);
      }});

      /* ---- SWIPE ---- */
      var wrap=document.getElementById('wrap');
      var rDiv=document.getElementById('mR');
      var bar=document.getElementById('bar');
      var drag=false;
      function mv(cx){{
        var r=wrap.getBoundingClientRect();
        var pct=Math.min(100,Math.max(0,((cx-r.left)/r.width)*100));
        rDiv.style.clipPath='inset(0 0 0 '+pct.toFixed(2)+'%)';
        bar.style.left=pct.toFixed(2)+'%';
      }}
      bar.addEventListener('mousedown',function(){{drag=true}});
      window.addEventListener('mouseup',function(){{drag=false}});
      window.addEventListener('mousemove',function(e){{if(drag)mv(e.clientX)}});
      bar.addEventListener('touchstart',function(){{drag=true}});
      window.addEventListener('touchend',function(){{drag=false}});
      window.addEventListener('touchmove',function(e){{if(drag&&e.touches.length)mv(e.touches[0].clientX)}});

      setTimeout(function(){{mL.invalidateSize();mR.invalidateSize()}},300);
      window.addEventListener('resize',function(){{mL.invalidateSize();mR.invalidateSize()}});
    }})();
    </script>
    </body>
    </html>
    """

    components.html(html, height=height)
