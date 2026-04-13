import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import random
import base64
from pathlib import Path
from textwrap import dedent

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="BlueHorizon · Sustainable Finance",
    page_icon="🌊",
    layout="wide",
)

# ══════════════════════════════════════════════════════════
# LOGO — text only (replace with <img> once static folder ready)
# ══════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).parent
LOGO_DIR = BASE_DIR / "static" / "logos"
APP_ICON_PATH = LOGO_DIR / "app-icon.png"
HERO_LOGO_PATH = LOGO_DIR / "hero-logo.png"
MICRO_ICON_PATH = LOGO_DIR / "micro-icon.png"

@st.cache_data
def image_data_uri(path_str):
    path = Path(path_str)
    if not path.exists():
        return None
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

def logo_html(size=56):
    asset_path = MICRO_ICON_PATH if size <= 48 and MICRO_ICON_PATH.exists() else APP_ICON_PATH
    data_uri = image_data_uri(str(asset_path)) if asset_path.exists() else None
    if data_uri:
        return f"""
<img src="{data_uri}" alt="BlueHorizon logo" style="
    width:{size}px;height:{size}px;object-fit:contain;display:block;flex-shrink:0;
">"""
    font = max(14, size // 3)
    return f"""
<div style="
    width:{size}px;height:{size}px;border-radius:50%;
    background:linear-gradient(135deg,#042C53,#185FA5);
    display:inline-flex;align-items:center;justify-content:center;
    font-family:'Inter',sans-serif;font-weight:700;font-size:{font}px;
    color:#F8FBFF;letter-spacing:1px;flex-shrink:0;
">BH</div>"""

def hero_logo_html(width=280):
    data_uri = image_data_uri(str(HERO_LOGO_PATH)) if HERO_LOGO_PATH.exists() else None
    if data_uri:
        return f"""
<img src="{data_uri}" alt="BlueHorizon hero logo" style="
    width:{width}px;max-width:100%;height:auto;display:block;object-fit:contain;
    filter:drop-shadow(0 14px 28px rgba(4,44,83,0.18));
">"""
    return logo_html(max(72, width // 4))

# ══════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600&display=swap');

:root {
    --bh-deep:  #042C53;
    --bh-navy:  #0C447C;
    --bh-ocean: #185FA5;
    --bh-mid:   #378ADD;
    --bh-sky:   #85B7EB;
    --bh-mist:  #B5D4F4;
    --bh-foam:  #E6F1FB;
    --bh-white: #F8FBFF;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(160deg, var(--bh-foam) 0%, #F0F7FF 60%, #EAF3FB 100%);
}
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; }

h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.6rem !important; font-weight: 600 !important;
    color: var(--bh-deep) !important; letter-spacing: -0.5px;
    margin-bottom: 0.25rem !important;
}
h2 {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.35rem !important; font-weight: 600 !important;
    color: var(--bh-navy) !important;
    border-bottom: 2px solid var(--bh-mist); padding-bottom: 0.4rem;
    margin-top: 1.6rem !important;
}
h3 {
    font-family: 'Inter', sans-serif !important; font-size: 1.05rem !important;
    font-weight: 600 !important; color: var(--bh-ocean) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent; border-bottom: 2px solid var(--bh-mist); gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif; font-size: 0.85rem; font-weight: 500;
    color: var(--bh-ocean); padding: 0.6rem 1.2rem;
    border-bottom: 3px solid transparent; background: transparent !important; transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    color: var(--bh-deep) !important;
    border-bottom: 3px solid var(--bh-ocean) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--bh-deep); background: var(--bh-foam) !important; border-radius: 6px 6px 0 0;
}

/* Minimal navigation */
[data-testid="stSegmentedControl"] {
    margin: 0 0 1.35rem 0;
}
[data-testid="stSegmentedControl"] > div {
    background: transparent;
    border: none;
    box-shadow: none;
    gap: 1.6rem;
    padding: 0;
}
[data-testid="stSegmentedControl"] button {
    border: none !important;
    background: transparent !important;
    border-radius: 0 !important;
    padding: 0.1rem 0.05rem 0.35rem !important;
    min-height: 2.2rem !important;
    color: rgba(12, 68, 124, 0.72) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transition: color 0.2s ease, transform 0.2s ease !important;
}
[data-testid="stSegmentedControl"] button:hover {
    color: var(--bh-deep) !important;
    transform: translateY(-1px);
}
[data-testid="stSegmentedControl"] button[aria-selected="true"] {
    color: var(--bh-deep) !important;
    border-bottom: 2px solid transparent !important;
    border-image: linear-gradient(90deg, #7CC6E8 0%, #378ADD 45%, #0C447C 100%) 1 !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.9rem;
    background: linear-gradient(135deg, var(--bh-ocean), var(--bh-navy));
    color: #ffffff; border: none; border-radius: 12px; padding: 0.7rem 1.45rem;
    transition: all 0.22s; box-shadow: 0 10px 24px rgba(24,95,165,0.18);
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--bh-navy), var(--bh-deep));
    box-shadow: 0 14px 28px rgba(24,95,165,0.24); transform: translateY(-1px);
}
.stButton > button:active { transform: translateY(0); }

/* ── Alerts ── */
.stAlert {
    border-radius: 10px !important; border-left: 4px solid var(--bh-ocean) !important;
    background: var(--bh-foam) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #ffffff; border: 1.5px solid var(--bh-mist); border-radius: 12px;
    padding: 1rem 1.25rem !important; box-shadow: 0 2px 10px rgba(55,138,221,0.08);
}
[data-testid="metric-container"] label {
    color: var(--bh-ocean) !important; font-size: 0.78rem !important;
    text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif; font-size: 1.8rem !important;
    color: var(--bh-deep) !important; font-weight: 600;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px; overflow: hidden; border: 1.5px solid var(--bh-mist) !important;
}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--bh-ocean) !important; border-color: var(--bh-ocean) !important;
}

