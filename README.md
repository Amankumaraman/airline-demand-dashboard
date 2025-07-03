# Airline Booking Market Demand Dashboard

This is a Python web application that fetches, processes, and visualizes market demand trends for airline bookings between Australian cities. The app scrapes publicly available Google Trends data, processes it to reveal insights, and uses AI to generate market intelligence summaries. The UI is built with Streamlit for an easy-to-use, interactive experience.

---

## Features

* Fetch airline booking demand trends using Google Trends data
* Analyze and visualize search interest over time
* Generate AI-driven insights on demand patterns and popular routes
* Simple input form for origin and destination airports
* Interactive charts and data tables
* Fully free and open-source solution using public data and APIs

---

## Demo

> [Live Demo on Streamlit Cloud](https://your-streamlit-demo-link)

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Amankumaraman/airline-demand-dashboard.git
cd airline-demand-dashboard
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file with your AI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

*Note:* The Google Trends data scraping uses the free `pytrends` library and does not require API keys.

---

## Usage

Run the app locally with:

```bash
streamlit run app.py
```

Open the provided URL (usually `http://localhost:8501`) in your browser.
Enter the origin and destination airport codes (e.g., SYD and MEL), and click **Analyze Market Demand** to fetch, analyze, and view airline booking trends and AI insights.

---

## Project Structure

* `app.py` — Main Streamlit app
* `scraper.py` — Fetches Google Trends data
* `processor.py` — Processes and analyzes trend data
* `insights.py` — Generates AI insights from processed data
* `.env` — Environment variables for API keys (not included in repo)
* `requirements.txt` — Python dependencies

---

## Technologies

* Python 3.10+
* Streamlit (web UI)
* Pytrends (Google Trends API)
* OpenAI / Groq AI (for AI-generated insights)
* Pandas (data processing)

---

## License

This project is open source and available under the MIT License.

---

If you want, I can help generate your actual `requirements.txt` and push your repo content to GitHub with this README ready to go!
