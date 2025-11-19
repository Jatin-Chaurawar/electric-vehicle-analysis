import pandas as pd

def test_processed_exists():
    df = pd.read_csv("data/processed/ev_population_features.csv")
    assert df.shape[0] > 0

def test_no_duplicate_ids():
    df = pd.read_csv("data/processed/ev_population_features.csv")
    if "DOL Vehicle ID" in df.columns:
        assert df["DOL Vehicle ID"].duplicated().sum() == 0
