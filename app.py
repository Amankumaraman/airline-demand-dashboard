# app.py

import streamlit as st
import pandas as pd
from scraper import fetch_trending_routes
from processor import analyze_demand
from insights import generate_insight
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Airline Market Demand Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Australian airport codes with city names
AIRPORT_CODES = {
    "SYD": "Sydney (Kingsford Smith)",
    "MEL": "Melbourne (Tullamarine)",
    "BNE": "Brisbane",
    "PER": "Perth",
    "ADL": "Adelaide",
    "CBR": "Canberra",
    "OOL": "Gold Coast",
    "HBA": "Hobart",
    "LST": "Launceston",
    "CNS": "Cairns",
    "TSV": "Townsville",
    "AVV": "Melbourne (Avalon)",
    "MCY": "Sunshine Coast",
    "DRW": "Darwin",
    "PPP": "Proserpine (Whitsunday Coast)",
    "HTI": "Hamilton Island",
    "MKY": "Mackay",
    "ROK": "Rockhampton",
    "BME": "Broome",
    "KTA": "Karratha",
    "PHE": "Port Hedland",
    "ZNE": "Newman",
    "KNX": "Kununurra",
    "GET": "Geraldton",
    "BQB": "Busselton",
    "ALH": "Albany",
    "KGI": "Kalgoorlie",
    "PBO": "Paraburdoo",
    "LEA": "Learmonth",
    "NTL": "Newcastle",
    "ABX": "Albury",
    "WGA": "Wagga Wagga",
    "DBO": "Dubbo",
    "CFS": "Coffs Harbour",
    "BHS": "Bathurst",
    "TMW": "Tamworth",
    "ARM": "Armidale",
    "PQQ": "Port Macquarie",
    "TRO": "Taree",
    "LRE": "Longreach"
}

# ---------- Custom Styling ---------- #
st.markdown("""
    <style>
        :root {
            --primary: #2563eb;
            --primary-light: #3b82f6;
            --secondary: #7c3aed;
            --dark: #1e293b;
            --light: #f8fafc;
            --gray: #94a3b8;
            --success: #10b981;
        }
        
        .main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }
        
        .main-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--dark);
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: var(--gray);
            margin-bottom: 2.5rem;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 2.5rem 0 1rem 0;
            color: var(--dark);
            position: relative;
            padding-bottom: 0.5rem;
        }
        
        .section-title:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 2px;
        }
        
        .card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
        }
        
        .ai-box {
            background: linear-gradient(135deg, #f9fafb, #f3f4f6);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            color: var(--dark);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            line-height: 1.6;
        }
        
        .footer {
            color: var(--gray);
            margin-top: 4rem;
            font-size: 0.9rem;
            text-align: center;
            padding: 1.5rem 0;
            border-top: 1px solid #e2e8f0;
        }
        
        .stButton>button {
            background: linear-gradient(90deg, var(--primary), var(--primary-light));
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        
        .stSelectbox>div>div>select {
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
        }
        
        .stSuccess {
            background-color: #ecfdf5 !important;
            color: #065f46 !important;
            border-radius: 8px !important;
        }
        
        .stSpinner>div {
            border-top-color: var(--primary) !important;
        }
        
        /* Custom table styling */
        .dataframe {
            width: 100%;
            border-collapse: collapse;
            font-family: sans-serif;
            box-shadow: 0 0 0 1px #e2e8f0;
            border-radius: 8px !important;
            overflow: hidden;
        }
        
        .dataframe thead {
            background: linear-gradient(90deg, var(--primary), var(--primary-light));
            color: white;
        }
        
        .dataframe th {
            padding: 0.75rem 1rem;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
        }
        
        .dataframe td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #e2e8f0;
            font-size: 0.875rem;
        }
        
        .dataframe tr:hover {
            background-color: #f8fafc;
        }
        
        .dataframe tr:nth-child(even) {
            background-color: #f8fafc;
        }
        
        /* Custom scrollbar for table */
        .dataframe-container {
            max-height: 400px;
            overflow-y: auto;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        
        .dataframe-container::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        .dataframe-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        .dataframe-container::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        
        .dataframe-container::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        
        /* Airport code dropdown styling */
        .airport-select-container {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .airport-code {
            font-weight: 700;
            color: var(--primary);
        }
        
        .airport-city {
            font-size: 0.85rem;
            color: var(--gray);
        }
    </style>
""", unsafe_allow_html=True)

def format_airport_name(code):
    """Format airport code with city name for dropdown display"""
    return f"{code} - {AIRPORT_CODES[code]}"