/* ── Selectbox ── */
.stSelectbox [data-baseweb="select"] > div:first-child {
    border-color: var(--bh-mist) !important; border-radius: 8px !important;
    background: #ffffff !important;
}
.stSelectbox [data-baseweb="select"] > div:first-child:focus-within {
    border-color: var(--bh-ocean) !important;
    box-shadow: 0 0 0 3px rgba(24,95,165,0.15) !important;
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input {
    border-radius: 8px !important; border-color: var(--bh-mist) !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: var(--bh-ocean) !important;
    box-shadow: 0 0 0 3px rgba(24,95,165,0.15) !important;
}

/* ── Checkboxes ── */
.stCheckbox label { color: var(--bh-navy) !important; }

/* ── Captions ── */
.stCaption {
    color: var(--bh-sky) !important; font-size: 0.78rem !important;
    text-align: center; border-top: 1px solid var(--bh-foam);
    padding-top: 0.75rem; margin-top: 2rem;
}

/* ── Fact pill ── */
.fact-pill {
    display: inline-block;
    background: linear-gradient(135deg, rgba(4,44,83,0.96), rgba(24,95,165,0.92));
    color: #D9EDFF; font-size: 0.8rem; border-radius: 999px;
    padding: 0.55rem 1rem; margin: 0.5rem 0;
    box-shadow: 0 10px 24px rgba(4,44,83,0.12);
}

/* ── Auto-scrolling review carousel ── */
.carousel-outer {
    overflow: hidden;
    width: 100%;
    position: relative;
    padding: 0.5rem 0 1rem;
    mask-image: linear-gradient(to right, transparent 0%, black 8%, black 92%, transparent 100%);
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 8%, black 92%, transparent 100%);
}
.carousel-track {
    display: flex;
    gap: 1.25rem;
    width: max-content;
    animation: scroll-left 32s linear infinite;
}
@keyframes scroll-left {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.review-card {
    width: 320px; flex-shrink: 0;
    background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(248,251,255,0.92));
    border: 1px solid rgba(181,212,244,0.9); border-radius: 18px;
    padding: 1.15rem 1.15rem 0.95rem;
    box-shadow: 0 16px 34px rgba(55,138,221,0.08);
}

/* ── T&C / Quiz overlay ── */
.overlay-backdrop {
    position: fixed; inset: 0;
    background: rgba(4,44,83,0.72);
    backdrop-filter: blur(4px);
    z-index: 8000;
}
.overlay-box {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: #ffffff;
    border-radius: 16px;
    padding: 2rem 2.25rem 1.75rem;
    width: min(680px, 94vw);
    max-height: 88vh;
    overflow-y: auto;
    z-index: 8001;
    box-shadow: 0 24px 64px rgba(4,44,83,0.28);
}
.overlay-box::-webkit-scrollbar { width: 4px; }
.overlay-box::-webkit-scrollbar-thumb { background: #B5D4F4; border-radius: 4px; }

/* ── Toggle switch ── */
.tc-toggle-row {
    display: flex; align-items: center; gap: 0.75rem; margin-top: 1.25rem;
}
.toggle-label {
    font-size: 0.88rem; color: #042C53; font-weight: 500;
}

/* ── Profile result card ── */
.result-card {
    background: #ffffff; border: 1.5px solid #B5D4F4; border-radius: 14px;
    padding: 1.5rem 1.5rem 1.25rem;
    box-shadow: 0 2px 12px rgba(55,138,221,0.09);
    margin-top: 1.5rem;
}
.soft-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248,251,255,0.88));
    border: 1px solid rgba(181,212,244,0.9);
    border-radius: 18px;
    padding: 1.15rem 1.25rem;
    box-shadow: 0 14px 30px rgba(55,138,221,0.08);
}
.soft-card h4 {
    margin: 0 0 0.45rem;
    color: var(--bh-deep);
    font-size: 1rem;
    font-weight: 700;
}
.soft-card p {
    margin: 0;
    color: var(--bh-ocean);
    font-size: 0.86rem;
    line-height: 1.65;
}
.profile-banner {
    background: linear-gradient(135deg, rgba(4,44,83,0.98), rgba(24,95,165,0.95));
    border-radius: 16px;
    padding: 1.15rem 1.35rem;
    margin-bottom: 1.25rem;
    color: #F8FBFF;
    box-shadow: 0 18px 36px rgba(4,44,83,0.16);
}
.profile-banner .eyebrow {
    color: #B5D4F4;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 0.45rem;
}
.profile-banner .body {
    color: #F8FBFF;
    font-size: 0.98rem;
    line-height: 1.7;
}
.empty-state {
    background: linear-gradient(180deg, rgba(230,241,251,0.92), rgba(240,247,255,0.85));
    border: 1px solid rgba(181,212,244,0.95);
    border-radius: 18px;
    padding: 1.15rem 1.25rem;
    color: var(--bh-ocean);
    box-shadow: 0 12px 24px rgba(55,138,221,0.06);
}
.choice-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
    margin-bottom: 0.8rem;
}
.choice-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.97), rgba(248,251,255,0.9));
    border: 1px solid rgba(181,212,244,0.9);
    border-radius: 18px;
    padding: 1.15rem 1.2rem;
    box-shadow: 0 14px 28px rgba(55,138,221,0.06);
}
.choice-card .title {
    margin: 0 0 0.38rem;
    color: var(--bh-deep);
    font-size: 1rem;
    font-weight: 700;
}
.choice-card .copy {
    margin: 0;
    color: var(--bh-ocean);
    font-size: 0.84rem;
    line-height: 1.65;
}
.excluded-chip {
    display: inline-block;
    padding: 0.32rem 0.72rem;
    border-radius: 999px;
    margin: 0.2rem 0.35rem 0 0;
    background: rgba(55,138,221,0.10);
    border: 1px solid rgba(55,138,221,0.18);
    color: #2B74B0;
    font-size: 0.78rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════
ASSETS = {
    "Vestas Wind Systems":      {"ret": 7.5,  "sd": 18.0, "esg": 8.9, "sector": "Renewables",  "tags": []},
    "NextEra Energy":           {"ret": 9.2,  "sd": 15.0, "esg": 8.1, "sector": "Clean Energy", "tags": []},
    "TSMC":                     {"ret": 14.0, "sd": 24.0, "esg": 5.4, "sector": "Technology",   "tags": []},
    "Johnson & Johnson":        {"ret": 6.0,  "sd": 12.0, "esg": 6.8, "sector": "Healthcare",   "tags": []},
    "Shell PLC":                {"ret": 11.0, "sd": 22.0, "esg": 3.2, "sector": "Oil & Gas",    "tags": ["fossil"]},
    "British American Tobacco": {"ret": 8.5,  "sd": 16.0, "esg": 2.5, "sector": "Tobacco",     "tags": ["tobacco"]},
    "Lockheed Martin":          {"ret": 10.5, "sd": 19.0, "esg": 3.8, "sector": "Defence",      "tags": ["defence"]},
}
ASSET_NAMES = list(ASSETS.keys())

EXCLUSIONS = [
    ("tobacco", "Tobacco companies"),
    ("defence", "Defence companies"),
    ("fossil",  "Fossil fuel companies"),
    ("gambling","Gambling companies"),
    ("alcohol", "Alcohol companies"),
]

QUIZ_QUESTIONS = [
    "I prefer safe, predictable investments over risky ones.",
    "Large swings in my portfolio value make me uncomfortable.",
    "I would accept lower returns to avoid uncertainty.",
    "I would rather keep my money in cash than risk losing it in the market.",
    "Losing 10% of my portfolio in a month would cause me significant stress.",
    "I prioritise protecting my capital over maximising long-term growth.",
    "I feel nervous when markets are volatile, even if I know it's temporary.",
]

LIKERT_SCORE = {"Strongly Agree": 5, "Agree": 4, "Neutral": 3, "Disagree": 2, "Strongly Disagree": 1}
SLIDER_MAP   = {1: "Strongly Disagree", 2: "Disagree", 3: "Neutral", 4: "Agree", 5: "Strongly Agree"}
SLIDER_SCORE = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}   # slider 5 = Strongly Agree (score 5), slider 1 = Strongly Disagree (score 1)

