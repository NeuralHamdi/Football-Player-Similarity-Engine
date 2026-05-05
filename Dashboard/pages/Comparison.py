import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.eda_and_visualisation import radar_comparison

st.set_page_config(
    page_title="Scout-IA | Comparison",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
    --green:     #00FF87;
    --green-dim: rgba(0,255,135,0.10);
    --green-glow:rgba(0,255,135,0.35);
    --amber:     #FFB800;
    --amber-dim: rgba(255,184,0,0.10);
    --bg:        #050A0E;
    --surface:   #0C1419;
    --surface2:  #101B22;
    --border:    rgba(0,255,135,0.15);
    --border2:   rgba(255,255,255,0.06);
    --text:      #E8EDF2;
    --muted:     #6B7B8A;
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

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding-bottom: 28px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
}
.page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    letter-spacing: 0.06em;
    color: var(--text);
    line-height: 1;
}
.page-title span { color: var(--green); }
.page-sub {
    font-size: 0.88rem;
    color: var(--muted);
    margin-top: 6px;
    font-weight: 300;
}
.page-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    color: var(--green);
    border: 1px solid var(--border);
    padding: 5px 14px;
    border-radius: 2px;
    background: var(--green-dim);
    text-transform: uppercase;
}

/* ── Selector panels ── */
.selector-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 28px;
    position: relative;
}
.selector-panel.target  { border-left: 3px solid var(--green); }
.selector-panel.compare { border-left: 3px solid var(--amber); }

.panel-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.panel-label.target  { color: var(--green); }
.panel-label.compare { color: var(--amber); }

.panel-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.target  .panel-dot { background: var(--green); box-shadow: 0 0 8px var(--green); }
.compare .panel-dot { background: var(--amber); box-shadow: 0 0 8px var(--amber); }

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--border) !important;
}

/* ── Player info card ── */
.player-card {
    padding: 22px 24px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    gap: 18px;
    margin-top: 8px;
}
.player-card.target  { background: rgba(0,255,135,0.07); border: 1px solid rgba(0,255,135,0.2); }
.player-card.compare { background: rgba(255,184,0,0.07); border: 1px solid rgba(255,184,0,0.2); }

.player-avatar {
    width: 52px; height: 52px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}
.player-card.target  .player-avatar { background: rgba(0,255,135,0.15); }
.player-card.compare .player-avatar { background: rgba(255,184,0,0.15); }

.player-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.06em;
    line-height: 1;
}
.player-card.target  .player-name { color: var(--green); }
.player-card.compare .player-name { color: var(--amber); }

.player-meta {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.08em;
    margin-top: 5px;
}

/* ── vs divider ── */
.vs-divider {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 16px 0;
}
.vs-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    opacity: 0.5;
}
.vs-line {
    width: 1px;
    height: 32px;
    background: var(--border);
}

/* ── Stats table ── */
.stats-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin-top: 32px;
}
.stats-header {
    padding: 18px 24px;
    border-bottom: 1px solid var(--border2);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
}

div[data-testid="stDataFrame"] { border: none !important; }
div[data-testid="stDataFrame"] table {
    background: var(--surface) !important;
    border-collapse: collapse !important;
}
div[data-testid="stDataFrame"] th {
    background: var(--surface2) !important;
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
}
div[data-testid="stDataFrame"] td {
    color: var(--text) !important;
    font-size: 0.88rem !important;
    border-bottom: 1px solid var(--border2) !important;
}

/* ── Warning / info messages ── */
div[data-testid="stAlert"] {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Spinner ── */
div[data-testid="stSpinner"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: var(--green) !important;
    letter-spacing: 0.1em !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 6px !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    color: var(--muted) !important;
}
</style>
""", unsafe_allow_html=True)


# ── HELPER ──────────────────────────────────────────────────
def player_selector(df, key_prefix, color_class, label,
                    default_league="La Liga", default_club="Barcelona"):
    st.markdown(f"""
        <div class="selector-panel {color_class}">
            <div class="panel-label {color_class}">
                <div class="panel-dot"></div>{label}
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_p = st.columns(3)
    with col_l:
        leagues = sorted(df['Comp'].unique())
        l_idx = leagues.index(default_league) if default_league in leagues else 0
        selected_league = st.selectbox("League", leagues, index=l_idx, key=f"l_{key_prefix}")
    with col_c:
        clubs = sorted(df[df['Comp'] == selected_league]['Squad'].unique())
        c_idx = clubs.index(default_club) if default_club in clubs else 0
        selected_club = st.selectbox("Club", clubs, index=c_idx, key=f"c_{key_prefix}")
    with col_p:
        players = sorted(df[df['Squad'] == selected_club]['Player'].unique())
        selected_player = st.selectbox("Player", players, key=f"p_{key_prefix}")

    return selected_player


# ── MAIN ────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div>
        <div class="page-title">HEAD-TO-<span>HEAD</span></div>
        <div class="page-sub">Select two players to compare their tactical and statistical profiles</div>
    </div>
    <div class="page-badge">Radar · Multi-Axis Analysis</div>
</div>
""", unsafe_allow_html=True)

if 'df' not in st.session_state:
    st.warning("⚠ Data not loaded — please return to the Home page first.")
    st.stop()

df = st.session_state['df']

# ── SELECTORS ───────────────────────────────────────────────
col1, col_mid, col2 = st.columns([5, 1, 5])

with col1:
    player1 = player_selector(
        df, "target", "target", "TARGET PLAYER",
        default_league="La Liga", default_club="Barcelona"
    )

with col_mid:
    st.markdown("""
    <div class="vs-divider">
        <div class="vs-line"></div>
        <div class="vs-text">VS</div>
        <div class="vs-line"></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    player2 = player_selector(
        df, "compare", "compare", "COMPARISON PLAYER",
        default_league="Premier League", default_club="Manchester City"
    )

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ── PLAYER CARDS ────────────────────────────────────────────
if player1 != player2:
    p1 = df[df['Player'] == player1].iloc[0]
    p2 = df[df['Player'] == player2].iloc[0]

    card1, card2 = st.columns(2)
    with card1:
        st.markdown(f"""
        <div class="player-card target">
            <div class="player-avatar">⚡</div>
            <div>
                <div class="player-name">{player1}</div>
                <div class="player-meta">
                    {p1['Squad']} · {p1['Pos']} · {int(p1['Age'])} YRS · {p1['Comp']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with card2:
        st.markdown(f"""
        <div class="player-card compare">
            <div class="player-avatar">🎯</div>
            <div>
                <div class="player-name">{player2}</div>
                <div class="player-meta">
                    {p2['Squad']} · {p2['Pos']} · {int(p2['Age'])} YRS · {p2['Comp']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── RADAR ───────────────────────────────────────────────
    with st.spinner("Rendering radar profile..."):
        fig = radar_comparison(df, player1, player2)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    # ── DATA TABLE ──────────────────────────────────────────
    with st.expander("📊  DETAILED STATISTICAL BREAKDOWN"):
        comp_cols = ['Player', 'Squad', 'Pos', 'Age', 'Gls_90', 'Ast_90', 'Sh_90', 'Crs_90', 'Int_90']
        available = [c for c in comp_cols if c in df.columns]
        comparison_df = df[df['Player'].isin([player1, player2])][available]
        st.dataframe(comparison_df.set_index('Player'), use_container_width=True)

else:
    st.warning("Select two **different** players to generate the comparison.")