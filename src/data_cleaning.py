# src/data_cleaning.py
from pathlib import Path
import pandas as pd
import numpy as np

def read_raw(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_").replace(".", "").replace("-", "_"))
    return df

def parse_dates(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce')
    return df

def drop_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"dropped {before-after} exact duplicates")
    return df

def standardize_types(df: pd.DataFrame):
    # Example: if VIN exists, make it string
    for col in df.select_dtypes(include=['int64']).columns:
        # keep ints as is usually; add rules as needed
        pass
    # Example categorical cast:
    for col in ['make','model','fuel_type'] if 'make' in df.columns else []:
        df[col] = df[col].astype('string')
    return df

def flag_missing_pct(df: pd.DataFrame) -> pd.DataFrame:
    # Add missing percentage per row (optionally)
    df['_missing_pct'] = df.isna().mean(axis=1)
    return df

def handle_missing_simple(df: pd.DataFrame) -> pd.DataFrame:
    # PRINCIPLE: don't blindly fill everything. Use domain rules.
    # Example rules (modify for your dataset):
    if 'odometer' in df.columns:
        df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')
        # if odometer obviously zero or negative -> set NaN
        df.loc[df['odometer'] <= 0, 'odometer'] = np.nan

    # Fill small, safe defaults for columns where missing means 'unknown'
    for c in ['color','trim'] if 'color' in df.columns else []:
        df[c] = df[c].fillna("unknown")
    return df

def remove_outliers_iqr(df: pd.DataFrame, col: str, k: float = 1.5) -> pd.DataFrame:
    if col not in df.columns: 
        return df
    x = pd.to_numeric(df[col], errors='coerce')
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    mask = (x >= lower) & (x <= upper) | x.isna()
    print(f"{col}: dropping {(~mask).sum()} outliers")
    return df.loc[mask].copy()

def feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
    # Example time features
    if 'registration_date' in df.columns:
        df['reg_year'] = df['registration_date'].dt.year
        df['reg_month'] = df['registration_date'].dt.month
    # Example age (if model_year exists)
    if 'manufacture_year' in df.columns:
        current_year = pd.Timestamp.now().year
        df['vehicle_age'] = current_year - pd.to_numeric(df['manufacture_year'], errors='coerce')
    # Example aggregate: grouped counts later in analysis
    return df

def save_processed(df: pd.DataFrame, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print("Saved processed to", out_path)

def full_clean(raw_path: Path, out_path: Path):
    df = read_raw(raw_path)
    df = clean_column_names(df)
    # pick date columns by name heuristics
    date_cols = [c for c in df.columns if 'date' in c or 'reg' in c]
    df = parse_dates(df, date_cols)
    df = drop_exact_duplicates(df)
    df = standardize_types(df)
    df = flag_missing_pct(df)
    df = handle_missing_simple(df)
    # remove outliers for numeric columns you trust
    for num_col in ['odometer','range_km','battery_capacity'] if 'odometer' in df.columns else []:
        df = remove_outliers_iqr(df, num_col)
    df = feature_engineer(df)
    save_processed(df, out_path)
    return df

if __name__ == "__main__":
    ROOT = Path(__file__).parents[1]
    raw = ROOT/"data"/"raw"/"Electric_Vehicle_Population_Data.csv"
    out = ROOT/"data"/"processed"/"ev_population_clean.csv"
    full_clean(raw, out)
