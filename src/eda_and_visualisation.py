import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('../data/football_data_cleaned.csv')


# ── 1. Scatter : Goals vs Assists ────────────────────────────
def scatter_goals_vs_assists(df):
    df_attacker = df[df['Pos'].str.contains('FW|MF', na=False)]
    fig = px.scatter(
        df_attacker,
        x='Ast_90',
        y='Gls_90',
        color='Comp',
        hover_name='Player',
        hover_data=['Squad', 'Age', 'Min'],
        title='Evaluation Offensive : Buts vs Passes Décisives (par 90  min)',
        labels={
            "Ast_90": "Assist (90 min)",
            "Gls_90": "Goal (90 min)",
            "Comp": "Championnat"
        },
        template='plotly_dark'
    )
    fig.update_traces(marker=dict(size=10, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
    return fig


# ── 2. Radar : comparaison deux joueurs ──────────────────────
def radar_comparison(df, joueur_1, joueur_2):
    categories = ['Gls_90', 'Ast_90', 'Sh_90', 'SoT_90', 'Crs_90', 'Int_90']

    joueur_1_data = df[df['Player'] == joueur_1]
    joueur_2_data = df[df['Player'] == joueur_2]

    if joueur_1_data.empty or joueur_2_data.empty:
        print("un joueur n'a pas trouvee")
        return None

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=joueur_1_data[categories].values[0],
            theta=categories,
            fill='toself',
            name=joueur_1,
            line=dict(color='#00D9FF', width=3),
            fillcolor='rgba(0, 217, 255, 0.3)',
            marker=dict(size=8, color='#00D9FF', line=dict(width=2, color='white'))
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=joueur_2_data[categories].values[0],
            theta=categories,
            fill='toself',
            name=joueur_2,
            line=dict(color='#FF6B35', width=3),
            fillcolor='rgba(255, 107, 53, 0.3)',
            marker=dict(size=8, color='#FF6B35', line=dict(width=2, color='white'))
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(20, 20, 20, 0.8)',
            radialaxis=dict(
                visible=True,
                range=[0, max(joueur_1_data[categories].max().max(), joueur_2_data[categories].max().max()) + 0.5],
                gridcolor='rgba(100, 100, 100, 0.5)',
                tickfont=dict(size=11, color='#E0E0E0')
            ),
            angularaxis=dict(
                gridcolor='rgba(100, 100, 100, 0.5)',
                tickfont=dict(size=12, color='#E0E0E0', family='Arial Black')
            )
        ),
        showlegend=True,
        legend=dict(
            x=1.1,
            y=1,
            font=dict(size=13, color='white'),
            bgcolor='rgba(0, 0, 0, 0.5)',
            bordercolor='#E0E0E0',
            borderwidth=1
        ),
        title=dict(
            text=f"Evaluation Offensive : {joueur_1} vs {joueur_2}",
            font=dict(size=18, color='white', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        template='plotly_dark',
        paper_bgcolor='#0A0A0A',
        font=dict(color='white', size=12),
        height=700,
        width=900,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    return fig


# ── 3. Scatter : Finishing quality ───────────────────────────
def scatter_finishing(df):
    df_finishers = df[(df['Pos'].str.contains('FW|MF', na=False)) & (df['Sh_90'] > 1.0)]
    fig = px.scatter(
        df_finishers,
        x='Sh_90',
        y='Gls_90',
        color='Comp',
        hover_name='Player',
        hover_data=['Squad', 'Age', 'Gls', 'Sh', 'G/Sh'],
        title='Analyse de la Finition : Volume de Tirs (Sh_90) vs Buts (Gls_90)',
        labels={
            'Sh_90': 'Tirs tentés (par 90 min)',
            'Gls_90': 'Buts marqués (par 90 min)',
            'Comp': 'Championnat'
        },
        template='plotly_dark'
    )
    fig.update_traces(marker=dict(size=9, opacity=0.8, line=dict(width=0.5, color='white')))
    return fig


# ── 4. Bar : Top 15 milieux créateurs ────────────────────────
def bar_top_creators(df):
    df_midfielders = df[df['Pos'].str.contains('MF', na=False)]
    top_15_creators = df_midfielders.sort_values(by='Ast_90', ascending=False).head(15)

    fig = px.bar(
        top_15_creators,
        x='Ast_90',
        y='Player',
        orientation='h',
        color='Comp',
        hover_data=['Squad', 'Age', 'Ast', 'Min'],
        title="Les 15 Meilleurs Milieux Créateurs d'Europe (Passes Décisives / 90 min)",
        labels={
            'Ast_90': 'Passes Décisives (par 90 min)',
            'Player': 'Joueur',
            'Comp': 'Championnat'
        },
        template='plotly_dark'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


# ── 5. Scatter : Player influence ────────────────────────────
def scatter_influence(df):
    df_impact = df[df['Min'] >= 900]

    fig = px.scatter(
        df_impact,
        x='+/-90',
        y='On-Off',
        color='Comp',
        hover_name='Player',
        hover_data=['Squad', 'Pos', 'Age', 'Min%'],
        title="Analyse de l'Influence : Performance Équipe (+/-90) vs Importance du Joueur (On-Off)",
        labels={
            '+/-90': "Différentiel de buts de l'équipe (par 90 min)",
            'On-Off': 'Impact Net (Performance avec lui - sans lui)',
            'Comp': 'Championnat'
        },
        template='plotly_dark'
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    return fig


# ── Run all (test) ────────────────────────────────────────────
if __name__ == '__main__':
    scatter_goals_vs_assists(df).show()
    radar_comparison(df, "Ousmane Dembélé", "Lamine Yamal").show()
    scatter_finishing(df).show()
    bar_top_creators(df).show()
    scatter_influence(df).show()
