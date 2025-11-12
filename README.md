# Market Signal Summarizer

An LLM-based application that summarizes financial news from Finnhub News API and SEC EDGAR filings (if free) and integrates with paper trading.

## Architecture

### System Components

- **Frontend:** React with Vite, Tailwind CSS, Axios for API calls, Zustand for state management. Optional use of Bootstrap or Recharts for UI consistency.
- **Backend:** Python with FastAPI for secure communication with Alpaca API and web services. Custom solutions using Starlette and Pydantic for data validation and async operations.
- **Deployment:** Local server using Uvicorn (ASGI) to minimize costs and legal constraints.
- **LLM:** ChatGPT API (via OpenAI) for summarization.

### Application Flow

1. Obtain news from Marketaux API (free version) and (maybe) SEC EDGAR filings API
2. Normalize, dedupe, and link tickers
3. Retrieve relevant passages for queries/tickers (Retrieval-Augmented Generation)
4. Summarize with ChatGPT API
5. Display summaries and signals in React UI
6. Optional paper trade execution via Alpaca API
7. Log trades and track basic P&L locally

## Installation

### Prerequisites

- Node.js (for frontend)
- Python 3.8+ (for backend)
- OpenAI API key (for ChatGPT)
- Marketaux API key (free tier available)
- Alpaca API credentials (for paper trading)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/icombe/market-signal-summarizer.git
   cd market-signal-summarizer
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Install backend dependencies:
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create `.env` file in backend directory
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
   - Add Marketaux API key: `MARKETAUX_API_KEY=your_key_here`
   - Add Alpaca credentials if using paper trading

## Usage

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser to `http://localhost:3000`

### Features

- News ingestion and summarization
- Paper trading integration
- Profit/loss tracking

## Development

### Project Structure

```
market-signal-summarizer/
├── frontend/          # React application
├── backend/           # FastAPI server
├── README.md
└── .gitignore
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Testing

Run tests with:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## License

This project is for educational purposes as part of CSCI/DSCI 470/570.