REVIEWS = [
    {"name": "Luca",     "role": "Rising employee, BlueHorizon",
     "text": "BlueHorizon changed how I think about money and my own app. I used to assume 'green' meant lower returns — the efficient frontier proof here blew my mind.",
     "stars": 5},
    {"name": "Octavian", "role": "Professor in Green Washing",
     "text": "The ESG-adjusted portfolio optimisation is exactly what I needed for my paper. Clean, rigorous, and actually fun to use.",
     "stars": 5},
    {"name": "Steph",    "role": "Sustainable finance analyst",
     "text": "Finally a tool that doesn't treat ESG as a checkbox. The Sharpe vs ESG trade-off chart is something I now show to clients regularly.",
     "stars": 5},
    {"name": "Marcele",  "role": "Independent investor",
     "text": "I had no idea where to start with ethical investing. BlueHorizon walked me through everything from risk appetite to portfolio weights.",
     "stars": 5},
    {"name": "Priya",    "role": "Portfolio analyst",
     "text": "Incredibly intuitive. I completed the quiz in under 3 minutes and had a personalised allocation I actually trust.",
     "stars": 5},
    {"name": "Tom",      "role": "Undergraduate Economics",
     "text": "Used this for my final-year project. The no-short-selling constraint makes the outputs so much more realistic than textbook models.",
     "stars": 5},
]

OCEAN_FACTS = [
    "🌊 The ocean covers 71% of Earth's surface and regulates our entire climate — protecting it is protecting our economy.",
    "🐋 Whales sequester carbon equivalent to thousands of trees each — blue finance is carbon finance.",
    "🌿 ESG-labelled bond issuance hit over $900 billion globally in 2023 — green investing is no longer niche.",
    "☀️ Renewable energy now accounts for over 30% of global electricity generation — up from 22% in 2015.",
    "🦈 Ocean economies generate $2.5 trillion annually — sustainable ocean finance is the next frontier.",
    "📈 ESG funds have outperformed traditional benchmarks in 7 of the last 10 years.",
    "🌍 Over $35 trillion is now managed under ESG principles worldwide — a 15× increase since 2004.",
    "💧 Water scarcity affects 40% of the global population — blue bonds are financing solutions.",
    "🌱 Companies with high ESG scores have on average 14% lower cost of capital than low-ESG peers.",
    "🐠 Coral reefs support 25% of all marine life and $375 billion in economic value — at risk without green finance.",
]

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
TAB_LABELS = ["Home", "Portfolio", "Charts"]

