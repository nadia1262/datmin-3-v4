# dashboard/components/kipp_swipe_map.py
import os
import base64
import streamlit as st
import streamlit.components.v1 as components

@st.cache_data(show_spinner=False)
def load_overlay_base64():
    """Load and base64-encode the 10m classification raster overlays."""
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'cache')
    p19 = os.path.join(cache_dir, 'kipp_10m_2019_overlay.png')
    p24 = os.path.join(cache_dir, 'kipp_10m_2024_overlay.png')
    
    b64_19 = ""
    b64_24 = ""
    
    if os.path.exists(p19):
        with open(p19, 'rb') as f:
            b64_19 = base64.b64encode(f.read()).decode('utf-8')
            
    if os.path.exists(p24):
        with open(p24, 'rb') as f:
            b64_24 = base64.b64encode(f.read()).decode('utf-8')
            
    return b64_19, b64_24

def render_kipp_swipe_map(split_pct=50, height=560, overlay_opacity=0.72):
    """
    Renders an ultra-fast, interactive dual-map swipe comparison of KIPP IKN (2019 vs 2024).
    Uses hardware-accelerated CSS clip-path and synchronized Leaflet instances.
    """
    b64_19, b64_24 = load_overlay_base64()
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            * {{ box-sizing: border-box; }}
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }}
            #swipe-container {{
                position: relative;
                width: 100%;
                height: 100%;
                background: #111B15;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            }}
            .map-view {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }}
            #map-2019 {{
                z-index: 1;
            }}
            #map-2024 {{
                clip-path: inset(0 0 0 {split_pct}%);
                z-index: 2;
            }}
            #slider-bar {{
                position: absolute;
                top: 0;
                bottom: 0;
                left: {split_pct}%;
                width: 4px;
                background: #FFFFFF;
                box-shadow: 0 0 14px rgba(0,0,0,0.8);
                z-index: 9999;
                cursor: ew-resize;
                transform: translateX(-50%);
            }}
            #slider-handle {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 46px;
                height: 46px;
                background: #1E482D;
                border: 2.5px solid #FFFFFF;
                border-radius: 50%;
                box-shadow: 0 4px 14px rgba(0,0,0,0.6);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #FFFFFF;
                font-size: 15px;
                font-weight: 800;
                user-select: none;
                cursor: grab;
                transition: background 0.15s ease, transform 0.1s ease;
            }}
            #slider-handle:hover {{
                background: #2D6A4F;
                transform: translate(-50%, -50%) scale(1.1);
            }}
            #slider-handle:active {{
                cursor: grabbing;
                background: #52B788;
            }}
            .period-badge {{
                position: absolute;
                top: 14px;
                padding: 7px 16px;
                background: rgba(18, 30, 22, 0.92);
                backdrop-filter: blur(8px);
                color: #FFFFFF;
                border-radius: 20px;
                font-size: 11.5px;
                font-weight: 700;
                letter-spacing: 0.05em;
                z-index: 9000;
                box-shadow: 0 3px 10px rgba(0,0,0,0.4);
                border: 1px solid rgba(255,255,255,0.3);
                pointer-events: none;
            }}
            #badge-2019 {{
                left: 14px;
                border-left: 4px solid #52B788;
            }}
            #badge-2024 {{
                right: 14px;
                border-right: 4px solid #E63946;
            }}
            .floating-legend {{
                position: absolute;
                bottom: 14px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(8px);
                padding: 7px 18px;
                border-radius: 24px;
                box-shadow: 0 4px 18px rgba(0,0,0,0.3);
                z-index: 9000;
                display: flex;
                gap: 14px;
                align-items: center;
                font-size: 11px;
                font-weight: 600;
                color: #1F2937;
                border: 1px solid rgba(220, 228, 216, 0.8);
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .legend-dot {{
                width: 10px;
                height: 10px;
                border-radius: 50%;
                display: inline-block;
            }}
            .leaflet-popup-content-wrapper {{
                border-radius: 8px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div id="swipe-container">
            <div id="badge-2019" class="period-badge">2019: RONA AWAL ALAMI (PRA-IKN)</div>
            <div id="badge-2024" class="period-badge">2024: PUNCAK KONSTRUKSI KIPP IKN</div>
            
            <div id="map-2019" class="map-view"></div>
            <div id="map-2024" class="map-view"></div>
            
            <div id="slider-bar">
                <div id="slider-handle">⟨ ❘ ⟩</div>
            </div>

            <div class="floating-legend">
                <div class="legend-item"><span class="legend-dot" style="background:#2D6A4F;"></span> Hutan Alami</div>
                <div class="legend-item"><span class="legend-dot" style="background:#6E9A2E;"></span> Semak / Belukar</div>
                <div class="legend-item"><span class="legend-dot" style="background:#C6371F;"></span> Terbangun (Gedung Tapak)</div>
                <div class="legend-item"><span class="legend-dot" style="background:#D97706;"></span> Tanah Terbuka / Koridor Tol</div>
                <div class="legend-item"><span class="legend-dot" style="background:#1B5FA8;"></span> Air (Bendungan Sepaku)</div>
            </div>
        </div>

        <script>
            const bounds = [[-0.990033, 116.629980], [-0.919965, 116.780089]];
            const center = [-0.955, 116.705];
            const zoom = 13;

            const esriSat = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}';
            const esriAttr = 'Tiles &copy; Esri &mdash; Sentinel-2 10m Classification Overlay';

            // Base Map 2019
            const map1 = L.map('map-2019', {{
                center: center,
                zoom: zoom,
                zoomControl: false,
                attributionControl: false
            }});
            L.tileLayer(esriSat, {{ maxZoom: 18, attribution: esriAttr }}).addTo(map1);
            L.control.zoom({{ position: 'topleft' }}).addTo(map1);

            // Base Map 2024
            const map2 = L.map('map-2024', {{
                center: center,
                zoom: zoom,
                zoomControl: false,
                attributionControl: false
            }});
            L.tileLayer(esriSat, {{ maxZoom: 18, attribution: esriAttr }}).addTo(map2);

            // Add 10m Classification Raster Overlays
            const b64_19 = "{b64_19}";
            const b64_24 = "{b64_24}";

            if (b64_19) {{
                L.imageOverlay("data:image/png;base64," + b64_19, bounds, {{
                    opacity: {overlay_opacity},
                    interactive: false
                }}).addTo(map1);
            }}

            if (b64_24) {{
                L.imageOverlay("data:image/png;base64," + b64_24, bounds, {{
                    opacity: {overlay_opacity},
                    interactive: false
                }}).addTo(map2);
            }}

            // Two-way synchronization
            let isSyncing = false;
            function syncViews(src, target) {{
                src.on('move', function() {{
                    if (!isSyncing) {{
                        isSyncing = true;
                        target.setView(src.getCenter(), src.getZoom(), {{ animate: false }});
                        isSyncing = false;
                    }}
                }});
            }}
            syncViews(map1, map2);
            syncViews(map2, map1);

            // Landmarks
            const landmarks = [
                {{ pos: [-0.965, 116.705], title: "Istana Negara / Sumbu Kebangsaan", desc: "Zona Inti KIPP (Titik Nol IKN)" }},
                {{ pos: [-0.940, 116.755], title: "Bendungan Sepaku Semoi", desc: "Infrastruktur Pasokan Air Baku KIPP" }},
                {{ pos: [-0.985, 116.765], title: "Koridor Tol Akses IKN", desc: "Konektivitas Balikpapan - KIPP (Seksi 3A/3B)" }}
            ];

            landmarks.forEach(lm => {{
                [map1, map2].forEach(m => {{
                    const mk = L.circleMarker(lm.pos, {{
                        radius: 7,
                        fillColor: "#FFFFFF",
                        color: "#1E482D",
                        weight: 2.5,
                        opacity: 1,
                        fillOpacity: 0.95
                    }}).addTo(m);
                    mk.bindPopup(`<strong>${{lm.title}}</strong><br><span style="font-size:11px;color:#555;">${{lm.desc}}</span>`);
                }});
            }});

            // Interactive Drag Divider Handle
            const container = document.getElementById('swipe-container');
            const map2024 = document.getElementById('map-2024');
            const sliderBar = document.getElementById('slider-bar');
            let isDragging = false;

            function updateSlider(xPos) {{
                const rect = container.getBoundingClientRect();
                let ratio = (xPos - rect.left) / rect.width;
                ratio = Math.max(0, Math.min(1, ratio));
                const pct = (ratio * 100).toFixed(2);
                map2024.style.clipPath = `inset(0 0 0 ${{pct}}%)`;
                sliderBar.style.left = `${{pct}}%`;
            }}

            sliderBar.addEventListener('mousedown', () => {{ isDragging = true; }});
            window.addEventListener('mouseup', () => {{ isDragging = false; }});
            window.addEventListener('mousemove', (e) => {{
                if (isDragging) updateSlider(e.clientX);
            }});

            // Touch support for mobile/tablets
            sliderBar.addEventListener('touchstart', () => {{ isDragging = true; }});
            window.addEventListener('touchend', () => {{ isDragging = false; }});
            window.addEventListener('touchmove', (e) => {{
                if (isDragging && e.touches.length > 0) updateSlider(e.touches[0].clientX);
            }});

            // Force initial tile sizing calculation after render
            setTimeout(() => {{
                map1.invalidateSize();
                map2.invalidateSize();
            }}, 250);

            window.addEventListener('resize', () => {{
                map1.invalidateSize();
                map2.invalidateSize();
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)
