import streamlit as st

st.set_page_config(
    page_title="Scouting Engine",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@400;600;700&display=swap');

/* ── Root palette ── */
:root {
    --bg:       #0A0A0F;
    --card:     #111118;
    --card2:    #16161F;
    --border:   #1E1E2A;
    --accent:   #E8FF47;
    --accent2:  #00C6A7;
    --text:     #F0EFE8;
    --muted:    #6B6A72;
    --danger:   #FF5E5E;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem 2rem !important; max-width: 1400px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebarNav"] { padding-top: 0.5rem; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0A0A0F !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.03em !important;
    transition: opacity .15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Selectbox / Inputs ── */
[data-testid="stSelectbox"] > div,
[data-testid="stMultiSelect"] > div,
[data-testid="stTextInput"] > div {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border-bottom: 2px solid transparent !important;
    padding-bottom: 6px !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── Custom pill badge ── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.badge-green  { background: rgba(0,198,167,0.15); color: #00C6A7; border: 1px solid rgba(0,198,167,0.3); }
.badge-yellow { background: rgba(232,255,71,0.12); color: #E8FF47; border: 1px solid rgba(232,255,71,0.25); }
.badge-red    { background: rgba(255,94,94,0.12);  color: #FF5E5E; border: 1px solid rgba(255,94,94,0.25); }

/* ── Section header ── */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar branding ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem 0;'>
        <div style='font-family:"Space Grotesk",sans-serif; font-size:20px; font-weight:700;
                    color:#E8FF47; letter-spacing:-0.02em;'>⚽ Scouting Engine</div>
        <div style='font-size:11px; color:#6B6A72; margin-top:4px; letter-spacing:0.06em;
                    text-transform:uppercase;'>Football Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#6B6A72;'>
        <div style='margin-bottom:6px;'>📊 Top 5 European Leagues</div>
        <div style='margin-bottom:6px;'>🤖 KNN Similarity Model</div>
        <div>📐 Per-90 Normalized Metrics</div>
    </div>
    """, unsafe_allow_html=True)

# ── Landing page ─────────────────────────────────────────────
st.markdown("""
<div style='padding: 3rem 0 2rem 0;'>
    <div style='font-family:"Space Grotesk",sans-serif; font-size:48px; font-weight:700;
                letter-spacing:-0.03em; line-height:1.1;'>
        Find the<br><span style='color:#E8FF47;'>right player.</span>
    </div>
    <div style='color:#6B6A72; font-size:16px; margin-top:1rem; max-width:520px; line-height:1.6;'>
        Compare players, discover similar profiles, and explore league statistics
        — all based on objective per-90 metrics.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style='background:#111118; border:1px solid #1E1E2A; border-radius:14px;
                padding:1.5rem; cursor:pointer;'>
        <div style='font-size:28px; margin-bottom:0.8rem;'>🔄</div>
        <div style='font-family:"Space Grotesk",sans-serif; font-size:15px; font-weight:600;
                    color:#F0EFE8; margin-bottom:0.4rem;'>Player Comparison</div>
        <div style='font-size:12px; color:#6B6A72; line-height:1.5;'>
            Compare 2 players across all metrics with radar & bar charts.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background:#111118; border:1px solid #1E1E2A; border-radius:14px;
                padding:1.5rem;'>
        <div style='font-size:28px; margin-bottom:0.8rem;'>🏆</div>
        <div style='font-family:"Space Grotesk",sans-serif; font-size:15px; font-weight:600;
                    color:#F0EFE8; margin-bottom:0.4rem;'>Similar Players</div>
        <div style='font-size:12px; color:#6B6A72; line-height:1.5;'>
            KNN model finds the 10 most statistically similar profiles.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background:#111118; border:1px solid #1E1E2A; border-radius:14px;
                padding:1.5rem;'>
        <div style='font-size:28px; margin-bottom:0.8rem;'>📊</div>
        <div style='font-family:"Space Grotesk",sans-serif; font-size:15px; font-weight:600;
                    color:#F0EFE8; margin-bottom:0.4rem;'>League Overview</div>
        <div style='font-size:12px; color:#6B6A72; line-height:1.5;'>
            Top performers, distributions, and scatter analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:2rem; color:#6B6A72; font-size:12px;'>← Navigate using the sidebar</div>",
            unsafe_allow_html=True)