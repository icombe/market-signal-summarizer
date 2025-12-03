import { useState , useEffect } from 'react';
import './App.css';



interface TickerRecommendation {
  ticker: string;
  recommended_action: string;
}

interface MarketSignal {
  id: number;
  timestamp: string;
  summary: string;
  sentiment: string;
  ticker_recommendations: TickerRecommendation[];
}

interface Position {
  symbol: string;
  qty: number;
  market_value: number;
  unrealized_pl: number;
  unrealized_plpc: number;
  change_today: number;
  change_today_pc: number;
  price_per_share: number;
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
  
  // Trading form state
  const [ticker, setTicker] = useState('');
  const [amount, setAmount] = useState('');
  const [isTrading, setIsTrading] = useState(false);
  //notifications
  const [notification, setNotification] = useState<string>('');


  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const generateMarketSignal = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/signal");
      const newSignals: MarketSignal[] = await response.json();

      console.log('=== NEW SIGNALS FROM API ===');
      newSignals.forEach(sig => {
        console.log("Signal:", sig.id, sig.timestamp);
      });

      setSignals(prevSignals => {
        console.log('=== PREVIOUS SIGNALS ===');
        prevSignals.forEach(s => console.log("Prev:", s.id, s.timestamp));
        
        const existingKeys = new Set(prevSignals.map(s => `${s.id}-${s.timestamp}`));
        console.log('Existing keys:', Array.from(existingKeys));
        
        const uniqueNewSignals = newSignals.filter(s => {
          const key = `${s.id}-${s.timestamp}`;
          const isDupe = existingKeys.has(key);
          console.log(`Checking ${key}: ${isDupe ? 'DUPLICATE' : 'UNIQUE'}`);
          return !isDupe;
        });
        
        console.log('=== UNIQUE NEW SIGNALS ===', uniqueNewSignals.length);
        
        return [...uniqueNewSignals, ...prevSignals];
      });
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

  const handleTrade = async (action: 'buy' | 'sell') => {
    if (!ticker || !amount || isTrading) return;
    
    const amountNum = parseFloat(amount);
    if (isNaN(amountNum) || amountNum <= 0) {
      setNotification('Please enter a valid amount');
      setTimeout(() => setNotification(''), 3000);
      return;
    }

    setIsTrading(true);
    try {
      const endpoint = action === 'buy' 
        ? 'http://127.0.0.1:8000/place-order'
        : 'http://127.0.0.1:8000/sell-order';
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ticker: ticker.toUpperCase(),
          amount: amountNum
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `${action} order failed`);
      }

      const result = await response.json();
      console.log('Trade result:', result);
      
      // Clear form and refresh positions
      setTicker('');
      setAmount('');
      await fetchPositions();
      
      setNotification(
      `Successfully ${action === 'buy' ? 'bought' : 'sold'} $${amountNum} of ${ticker.toUpperCase()}`
      );

      setTimeout(() => setNotification(''), 4000);

    } catch (error) {
      console.error('Trade error:', error);
      setNotification(
      `Trade failed: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
      setTimeout(() => setNotification(''), 4000);

    } finally {
      setIsTrading(false);
    }
  };

  // Fetch positions on component mount and set up auto-refresh
  useEffect(() => {
    fetchPositions();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchPositions, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const isFormValid = ticker.trim() !== '' && amount && parseFloat(amount) > 0;

  return (
    
    <div className={`app-container ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      {notification && (
    <div className="notification">
      {notification}
    </div>
    )}

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
              <div className="history-list">
                  {signals.length === 0 ? (
                    <p className="empty-state">
                      No signals generated yet. Click the button above to generate your first market signal.
                    </p>
                  ) : (
                    signals.map((signal, index) => (
                      <div key={`${signal.id}-${signal.timestamp}-${index}`} className="history-item">
                        <div className="history-item__header">
                          <span className="history-item__time">{signal.timestamp}</span>
                          <span
                            className={`history-item__sentiment history-item__sentiment--${signal.sentiment.toLowerCase()}`}
                          >
                            {signal.sentiment}
                          </span>
                        </div>
                        <p className="history-item__summary">{signal.summary}</p>
                        <div className="history-item__actions">
                          {signal.ticker_recommendations.length === 0 ? (
                            <div>No ticker recommendations</div>
                          ) : (
                            signal.ticker_recommendations.map((rec) => (
                              <div key={rec.ticker} className="ticker-card">
                                <div className="ticker-symbol">{rec.ticker}</div>
                                <div className={`ticker-action ${rec.recommended_action.toLowerCase()}`}>
                                  {rec.recommended_action.toUpperCase()}
                                </div>
                              </div>
                            ))
                          )}
                        </div>
                      </div>
                    ))
                )}
              </div>
            </div>
          </div>

          {/* Right Half - Portfolio Overview */}
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

            {/* Trading Interface */}
            <div className="trading-interface">
              <h3>Trade</h3>
              <div className="trading-form">
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Ticker Symbol</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="e.g., AAPL"
                      value={ticker}
                      onChange={(e) => setTicker(e.target.value.toUpperCase())}
                      disabled={isTrading}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Amount ($)</label>
                    <input
                      type="number"
                      className="form-input"
                      placeholder="e.g., 100.00"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      min="0"
                      step="0.01"
                      disabled={isTrading}
                    />
                  </div>
                </div>
                <div className="trading-buttons">
                  <button
                    className="trade-button trade-button--buy"
                    onClick={() => handleTrade('buy')}
                    disabled={!isFormValid || isTrading}
                  >
                    {isTrading ? 'Processing...' : 'Buy'}
                  </button>
                  <button
                    className="trade-button trade-button--sell"
                    onClick={() => handleTrade('sell')}
                    disabled={!isFormValid || isTrading}
                  >
                    {isTrading ? 'Processing...' : 'Sell'}
                  </button>
                </div>
              </div>
            </div>

            {/* Positions Section */}
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
                        <span className="position-card_pps">${position.price_per_share.toFixed(2)} per share</span>
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