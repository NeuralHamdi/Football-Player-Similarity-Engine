import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Similarity import find_similar_players
from src.eda_and_visualisation import radar_comparison

st.set_page_config(page_title="Scout-IA | Similarity", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
    --green:      #00FF87;
    --green-dim:  rgba(0,255,135,0.10);
    --green-glow: rgba(0,255,135,0.35);
    --amber:      #FFB800;
    --amber-dim:  rgba(255,184,0,0.10);
    --blue:       #00BFFF;
    --blue-dim:   rgba(0,191,255,0.10);
    --bg:         #050A0E;
    --surface:    #0C1419;
    --surface2:   #101B22;
    --border:     rgba(0,255,135,0.15);
    --border2:    rgba(255,255,255,0.06);
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

/* ── Config panel ── */
.config-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--green);
    border-radius: 6px;
    padding: 28px 32px 32px;
}
.panel-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--green);
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 24px;
}
.panel-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    flex-shrink: 0;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
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
div[data-testid="stSlider"] > div > div > div {
    background: var(--green) !important;
}

/* ── Launch button ── */
div[data-testid="stButton"] > button {
    background: var(--green) !important;
    color: #050A0E !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.12em !important;
    padding: 12px 36px !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 0 24px var(--green-glow) !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Results header ── */
.results-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 40px 0 28px;
}
.results-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.06em;
    color: var(--text);
}
.results-title span { color: var(--green); }
.results-divider {
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Clone cards ── */
.clone-card {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 6px;
    padding: 24px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.clone-card:hover {
    border-color: var(--border);
    transform: translateY(-2px);
}
.clone-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.clone-card.rank-1::after { background: var(--green); box-shadow: 0 0 12px var(--green); }
.clone-card.rank-2::after { background: var(--amber); box-shadow: 0 0 12px var(--amber); }
.clone-card.rank-3::after { background: var(--blue);  box-shadow: 0 0 12px var(--blue);  }

.clone-rank {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 12px;
}
.clone-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    line-height: 1;
    margin-bottom: 4px;
}
.rank-1 .clone-score { color: var(--green); text-shadow: 0 0 20px var(--green-glow); }
.rank-2 .clone-score { color: var(--amber); text-shadow: 0 0 20px var(--amber-dim); }
.rank-3 .clone-score { color: var(--blue);  text-shadow: 0 0 20px var(--blue-dim);  }

.clone-score-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 18px;
}
.clone-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 0.05em;
    color: var(--text);
    line-height: 1;
    margin-bottom: 6px;
}
.clone-meta {
    font-size: 0.8rem;
    color: var(--muted);
    font-weight: 300;
}
.clone-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border2);
}
.clone-stat-item {
    text-align: center;
}
.clone-stat-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: var(--text);
}
.clone-stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.1em;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Radar section label ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 40px 0 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 6px !important;
    margin-top: 24px;
}
div[data-testid="stExpander"] summary {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    color: var(--muted) !important;
}
div[data-testid="stDataFrame"] th {
    background: var(--surface2) !important;
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
div[data-testid="stDataFrame"] td {
    color: var(--text) !important;
    font-size: 0.85rem !important;
}

div[data-testid="stSpinner"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: var(--green) !important;
    letter-spacing: 0.1em !important;
}
div[data-testid="stAlert"] {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ─────────────────────────────────────────────────
RANK_CLASSES = ["rank-1", "rank-2", "rank-3"]
RANK_ICONS   = ["🥇", "🥈", "🥉"]

def player_selector(df, key_prefix):
    col_l, col_c, col_p = st.columns(3)
    with col_l:
        leagues = sorted(df['Comp'].unique())
        selected_league = st.selectbox("League", leagues, key=f"l_{key_prefix}")
    with col_c:
        clubs = sorted(df[df['Comp'] == selected_league]['Squad'].unique())
        selected_club = st.selectbox("Club", clubs, key=f"c_{key_prefix}")
    with col_p:
        players = sorted(df[df['Squad'] == selected_club]['Player'].unique())
        selected_player = st.selectbox("Target Player", players, key=f"p_{key_prefix}")
    return selected_player


# ── MAIN ────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div>
        <div class="page-title">SIMILARITY<br><span>ENGINE</span></div>
        <div class="page-sub">KNN vector search — find statistically identical player profiles</div>
    </div>
    <div class="page-badge">KNN · Cosine Distance</div>
</div>
""", unsafe_allow_html=True)

if 'df' not in st.session_state:
    st.warning("⚠ Data not loaded — please return to the Home page first.")
    st.stop()

df = st.session_state['df']

# ── CONFIG PANEL ────────────────────────────────────────────
st.markdown("""
<div class="config-panel">
    <div class="panel-label"><div class="panel-dot"></div>Search Configuration</div>
</div>
""", unsafe_allow_html=True)

target_player = player_selector(df, "Sim_Target")

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

col_n, col_btn, _ = st.columns([2, 2, 3])
with col_n:
    n_results = st.slider("Number of clones", 1, 10, 5)
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run = st.button("⚡  Launch Scouting AI", type="primary")

# ── RESULTS ─────────────────────────────────────────────────
if run:
    with st.spinner("Computing vector distances..."):
        try:
            results = find_similar_players(df, target_player, n_neighbors=n_results)

            # ── Results header
            st.markdown(f"""
            <div class="results-header">
                <div class="results-title">CLONES OF <span>{target_player.upper()}</span></div>
                <div class="results-divider"></div>
            </div>
            """, unsafe_allow_html=True)

            # ── Top 3 cards
            top_n = min(3, len(results))
            cols  = st.columns(top_n)

            for i in range(top_n):
                row        = results.iloc[i]
                rank_class = RANK_CLASSES[i]
                rank_icon  = RANK_ICONS[i]
                gls  = round(row.get('Gls_90', 0), 2)
                ast  = round(row.get('Ast_90', 0), 2)

                with cols[i]:
                    st.markdown(f"""
                    <div class="clone-card {rank_class}">
                        <div class="clone-rank">{rank_icon} CLONE #{i+1}</div>
                        <div class="clone-score">{row['Similarity']}%</div>
                        <div class="clone-score-label">Similarity Score</div>
                        <div class="clone-name">{row['Player']}</div>
                        <div class="clone-meta">{row['Squad']} · {row['Comp']} · {row['Age']} yrs</div>
                        <div class="clone-stats">
                            <div class="clone-stat-item">
                                <div class="clone-stat-val">{gls}</div>
                                <div class="clone-stat-lbl">Gls / 90</div>
                            </div>
                            <div class="clone-stat-item">
                                <div class="clone-stat-val">{ast}</div>
                                <div class="clone-stat-lbl">Ast / 90</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Radar vs Clone #1
            clone_1 = results.iloc[0]['Player']
            st.markdown(f"""
            <div class="section-label">Radar Profile — {target_player} vs {clone_1}</div>
            """, unsafe_allow_html=True)

            fig = radar_comparison(df, target_player, clone_1)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

            # ── Full table
            with st.expander("📊  FULL STATISTICAL BREAKDOWN"):
                st.dataframe(results, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")