# ---------- Main Container ---------- #
with st.container():
    # ---------- Header ---------- #
    st.markdown("<div class='main-title'>Airline Market Demand Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analyze flight demand trends between Australian cities to optimize your hospitality strategy with data-driven insights</div>", unsafe_allow_html=True)
    
    # ---------- Input Form Card ---------- #
    with st.form("input_form"):
        st.markdown("<div class='section-title'>Route Selection</div>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                origin = st.selectbox(
                    "Origin Airport",
                    options=list(AIRPORT_CODES.keys()),
                    index=0,  # Default to SYD
                    format_func=format_airport_name,
                    help="Select origin airport"
                )
                st.markdown(f"""
                    <div class='airport-select-container'>
                        <div class='airport-code'>{origin}</div>
                        <div class='airport-city'>{AIRPORT_CODES[origin]}</div>
                    </div>
                """, unsafe_allow_html=True)
                
            with col2:
                destination = st.selectbox(
                    "Destination Airport",
                    options=[code for code in AIRPORT_CODES.keys() if code != origin],
                    index=1 if origin != "MEL" else 0,  # Default to MEL if not origin
                    format_func=format_airport_name,
                    help="Select destination airport"
                )
                st.markdown(f"""
                    <div class='airport-select-container'>
                        <div class='airport-code'>{destination}</div>
                        <div class='airport-city'>{AIRPORT_CODES[destination]}</div>
                    </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.write("")  # Empty column for spacing
                submitted = st.form_submit_button("Analyze Market Demand", 
                                              help="Fetch and analyze demand data for this route")
    
    # ---------- Results Section ---------- #
    if submitted:
        with st.spinner(f"Fetching trends for {origin}-{destination} route..."):
            df = fetch_trending_routes(origin, destination)
            trend_df = analyze_demand(df)
            insight = generate_insight(trend_df.to_dict(orient="records"))
        
        st.success(f"Successfully analyzed {origin}-{destination} route with {len(df)} data points!")
        
        # ---------- Route Summary ---------- #
        with st.container():
            st.markdown(f"""
                <div style="background: linear-gradient(90deg, #f8fafc, #f1f5f9);
                         padding: 1rem;
                         border-radius: 8px;
                         margin: 1rem 0 2rem 0;
                         border-left: 4px solid var(--primary);">
                    <div style="font-size: 1.1rem; font-weight: 600; color: var(--dark);">
                        Route: <span style="color: var(--primary);">{origin}</span> → 
                        <span style="color: var(--primary);">{destination}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: var(--gray);">
                        {AIRPORT_CODES[origin]} to {AIRPORT_CODES[destination]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # ---------- Metrics Row ---------- #
        with st.container():
            cols = st.columns(4)
            metrics = [
                ("Total Data Points", f"{len(df):,}", "Observations"),
                ("Peak Interest", f"{trend_df['interest'].max():.0f}%", "Highest search volume"),
                ("Current Interest", f"{trend_df['interest'].iloc[-1]:.0f}%", "Latest search volume"),
                ("Avg. Interest", f"{trend_df['interest'].mean():.0f}%", "Historical average")
            ]
            
            for col, (title, value, delta) in zip(cols, metrics):
                with col:
                    st.metric(title, value, delta)
        
        # ---------- Raw Data Card ---------- #
        with st.container():
            st.markdown("<div class='section-title'>Google Trends Data</div>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
                st.dataframe(df.style.format({
                    'interest': '{:.0f}%',
                    'date': lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else ''
                }).applymap(
                    lambda x: 'color: #2563eb' if isinstance(x, (int, float)) else '', 
                    subset=['interest']
                ), 
                use_container_width=True,
                height=400)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # ---------- Visualization Card ---------- #
        with st.container():
            st.markdown("<div class='section-title'>Search Interest Trend</div>", unsafe_allow_html=True)
            with st.container():
                st.line_chart(trend_df.set_index("date")["interest"], 
                             use_container_width=True,
                             color="#2563eb")
        
        # ---------- Insights Card ---------- #
        with st.container():
            st.markdown("<div class='section-title'>Market Intelligence</div>", unsafe_allow_html=True)
            with st.container():
                st.markdown(f"<div class='ai-box'>{insight}</div>", unsafe_allow_html=True)

# ---------- Footer ---------- #
st.markdown("""
<div class='footer'>
    <div style="margin-bottom: 0.5rem;">✈️ Built by Aman Kumar</div>
    <div style="font-size: 0.8rem; color: #cbd5e1;">Powered by Streamlit, Google Trends, and Groq AI</div>
</div>
""", unsafe_allow_html=True)