import { useState } from 'react';
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
  current_price: number;
  market_value: number;
  unrealized_pl: number;
  unrealized_plpc: number;
}

function App() {
  const [signals, setSignals] = useState<MarketSignal[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [accountValue, setAccountValue] = useState<number>(0);
  const [totalPL, setTotalPL] = useState<number>(0);
  const [isGenerating, setIsGenerating] = useState(false);

  const generateMarketSignal = async () => {
    setIsGenerating(true);
    try {
      // TODO: Replace with actual API call to backend
      // For now, creating a mock signal
      const newSignal: MarketSignal = {
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        summary: 'Market analysis generated',
        sentiment: 'Positive',
        action: 'Hold',
      };
      
      setSignals([newSignal, ...signals]);
    } catch (error) {
      console.error('Error generating signal:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const fetchPositions = async () => {
    try {
      // TODO: Replace with actual API call to backend alpaca_api
      // const response = await fetch('http://localhost:8000/api/positions');
      // const data = await response.json();
      // setPositions(data.positions);
      // setAccountValue(data.accountValue);
      // setTotalPL(data.totalPL);
    } catch (error) {
      console.error('Error fetching positions:', error);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="header__content">
          {/* Logo */} 
          <div className="header__logo">
            <div className="logo-placeholder">
              <span className="logo-text">MSS</span>
            </div>
          </div>
          <h1 className="header__title">Market Signal Summarizer</h1>
        </div>
      </header>

      <main className="app">
        <div className="split-layout">
          {/* Left Half - Generate & History */}
          <div className="left-column">
             <div style={{ marginBottom: '30px', textAlign: 'center' }}>
              <button 
                onClick={generateMarketSignal}
                disabled={isGenerating}
                style={{
                  alignItems: 'center',
                  backgroundImage: 'linear-gradient(144deg, #af40ff, #5b42f3 50%, #00ddeb)',
                  border: '0',
                  borderRadius: '8px',
                  boxShadow: 'rgba(151, 65, 252, 0.2) 0 15px 30px -5px',
                  boxSizing: 'border-box',
                  color: '#ffffff',
                  display: 'flex',
                  fontSize: '18px',
                  justifyContent: 'center',
                  lineHeight: '1em',
                  maxWidth: '100%',
                  minWidth: '140px',
                  padding: '3px',
                  textDecoration: 'none',
                  userSelect: 'none',
                  WebkitUserSelect: 'none',
                  touchAction: 'manipulation',
                  whiteSpace: 'nowrap',
                  cursor: isGenerating ? 'not-allowed' : 'pointer',
                  transition: 'all 0.3s',
                  opacity: isGenerating ? 0.7 : 1,
                  margin: '0 auto'
                }}
                onMouseOver={(e) => {
                  if (!isGenerating) {
                    const span = e.currentTarget.querySelector('span');
                    if (span) (span as HTMLElement).style.background = 'none';
                  }
                }}
                onMouseOut={(e) => {
                  const span = e.currentTarget.querySelector('span');
                  if (span) (span as HTMLElement).style.background = 'rgb(5, 6, 45)';
                }}
                onMouseDown={(e) => {
                  if (!isGenerating) {
                    e.currentTarget.style.transform = 'scale(0.9)';
                  }
                }}
                onMouseUp={(e) => {
                  e.currentTarget.style.transform = 'scale(1)';
                }}
              >
              <span style={{
                backgroundColor: 'rgb(5, 6, 45)',
                padding: '16px 24px',
                borderRadius: '6px',
                width: '100%',
                height: '100%',
                transition: '300ms',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: 'Inter, sans-serif',
                fontSize: '18px',
                fontWeight: '700',
                letterSpacing: '0.5px',
              }}>
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
            
            <div className="account-summary">
              <div className="summary-card">
                <span className="summary-card__label">Account Value</span>
                <span className="summary-card__value">${accountValue.toFixed(2)}</span>
              </div>
              <div className="summary-card">
                <span className="summary-card__label">Total P/L</span>
                <span className={`summary-card__value ${totalPL >= 0 ? 'positive' : 'negative'}`}>
                  {totalPL >= 0 ? '+' : ''}{totalPL.toFixed(2)}
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
                          <span className="position-detail__label">Current Price</span>
                          <span className="position-detail__value">${position.current_price.toFixed(2)}</span>
                        </div>
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