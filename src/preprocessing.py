import pandas as pd

def load_raw_data(path='../data/data.csv'):
    return pd.read_csv(path)


def audit_data(df):
    """Affiche un rapport sur les valeurs nulles et types."""
    report = pd.DataFrame({
        'Type':            df.dtypes,
        'Valeurs Nulles':  df.isnull().sum(),
        '% Nulles':        (df.isnull().sum() / len(df)) * 100,
        'Valeurs Uniques': df.nunique()
    })
    return report


def clean_data(df):
    """Pipeline de nettoyage complet."""

    # 1. Supprimer colonnes redondantes (stats, Born)
    cols_to_drop = [c for c in df.columns if 'stats' in c or 'Born' in c]
    df = df.drop(columns=cols_to_drop)

    # 2. Exclure les gardiens
    df = df[df['Pos'] != 'GK']

    # 3. Supprimer colonnes entièrement nulles
    df = df.dropna(axis=1, how='all')

    # 4. Supprimer colonnes non pertinentes
    cols_to_drop = ['Rk', 'OG', 'unSub', 'Mn/Start']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=False)

    # 5. Garder uniquement joueurs fiables (> 900 min)
    df = df[df['Min'] >= 900]

    # 6. Remplir NaN numériques par 0
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    return df


def add_per90_features(df):
    """Feature engineering — créer les stats par 90 minutes."""
    cols_to_normalize = ['Gls', 'Ast', 'Sh', 'SoT', 'Int', 'TklW', 'Crs']
    for col in cols_to_normalize:
        if col in df.columns:
            df[f'{col}_90'] = (df[col] / df['Min']) * 90
    return df


def run_pipeline(input_path='../data/data.csv',
                 output_path='../data/football_data_cleaned.csv'):
    """Lance le pipeline complet et sauvegarde."""
    df = load_raw_data(input_path)
    df = clean_data(df)
    df = add_per90_features(df)
    df.to_csv(output_path, index=False)
    print(f"✅ Done — {df.shape[0]} players, {df.shape[1]} columns saved to {output_path}")
    return df


if __name__ == '__main__':
    run_pipeline()