import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="BlueHorizon · Sustainable Finance",
    page_icon="🌊",
    layout="wide",
)

# ══════════════════════════════════════════════════════════
# OCEAN BLUE CSS INJECTION
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font ───────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600&display=swap');

/* ── Root palette ──────────────────────────────────────── */
:root {
    --bh-deep:    #042C53;
    --bh-navy:    #0C447C;
    --bh-ocean:   #185FA5;
    --bh-mid:     #378ADD;
    --bh-sky:     #85B7EB;
    --bh-mist:    #B5D4F4;
    --bh-foam:    #E6F1FB;
    --bh-white:   #F8FBFF;
}

/* ── Global body & font ───────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ───────────────────────────────────── */
.stApp {
    background: linear-gradient(160deg, var(--bh-foam) 0%, #F0F7FF 60%, #EAF3FB 100%);
}

/* ── Main content area ────────────────────────────────── */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ── H1 — Playfair for the brand title ────────────────── */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.6rem !important;
    font-weight: 600 !important;
    color: var(--bh-deep) !important;
    letter-spacing: -0.5px;
    margin-bottom: 0.25rem !important;
}

/* ── H2 / H3 ──────────────────────────────────────────── */
h2 {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.35rem !important;
    font-weight: 600 !important;
    color: var(--bh-navy) !important;
    border-bottom: 2px solid var(--bh-mist);
    padding-bottom: 0.4rem;
    margin-top: 1.6rem !important;
}
h3 {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--bh-ocean) !important;
}

/* ── Tabs ─────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid var(--bh-mist);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--bh-ocean);
    padding: 0.6rem 1.2rem;
    border-bottom: 3px solid transparent;
    background: transparent !important;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    color: var(--bh-deep) !important;
    border-bottom: 3px solid var(--bh-ocean) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--bh-deep);
    background: var(--bh-foam) !important;
    border-radius: 6px 6px 0 0;
}

/* ── Buttons ──────────────────────────────────────────── */
.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.875rem;
    background: linear-gradient(135deg, var(--bh-ocean), var(--bh-navy));
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.4rem;
    transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(24, 95, 165, 0.25);
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--bh-navy), var(--bh-deep));
    box-shadow: 0 4px 14px rgba(24, 95, 165, 0.35);
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Info / alert boxes ───────────────────────────────── */
.stAlert {
    border-radius: 10px !important;
    border-left: 4px solid var(--bh-ocean) !important;
    background: var(--bh-foam) !important;
}

/* ── Metric cards ─────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1.5px solid var(--bh-mist);
    border-radius: 12px;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 2px 10px rgba(55, 138, 221, 0.08);
}
[data-testid="metric-container"] label {
    color: var(--bh-ocean) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem !important;
    color: var(--bh-deep) !important;
    font-weight: 600;
}

/* ── DataFrames / tables ──────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1.5px solid var(--bh-mist) !important;
}

/* ── Sliders ──────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--bh-ocean) !important;
    border-color: var(--bh-ocean) !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {
    color: var(--bh-sky);
}

/* ── Select boxes ─────────────────────────────────────── */
.stSelectbox [data-baseweb="select"] > div:first-child {
    border-color: var(--bh-mist) !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}
.stSelectbox [data-baseweb="select"] > div:first-child:focus-within {
    border-color: var(--bh-ocean) !important;
    box-shadow: 0 0 0 3px rgba(24, 95, 165, 0.15) !important;
}

/* ── Number inputs ────────────────────────────────────── */
.stNumberInput input {
    border-radius: 8px !important;
    border-color: var(--bh-mist) !important;
}
.stNumberInput input:focus {
    border-color: var(--bh-ocean) !important;
    box-shadow: 0 0 0 3px rgba(24, 95, 165, 0.15) !important;
}

/* ── Text inputs ──────────────────────────────────────── */
.stTextInput input {
    border-radius: 8px !important;
    border-color: var(--bh-mist) !important;
}
.stTextInput input:focus {
    border-color: var(--bh-ocean) !important;
    box-shadow: 0 0 0 3px rgba(24, 95, 165, 0.15) !important;
}

/* ── Radio buttons ────────────────────────────────────── */
.stRadio [data-testid="stMarkdownContainer"] p {
    color: var(--bh-navy);
}

/* ── Checkboxes ───────────────────────────────────────── */
.stCheckbox label {
    color: var(--bh-navy) !important;
}

