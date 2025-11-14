import { useState } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="app-container">
      <header className="header">
        <div className="header__content">
          {/* Logo TODO: add hampter :) */} 
          <button 
            className="header__logo" 
            onClick={() => setActiveTab('home')}
            aria-label="Go to homepage">

            <div className="logo-placeholder">
              <span className="logo-text">MSS</span>
            </div>
          </button>

          {/* Navigation */}
          <nav className="header__nav">
            
            <button
              className={`nav-item ${activeTab === 'history' ? 'nav-item--active' : ''}`}
              onClick={() => setActiveTab('history')}
            >
              History
            </button>
            
            <button
              className={`nav-item ${activeTab === 'TemplateA' ? 'nav-item--active' : ''}`}
              onClick={() => setActiveTab('TemplateA')}
            >
              TemplateA
            </button>

            {/* Add more nav Buttons here as needed */}
          </nav>
        </div>
      </header>

      <main className="app">
        <div className="app__content">
          <section className="app__hero">
            <h1>Market Signal Summarizer</h1>
            <p>Your React + Vite frontend is live. Build the UI for market insights here.</p>
            <p style={{ marginTop: '1rem', fontSize: '0.875rem', opacity: 0.8 }}>
              Current tab: <strong>{activeTab}</strong>
            </p>
          </section>

          <section className="app__hero">
            <h1>Your Stocks</h1>
            <p>Etiam sodales leo at malesuada mattis. In urna elit, ullamcorper vel pharetra ut, hendrerit eu leo. Nulla blandit nec lacus id blandit. Proin egestas eleifend magna non scelerisque. Vivamus nisi libero, molestie vel pellentesque at, finibus viverra sem. Suspendisse potenti. Vivamus ipsum justo, posuere scelerisque lorem in, pulvinar euismod sapien. Fusce tincidunt, neque ut lobortis faucibus, magna nulla tempor est, nec pulvinar sapien ex vitae eros. Nulla bibendum a eros vitae congue. Fusce hendrerit pellentesque odio, id convallis ligula placerat et. Nulla metus libero, congue ut velit</p>
          </section>

          <section className="app__hero">
            <h1>Sentiment</h1>
            <p>el. Proin efficitur id enim at luctus. Donec eu diam sed dui hendrerit tempor. Maecenas eleifend auctor magna, ac bibendum tellus lobortis eget. Mauris dignissim nec diam sed ultrices.</p>
          </section>

          <section className="app__hero">
            <div className="hero__split">
              <div className="hero__text">
                <h1>Market Signal Summarizer</h1>
                <p>el. Proin efficitur id enim at luctus. Donec eu diam sed dui hendrerit tempor. Maecenas eleifend auctor magna, ac bibendum tellus lobortis eget. Mauris dignissim nec diam sed ultrices.</p>
              </div>
              <div className="hero__action">
                <button className="cool-button">
                  <span className="button__text">Execute Trade</span>
                  <span className="button__icon">→</span>
                </button>
              </div>
            </div>
          </section>

        </div>
      </main>
    </div>
  );
}

export default App;