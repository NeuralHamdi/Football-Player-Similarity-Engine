import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing import load_raw_data

st.set_page_config(
    page_title="Scout-IA | Home",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
    --green:      #00FF87;
    --green-dim:  rgba(0,255,135,0.12);
    --green-glow: rgba(0,255,135,0.35);
    --bg:         #050A0E;
    --surface:    #0C1419;
    --border:     rgba(0,255,135,0.18);
    --text:       #E8EDF2;
    --muted:      #6B7B8A;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }

/* ── Top nav bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 32px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 48px;
}
.logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 0.12em;
    color: var(--green);
    text-shadow: 0 0 24px var(--green-glow);
}
.badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: var(--green);
    border: 1px solid var(--border);
    padding: 4px 12px;
    border-radius: 2px;
    background: var(--green-dim);
    letter-spacing: 0.1em;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 40px 0 56px;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    color: var(--green);
    text-transform: uppercase;
    margin-bottom: 20px;
    opacity: 0.9;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 10vw, 8rem);
    line-height: 0.92;
    letter-spacing: 0.04em;
    color: var(--text);
    margin-bottom: 8px;
}
.hero-title span {
    color: var(--green);
    text-shadow: 0 0 60px var(--green-glow);
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 520px;
    margin: 20px auto 0;
    line-height: 1.7;
    font-weight: 300;
}

/* ── Stats row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    margin: 48px 0;
}
.stat-cell {
    background: var(--surface);
    padding: 28px 24px;
    text-align: center;
}
.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    color: var(--green);
    line-height: 1;
    text-shadow: 0 0 20px var(--green-glow);
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 6px;
}

/* ── Tool cards ── */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin: 48px 0 0;
}
.tool-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 36px 32px 28px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.tool-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--green), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.tool-card:hover { border-color: var(--green); transform: translateY(-3px); }
.tool-card:hover::before { opacity: 1; }

.card-icon {
    font-size: 2.2rem;
    margin-bottom: 18px;
    display: block;
}
.card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.08em;
    color: var(--text);
    margin-bottom: 10px;
}
.card-desc {
    font-size: 0.9rem;
    color: var(--muted);
    line-height: 1.7;
    margin-bottom: 20px;
}
.card-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    color: var(--green);
    border: 1px solid var(--border);
    padding: 3px 10px;
    border-radius: 2px;
    background: var(--green-dim);
    text-transform: uppercase;
}
.card-divider {
    height: 1px;
    background: var(--border);
    margin: 22px 0 20px;
    opacity: 0.5;
}

/* ── Page link buttons — centered ── */
div[data-testid="stPageLink"] {
    display: flex !important;
    justify-content: center !important;
}
div[data-testid="stPageLink"] > a {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    background: var(--green) !important;
    color: #050A0E !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 0.12em !important;
    padding: 10px 36px !important;
    text-decoration: none !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 0 18px var(--green-glow) !important;
    width: fit-content !important;
}
div[data-testid="stPageLink"] > a:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

/* ── Status bar ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 16px 20px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    margin-top: 32px;
}
.dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    flex-shrink: 0;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}
.status-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.1em;
}
.status-text strong { color: var(--green); }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_clean_data():
    return pd.read_csv('data/football_data_cleaned.csv')


if 'df' not in st.session_state:
    st.session_state['df'] = get_clean_data()

df        = st.session_state['df']
n_players = len(df)
n_leagues = df['Comp'].nunique() if 'Comp' in df.columns else 5
n_clubs   = df['Squad'].nunique() if 'Squad' in df.columns else 98

# ── TOP BAR ──────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="logo">⚽ SCOUT-IA</div>
    <div class="badge">SYSTEM ONLINE · v2.0</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI-Powered Football Intelligence</div>
    <div class="hero-title">Find Your<br><span>Next Star</span></div>
    <div class="hero-sub">
        Advanced machine learning meets football analytics.
        Identify talent, compare players, and discover hidden gems
        across Europe's top leagues.
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ROW ────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-row">
    <div class="stat-cell">
        <div class="stat-num">{n_players:,}</div>
        <div class="stat-label">Players Tracked</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">{n_leagues}</div>
        <div class="stat-label">Top Leagues</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">{n_clubs}</div>
        <div class="stat-label">Clubs Monitored</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TOOL CARDS ───────────────────────────────────────────────
st.markdown("""
<div class="cards-grid">
    <div class="tool-card">
        <span class="card-icon">🧬</span>
        <div class="card-title">Similarity Engine</div>
        <div class="card-desc">
            KNN-powered player cloning. Enter any player and instantly
            discover statistically identical profiles across all five leagues.
        </div>
        <span class="card-tag">KNN · Cosine Distance</span>
        <div class="card-divider"></div>
    </div>
    <div class="tool-card">
        <span class="card-icon">⚔️</span>
        <div class="card-title">Head-to-Head</div>
        <div class="card-desc">
            Deep tactical comparison with interactive radar charts.
            Filter by league, club and position to find the right match.
        </div>
        <span class="card-tag">Radar · Multi-Axis</span>
        <div class="card-divider"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── NAV BUTTONS — each centered in its column ─────────────────
col1, col2 = st.columns(2)
with col1:
    _, btn1, _ = st.columns([1, 2, 1])
    with btn1:
        st.page_link("pages/Similarity.py", label="⚡  Launch Similarity Engine")
with col2:
    _, btn2, _ = st.columns([1, 2, 1])
    with btn2:
        st.page_link("pages/Comparison.py", label="⚔️  Launch Head-to-Head")

# ── STATUS BAR ───────────────────────────────────────────────
st.markdown(f"""
<div class="status-bar">
    <div class="dot"></div>
    <div class="status-text">
        Dataset loaded — <strong>{n_players} players</strong> ready for analysis ·
        Use the sidebar to navigate between tools
    </div>
</div>
""", unsafe_allow_html=True)