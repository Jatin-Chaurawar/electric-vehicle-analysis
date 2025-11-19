from pathlib import Path
import pandas as pd
import numpy as np

def add_time_features(df, date_col="Registration Date"):
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df["reg_year"] = df[date_col].dt.year
        df["reg_month"] = df[date_col].dt.month
        df["reg_quarter"] = df[date_col].dt.to_period("Q").astype(str)
    return df

def add_age_feature(df, manufacture_col="Model Year"):
    if manufacture_col in df.columns:
        current_year = pd.Timestamp.now().year
        df["vehicle_age"] = current_year - pd.to_numeric(df[manufacture_col], errors='coerce')
    return df

def add_make_aggregations(df):
    if "Make" in df.columns:
        make_counts = df.groupby("Make").size().rename("make_count")
        make_mean_range = df.groupby("Make")["Electric Range"].mean().rename("make_avg_range")
        df = df.join(make_counts, on="Make")
        df = df.join(make_mean_range, on="Make")
    return df

def add_state_aggregations(df):
    if "State" in df.columns:
        state_counts = df.groupby("State").size().rename("state_ev_count")
        df = df.join(state_counts, on="State")
    return df

def build_features(input_path, output_path):
    df = pd.read_csv(input_path)
    df = add_time_features(df)
    df = add_age_feature(df)
    df = add_make_aggregations(df)
    df = add_state_aggregations(df)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print("Saved features to", output_path)
    return df

if __name__ == "__main__":
    ROOT = Path(__file__).parents[1]
    raw = ROOT/"data"/"processed"/"ev_population_imputed.csv"
    out = ROOT/"data"/"processed"/"ev_population_features.csv"
    build_features(raw, out)
