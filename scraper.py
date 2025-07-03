# scraper.py

from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta
import time

def fetch_trending_routes(origin, destination):
    kw = f"{origin} to {destination} flight"

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        time.sleep(3)  # Add delay to avoid 429 rate limit
        pytrends.build_payload([kw], cat=0, timeframe='today 3-m', geo='AU', gprop='')
        data = pytrends.interest_over_time()

        if data.empty or 'isPartial' not in data:
            print("⚠️ No trend data returned. Using fallback.")
            return generate_mock_data()

        data = data.reset_index()
        data = data.rename(columns={kw: "interest"})
        return data[["date", "interest"]]

    except Exception as e:
        print(f"❌ pytrends failed: {e}")
        return generate_mock_data()

def generate_mock_data():
    today = datetime.today()
    dates = [today - timedelta(days=i) for i in range(30)][::-1]
    interest = [max(20 + (i % 15), 0) for i in range(30)]
    return pd.DataFrame({
        "date": dates,
        "interest": interest
    })
