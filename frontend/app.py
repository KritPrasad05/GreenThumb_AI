"""
GreenThumb AI — Streamlit Frontend v3
Clean chat interface: fixed input bar at bottom, results scroll above.
Camera activates only on user click. No persistent camera widget.
"""
"""
GreenThumb AI — Streamlit Frontend v4
Fixed: st variable shadowing bug, clean chat render, camera on-demand only.
"""

import streamlit as st
import requests
import base64
import io
from PIL import Image

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="GreenThumb AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --forest: #1a2e1a; --moss: #2d4a2d; --sage: #4a7c59;
    --mint: #7ab892; --cream: #f4f0e6; --parch: #ede6d6;
    --amber: #c8962a; --rust: #b85c38; --blue: #2a6abf;
    --text: #1a1a14; --muted: #6a7a6a; --border: #d4dfd4;
}
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--cream) !important; color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Topbar ── */
.topbar {
    background: var(--forest); padding: 14px 36px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 999;
    border-bottom: 1px solid rgba(122,184,146,0.2);
}
.brand { font-family:'Playfair Display',serif; font-size:20px; color:var(--cream); display:flex; align-items:center; gap:8px; }
.brand em { color:var(--mint); font-style:italic; }
.pills { display:flex; gap:14px; }
.pill { font-size:11px; font-weight:500; padding:4px 12px; border-radius:20px; display:flex; align-items:center; gap:5px; }
.pill-on  { background:rgba(76,175,80,0.15);  color:#81c784; border:1px solid rgba(76,175,80,0.3); }
.pill-off { background:rgba(239,83,80,0.15);  color:#ef9a9a; border:1px solid rgba(239,83,80,0.3); }
.pill-warn{ background:rgba(200,150,42,0.15); color:#ffd54f; border:1px solid rgba(200,150,42,0.3); }

/* ── Hero ── */
.hero {
    background: linear-gradient(145deg, var(--forest) 0%, #2a4a32 100%);
    padding: 44px 40px 52px; position:relative; overflow:hidden;
}
.hero::after { content:'🌿'; position:absolute; right:48px; top:50%; transform:translateY(-50%); font-size:120px; opacity:0.06; pointer-events:none; }
.hero-eye { font-size:10px; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:var(--mint); margin-bottom:10px; }
.hero-h1 { font-family:'Playfair Display',serif; font-size:clamp(28px,3.5vw,46px); color:var(--cream); line-height:1.15; margin:0 0 12px; max-width:560px; }
.hero-h1 em { color:var(--mint); font-style:italic; }
.hero-p { font-size:14px; font-weight:300; color:rgba(245,240,232,0.65); max-width:460px; line-height:1.7; margin:0; }

/* ── Chat area ── */
.chat-area { max-width:820px; margin:0 auto; padding:28px 20px 200px; }

/* ── Bubbles ── */
.bubble-bot {
    background:white; border:1px solid var(--border);
    border-radius:16px 16px 16px 4px; padding:16px 20px; margin-bottom:14px;
    font-size:14px; color:var(--muted); line-height:1.65; max-width:480px;
}
.bubble-user {
    background:var(--forest); border-radius:16px 16px 4px 16px;
    padding:12px 18px; margin-bottom:14px; font-size:14px; color:var(--cream);
    max-width:360px; margin-left:auto; display:flex; align-items:center; gap:10px;
}
.bubble-user img { width:48px; height:48px; object-fit:cover; border-radius:7px; flex-shrink:0; }

/* ── Diagnosis card ── */
.card { background:white; border:1px solid var(--border); border-radius:16px; overflow:hidden; margin-bottom:14px; }
.card-head { padding:20px 24px 16px; }
.badge { font-size:10px; font-weight:500; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.badge-a { color:#2d7a4a; } .badge-r { color:var(--rust); } .badge-h { color:var(--blue); }
.card-title { font-family:'Playfair Display',serif; font-size:22px; font-weight:600; color:var(--forest); }
.card-sub { font-size:13px; color:var(--muted); margin-top:4px; }
.tag-p { display:inline-block; background:var(--forest); color:var(--mint); font-size:11px; font-style:italic; padding:3px 12px; border-radius:20px; margin-top:8px; }
.tag-e { display:inline-block; background:#eef4ee; color:var(--sage); font-size:11px; font-weight:500; padding:3px 10px; border-radius:6px; margin-top:4px; margin-left:6px; }

/* ── Score strip ── */
.score-strip { display:flex; gap:8px; flex-wrap:wrap; padding:14px 24px; background:#f8fbf8; border-top:1px solid #eef4ee; }
.chip { flex:1; min-width:80px; background:white; border:1px solid var(--border); border-radius:10px; padding:10px 12px; text-align:center; }
.chip-val { font-family:'Playfair Display',serif; font-size:20px; font-weight:600; }
.chip-lbl { font-size:10px; text-transform:uppercase; letter-spacing:1px; color:var(--muted); margin-top:2px; }
.cg { color:#2d7a4a; } .ca { color:var(--amber); } .cr { color:var(--rust); }

/* ── Evidence ── */
.ev-section { padding:18px 24px; }
.ev-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:14px; }
.ev-card { background:var(--cream); border-radius:10px; padding:13px 15px; border:1px solid #dde8dd; }
.ev-icon { font-size:15px; margin-bottom:5px; }
.ev-ttl { font-size:10px; font-weight:500; text-transform:uppercase; letter-spacing:1.5px; color:var(--sage); margin-bottom:5px; }
.ev-txt { font-size:13px; line-height:1.6; color:#3d4a3d; }

/* ── Reasoning ── */
.rea { background:var(--parch); border-left:3px solid var(--amber); border-radius:0 8px 8px 0; padding:13px 17px; font-size:13px; line-height:1.75; color:#4a3a1a; font-style:italic; }
.rea-lbl { font-size:10px; font-weight:500; text-transform:uppercase; letter-spacing:1.5px; color:var(--amber); font-style:normal; margin-bottom:7px; }

/* ── Top-3 ── */
.top3 { padding:14px 24px; border-top:1px solid #eef4ee; background:#f8fbf8; }
.top3-ttl { font-size:10px; font-weight:500; text-transform:uppercase; letter-spacing:1.5px; color:var(--muted); margin-bottom:10px; }
.bar-row { margin-bottom:8px; }
.bar-lbl { font-size:12px; color:var(--text); margin-bottom:3px; }
.bar-track { background:#e0e8e0; border-radius:4px; height:6px; overflow:hidden; }
.bar-fill { height:100%; border-radius:4px; }

/* ── Suggestion ── */
.sugg { font-size:13px; color:#5a4a3a; padding:7px 0; border-bottom:1px solid #f0e8e0; }
.sugg:last-child { border:none; }

/* ── Fixed input bar ── */
.input-wrap {
    position:fixed; bottom:0; left:0; right:0; z-index:998;
    background:white; border-top:1px solid var(--border);
    box-shadow:0 -6px 28px rgba(26,46,26,0.09);
    padding:14px 24px 18px;
}
.input-inner { max-width:820px; margin:0 auto; }
.input-hint { font-size:12px; color:var(--muted); text-align:center; margin-bottom:10px; }

/* Widget overrides */
.stFileUploader > div { background:white !important; border:1.5px solid var(--border) !important; border-radius:12px !important; padding:8px 14px !important; min-height:44px !important; }
.stFileUploader label { display:none !important; }
.stButton > button {
    background:var(--forest) !important; color:var(--cream) !important;
    border:none !important; border-radius:12px !important;
    padding:0 20px !important; height:48px !important;
    font-size:14px !important; font-weight:500 !important;
    font-family:'DM Sans',sans-serif !important; width:100% !important;
}
.stButton > button:hover { background:var(--moss) !important; }
.stSpinner > div { border-top-color:var(--sage) !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=10)
def check_health():
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None

def call_api(img_bytes: bytes, fname: str) -> dict:
    resp = requests.post(
        f"{API_URL}/diagnose",
        files={"file": (fname, img_bytes, "image/jpeg")},
        timeout=180
    )
    resp.raise_for_status()
    return resp.json()

def conf_color(val: float) -> str:
    if val >= 0.80: return "cg"
    if val >= 0.60: return "ca"
    return "cr"

def parse_label(cls: str) -> str:
    parts = cls.split("___")
    if len(parts) == 2:
        return f"{parts[0].replace('_',' ')} — {parts[1].replace('_',' ')}"
    return cls.replace("_", " ")

def bar_html(label: str, val: float, color: str = "#4a7c59") -> str:
    pct = int(val * 100)
    return (
        f'<div class="bar-row">'
        f'<div class="bar-lbl">{label} <strong style="color:{color}">{pct}%</strong></div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{color};"></div></div>'
        f'</div>'
    )

def render_result(result: dict):
    """Render one diagnosis result card. Uses only local variables — no st shadowing."""
    status = result.get("status", "UNKNOWN")

    # ── HEALTHY ──────────────────────────────────────────────────────────────
    if status == "HEALTHY":
        crop    = result.get("crop", "")
        cvc     = result.get("cv_confidence", 0)
        message = result.get("message", "")
        cc      = conf_color(cvc)
        st.markdown(f"""
        <div class="card">
          <div class="card-head">
            <div class="badge badge-h">✅ Healthy Plant</div>
            <div class="card-title">{crop} — Healthy</div>
            <div class="card-sub">{message}</div>
          </div>
          <div class="score-strip">
            <div class="chip">
              <div class="chip-val {cc}">{cvc:.0%}</div>
              <div class="chip-lbl">CV Confidence</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── ACCEPTED ─────────────────────────────────────────────────────────────
    elif status == "ACCEPTED":
        disease  = result.get("disease", "Unknown")
        crop     = result.get("crop", "")
        pathogen = result.get("pathogen", "")
        eppo     = result.get("eppo_code", "")
        cvc      = result.get("cv_confidence", 0)
        score    = result.get("consistency_score", 0)
        comp     = result.get("component_scores", {})
        evidence = result.get("supporting_evidence", {})
        reasoning= result.get("llm_reasoning", "")
        top3     = result.get("top3_predictions", [])

        lm = comp.get("label_match", 0)
        es = comp.get("evidence_strength", 0)

        # Evidence grid
        symp  = evidence.get("symptoms",   "—")
        caus  = evidence.get("causes",     "—")
        treat = evidence.get("treatment",  "—")
        prev  = evidence.get("prevention", "—")

        ev_html = f"""
        <div class="ev-grid">
          <div class="ev-card"><div class="ev-icon">🔬</div><div class="ev-ttl">Symptoms</div><div class="ev-txt">{symp}</div></div>
          <div class="ev-card"><div class="ev-icon">🧫</div><div class="ev-ttl">Causes</div><div class="ev-txt">{caus}</div></div>
          <div class="ev-card"><div class="ev-icon">💊</div><div class="ev-ttl">Treatment</div><div class="ev-txt">{treat}</div></div>
          <div class="ev-card"><div class="ev-icon">🛡️</div><div class="ev-ttl">Prevention</div><div class="ev-txt">{prev}</div></div>
        </div>"""

        rea_html = ""
        if reasoning:
            rea_html = f'<div class="rea"><div class="rea-lbl">🤖 LLM Reasoning</div>{reasoning}</div>'

        top3_html = ""
        if top3:
            bars = "".join(bar_html(parse_label(p["class"]), p["confidence"]) for p in top3)
            top3_html = f'<div class="top3"><div class="top3-ttl">Top-3 CV Predictions</div>{bars}</div>'

        st.markdown(f"""
        <div class="card">
          <div class="card-head">
            <div class="badge badge-a">✦ Diagnosis Accepted</div>
            <div class="card-title">{disease}</div>
            <div class="card-sub">Crop: <strong>{crop}</strong></div>
            <span class="tag-p">{pathogen}</span>
            <span class="tag-e">EPPO: {eppo}</span>
          </div>
          <div class="score-strip">
            <div class="chip"><div class="chip-val {conf_color(cvc)}">{cvc:.0%}</div><div class="chip-lbl">CV Confidence</div></div>
            <div class="chip"><div class="chip-val {conf_color(score)}">{score:.2f}</div><div class="chip-lbl">Consistency</div></div>
            <div class="chip"><div class="chip-val {conf_color(lm)}">{lm:.2f}</div><div class="chip-lbl">Label Match</div></div>
            <div class="chip"><div class="chip-val {conf_color(es)}">{es:.2f}</div><div class="chip-lbl">Evidence</div></div>
          </div>
          <div class="ev-section">{ev_html}{rea_html}</div>
          {top3_html}
        </div>
        """, unsafe_allow_html=True)

    # ── REFUSED ──────────────────────────────────────────────────────────────
    elif status == "REFUSED":
        pred     = result.get("pred_disease", "")
        crop     = result.get("crop", "")
        cvc      = result.get("cv_confidence", 0)
        score    = result.get("consistency_score", 0)
        reasoning= result.get("llm_reasoning", "")
        matches  = result.get("possible_matches", [])
        suggs    = result.get("suggestions", [])
        top3     = result.get("top3_predictions", [])

        rea_html = ""
        if reasoning:
            rea_html = f'<div class="rea" style="border-color:var(--rust)"><div class="rea-lbl" style="color:var(--rust)">🤖 LLM Analysis</div>{reasoning}</div>'

        mat_html = ""
        if matches:
            bars = "".join(bar_html(m.get("disease",""), m.get("similarity",0), "#b85c38") for m in matches)
            mat_html = f'<div style="margin-top:14px"><div class="top3-ttl">Closest knowledge base matches</div>{bars}</div>'

        sug_html = ""
        if suggs:
            items = "".join(f'<div class="sugg">→ {s}</div>' for s in suggs)
            sug_html = f'<div style="margin-top:14px">{items}</div>'

        top3_html = ""
        if top3:
            bars = "".join(bar_html(parse_label(p["class"]), p["confidence"]) for p in top3)
            top3_html = f'<div class="top3"><div class="top3-ttl">Top-3 CV Predictions</div>{bars}</div>'

        st.markdown(f"""
        <div class="card">
          <div class="card-head">
            <div class="badge badge-r">⚠ Prediction Refused</div>
            <div class="card-title">Diagnosis Inconclusive</div>
            <div class="card-sub">
              CV predicted <strong>{pred}</strong> on <strong>{crop}</strong>
              ({cvc:.0%} confidence) — consistency score
              <strong style="color:var(--rust)">{score:.2f}</strong> below threshold 0.70
            </div>
          </div>
          <div class="ev-section">{rea_html}{mat_html}{sug_html}</div>
          {top3_html}
        </div>
        """, unsafe_allow_html=True)

    # ── CV_ONLY fallback ──────────────────────────────────────────────────────
    else:
        st.markdown(f"""
        <div class="bubble-bot">
          ⚠ Partial result — {result.get("message","")}
          <br><br>CV predicted: <strong>{result.get("disease","")}</strong>
          on <strong>{result.get("crop","")}</strong>
          ({result.get("cv_confidence",0):.0%} confidence)
        </div>
        """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────

if "messages"    not in st.session_state: st.session_state.messages    = []
if "show_camera" not in st.session_state: st.session_state.show_camera = False

# ── Health check ──────────────────────────────────────────────────────────────

health    = check_health()
api_ok    = health is not None
ollama_ok = health.get("ollama",    False) if health else False
cv_ok     = health.get("cv_model",  False) if health else False

# ── Top nav ───────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="topbar">
  <div class="brand">🌿 GreenThumb <em>AI</em></div>
  <div class="pills">
    <div class="pill {'pill-on' if api_ok    else 'pill-off'}">{"●" if api_ok    else "○"} API</div>
    <div class="pill {'pill-on' if cv_ok     else 'pill-warn'}">{"●" if cv_ok    else "○"} CV Model</div>
    <div class="pill {'pill-on' if ollama_ok else 'pill-off'}">{"●" if ollama_ok else "○"} LLM</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
  <div class="hero-eye">AI · Plant Pathology · Knowledge-Verified</div>
  <h1 class="hero-h1">Detect plant disease<br>with <em>verified</em> intelligence</h1>
  <p class="hero-p">Upload a leaf photo or take one with your camera.
  EfficientNet-B0 classifies the disease, then our RAG system cross-checks
  against scientific knowledge before delivering an evidence-backed diagnosis.</p>
</div>
""", unsafe_allow_html=True)

# ── Chat area ─────────────────────────────────────────────────────────────────

st.markdown('<div class="chat-area">', unsafe_allow_html=True)

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    <div class="bubble-bot">
      👋 Hello! I'm <strong>GreenThumb AI</strong>.<br><br>
      Use the input bar at the bottom to <strong>upload a leaf photo</strong>
      or <strong>take one with your camera</strong>. I'll classify the disease
      using computer vision and verify the diagnosis against a scientific
      knowledge base before giving you a full report.
    </div>
    """, unsafe_allow_html=True)

# Render conversation history
for msg in st.session_state.messages:
    msg_type = msg["type"]

    if msg_type == "user_image":
        st.markdown(f"""
        <div class="bubble-user">
          <img src="data:image/jpeg;base64,{msg['b64']}">
          <div>
            <div style="font-size:11px;opacity:0.6;margin-bottom:2px;">Leaf uploaded</div>
            <div style="font-size:13px;">{msg['name']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    elif msg_type == "result":
        render_result(msg["data"])

    elif msg_type == "error":
        st.markdown(f"""
        <div class="bubble-bot" style="border-color:#e8c8c8;background:#fdf0f0;color:#7a2020;">
          ❌ {msg['text']}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Fixed bottom input bar ────────────────────────────────────────────────────

st.markdown('<div class="input-wrap"><div class="input-inner">', unsafe_allow_html=True)
st.markdown('<div class="input-hint">📷 Take a photo or 📁 upload a leaf image to begin</div>', unsafe_allow_html=True)

col_file, col_cam_btn, col_send = st.columns([4, 2, 1.5])

with col_file:
    uploaded = st.file_uploader(
        "Upload leaf image",
        type=["jpg","jpeg","png","webp"],
        label_visibility="collapsed",
        key="uploader"
    )

with col_cam_btn:
    cam_label = "📷 Close camera" if st.session_state.show_camera else "📷 Use camera"
    if st.button(cam_label, key="cam_toggle", use_container_width=True):
        st.session_state.show_camera = not st.session_state.show_camera
        st.rerun()

with col_send:
    send_btn = st.button("🔬 Analyse", key="analyse", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Camera widget — only shown when toggled on
cam_capture = None
if st.session_state.show_camera:
    cam_capture = st.camera_input(
        "Point camera at the leaf and capture",
        label_visibility="visible",
        key="cam_input"
    )

# ── Determine active image ────────────────────────────────────────────────────

active_bytes = None
active_name  = None

if uploaded:
    active_bytes = uploaded.read()
    active_name  = uploaded.name
elif cam_capture:
    active_bytes = cam_capture.read()
    active_name  = "camera_capture.jpg"
    st.session_state.show_camera = False   # auto-close after capture

# ── Run analysis on button click ──────────────────────────────────────────────

if send_btn:
    if not active_bytes:
        st.warning("Please upload or capture a leaf image first.", icon="🌱")
    else:
        # Add user bubble with thumbnail
        b64_str = base64.b64encode(active_bytes).decode()
        st.session_state.messages.append({
            "type": "user_image",
            "b64":  b64_str,
            "name": active_name
        })

        # Call API and add result
        with st.spinner("Running CV → RAG → LLM pipeline..."):
            try:
                result = call_api(active_bytes, active_name)
                st.session_state.messages.append({"type": "result", "data": result})
            except requests.exceptions.ConnectionError:
                st.session_state.messages.append({
                    "type": "error",
                    "text": "Lost connection to backend. Is FastAPI still running on port 8000?"
                })
            except Exception as exc:
                st.session_state.messages.append({
                    "type": "error",
                    "text": f"Unexpected error: {exc}"
                })

        st.rerun()