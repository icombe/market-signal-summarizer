# Market Signal Summarizer

An AI-powered financial analysis tool that aggregates market news, generates concise summaries using LLMs, and provides actionable trading insights. The application integrates with the Alpaca API for paper trading and portfolio management.

## 🚀 Features

- **AI-Driven Summarization:** Uses OpenAI's GPT models to summarize complex financial news articles into actionable insights.
- **Real-Time Market Data:** Fetches the latest financial news via the Marketaux API.
- **Sentiment Analysis:** Analyzes news sentiment to gauge market trends.
- **Paper Trading Integration:** Connects with Alpaca to simulate trades based on generated signals.
- **Interactive Dashboard:** A modern React-based frontend to view summaries, signals, and portfolio performance.

## 🛠️ Tech Stack

### Frontend
- **Framework:** React (with Vite)
- **Language:** TypeScript

### Backend
- **Framework:** FastAPI (Python)
- **AI/LLM:** OpenAI API
- **Data Sources:** Marketaux API (News), Alpaca API (Trading)
- **Scraping:** Trafilatura
- **Server:** Uvicorn

## 📦 Installation

### Prerequisites
- Node.js (LTS version recommended)
- Python 3.8+
- API Keys for:
  - OpenAI
  - Marketaux
  - Alpaca (Paper Trading)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the `backend` directory with the following keys:
   ```env
   OPENAI_API_KEY=your_openai_key
   MARKETAUX_API_KEY=your_marketaux_key
   ALPACA_API_KEY=your_alpaca_key
   ALPACA_SECRET_API_KEY=your_alpaca_secret
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## 🏃‍♂️ Usage

1. **Start the Backend Server:**
   ```bash
   # From the backend directory
   python frontendApiMain.py
   ```
   The API will run on `http://localhost:8000` (or the port specified in the console).

2. **Start the Frontend Application:**
   ```bash
   # From the frontend directory
   npm run dev
   ```
   Open the provided localhost URL (usually `http://localhost:5173`) in your browser.

3. **Generate Signals:**
   - Click the "Generate Prediction" button on the dashboard.
   - The system will fetch the latest news, summarize it, and display trading recommendations.

## 📄 License

This project is licensed under the MIT License.