/* ── Captions ─────────────────────────────────────────── */
.stCaption {
    color: var(--bh-sky) !important;
    font-size: 0.78rem !important;
    text-align: center;
    border-top: 1px solid var(--bh-foam);
    padding-top: 0.75rem;
    margin-top: 2rem;
}

/* ── Sidebar (if used) ────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bh-deep) 0%, var(--bh-navy) 100%);
}
</style>
""", unsafe_allow_html=True)

# ── Welcome page hero banner ──────────────────────────────────────────────────
HERO_HTML = """
<div style="
    background: linear-gradient(135deg, #042C53 0%, #185FA5 60%, #378ADD 100%);
    border-radius: 16px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute; top: -30px; right: -30px;
        width: 220px; height: 220px; border-radius: 50%;
        background: rgba(133, 183, 235, 0.15);
    "></div>
    <div style="
        position: absolute; bottom: -50px; right: 80px;
        width: 140px; height: 140px; border-radius: 50%;
        background: rgba(181, 212, 244, 0.10);
    "></div>
    <p style="
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem; font-weight: 600; letter-spacing: 0.14em;
        color: #85B7EB; text-transform: uppercase; margin: 0 0 0.5rem;
    ">ECN316 · Sustainable Finance</p>
    <h1 style="
        font-family: 'Playfair Display', serif !important;
        font-size: 3rem; font-weight: 600;
        color: #F8FBFF; margin: 0 0 0.75rem; line-height: 1.15;
    ">BlueHorizon 🌊</h1>
    <p style="
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem; color: #B5D4F4;
        margin: 0; max-width: 520px; line-height: 1.6;
    ">Your personalised gateway to responsible investing — aligning your financial goals with your values and your appetite for risk.</p>
</div>
"""

# ── Info card HTML helper ─────────────────────────────────────────────────────
def info_card(icon, title, body):
    return f"""
<div style="
    background: #ffffff;
    border: 1.5px solid #B5D4F4;
    border-radius: 14px;
    padding: 1.5rem 1.25rem;
    height: 100%;
    box-shadow: 0 2px 10px rgba(55, 138, 221, 0.07);
">
    <div style="font-size: 1.6rem; margin-bottom: 0.6rem;">{icon}</div>
    <p style="
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem; font-weight: 600;
        color: #0C447C; margin: 0 0 0.5rem;
    ">{title}</p>
    <p style="
        font-family: 'Inter', sans-serif;
        font-size: 0.84rem; color: #185FA5; line-height: 1.6; margin: 0;
    ">{body}</p>
</div>
"""

# ══════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════
ASSETS = {
    "Vestas Wind Systems": {"ret": 7.5, "sd": 18.0, "esg": 8.9, "sector": "Renewables", "tags": []},
    "NextEra Energy": {"ret": 9.2, "sd": 15.0, "esg": 8.1, "sector": "Clean Energy", "tags": []},
    "TSMC": {"ret": 14.0, "sd": 24.0, "esg": 5.4, "sector": "Technology", "tags": []},
    "Johnson & Johnson": {"ret": 6.0, "sd": 12.0, "esg": 6.8, "sector": "Healthcare", "tags": []},
    "Shell PLC": {"ret": 11.0, "sd": 22.0, "esg": 3.2, "sector": "Oil & Gas", "tags": ["fossil"]},
    "British American Tobacco": {"ret": 8.5, "sd": 16.0, "esg": 2.5, "sector": "Tobacco", "tags": ["tobacco"]},
    "Lockheed Martin": {"ret": 10.5, "sd": 19.0, "esg": 3.8, "sector": "Defence", "tags": ["defence"]},
}
ASSET_NAMES = list(ASSETS.keys())

EXCLUSIONS = [
    ("tobacco", "Tobacco companies"),
    ("defence", "Defence companies"),
    ("fossil", "Fossil fuel companies"),
    ("gambling", "Gambling companies"),
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

LIKERT = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
LIKERT_SCORE = {
    "Strongly Agree": 5,
    "Agree": 4,
    "Neutral": 3,
    "Disagree": 2,
    "Strongly Disagree": 1,
}

# ══════════════════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ══════════════════════════════════════════════════════════
defaults = {
    "active_tab": 0,
    "gamma": 5.0,
    "delta": 0.1,
    "risk_label": "Moderate",
    "esg_label": "Low",
    "quiz_answers": {},
    "portfolio_type": None,
    "exclusions": {k: False for k, _ in EXCLUSIONS},
    "sel1": None,
    "sel2": None,
    "rho": -0.2,
    "r_free": 2.0,
    "results": None,
    "custom_a1": None,
    "custom_a2": None,
    "custom_rho": -0.2,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════
# MATHS
# ══════════════════════════════════════════════════════════
def p_ret(w, r1, r2):
    return w * r1 + (1 - w) * r2

def p_sd(w, s1, s2, rho):
    return np.sqrt(w**2 * s1**2 + (1 - w)**2 * s2**2 + 2 * rho * w * (1 - w) * s1 * s2)

def p_esg(w, e1, e2):
    return w * e1 + (1 - w) * e2

def compute_results(a1, a2, rho, r_free, gamma, delta):
    R1, R2 = a1["ret"] / 100, a2["ret"] / 100
    S1, S2 = a1["sd"] / 100, a2["sd"] / 100
    RF = r_free / 100
    E1, E2 = a1["esg"] / 10, a2["esg"] / 10
    ESG_RF = 0.5
    N = 500

    frontier, best_sharpe, idx_tan = [], -np.inf, 0
    for i in range(N + 1):
        w = i / N
        ret = p_ret(w, R1, R2)
        sd = p_sd(w, S1, S2, rho)
        esg = p_esg(w, E1, E2)
        sharpe = (ret - RF) / sd if sd > 0 else -np.inf
        frontier.append({"w": w, "ret": ret, "sd": sd, "esg": esg, "sharpe": sharpe})
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            idx_tan = i

    tan = frontier[idx_tan]
    y_std = (tan["ret"] - RF) / (gamma * tan["sd"]**2) if tan["sd"] > 0 else 0
    y_esg = ((tan["ret"] - RF) + delta * (tan["esg"] - ESG_RF)) / (gamma * tan["sd"]**2) if tan["sd"] > 0 else 0

    opt = {
        "wRf": 1 - y_esg,
        "w1": y_esg * tan["w"],
        "w2": y_esg * (1 - tan["w"]),
        "ret": RF + y_esg * (tan["ret"] - RF),
        "sd": abs(y_esg) * tan["sd"],
        "esg": y_esg * tan["esg"] + (1 - y_esg) * ESG_RF,
    }
    std = {
        "wRf": 1 - y_std,
        "w1": y_std * tan["w"],
        "w2": y_std * (1 - tan["w"]),
        "ret": RF + y_std * (tan["ret"] - RF),
        "sd": abs(y_std) * tan["sd"],
        "esg": y_std * tan["esg"] + (1 - y_std) * ESG_RF,
    }

    pts = frontier[::3]
    frontier_sd = [round(p["sd"] * 100, 2) for p in pts]
    frontier_ret = [round(p["ret"] * 100, 2) for p in pts]
    sharpe_vals = [round(p["sharpe"], 4) for p in pts]
    esg_x = [round(p["esg"] * 10, 2) for p in pts]
    esg_y = [round(p["ret"] * 100, 2) for p in pts]

    cml_sd, cml_ret = [], []
    if tan["sd"] > 0:
        slope = (tan["ret"] - RF) / tan["sd"]
        max_sd = max(p["sd"] for p in frontier) * 1.3
        for s in np.arange(0, max_sd * 100, 0.2):
            cml_sd.append(round(s, 2))
            cml_ret.append(round((RF + slope * s / 100) * 100, 2))

    return {
        "frontier_sd": frontier_sd,
        "frontier_ret": frontier_ret,
        "cml_sd": cml_sd,
        "cml_ret": cml_ret,
        "esg_x": esg_x,
        "esg_y": esg_y,
        "sharpe_vals": sharpe_vals,
        "tan": tan,
        "opt": opt,
        "std": std,
        "RF": RF,
        "a1_name": a1.get("name", "Asset 1"),
        "a2_name": a2.get("name", "Asset 2"),
    }

# ── Plotly theme helper ───────────────────────────────────────────────────────
PLOTLY_COLORS = {
    "frontier": "#378ADD",
    "cml": "#0C447C",
    "tangency": "#042C53",
    "esg_opt": "#1D9E75",
    "std_opt": "#85B7EB",
    "rf": "#B5D4F4",
    "scatter": "#378ADD",
}

def styled_fig(height=430):
    fig = go.Figure()
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#F8FBFF",
        font=dict(family="Inter, sans-serif", color="#042C53"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#B5D4F4",
            borderwidth=1,
        ),
        xaxis=dict(
            gridcolor="#E6F1FB",
            linecolor="#B5D4F4",
            zerolinecolor="#B5D4F4",
        ),
        yaxis=dict(
            gridcolor="#E6F1FB",
            linecolor="#B5D4F4",
            zerolinecolor="#B5D4F4",
        ),
    )
    return fig

# ── Reset helper ──────────────────────────────────────────────────────────────
def do_reset():
    for k, v in defaults.items():
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════
tab_labels = ["🌊 Welcome", "📋 Risk Quiz", "🗂️ My Portfolio", "📊 Results", "📈 Charts"]
tabs = st.tabs(tab_labels)

# ─────────────────────────────────────────────────────────
# TAB 0 · WELCOME
# ─────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown(HERO_HTML, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(info_card(
            "🎯", "Our Mission",
            "BlueHorizon exists to make sustainable investing accessible to everyone. "
            "We believe that strong financial returns and positive environmental and "
            "social impact are not mutually exclusive."
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(info_card(
            "🔬", "Who We Are",
            "We are a team of sustainable finance researchers building tools that help "
            "individual investors understand the trade-offs between risk, return, and ESG performance."
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(info_card(
            "⚙️", "What We Do",
            "Using modern portfolio theory, we compute the efficient frontier, tangency "
            "portfolio, and capital market line — then adjust the optimal allocation "
            "based on your ESG preferences and risk tolerance."
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: #ffffff; border: 1.5px solid #B5D4F4;
        border-left: 4px solid #378ADD; border-radius: 10px;
        padding: 1rem 1.25rem;
    ">
        <p style="margin:0; font-size:0.95rem; color:#042C53; line-height:1.6;">
            Ready to get started? Head over to the
            <strong style="color:#185FA5;">📋 Risk Aversion Quiz</strong>
            tab to discover your investor profile, then build your personalised sustainable portfolio.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("BlueHorizon · ECN316 Sustainable Finance")

# ─────────────────────────────────────────────────────────
# TAB 1 · RISK QUIZ
# ─────────────────────────────────────────────────────────
with tabs[1]:
    st.header("Risk Aversion Quiz")
    st.write(
        "Answer each question honestly. Your responses will be used to calculate your "
        "personal risk aversion score (γ), which drives the portfolio optimisation."
    )

    answers = {}
    for idx, question in enumerate(QUIZ_QUESTIONS):
        st.markdown(f"""
        <div style="
            background: #ffffff; border: 1.5px solid #B5D4F4;
            border-left: 4px solid #378ADD; border-radius: 10px;
            padding: 1rem 1.25rem; margin-bottom: 0.4rem;
        ">
            <p style="font-size:0.78rem; color:#378ADD; font-weight:600;
               text-transform:uppercase; letter-spacing:0.08em; margin:0 0 0.25rem;">
                Question {idx + 1} of {len(QUIZ_QUESTIONS)}
            </p>
            <p style="font-size:0.95rem; color:#042C53; font-weight:500; margin:0;">
                {question}
            </p>
        </div>
        """, unsafe_allow_html=True)

        saved = st.session_state["quiz_answers"].get(f"q{idx}", "Neutral")
        saved_idx = LIKERT.index(saved) if saved in LIKERT else 2
        choice = st.radio(
            label=f"q{idx}",
            options=LIKERT,
            index=saved_idx,
            horizontal=True,
            key=f"quiz_radio_{idx}",
            label_visibility="collapsed",
        )
        answers[f"q{idx}"] = choice
        st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

    st.subheader("ESG Commitment")
    delta_quiz = st.slider(
        "ESG Preference (δ)",
        0.0, 1.0, float(st.session_state["delta"]), 0.01,
        key="delta_quiz",
        help="0 = pure finance · 1 = maximise ESG",
    )
    esg_lbl = "High" if delta_quiz >= 0.5 else ("Moderate" if delta_quiz >= 0.15 else "Low")
    st.caption(f"ESG commitment: **{esg_lbl}**")

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    q1, q2 = st.columns(2)
    with q1:
        if st.button("🔄 Reset Quiz", key="quiz_reset"):
            do_reset()
            st.rerun()
    with q2:
        if st.button("Submit →", key="quiz_next"):
            st.session_state["quiz_answers"] = answers
            total = sum(LIKERT_SCORE[v] for v in answers.values())
            max_score = 5 * len(QUIZ_QUESTIONS)
            gamma_calc = round(
                1 + (total - len(QUIZ_QUESTIONS)) / (max_score - len(QUIZ_QUESTIONS)) * 14, 2
            )
            st.session_state["gamma"] = gamma_calc
            st.session_state["delta"] = delta_quiz
            st.session_state["risk_label"] = (
                "Conservative" if gamma_calc >= 8 else
                ("Moderate" if gamma_calc >= 4 else "Aggressive")
            )
            st.session_state["esg_label"] = esg_lbl
            st.success("Quiz saved! Head over to the **🗂️ My Portfolio** tab to build your portfolio.")

    st.caption("BlueHorizon · ECN316 Sustainable Finance")

# ─────────────────────────────────────────────────────────
# TAB 2 · MY PORTFOLIO
# ─────────────────────────────────────────────────────────
with tabs[2]:
    gamma = st.session_state["gamma"]
    delta = st.session_state["delta"]
    risk_label = st.session_state["risk_label"]
    esg_label = st.session_state["esg_label"]

    st.header("My Portfolio")

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #042C53, #185FA5);
        border-radius: 12px; padding: 1rem 1.5rem;
        display: flex; gap: 2rem; align-items: center; margin-bottom: 1rem;
    ">
        <div>
            <p style="font-size:0.72rem; color:#85B7EB; text-transform:uppercase;
               letter-spacing:0.1em; margin:0 0 0.2rem; font-weight:600;">Risk Profile</p>
            <p style="font-size:1.1rem; color:#F8FBFF; font-weight:600; margin:0;">
                {risk_label} &nbsp;<span style="font-size:0.85rem; color:#B5D4F4;">(γ = {gamma})</span>
            </p>
        </div>
        <div style="width:1px; background:#378ADD; height:36px;"></div>
        <div>
            <p style="font-size:0.72rem; color:#85B7EB; text-transform:uppercase;
               letter-spacing:0.1em; margin:0 0 0.2rem; font-weight:600;">ESG Commitment</p>
            <p style="font-size:1.1rem; color:#F8FBFF; font-weight:600; margin:0;">
                {esg_label} &nbsp;<span style="font-size:0.85rem; color:#B5D4F4;">(δ = {delta})</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Choose Portfolio Type")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div style="background:#ffffff; border:1.5px solid #B5D4F4; border-radius:12px; padding:1.25rem; margin-bottom:0.5rem;">
            <p style="font-weight:600; color:#0C447C; margin:0 0 0.4rem;">🗂️ General Portfolio</p>
            <p style="font-size:0.84rem; color:#185FA5; margin:0; line-height:1.6;">
                Choose from our curated asset list, set exclusion criteria, and let us optimise the allocation for you.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create General Portfolio", key="btn_general"):
            st.session_state["portfolio_type"] = "general"

    with p2:
        st.markdown("""
        <div style="background:#ffffff; border:1.5px solid #B5D4F4; border-radius:12px; padding:1.25rem; margin-bottom:0.5rem;">
            <p style="font-weight:600; color:#0C447C; margin:0 0 0.4rem;">✏️ Custom Portfolio</p>
            <p style="font-size:0.84rem; color:#185FA5; margin:0; line-height:1.6;">
                Enter your own assets — name, return, std dev, correlation, and ESG score — for a fully bespoke result.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Custom Portfolio", key="btn_custom"):
            st.session_state["portfolio_type"] = "custom"

    # ── GENERAL PORTFOLIO ─────────────────────────────────
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
                    key=f"gen_excl_{key}"
                )
        st.session_state["exclusions"] = excl

        excluded_names = [
            name for name in ASSET_NAMES
            if any(tag in ASSETS[name]["tags"] for tag in excl if excl[tag])
        ]
        if excluded_names:
            st.write("Excluded assets:")
            for name in excluded_names:
                st.markdown(f"<span style='color:#378ADD;'>— {name}</span>", unsafe_allow_html=True)

        st.subheader("Market Parameters")
        mp1, mp2 = st.columns(2)
        with mp1:
            rho_gen = st.slider("Asset Correlation (ρ)", -1.0, 1.0, float(st.session_state["rho"]), 0.01, key="gen_rho")
        with mp2:
            rf_gen = st.number_input("Risk-Free Rate (%)", 0.0, 20.0, float(st.session_state["r_free"]), 0.1, key="gen_rf")

        st.subheader("Select Assets")

        valid1 = [n for n in ASSET_NAMES if n not in excluded_names]
        if not valid1:
            st.error("All assets excluded. Please loosen your exclusion criteria.")
        else:
            ac1, ac2 = st.columns(2)

            with ac1:
                st.markdown("""<p style="font-weight:600; color:#0C447C; margin-bottom:0.25rem;">Asset 1</p>""", unsafe_allow_html=True)
                prev1 = st.session_state.get("sel1") or valid1[0]
                idx1 = valid1.index(prev1) if prev1 in valid1 else 0
                sel1 = st.selectbox("Choose Asset 1", valid1, index=idx1, key="gen_sel1", label_visibility="collapsed")
                a1_d = ASSETS[sel1]
                st.markdown(f"""
                <div style="background:#E6F1FB; border-radius:8px; padding:0.75rem 1rem; font-size:0.84rem; color:#042C53; line-height:1.9;">
                    <b>Return:</b> {a1_d['ret']}% &nbsp;|&nbsp;
                    <b>Std Dev:</b> {a1_d['sd']}% &nbsp;|&nbsp;
                    <b>ESG:</b> {a1_d['esg']}/10<br>
                    <b>Sector:</b> {a1_d['sector']}
                </div>
                """, unsafe_allow_html=True)

            with ac2:
                st.markdown("""<p style="font-weight:600; color:#0C447C; margin-bottom:0.25rem;">Asset 2</p>""", unsafe_allow_html=True)
                valid2 = [n for n in valid1 if n != sel1]
                if not valid2:
                    st.error("No second asset available.")
                else:
                    prev2 = st.session_state.get("sel2") or ("TSMC" if "TSMC" in valid2 else valid2[0])
                    idx2 = valid2.index(prev2) if prev2 in valid2 else 0
                    sel2 = st.selectbox("Choose Asset 2", valid2, index=idx2, key="gen_sel2", label_visibility="collapsed")
                    a2_d = ASSETS[sel2]
                    st.markdown(f"""
                    <div style="background:#E6F1FB; border-radius:8px; padding:0.75rem 1rem; font-size:0.84rem; color:#042C53; line-height:1.9;">
                        <b>Return:</b> {a2_d['ret']}% &nbsp;|&nbsp;
                        <b>Std Dev:</b> {a2_d['sd']}% &nbsp;|&nbsp;
                        <b>ESG:</b> {a2_d['esg']}/10<br>
                        <b>Sector:</b> {a2_d['sector']}
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
            gs1, gs2 = st.columns(2)
            with gs1:
                if st.button("🔄 Reset", key="gen_reset"):
                    do_reset()
                    st.rerun()
            with gs2:
                if st.button("Submit →", key="gen_submit"):
                    a1_f = dict(a1_d)
                    a1_f["name"] = sel1
                    a2_f = dict(a2_d)
                    a2_f["name"] = sel2
                    st.session_state["sel1"] = sel1
                    st.session_state["sel2"] = sel2
                    st.session_state["rho"] = rho_gen
                    st.session_state["r_free"] = rf_gen
                    st.session_state["results"] = compute_results(a1_f, a2_f, rho_gen, rf_gen, gamma, delta)
                    st.success("Portfolio calculated! View your results in the **📊 Results** tab.")

    # ── CUSTOM PORTFOLIO ──────────────────────────────────
    elif st.session_state["portfolio_type"] == "custom":
        st.subheader("Custom Asset Entry")
        st.write("Enter the details for your two assets. All fields are required.")

        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("""<p style="font-weight:600; color:#0C447C;">Asset 1</p>""", unsafe_allow_html=True)
            c_name1 = st.text_input("Asset Name", value="Asset 1", key="c_name1")
            c_ret1 = st.number_input("Expected Return (%)", 0.0, 100.0, 8.0, 0.1, key="c_ret1")
            c_sd1 = st.number_input("Standard Deviation (%)", 0.1, 100.0, 15.0, 0.1, key="c_sd1")
            c_esg1 = st.number_input("ESG Score (0–10)", 0.0, 10.0, 7.0, 0.1, key="c_esg1")

        with cc2:
            st.markdown("""<p style="font-weight:600; color:#0C447C;">Asset 2</p>""", unsafe_allow_html=True)
            c_name2 = st.text_input("Asset Name", value="Asset 2", key="c_name2")
            c_ret2 = st.number_input("Expected Return (%)", 0.0, 100.0, 12.0, 0.1, key="c_ret2")
            c_sd2 = st.number_input("Standard Deviation (%)", 0.1, 100.0, 20.0, 0.1, key="c_sd2")
            c_esg2 = st.number_input("ESG Score (0–10)", 0.0, 10.0, 5.0, 0.1, key="c_esg2")

        st.subheader("Market Parameters")
        cm1, cm2 = st.columns(2)
        with cm1:
            c_rho = st.slider("Correlation between assets (ρ)", -1.0, 1.0, -0.2, 0.01, key="c_rho")
        with cm2:
            c_rf = st.number_input("Risk-Free Rate (%)", 0.0, 20.0, 2.0, 0.1, key="c_rf")

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        cs1, cs2 = st.columns(2)
        with cs1:
            if st.button("🔄 Reset", key="cust_reset"):
                do_reset()
                st.rerun()
        with cs2:
            if st.button("Submit →", key="cust_submit"):
                a1_c = {"name": c_name1, "ret": c_ret1, "sd": c_sd1, "esg": c_esg1}
                a2_c = {"name": c_name2, "ret": c_ret2, "sd": c_sd2, "esg": c_esg2}
                st.session_state["custom_a1"] = a1_c
                st.session_state["custom_a2"] = a2_c
                st.session_state["custom_rho"] = c_rho
                st.session_state["results"] = compute_results(a1_c, a2_c, c_rho, c_rf, gamma, delta)
                st.success("Portfolio calculated! View your results in the **📊 Results** tab.")

    elif st.session_state["portfolio_type"] is None:
        st.markdown("""
        <div style="background:#E6F1FB; border-radius:10px; padding:1.25rem;
             text-align:center; color:#185FA5; font-size:0.9rem; margin-top:1rem;">
            Select a portfolio type above to continue.
        </div>
        """, unsafe_allow_html=True)

    st.caption("BlueHorizon · ECN316 Sustainable Finance")

# ─────────────────────────────────────────────────────────
# TAB 3 · RESULTS
# ─────────────────────────────────────────────────────────
with tabs[3]:
    results = st.session_state.get("results")

    if results is None:
        st.markdown("""
        <div style="background:#E6F1FB; border-radius:10px; padding:2rem;
             text-align:center; color:#185FA5; font-size:0.95rem; margin-top:2rem;">
            No results yet — complete the quiz and build your portfolio first.
        </div>
        """, unsafe_allow_html=True)
    else:
        opt = results["opt"]
        std_r = results["std"]
        gamma = st.session_state["gamma"]
        delta = st.session_state["delta"]
        risk_label = st.session_state["risk_label"]
        esg_label = st.session_state["esg_label"]
        a1_name = results["a1_name"]
        a2_name = results["a2_name"]

        st.header("Recommended Portfolio")

        m1, m2, m3 = st.columns(3)
        m1.metric("Expected Return", f"{opt['ret']*100:.2f}%")
        m2.metric("Portfolio Risk (σ)", f"{opt['sd']*100:.2f}%")
        m3.metric("ESG Score", f"{opt['esg']*10:.1f}", "out of 10")

        st.subheader("Portfolio Weights")
        df = pd.DataFrame({
            "Asset": ["Risk-Free Asset", a1_name, a2_name],
            "Standard (δ=0)": [
                f"{std_r['wRf']*100:.2f}%",
                f"{std_r['w1']*100:.2f}%",
                f"{std_r['w2']*100:.2f}%"
            ],
            "ESG-Adjusted": [
                f"{opt['wRf']*100:.2f}%",
                f"{opt['w1']*100:.2f}%",
                f"{opt['w2']*100:.2f}%"
            ],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        risky_pct = (1 - opt["wRf"]) * 100
        sharpe_opt = (opt["ret"] - results["RF"]) / opt["sd"] if opt["sd"] > 0 else 0

        st.subheader("Your Investor Profile")

        profile_items = [
            ("Risk tolerance", f"{risk_label} (γ = {gamma})"),
            ("ESG commitment", f"{esg_label} (δ = {delta})"),
            ("Allocation to risky assets", f"{risky_pct:.1f}%  |  {opt['wRf']*100:.1f}% risk-free"),
            ("Blended ESG score", f"{opt['esg']*10:.1f} / 10"),
            ("Sharpe ratio", f"{sharpe_opt:.3f}"),
        ]
        for label, value in profile_items:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                 padding:0.6rem 0; border-bottom:1px solid #E6F1FB;">
                <span style="font-size:0.88rem; color:#378ADD; font-weight:500;">{label}</span>
                <span style="font-size:0.95rem; color:#042C53; font-weight:600;">{value}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background: #E6F1FB; border-left: 4px solid #378ADD;
            border-radius: 10px; padding: 0.9rem 1.25rem;
            color: #042C53; font-size: 0.9rem;
        ">
            Head over to the <strong style="color:#185FA5;">📈 Charts</strong> tab
            to visualise your portfolio on the efficient frontier.
        </div>
        """, unsafe_allow_html=True)

    st.caption("BlueHorizon · ECN316 Sustainable Finance")

# ─────────────────────────────────────────────────────────
# TAB 4 · CHARTS
# ─────────────────────────────────────────────────────────
with tabs[4]:
    results = st.session_state.get("results")

    if results is None:
        st.markdown("""
        <div style="background:#E6F1FB; border-radius:10px; padding:2rem;
             text-align:center; color:#185FA5; font-size:0.95rem; margin-top:2rem;">
            No charts yet — complete the quiz and build your portfolio first.
        </div>
        """, unsafe_allow_html=True)
    else:
        opt = results["opt"]
        std_r = results["std"]
        tan = results["tan"]

        st.header("Portfolio Charts")

        st.subheader("Efficient Frontier")
        fig1 = styled_fig(430)
        fig1.add_trace(go.Scatter(
            x=results["frontier_sd"], y=results["frontier_ret"],
            mode="lines", name="Efficient Frontier",
            line=dict(color=PLOTLY_COLORS["frontier"], width=2.5),
        ))
        fig1.add_trace(go.Scatter(
            x=results["cml_sd"], y=results["cml_ret"],
            mode="lines", name="Capital Market Line",
            line=dict(color=PLOTLY_COLORS["cml"], dash="dash", width=1.8),
        ))
        fig1.add_trace(go.Scatter(
            x=[round(tan["sd"]*100, 2)], y=[round(tan["ret"]*100, 2)],
            mode="markers+text", name="Tangency Portfolio",
            text=["Tangency"], textposition="top center",
            marker=dict(color=PLOTLY_COLORS["tangency"], size=10, symbol="diamond"),
        ))
        fig1.add_trace(go.Scatter(
            x=[round(opt["sd"]*100, 2)], y=[round(opt["ret"]*100, 2)],
            mode="markers+text", name="ESG-Optimal",
            text=["ESG-Optimal"], textposition="top center",
            marker=dict(color="#1D9E75", size=12, symbol="star"),
        ))
        fig1.add_trace(go.Scatter(
            x=[round(std_r["sd"]*100, 2)], y=[round(std_r["ret"]*100, 2)],
            mode="markers+text", name="Standard Optimal",
            text=["Standard"], textposition="top center",
            marker=dict(color=PLOTLY_COLORS["std_opt"], size=10),
        ))
        fig1.add_trace(go.Scatter(
            x=[0], y=[round(results["RF"]*100, 2)],
            mode="markers+text", name="Risk-Free Asset",
            text=["Risk-Free"], textposition="top right",
            marker=dict(color=PLOTLY_COLORS["rf"], size=10, symbol="square"),
        ))
        fig1.update_layout(xaxis_title="Risk (σ %)", yaxis_title="Return %")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("ESG Score vs Sharpe Ratio Trade-off")
        st.write(
            "Each point is a different portfolio weighting. "
            "See how improving ESG quality affects risk-adjusted returns."
        )

        sharpe_vals = results["sharpe_vals"]
        esg_x = results["esg_x"]
        opt_sharpe = (opt["ret"] - results["RF"]) / opt["sd"] if opt["sd"] > 0 else 0
        std_sharpe = (std_r["ret"] - results["RF"]) / std_r["sd"] if std_r["sd"] > 0 else 0

        fig2 = styled_fig(390)
        fig2.add_trace(go.Scatter(
            x=esg_x, y=sharpe_vals,
            mode="markers", name="Portfolio Combinations",
            marker=dict(color=PLOTLY_COLORS["scatter"], size=6, opacity=0.7),
        ))
        fig2.add_trace(go.Scatter(
            x=[round(opt["esg"]*10, 2)], y=[round(opt_sharpe, 4)],
            mode="markers+text", name="ESG-Optimal",
            text=["ESG-Optimal"], textposition="top center",
            marker=dict(color="#1D9E75", size=12, symbol="star"),
        ))
        fig2.add_trace(go.Scatter(
            x=[round(std_r["esg"]*10, 2)], y=[round(std_sharpe, 4)],
            mode="markers+text", name="Standard Optimal",
            text=["Standard"], textposition="top center",
            marker=dict(color=PLOTLY_COLORS["std_opt"], size=10),
        ))
        fig2.update_layout(xaxis_title="ESG Score (1–10)", yaxis_title="Sharpe Ratio")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Start Over", key="chart_restart"):
            do_reset()
            st.rerun()

    st.caption("BlueHorizon · ECN316 Sustainable Finance")
