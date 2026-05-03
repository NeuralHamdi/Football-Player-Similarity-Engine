import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

KNN_FEATURES = [
    'Gls_90',   # Finition
    'Ast_90',   # Création
    'Sh_90',    # Volume d'attaque
    'TklW_90',  # Défense (Tacles)
    'Int_90',   # Anticipation
    'Crs_90',   # Danger provoqué
    '+/-90'     # Influence globale
]


def build_model(df, features=KNN_FEATURES):
    """Entraîne le scaler + KNN sur tout le dataset."""
    df_f = df[[c for c in features if c in df.columns]].fillna(0)
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_f)
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(df_scaled)
    return model, scaler, df_f.columns.tolist()


def find_similar_players(df, player_name, n_neighbors=6,
                         same_position=True, features=KNN_FEATURES):
    """
    Retourne un DataFrame avec les joueurs les plus similaires.

    Parameters
    ----------
    df            : DataFrame nettoyé
    player_name   : str — nom exact du joueur
    n_neighbors   : int — nombre de résultats
    same_position : bool — filtrer par même poste
    features      : list — colonnes utilisées

    Returns
    -------
    DataFrame avec colonnes [Player, Squad, Pos, Comp, Age, Similarity%]
    """
    # Vérifier que le joueur existe
    player_row = df[df['Player'] == player_name]
    if player_row.empty:
        raise ValueError(f"Joueur '{player_name}' introuvable dans le dataset.")

    poste_cible = player_row.iloc[0]['Pos']

    # Filtrer par poste si demandé
    df_work = df[df['Pos'] == poste_cible].copy() if same_position else df.copy()

    if player_name not in df_work['Player'].values:
        raise ValueError(f"'{player_name}' introuvable dans le groupe de poste {poste_cible}.")

    # Préparer les features
    available_features = [c for c in features if c in df_work.columns]
    df_f = df_work[available_features].fillna(0)

    # Scaler + KNN
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_f)

    model = NearestNeighbors(
        n_neighbors=min(n_neighbors + 1, len(df_work)),
        metric='cosine',
        algorithm='brute'
    )
    model.fit(df_scaled)

    # Trouver l'index du joueur dans df_work
    idx = list(df_work['Player'].values).index(player_name)
    distances, indices = model.kneighbors(
        df_scaled[idx].reshape(1, -1)
    )

    # Construire le résultat (exclure le joueur lui-même — indice 0)
    results = []
    for i in range(1, len(indices.flatten())):
        clone = df_work.iloc[indices.flatten()[i]]
        similarity = round((1 - distances.flatten()[i]) * 100, 1)
        results.append({
            'Player':     clone['Player'],
            'Squad':      clone.get('Squad', '—'),
            'Pos':        clone.get('Pos', '—'),
            'Comp':       clone.get('Comp', '—'),
            'Age':        clone.get('Age', '—'),
            'Min':        clone.get('Min', 0),
            'Gls_90':     round(clone.get('Gls_90', 0), 2),
            'Ast_90':     round(clone.get('Ast_90', 0), 2),
            'Similarity': similarity,
        })

    return pd.DataFrame(results)