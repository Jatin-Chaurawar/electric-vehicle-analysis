from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer

def missing_report(df: pd.DataFrame, show_top: int = 20):
    miss_col = df.isna().mean().sort_values(ascending=False)
    print("Missingness per column (top):")
    print(miss_col.head(show_top).to_string())
    miss_row = (df.isna().mean(axis=1)).value_counts().sort_index()
    print("\nMissingness per row (fraction counts):")
    print(miss_row.head(20).to_string())
    return miss_col

def drop_high_missing_columns(df: pd.DataFrame, thresh: float = 0.8):
    """
    Drop columns with more than thresh fraction of missing values.
    """
    miss = df.isna().mean()
    to_drop = miss[miss > thresh].index.tolist()
    if to_drop:
        print(f"Dropping {len(to_drop)} columns with >{thresh*100:.0f}% missing: {to_drop}")
        df = df.drop(columns=to_drop)
    return df, to_drop

def create_missing_flags(df: pd.DataFrame, cols: list):
    for c in cols:
        flag = c + "_was_missing"
        df[flag] = df[c].isna().astype(int)
    return df

def impute_numeric_groupwise(df: pd.DataFrame, col: str, groupby: str, method: str = "median"):
    """
    Impute numeric column 'col' using the group's statistic (median or mean).
    If group statistic is missing, fallback to global median.
    """
    if col not in df.columns or groupby not in df.columns:
        return df
    stat = df.groupby(groupby)[col].transform(
        lambda x: x.median() if method == "median" else x.mean()
    )
    fallback = df[col].median()
    df[col] = df[col].fillna(stat).fillna(fallback)
    return df

def simple_impute_numeric(df: pd.DataFrame, cols: list, strategy: str = "median"):
    imputer = SimpleImputer(strategy=strategy)
    df[cols] = imputer.fit_transform(df[cols])
    return df

def knn_impute(df: pd.DataFrame, cols: list, n_neighbors: int = 5):
    """
    KNN imputer for a subset of numeric cols (and any numeric predictors).
    cols: list of numeric columns to impute; this function will try to use all numeric cols as predictors.
    """
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    use_cols = sorted(set(cols).intersection(numeric))
    if not use_cols:
        return df
    imputer = KNNImputer(n_neighbors=n_neighbors)
    subset = df[numeric]
    imputed = imputer.fit_transform(subset)
    df[numeric] = pd.DataFrame(imputed, columns=numeric, index=df.index)
    return df

def iterative_impute(df: pd.DataFrame, cols: list, max_iter: int = 10):
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    use_cols = sorted(set(cols).intersection(numeric))
    if not use_cols:
        return df
    imputer = IterativeImputer(max_iter=max_iter, random_state=42)
    subset = df[numeric]
    imputed = imputer.fit_transform(subset)
    df[numeric] = pd.DataFrame(imputed, columns=numeric, index=df.index)
    return df

def impute_categorical_mode(df: pd.DataFrame, cols: list, groupby: str = None):
    for c in cols:
        if c not in df.columns:
            continue
        if groupby and groupby in df.columns:
            # fill with group mode if possible
            modes = df.groupby(groupby)[c].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
            df[c] = df.apply(lambda r: modes.get(r[groupby], np.nan) if pd.isna(r[c]) else r[c], axis=1)
            df[c] = df[c].fillna(df[c].mode().iloc[0] if not df[c].mode().empty else "unknown")
        else:
            mode = df[c].mode()
            fill = mode.iloc[0] if not mode.empty else "unknown"
            df[c] = df[c].fillna(fill)
    return df

def run_imputation_pipeline(raw_path: Path, out_path: Path):
    df = pd.read_csv(raw_path)
    # 1. report
    miss_col = missing_report(df)

    # 2. drop high-missing columns (optional threshold)
    df, dropped = drop_high_missing_columns(df, thresh=0.9)  # change threshold as needed

    # 3. choose candidate columns to impute
    # numeric candidates (example heuristics)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # categorical candidates
    cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

    # 4. create flags for the columns we will impute
    to_impute_num = [c for c in numeric_cols if df[c].isna().sum() > 0]
    to_impute_cat = [c for c in cat_cols if df[c].isna().sum() > 0]
    df = create_missing_flags(df, to_impute_num + to_impute_cat)

    # 5. group-wise imputation example: try to impute numeric cols by 'make' if exists
    group_by = "make" if "make" in df.columns else None
    for col in to_impute_num:
        if group_by:
            df = impute_numeric_groupwise(df, col, groupby=group_by, method="median")

    # 6. still-missing numerics -> iterative imputer
    still_missing_num = [c for c in to_impute_num if df[c].isna().sum() > 0]
    if still_missing_num:
        try:
            df = iterative_impute(df, still_missing_num)
        except Exception as e:
            print("Iterative imputer failed:", e)
            # fallback to KNN
            df = knn_impute(df, still_missing_num)

    # 7. categorical impute
    df = impute_categorical_mode(df, to_impute_cat, groupby=group_by)

    # 8. verify
    print("\nAfter imputation missing counts:")
    print(df[to_impute_num + to_impute_cat].isna().sum())

    # 9. save
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print("Saved imputed dataset to:", out_path)
    return df

if __name__ == "__main__":
    BASE = Path(__file__).parents[1]
    raw = BASE/"data"/"raw"/"Electric_Vehicle_Population_Data.csv"
    out = BASE/"data"/"processed"/"ev_population_imputed.csv"
    run_imputation_pipeline(raw, out)
