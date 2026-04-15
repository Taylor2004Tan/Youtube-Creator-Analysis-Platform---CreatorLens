# CreatorLens

CreatorLens is a Flask-powered YouTube creator analytics dashboard that combines YouTube Data API insights with VADER sentiment analysis. The app helps creators, marketers, and collaboration managers discover audience sentiment, explore recommended channels by category, and analyze the latest video comment trends for collaboration decisions.

## 🚀 Features

- Search YouTube channels by keyword
- Browse curated creator categories like Technology, Gaming, Education, Lifestyle, Finance, and Health & Fitness
- Resolve creator handles to full channel profiles
- Analyze a creator's latest videos and comments for sentiment distribution
- Generate collaboration recommendations using AI-powered sentiment scoring
- Responsive single-page frontend with Chart.js visualizations

## 🧰 Tech Stack

- Python 3.13+
- Flask
- Flask-CORS
- Google YouTube Data API v3
- VADER sentiment analysis
- Vanilla JavaScript frontend
- Chart.js for charts

## 📁 Project Structure

- `app.py` — Flask application and route registration
- `run.py` — startup script with Python version check
- `config.py` — loads environment variables
- `api/` — Flask API blueprints for search, categories, and analysis
- `services/` — YouTube API client, sentiment analysis, and recommendation logic
- `static/` — CSS, JavaScript, and frontend views
- `templates/` — main HTML entry point

## ⚙️ Setup

1. Clone the repository:

```bash
git clone <repo-url>
cd "YTcreator analyzer"
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# Windows Command Prompt
venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your YouTube API key in a `.env` file:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

## ▶️ Run

Start the app with:

```bash
python run.py
```

Then open:

```text
http://localhost:5000
```

## 🧪 API Endpoints

- `GET /api/search?q=<query>` — search channels by keyword
- `GET /api/categories` — list curated category summaries
- `GET /api/categories/<category_name>` — get creators in a category
- `GET /api/resolve/<handle>` — resolve a YouTube @handle to channel info
- `POST /api/analyze` — analyze a channel and sentiment across recent comments

## 🔍 Analysis Workflow

1. Pick a creator from search or category listings
2. Send the selected channel to `/api/analyze`
3. The backend fetches:
   - channel details
   - latest videos
   - top comments per video
4. Sentiment is calculated and aggregated with VADER
5. A collaboration recommendation is returned based on overall sentiment

## 💡 Notes

- Requires a valid YouTube Data API key
- The frontend is designed as a lightweight SPA with dynamic route loading
- The sentiment analyzer uses `vaderSentiment` and classifies comments as positive, neutral, or negative

## 🔧 Troubleshooting

- If the app fails to start, verify the `.env` file contains `YOUTUBE_API_KEY`
- Confirm Python version is `3.13+`
- If YouTube requests fail, check API quota and key permissions

---

Happy building! 🎯