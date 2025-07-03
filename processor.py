def analyze_demand(df):
    df["7d_avg"] = df["interest"].rolling(window=7).mean()
    return df
