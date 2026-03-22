# Agentic AI Data Usage Advisor for Next-Generation Networks

An intelligent AI agent that analyzes your internet usage patterns and provides personalized recommendations to optimize data consumption.

---

## Features

- Predicts daily data usage (GB) using a Linear Regression model
- Classifies risk level: Low / Medium / High
- Generates natural language advice tailored to your habits
- What-if simulations: "What if I stop streaming?"
- Conversational CLI chat interface
- Optional Flask REST API

---

## Project Structure

```
├── agent.py          # Main conversational agent (CLI)
├── model.py          # ML model training & prediction
├── advisor.py        # AI decision engine + text generation
├── app.py            # Optional Flask REST API
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the CLI agent

```bash
python agent.py
```

You'll see an interactive prompt:

```
> analyze       # enter your usage details and get advice
> whatif        # see what-if simulations
> history       # review this session's analyses
> help          # list commands
> quit          # exit
```

### 3. (Optional) Run the Flask API

```bash
python app.py
```

Then POST to `http://localhost:5000/analyze`:

```json
{
  "daily_hours": 6,
  "streams_video": 1,
  "num_downloads": 5,
  "social_media_hours": 2
}
```

Response:

```json
{
  "predicted_gb": 12.4,
  "risk_level": "High",
  "advice": "Your estimated data usage is 12.4 GB due to video streaming...",
  "whatif_scenarios": [...]
}
```

---

## How It Works

### ML Model (`model.py`)
- Trains a `LinearRegression` model on synthetic usage data
- Features: daily hours, video streaming (0/1), downloads, social media hours
- Model and scaler are saved as `.pkl` files on first run

### Advisor (`advisor.py`)
- Classifies risk: Low (<3 GB), Medium (3–8 GB), High (>8 GB)
- Identifies usage drivers (streaming, downloads, social media)
- Generates targeted natural language suggestions
- Runs what-if scenarios by re-predicting with modified inputs

### Agent (`agent.py`)
- Conversational loop with session history
- Color-coded risk output in terminal

---

## Example Output

```
==============================
  Predicted Data Usage : 13.7 GB / day
  Risk Level           : High
==============================

Your estimated data usage is 13.7 GB due to video streaming, frequent downloads.
This is quite high and may lead to data cap issues or increased costs.

Suggestions:
  1. Switch video streaming quality to 480p or 720p instead of HD/4K —
     this alone can cut streaming data usage by up to 70%.
  2. You're downloading 8 files per day. Try batching downloads during
     off-peak hours or using a download manager to avoid duplicates.
```

---

## License

MIT — see [LICENSE](LICENSE)
