import { useState , useEffect } from 'react';
import './App.css';

interface MarketSignal {
  id: number;
  timestamp: string;
  summary: string;
  sentiment: string;
  action: string;
}

interface Position {
  symbol: string;
  qty: number;
  market_value: number;
  unrealized_pl: number;
  unrealized_plpc: number;
  change_today: number;
  change_today_pc: number;
}

interface AccountData {
  equity: number;
  cash: number;
  buying_power: number;
  total_unrealized_pl: number;
}
function App() {
  const [signals, setSignals] = useState<MarketSignal[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [accountData, setAccountData] = useState<AccountData>({
    equity: 0,
    cash: 0,
    buying_power: 0,
    total_unrealized_pl: 0
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [isLoadingPositions, setIsLoadingPositions] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

const generateMarketSignal = async () => {
  setIsGenerating(true);
  try {
    const response = await fetch("http://127.0.0.1:8000/signal");
    const newSignal: MarketSignal = await response.json();

    // console.log('Received signal:', newSignal);
    console.log('Signal details:', {
      id: newSignal.id,
      timestamp: newSignal.timestamp,
      summary: newSignal.summary,
      sentiment: newSignal.sentiment,
      action: newSignal.action
    });

    setSignals([newSignal, ...signals]); // Remove the duplicate
  } catch (error) {
    console.error('Error generating signal:', error);
  } finally {
    setIsGenerating(false);
  }
};

const fetchPositions = async () => {
    setIsLoadingPositions(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/positions');
      const data = await response.json();
      
      setPositions(data.positions || []);
      setAccountData({
        equity: data.equity || 0,
        cash: data.cash || 0,
        buying_power: data.buying_power || 0,
        total_unrealized_pl: data.total_unrealized_pl || 0
      });
      
      console.log('Fetched positions:', data);
    } catch (error) {
      console.error('Error fetching positions:', error);
    } finally {
      setIsLoadingPositions(false);
    }
  };
  // Fetch positions on component mount and set up auto-refresh
  useEffect(() => {
    fetchPositions();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchPositions, 30000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`app-container ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <header className="header">
        <div className="header__content">
          {/* Logo */} 
          <div className="header__logo">
            <div className="logo-placeholder">
              <span className="logo-text">MSS</span>
            </div>
          </div>
          <h1 className="header__title">Market Signal Summarizer</h1>
          
          {/* Dark Mode Toggle */}
          <button 
            className="theme-toggle"
            onClick={toggleDarkMode}
            aria-label="Toggle theme"
          >
            <span className="theme-toggle__text">{isDarkMode ? 'Light' : 'Dark'}</span>
          </button>
        </div>
      </header>

      <main className="app">
        <div className="split-layout">
          {/* Left Half - Generate & History */}
          <div className="left-column">
            <div className="generate-section">
              <button 
                className="generate-button"
                onClick={generateMarketSignal}
                disabled={isGenerating}
              >
                <span className="button__text">
                  {isGenerating ? 'Generating...' : 'Generate Signal'}
                </span>
              </button>
            </div>

            {/* History Section */}
            <div className="history-container">
              <h2>History</h2>
              <div className="history-section">
                <div className="history-list">
                  {signals.length === 0 ? (
                    <p className="empty-state">No signals generated yet. Click the button above to generate your first market signal.</p>
                  ) : (
                    signals.map((signal) => (
                      <div key={signal.id} className="history-item">
                        <div className="history-item__header">
                          <span className="history-item__time">{signal.timestamp}</span>
                          <span className={`history-item__sentiment history-item__sentiment--${signal.sentiment.toLowerCase()}`}>
                            {signal.sentiment}
                          </span>
                        </div>
                        <p className="history-item__summary">{signal.summary}</p>
                        <div className="history-item__action">
                          Action: <strong>{signal.action}</strong>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Right Half - Profit/Loss */}
          <section className="panel panel--right">
            <h2>Portfolio Overview</h2>
            
            {isLoadingPositions && <p className="loading-state">Loading positions...</p>}
            
            <div className="account-summary">
              <div className="summary-card">
                <span className="summary-card__label">Total Equity</span>
                <span className="summary-card__value">${accountData.equity.toFixed(2)}</span>
              </div>
              <div className="summary-card">
                <span className="summary-card__label">Cash</span>
                <span className="summary-card__value">${accountData.cash.toFixed(2)}</span>
              </div>
              <div className="summary-card">
                <span className="summary-card__label">Buying Power</span>
                <span className="summary-card__value">${accountData.buying_power.toFixed(2)}</span>
              </div>
              <div className="summary-card">
                <span className="summary-card__label">Total Unrealized P/L</span>
                <span className={`summary-card__value ${accountData.total_unrealized_pl >= 0 ? 'positive' : 'negative'}`}>
                  {accountData.total_unrealized_pl >= 0 ? '+' : ''}${accountData.total_unrealized_pl.toFixed(2)}
                </span>
              </div>
            </div>

            <div className="positions-section">
              <h3>Positions</h3>
              {positions.length === 0 ? (
                <p className="empty-state">No positions yet. Connect to Alpaca API to view your positions.</p>
              ) : (
                <div className="positions-list">
                  {positions.map((position) => (
                    <div key={position.symbol} className="position-card">
                      <div className="position-card__header">
                        <span className="position-card__symbol">{position.symbol}</span>
                        <span className="position-card__qty">{position.qty} shares</span>
                      </div>
                      <div className="position-card__details">
                        <div className="position-detail">
                          <span className="position-detail__label">Market Value</span>
                          <span className="position-detail__value">${position.market_value.toFixed(2)}</span>
                        </div>
                        <div className="position-detail">
                          <span className="position-detail__label">Unrealized P/L</span>
                          <span className={`position-detail__value ${position.unrealized_pl >= 0 ? 'positive' : 'negative'}`}>
                            {position.unrealized_pl >= 0 ? '+' : ''}${position.unrealized_pl.toFixed(2)} 
                            ({position.unrealized_plpc >= 0 ? '+' : ''}{(position.unrealized_plpc * 100).toFixed(2)}%)
                          </span>
                        </div>
                        <div className="position-detail">
                          <span className="position-detail__label">Intraday P/L</span>
                          <span className={`position-detail__value ${position.change_today >= 0 ? 'positive' : 'negative'}`}>
                            {position.change_today >= 0 ? '+' : ''}${position.change_today.toFixed(2)} 
                            ({position.change_today_pc >= 0 ? '+' : ''}{(position.change_today_pc * 100).toFixed(2)}%)
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;