defaults = {
    "app_loaded":       False,
    "tc_accepted":      False,
    "tc_toggle":        False,
    "show_quiz_modal":  False,
    "quiz_submitted":   False,
    "gamma":            5.0,
    "delta":            0.1,
    "risk_label":       "Moderate",
    "esg_label":        "Low",
    "quiz_answers":     {},
    "portfolio_type":   None,
    "exclusions":       {k: False for k, _ in EXCLUSIONS},
    "sel1":             None,
    "sel2":             None,
    "rho":              -0.2,
    "r_free":           2.0,
    "results":          None,
    "custom_a1":        None,
    "custom_a2":        None,
    "custom_rho":       -0.2,
    "active_tab":       0,
    "toast_message":    None,
    "page_facts":       {},   # stores one random fact index per page key
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════
def show_toast(message):
    st.markdown(f"""
    <div style="position:fixed;top:1.25rem;right:1.25rem;z-index:10001;
         min-width:300px;max-width:420px;padding:0.95rem 1.1rem;
         border-radius:16px;background:rgba(248,251,255,0.96);
         border:1px solid rgba(181,212,244,0.95);
         box-shadow:0 16px 36px rgba(4,44,83,0.14);
         backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);">
        <div style="display:flex;align-items:flex-start;gap:0.75rem;">
            <div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#18A999,#2F8FCE);
                 color:#F8FBFF;display:flex;align-items:center;justify-content:center;
                 font-size:0.9rem;font-weight:700;flex-shrink:0;">?</div>
            <div>
                <p style="margin:0 0 0.18rem;color:#0A3B66;font-size:0.8rem;font-weight:700;
                   letter-spacing:0.04em;text-transform:uppercase;">BlueHorizon Update</p>
                <p style="margin:0;color:#185FA5;font-size:0.92rem;line-height:1.45;">{message}</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

if st.session_state.get("toast_message"):
    show_toast(st.session_state["toast_message"])
    st.session_state["toast_message"] = None

# HELPERS
# ══════════════════════════════════════════════════════════
def get_fact(page_key):
    """Returns one stable random fact per page (re-randomises on full reset only)."""
    if page_key not in st.session_state["page_facts"]:
        st.session_state["page_facts"][page_key] = random.randint(0, len(OCEAN_FACTS) - 1)
    return OCEAN_FACTS[st.session_state["page_facts"][page_key]]

def fact_pill(page_key):
    st.markdown(f'<div class="fact-pill">{get_fact(page_key)}</div>', unsafe_allow_html=True)

def reset_quiz_only():
    for k in ["quiz_answers", "gamma", "delta", "risk_label", "esg_label",
              "quiz_submitted", "show_quiz_modal", "results"]:
        st.session_state[k] = defaults[k]
    st.session_state["page_facts"].pop("quiz", None)

def reset_portfolio_only():
    for k in ["portfolio_type", "exclusions", "sel1", "sel2", "rho",
              "r_free", "results", "custom_a1", "custom_a2", "custom_rho"]:
        st.session_state[k] = defaults[k]
    st.session_state["page_facts"].pop("portfolio", None)

def set_active_tab(index):
    st.session_state["active_tab"] = index

def soft_start_over():
    for k, v in defaults.items():
        st.session_state[k] = v
    st.session_state["app_loaded"] = True
    st.session_state["tc_accepted"] = True
    set_active_tab(0)

def go_home():
    set_active_tab(0)

def info_card(icon, title, body):
    return f"""
<div style="background:#ffffff;border:1.5px solid #B5D4F4;border-radius:14px;
     padding:1.5rem 1.25rem;height:100%;box-shadow:0 2px 10px rgba(55,138,221,0.07);">
    <div style="font-size:1.6rem;margin-bottom:0.6rem;">{icon}</div>
    <p style="font-family:'Inter',sans-serif;font-size:0.9rem;font-weight:600;
       color:#0C447C;margin:0 0 0.5rem;">{title}</p>
    <p style="font-family:'Inter',sans-serif;font-size:0.84rem;color:#185FA5;
       line-height:1.6;margin:0;">{body}</p>
</div>"""

def show_loading(message, duration=2.0, full_screen=False):
    ph = st.empty()
    overlay_inset = "0" if full_screen else "1.5rem"
    card_width = "min(560px, 88vw)" if full_screen else "min(520px, 88vw)"
    card_padding = "2.2rem 2.4rem 2rem" if full_screen else "2rem 2.25rem 1.8rem"
    loading_logo = hero_logo_html(220 if full_screen else 170)
    ph.markdown(f"""
    <div style="position:fixed;inset:{overlay_inset};background:rgba(4,44,83,0.42);
         backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
         display:flex;flex-direction:column;align-items:center;justify-content:center;
         z-index:9999;">
        <div style="width:{card_width};padding:{card_padding};border-radius:24px;
             background:linear-gradient(180deg,rgba(248,251,255,0.88),rgba(230,241,251,0.78));
             border:1px solid rgba(181,212,244,0.9);
             box-shadow:0 18px 60px rgba(4,44,83,0.18), inset 0 1px 0 rgba(255,255,255,0.55);
             text-align:center;">
            <div style="display:flex;justify-content:center;">
                {loading_logo}
            </div>
            <p style="font-family:'Playfair Display',serif;font-size:1.5rem;
               color:#042C53;margin:1.35rem 0 0.35rem;letter-spacing:-0.3px;">{message}</p>
            <p style="font-family:'Inter',sans-serif;font-size:0.88rem;color:#185FA5;margin:0;">
                BlueHorizon ? ECN316 Sustainable Finance</p>
            <div style="margin-top:1.5rem;display:flex;justify-content:center;gap:12px;">
                <div style="width:11px;height:11px;border-radius:50%;background:#1570B8;
                     box-shadow:0 0 0 6px rgba(21,112,184,0.10);
                     animation:pulse 1.2s ease-in-out infinite;"></div>
                <div style="width:11px;height:11px;border-radius:50%;background:#2F8FCE;
                     box-shadow:0 0 0 6px rgba(47,143,206,0.10);
                     animation:pulse 1.2s ease-in-out 0.3s infinite;"></div>
                <div style="width:11px;height:11px;border-radius:50%;background:#7CC6E8;
                     box-shadow:0 0 0 6px rgba(124,198,232,0.10);
                     animation:pulse 1.2s ease-in-out 0.6s infinite;"></div>
            </div>
            <div style="margin-top:1.2rem;height:6px;border-radius:999px;overflow:hidden;
                 background:rgba(181,212,244,0.55);">
                <div style="width:42%;height:100%;
                     background:linear-gradient(90deg,#1570B8 0%,#2F8FCE 55%,#7CC6E8 100%);
                     border-radius:999px;animation:drift 1.8s ease-in-out infinite;"></div>
            </div>
        </div>
        <style>
        @keyframes pulse {{
            0%,100%{{opacity:0.2;transform:scale(0.8);}}
            50%{{opacity:1;transform:scale(1.2);}}
        }}
        @keyframes drift {{
            0%{{transform:translateX(-55%);opacity:0.7;}}
            50%{{transform:translateX(85%);opacity:1;}}
            100%{{transform:translateX(-55%);opacity:0.7;}}
        }}
        </style>
    </div>""", unsafe_allow_html=True)
    time.sleep(duration)
    ph.empty()


# ══════════════════════════════════════════════════════════
# MATHS (no short selling)
# ══════════════════════════════════════════════════════════
def p_ret(w, r1, r2): return w*r1 + (1-w)*r2
def p_sd(w, s1, s2, rho):
    return np.sqrt(w**2*s1**2 + (1-w)**2*s2**2 + 2*rho*w*(1-w)*s1*s2)
def p_esg(w, e1, e2): return w*e1 + (1-w)*e2

def compute_results(a1, a2, rho, r_free, gamma, delta):
    R1,R2  = a1["ret"]/100, a2["ret"]/100
    S1,S2  = a1["sd"]/100,  a2["sd"]/100
    RF     = r_free/100
    E1,E2  = a1["esg"]/10,  a2["esg"]/10
    ESG_RF = 0.5
    N      = 500

    frontier, best_sharpe, idx_tan = [], -np.inf, 0
    for i in range(N+1):
        w      = i/N
        ret    = p_ret(w, R1, R2)
        sd     = p_sd(w, S1, S2, rho)
        esg    = p_esg(w, E1, E2)
        sharpe = (ret-RF)/sd if sd > 0 else -np.inf
        frontier.append({"w":w,"ret":ret,"sd":sd,"esg":esg,"sharpe":sharpe})
        if sharpe > best_sharpe:
            best_sharpe = sharpe; idx_tan = i

    tan   = frontier[idx_tan]
    y_std = (tan["ret"]-RF)/(gamma*tan["sd"]**2) if tan["sd"]>0 else 0
    y_esg = ((tan["ret"]-RF) + delta*(tan["esg"]-ESG_RF))/(gamma*tan["sd"]**2) if tan["sd"]>0 else 0
    y_std = max(0.0, min(1.0, y_std))
    y_esg = max(0.0, min(1.0, y_esg))

    opt = {"wRf":1-y_esg, "w1":y_esg*tan["w"], "w2":y_esg*(1-tan["w"]),
           "ret":RF+y_esg*(tan["ret"]-RF), "sd":y_esg*tan["sd"],
           "esg":y_esg*tan["esg"]+(1-y_esg)*ESG_RF}
    std = {"wRf":1-y_std, "w1":y_std*tan["w"], "w2":y_std*(1-tan["w"]),
           "ret":RF+y_std*(tan["ret"]-RF), "sd":y_std*tan["sd"],
           "esg":y_std*tan["esg"]+(1-y_std)*ESG_RF}

    pts         = frontier[::3]
    frontier_sd = [round(p["sd"]*100,2) for p in pts]
    frontier_ret= [round(p["ret"]*100,2) for p in pts]
    sharpe_vals = [round(p["sharpe"],4) for p in pts]
    esg_x       = [round(p["esg"]*10,2) for p in pts]

    cml_sd, cml_ret = [], []
    if tan["sd"]>0:
        slope  = (tan["ret"]-RF)/tan["sd"]
        max_sd = max(p["sd"] for p in frontier)*1.3
        for s in np.arange(0, max_sd*100, 0.2):
            cml_sd.append(round(s,2))
            cml_ret.append(round((RF+slope*s/100)*100,2))

    return {"frontier_sd":frontier_sd,"frontier_ret":frontier_ret,
            "cml_sd":cml_sd,"cml_ret":cml_ret,
            "esg_x":esg_x,"sharpe_vals":sharpe_vals,
            "tan":tan,"opt":opt,"std":std,"RF":RF,
            "a1_name":a1.get("name","Asset 1"),"a2_name":a2.get("name","Asset 2")}

PLOTLY_COLORS = {
    "frontier": "#1570B8",
    "frontier_fill": "rgba(21,112,184,0.10)",
    "cml": "#0A3B66",
    "tangency": "#083B5C",
    "esg_opt": "#18A999",
    "std_opt": "#6FB7E9",
    "rf": "#F4D35E",
    "scatter": "#2F8FCE",
    "outline": "#E6F4FB",
    "text": "#042C53",
}

def styled_fig(height=430):
    fig = go.Figure()
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#F7FCFF",
        font=dict(family="Inter, sans-serif", color=PLOTLY_COLORS["text"]),
        margin=dict(l=24, r=24, t=28, b=24),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#B5D4F4",
            font=dict(color=PLOTLY_COLORS["text"]),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#B5D4F4",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            title_font=dict(size=13),
            tickfont=dict(size=11),
            gridcolor="#DCEFFA",
            griddash="dot",
            linecolor="#9CC8E8",
            zerolinecolor="#C9E2F5",
            showline=True,
        ),
        yaxis=dict(
            title_font=dict(size=13),
            tickfont=dict(size=11),
            gridcolor="#DCEFFA",
            griddash="dot",
            linecolor="#9CC8E8",
            zerolinecolor="#C9E2F5",
            showline=True,
        ),
    )
    return fig

# ══════════════════════════════════════════════════════════
# STEP 1 · SPLASH SCREEN
# ══════════════════════════════════════════════════════════
if not st.session_state["app_loaded"]:
    splash = st.empty()
    splash.markdown(f"""
    <div style="position:fixed;inset:0;background:#042C53;
         display:flex;flex-direction:column;align-items:center;justify-content:center;
         z-index:9999;">
        {hero_logo_html(250)}
        <p style="font-family:'Playfair Display',serif;font-size:2rem;
           color:#F8FBFF;margin:1.75rem 0 0.4rem;letter-spacing:-0.3px;">
            Welcome to BlueHorizon</p>
        <p style="font-family:'Inter',sans-serif;font-size:0.9rem;color:#85B7EB;margin:0;">
            Sustainable · Responsible · Personal</p>
        <div style="margin-top:2rem;display:flex;gap:12px;">
            <div style="width:12px;height:12px;border-radius:50%;background:#378ADD;
                 animation:pulse 1.2s ease-in-out infinite;"></div>
            <div style="width:12px;height:12px;border-radius:50%;background:#85B7EB;
                 animation:pulse 1.2s ease-in-out 0.3s infinite;"></div>
            <div style="width:12px;height:12px;border-radius:50%;background:#B5D4F4;
                 animation:pulse 1.2s ease-in-out 0.6s infinite;"></div>
        </div>
        <style>
        @keyframes pulse{{
            0%,100%{{opacity:0.2;transform:scale(0.8);}}
            50%{{opacity:1;transform:scale(1.2);}}
        }}
        </style>
    </div>""", unsafe_allow_html=True)
    time.sleep(2.5)
    splash.empty()
    st.session_state["app_loaded"] = True
    st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 2 · TERMS & CONDITIONS OVERLAY
# ══════════════════════════════════════════════════════════
if not st.session_state["tc_accepted"]:
    st.markdown(
        f"""<div style="max-width:620px;margin:5rem auto 0;text-align:center;">
<div style="display:flex;justify-content:center;margin-bottom:0.1rem;">
{hero_logo_html(310)}
</div>
<h1 style="margin-top:0;font-size:2.2rem!important;">BlueHorizon</h1>
<p style="color:#185FA5;font-size:0.95rem;margin-bottom:2rem;">Sustainable investing, personalised for you.</p>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div style="max-width:680px;margin:0 auto;background:#ffffff;border-radius:16px;border:1.5px solid #B5D4F4;padding:2rem 2.25rem 1.75rem;box-shadow:0 8px 32px rgba(4,44,83,0.12);">
<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.25rem;">
<span style="font-size:1.3rem;">📋</span>
<p style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#042C53;font-weight:600;margin:0;">Privacy &amp; Terms of Use</p>
</div>
<p style="font-size:0.84rem;color:#185FA5;line-height:1.7;margin:0 0 1rem;">Before you continue, please review the following. BlueHorizon uses session-only data to personalise your experience and no personal data is stored or shared.</p>
<div style="background:#F8FBFF;border-radius:10px;padding:1.25rem 1.4rem;font-size:0.82rem;color:#0C447C;line-height:1.75;max-height:240px;overflow-y:auto;border:1px solid #E6F1FB;margin-bottom:1.25rem;">
<strong>1. Educational purpose only.</strong><br>
BlueHorizon is an academic tool developed for ECN316 Sustainable Finance. Nothing on this platform constitutes financial advice, an offer to invest, or a solicitation to buy or sell any security. All outputs are illustrative only.<br><br>
<strong>2. No liability.</strong><br>
The BlueHorizon team accepts no liability for any investment decisions made on the basis of outputs generated by this tool. Portfolio calculations rely on simplified assumptions and historical data that may not reflect future performance.<br><br>
<strong>3. Data &amp; privacy.</strong><br>
This platform does not collect, store, or transmit any personal information beyond your current browser session. All data is cleared when you close this tab. We do not use tracking cookies or analytics.<br><br>
<strong>4. Data accuracy.</strong><br>
Asset returns, standard deviations, and ESG scores are for illustrative purposes only and may not reflect current or accurate market data.<br><br>
<strong>5. ESG ratings.</strong><br>
ESG scores are approximate and drawn from publicly available sources. They should not be relied upon as definitive assessments of any company's environmental, social, or governance conduct.<br><br>
<strong>6. Intellectual property.</strong><br>
All content, design, and methodology within BlueHorizon remain the intellectual property of the ECN316 development team. Unauthorised reproduction is prohibited.
</div>
<p style="font-size:0.8rem;color:#85B7EB;margin:0 0 1rem;">By enabling the toggle below you confirm you have read and agree to these terms.</p>
</div>""",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='max-width:680px;margin:1rem auto 0;'>", unsafe_allow_html=True)
    toggle = st.toggle(
        "I have read and agree to the BlueHorizon Terms of Use and Privacy Policy",
        value=st.session_state["tc_toggle"],
        key="tc_toggle_widget",
    )
    st.session_state["tc_toggle"] = toggle
    if toggle:
        if st.button("Continue to BlueHorizon ->", key="tc_enter"):
            st.session_state["tc_accepted"] = True
            st.rerun()
    else:
        st.markdown('<p style="font-size:0.82rem;color:#85B7EB;margin-top:0.5rem;">Please enable the toggle above to continue.</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

def render_quiz_content():
    st.markdown(f'<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">{logo_html(40)}<div><p style="font-family:Playfair Display,serif;font-size:1.25rem;color:#042C53;font-weight:600;margin:0;">Risk Aversion Quiz</p><p style="font-size:0.8rem;color:#85B7EB;margin:0;">ECN316 | Sustainable Finance</p></div></div>', unsafe_allow_html=True)
    answers = {}
    label_lookup = {v:k for k,v in SLIDER_MAP.items()}
    for idx, q in enumerate(QUIZ_QUESTIONS):
        st.markdown(f'<p style="font-size:0.9rem;color:#042C53;font-weight:600;margin:1rem 0 0.35rem;">{idx+1}. {q}</p>', unsafe_allow_html=True)
        saved_label = st.session_state["quiz_answers"].get(f"q{idx}", "Neutral")
        saved_val = label_lookup.get(saved_label, 3)
        val = st.slider(f"Question {idx+1}", 1, 5, saved_val, 1, key=f"qm_slider_{idx}")
        answers[f"q{idx}"] = SLIDER_MAP[val]
    delta_quiz = st.slider("ESG Preference (delta)", 0.0, 1.0, float(st.session_state["delta"]), 0.01, key="qm_delta")
    esg_lbl = "High" if delta_quiz >= 0.5 else ("Moderate" if delta_quiz >= 0.15 else "Low")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Close", key="quiz_modal_close", use_container_width=True):
            st.session_state["show_quiz_modal"] = False
            st.rerun()
    with c2:
        if st.button("Submit Quiz", key="quiz_modal_submit", use_container_width=True):
            total = sum(SLIDER_SCORE[label_lookup[value]] for value in answers.values())
            max_score = 5 * len(QUIZ_QUESTIONS)
            gamma_calc = round(1 + (total - len(QUIZ_QUESTIONS)) / (max_score - len(QUIZ_QUESTIONS)) * 14, 2)
            st.session_state.update({
                "quiz_answers": answers,
                "gamma": gamma_calc,
                "delta": delta_quiz,
                "risk_label": "Conservative" if gamma_calc >= 8 else ("Moderate" if gamma_calc >= 4 else "Aggressive"),
                "esg_label": esg_lbl,
                "quiz_submitted": True,
                "show_quiz_modal": False,
            })
            set_active_tab(1)
            show_loading("Dorian is analysing your preferences...", duration=2.0, full_screen=True)
            st.session_state["toast_message"] = "Dorian successfully analysed your preferences."
            st.rerun()

if hasattr(st, "dialog"):
    @st.dialog("Risk Aversion Quiz", width="large")
    def quiz_dialog():
        render_quiz_content()
else:
    def quiz_dialog():
        with st.container(border=True):
            render_quiz_content()

if st.session_state.get("show_quiz_modal"):
    quiz_dialog()
    if not hasattr(st, "dialog"):
        st.stop()

tab_labels = TAB_LABELS
active_idx = int(st.session_state.get("active_tab", 0))
current_tab = tab_labels[active_idx]
if hasattr(st, "segmented_control"):
    selected_tab = st.segmented_control(
        "Navigation",
        options=tab_labels,
        default=current_tab,
        selection_mode="single",
        label_visibility="collapsed",
    ) or current_tab
else:
    selected_tab = st.radio(
        "Navigation",
        options=tab_labels,
        index=active_idx,
        horizontal=True,
        label_visibility="collapsed",
    )
st.session_state["active_tab"] = tab_labels.index(selected_tab)

with st.sidebar:
    st.markdown(f'<div style="text-align:center;padding:1rem 0 0.5rem;">{logo_html(52)}<p style="font-family:Playfair Display,serif;font-size:1.1rem;color:#042C53;margin:0.5rem 0 0;font-weight:600;">BlueHorizon</p><p style="font-size:0.72rem;color:#85B7EB;margin:0;">ECN316 | Sustainable Finance</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Home", key="sidebar_home", use_container_width=True):
        set_active_tab(0)
    if st.button("Retake Quiz", key="sidebar_retake_quiz", use_container_width=True):
        reset_quiz_only(); st.session_state["show_quiz_modal"] = True; st.rerun()

if st.session_state["active_tab"] == 0:
    st.markdown(f'<div style="background:linear-gradient(135deg,#042C53 0%,#185FA5 60%,#378ADD 100%);border-radius:16px;padding:3rem 2.5rem 2.5rem;margin-bottom:2rem;position:relative;overflow:hidden;"><div style="display:flex;flex-direction:column;align-items:flex-start;gap:1rem;margin-bottom:1rem;">{hero_logo_html(380)}<div><p style="font-family:Inter,sans-serif;font-size:0.78rem;font-weight:600;letter-spacing:0.14em;color:#85B7EB;text-transform:uppercase;margin:0 0 0.3rem;">ECN316 | Sustainable Finance</p><h1 style="font-family:Playfair Display,serif!important;font-size:3rem;font-weight:600;color:#F8FBFF;margin:0;line-height:1.1;">BlueHorizon</h1></div></div><p style="font-family:Inter,sans-serif;font-size:1.05rem;color:#B5D4F4;margin:0;max-width:520px;line-height:1.6;">Your personalised gateway to responsible investing.</p></div>', unsafe_allow_html=True)
    fact_pill("home")
    st.markdown('<div class="soft-card" style="margin:0.7rem 0 1.4rem;"><h4>Built for clarity</h4><p>BlueHorizon turns sustainable finance into a calmer decision flow: understand your profile, choose your portfolio style, then explore the results visually.</p></div>', unsafe_allow_html=True)
    st.subheader("What our users say")
    cards_html = ""
    for r in REVIEWS + REVIEWS:
        cards_html += f'<div class="review-card"><p style="font-size:0.88rem;color:#0C447C;font-weight:600;margin:0 0 0.2rem;">{r["name"]}</p><p style="font-size:0.72rem;color:#85B7EB;margin:0 0 0.6rem;">{r["role"]}</p><p style="font-size:0.8rem;color:#378ADD;margin:0 0 0.7rem;line-height:1.55;">&ldquo;{r["text"]}&rdquo;</p><p style="font-size:1rem;color:#378ADD;margin:0;letter-spacing:3px;">{"&#8767;"*5}</p></div>'
    st.markdown(f'<div class="carousel-outer"><div class="carousel-track">{cards_html}</div></div>', unsafe_allow_html=True)
    if st.button("Take the Risk Aversion Quiz", key="home_cta"):
        st.session_state["show_quiz_modal"] = True
        st.rerun()
    st.caption("BlueHorizon | ECN316 Sustainable Finance")
elif st.session_state["active_tab"] == 1:
    st.header("My Portfolio")
    fact_pill("portfolio")
    if not st.session_state["quiz_submitted"]:
        st.markdown('<div class="empty-state"><strong style="display:block;color:#0C447C;margin-bottom:0.35rem;">Complete the Risk Aversion Quiz first</strong>We use your quiz responses to shape the portfolio recommendations and ESG-adjusted allocation.</div>', unsafe_allow_html=True)
        if st.button("Open Risk Aversion Quiz", key="port_open_quiz"):
            st.session_state["show_quiz_modal"] = True
            st.rerun()
    else:
        gamma = st.session_state["gamma"]; delta = st.session_state["delta"]; risk_label = st.session_state["risk_label"]; esg_label = st.session_state["esg_label"]
        st.markdown(f'<div class="profile-banner"><div class="eyebrow">Investor Snapshot</div><div class="body"><strong>{risk_label}</strong> profile with <strong>{esg_label}</strong> ESG conviction.<br>Gamma = {gamma} and delta = {delta}, which feeds directly into the allocation logic.</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="choice-grid"><div class="choice-card"><p class="title">General Portfolio</p><p class="copy">Choose from the built-in asset universe, apply exclusions, and let BlueHorizon construct a cleaner recommendation for you.</p></div><div class="choice-card"><p class="title">Custom Portfolio</p><p class="copy">Bring your own return, risk, correlation, and ESG assumptions for a more hands-on portfolio build.</p></div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Create General Portfolio", key="btn_general"):
                reset_portfolio_only(); st.session_state["portfolio_type"] = "general"
        with c2:
            if st.button("Create Custom Portfolio", key="btn_custom"):
                reset_portfolio_only(); st.session_state["portfolio_type"] = "custom"
        if st.button("Retake Quiz", key="port_retake_quiz"):
            reset_quiz_only(); st.session_state["show_quiz_modal"] = True; st.rerun()
        if st.session_state["portfolio_type"] == "general":
            st.subheader("Exclusion Criteria")
            st.write("Toggle to remove asset categories from your investable universe.")
            excl_cols = st.columns(len(EXCLUSIONS))
            excl = {}
            for i, (key, label) in enumerate(EXCLUSIONS):
                with excl_cols[i]:
                    excl[key] = st.checkbox(
                        label,
                        value=st.session_state["exclusions"].get(key, False),
                        key=f"gen_excl_{key}",
                    )
            st.session_state["exclusions"] = excl

            valid1 = [n for n in ASSET_NAMES if n not in [n for n in ASSET_NAMES if any(tag in ASSETS[n]["tags"] for tag, enabled in st.session_state["exclusions"].items() if enabled)]]
            if any(excl.values()):
                excluded_names = [n for n in ASSET_NAMES if n not in valid1]
                for n in excluded_names:
                    st.markdown(
                        f"<span class='excluded-chip'>{n} excluded</span>",
                        unsafe_allow_html=True,
                    )
            st.subheader("General Portfolio")
            rho_gen = st.slider("Asset Correlation", -1.0, 1.0, float(st.session_state["rho"]), 0.01, key="gen_rho")
            rf_gen = st.number_input("Risk-Free Rate (%)", 0.0, 20.0, float(st.session_state["r_free"]), 0.1, key="gen_rf")
            sel1 = st.selectbox("Asset 1", valid1, index=0 if not st.session_state.get("sel1") or st.session_state.get("sel1") not in valid1 else valid1.index(st.session_state.get("sel1")), key="gen_sel1")
            valid2 = [n for n in valid1 if n != sel1]
            sel2 = st.selectbox("Asset 2", valid2, index=0 if not st.session_state.get("sel2") or st.session_state.get("sel2") not in valid2 else valid2.index(st.session_state.get("sel2")), key="gen_sel2")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Reset Portfolio", key="gen_reset"):
                    reset_portfolio_only(); st.rerun()
            with c2:
                if st.button("Submit Portfolio", key="gen_submit"):
                    a1_f = dict(ASSETS[sel1]); a1_f["name"] = sel1
                    a2_f = dict(ASSETS[sel2]); a2_f["name"] = sel2
                    st.session_state.update({"sel1": sel1, "sel2": sel2, "rho": rho_gen, "r_free": rf_gen})
                    show_loading("Dorian is constructing your portfolio...", duration=2.0)
                    st.session_state["results"] = compute_results(a1_f, a2_f, rho_gen, rf_gen, gamma, delta)
        elif st.session_state["portfolio_type"] == "custom":
            st.subheader("Custom Portfolio")
            c_name1 = st.text_input("Asset 1 Name", value="Asset 1", key="c_name1")
            c_ret1 = st.number_input("Asset 1 Return (%)", 0.0, 100.0, 8.0, 0.1, key="c_ret1")
            c_sd1 = st.number_input("Asset 1 Std Dev (%)", 0.1, 100.0, 15.0, 0.1, key="c_sd1")
            c_esg1 = st.number_input("Asset 1 ESG Score", 0.0, 10.0, 7.0, 0.1, key="c_esg1")
            c_name2 = st.text_input("Asset 2 Name", value="Asset 2", key="c_name2")
            c_ret2 = st.number_input("Asset 2 Return (%)", 0.0, 100.0, 12.0, 0.1, key="c_ret2")
            c_sd2 = st.number_input("Asset 2 Std Dev (%)", 0.1, 100.0, 20.0, 0.1, key="c_sd2")
            c_esg2 = st.number_input("Asset 2 ESG Score", 0.0, 10.0, 5.0, 0.1, key="c_esg2")
            c_rho = st.slider("Correlation", -1.0, 1.0, float(st.session_state.get("custom_rho", -0.2)), 0.01, key="c_rho")
            c_rf = st.number_input("Risk-Free Rate (%)", 0.0, 20.0, float(st.session_state["r_free"]), 0.1, key="c_rf")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Reset Portfolio", key="cust_reset"):
                    reset_portfolio_only(); st.rerun()
            with c2:
                if st.button("Submit Portfolio", key="cust_submit"):
                    a1_c = {"name": c_name1, "ret": c_ret1, "sd": c_sd1, "esg": c_esg1}
                    a2_c = {"name": c_name2, "ret": c_ret2, "sd": c_sd2, "esg": c_esg2}
                    st.session_state.update({"custom_a1": a1_c, "custom_a2": a2_c, "custom_rho": c_rho, "r_free": c_rf})
                    show_loading("Dorian is constructing your portfolio...", duration=2.0)
                    st.session_state["results"] = compute_results(a1_c, a2_c, c_rho, c_rf, gamma, delta)
        results = st.session_state.get("results")
        if results:
            opt = results["opt"]; std_r = results["std"]
            m1, m2, m3 = st.columns(3)
            m1.metric("Expected Return", f"{opt['ret']*100:.2f}%")
            m2.metric("Portfolio Risk", f"{opt['sd']*100:.2f}%")
            m3.metric("ESG Score", f"{opt['esg']*10:.1f}/10")
            df = pd.DataFrame({"Asset": ["Risk-Free Asset", results["a1_name"], results["a2_name"]], "Standard": [f"{std_r['wRf']*100:.2f}%", f"{std_r['w1']*100:.2f}%", f"{std_r['w2']*100:.2f}%"], "ESG": [f"{opt['wRf']*100:.2f}%", f"{opt['w1']*100:.2f}%", f"{opt['w2']*100:.2f}%"]})
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown('<div class="empty-state" style="margin-top:1rem;"><strong style="display:block;color:#0C447C;margin-bottom:0.3rem;">Portfolio ready</strong>Head over to the Charts tab to visualise your portfolio on the efficient frontier and compare ESG trade-offs.</div>', unsafe_allow_html=True)
    st.caption("BlueHorizon | ECN316 Sustainable Finance")
else:
    results = st.session_state.get("results")
    if results is None:
        st.markdown('<div class="empty-state"><strong style="display:block;color:#0C447C;margin-bottom:0.35rem;">No charts yet</strong>Complete the quiz and build a portfolio first, then the efficient frontier and ESG chart will appear here.</div>', unsafe_allow_html=True)
    else:
        opt = results["opt"]; std_r = results["std"]; tan = results["tan"]
        st.header("Portfolio Charts")
        fact_pill("charts")
        fig1 = styled_fig(430)
        fig1.add_trace(go.Scatter(x=results["frontier_sd"], y=results["frontier_ret"], mode="lines", name="Efficient Frontier", line=dict(color=PLOTLY_COLORS["frontier"], width=4, shape="spline", smoothing=0.6)))
        fig1.add_trace(go.Scatter(x=results["cml_sd"], y=results["cml_ret"], mode="lines", name="Capital Market Line", line=dict(color=PLOTLY_COLORS["cml"], dash="dash", width=3)))
        fig1.add_trace(go.Scatter(x=[round(tan["sd"]*100,2)], y=[round(tan["ret"]*100,2)], mode="markers+text", name="Tangency Portfolio", text=["Tangency"], textposition="top center", marker=dict(color=PLOTLY_COLORS["tangency"], size=18, symbol="diamond", line=dict(color=PLOTLY_COLORS["outline"], width=2))))
        fig1.add_trace(go.Scatter(x=[round(opt["sd"]*100,2)], y=[round(opt["ret"]*100,2)], mode="markers+text", name="ESG-Optimal", text=["ESG-Optimal"], textposition="top left", marker=dict(color=PLOTLY_COLORS["esg_opt"], size=22, symbol="star", line=dict(color=PLOTLY_COLORS["outline"], width=2))))
        fig1.add_trace(go.Scatter(x=[round(std_r["sd"]*100,2)], y=[round(std_r["ret"]*100,2)], mode="markers+text", name="Standard Optimal", text=["Standard"], textposition="bottom right", marker=dict(color=PLOTLY_COLORS["std_opt"], size=18, symbol="circle", line=dict(color=PLOTLY_COLORS["outline"], width=2))))
        fig1.update_layout(xaxis_title="Portfolio Risk (%)", yaxis_title="Expected Return (%)")
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = styled_fig(400)
        opt_sharpe = (opt["ret"] - results["RF"]) / opt["sd"] if opt["sd"] > 0 else 0
        std_sharpe = (std_r["ret"] - results["RF"]) / std_r["sd"] if std_r["sd"] > 0 else 0
        fig2.add_trace(go.Scatter(x=results["esg_x"], y=results["sharpe_vals"], mode="markers", name="Portfolio Combinations", marker=dict(color=PLOTLY_COLORS["scatter"], size=8, opacity=0.7, line=dict(color="#D9F0FF", width=1))))
        fig2.add_trace(go.Scatter(x=[round(opt["esg"]*10,2)], y=[round(opt_sharpe,4)], mode="markers+text", name="ESG-Optimal", text=["ESG-Optimal"], textposition="top left", marker=dict(color=PLOTLY_COLORS["esg_opt"], size=22, symbol="star", line=dict(color=PLOTLY_COLORS["outline"], width=2))))
        fig2.add_trace(go.Scatter(x=[round(std_r["esg"]*10,2)], y=[round(std_sharpe,4)], mode="markers+text", name="Standard Optimal", text=["Standard"], textposition="bottom right", marker=dict(color=PLOTLY_COLORS["std_opt"], size=18, symbol="circle", line=dict(color=PLOTLY_COLORS["outline"], width=2))))
        fig2.update_layout(xaxis_title="ESG Score (0-10)", yaxis_title="Sharpe Ratio")
        st.plotly_chart(fig2, use_container_width=True)
        if st.button("Start Over", key="chart_restart"):
            soft_start_over(); st.rerun()
    st.caption("BlueHorizon | ECN316 Sustainable Finance")
