import React, { useState } from 'react';
import '../styles.css';

const DataAnalysis = () => {
  const [budget, setBudget] = useState('');
  const [runtime, setRuntime] = useState('');
  const [hasHomepage, setHasHomepage] = useState(0); // Default state as 0
  const [genres, setGenres] = useState([]);
  const [results, setResults] = useState(null);
  const [currentGraph, setCurrentGraph] = useState('movies_by_decade');

  const genreOptions = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama',
    'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance',
    'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
  ];

  const graphMap = {
    movies_by_decade: "Count by Decade",
    avg_budget_and_revenue_by_decade: "Decade",
    budget_revenue_by_runtime: "Runtime",
    budget_revenue_by_score: "Score",
    revenue_budget_by_genre: "Genre",
    revenue_budget_by_language: "Language",
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      budget: parseFloat(budget),
      runtime: parseFloat(runtime),
      genres: genres,
      has_homepage: hasHomepage,
    };

    try {
      const response = await fetch('http://localhost:5001/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      setResults({ error: 'Failed to fetch predictions.' });
    }
  };

  const toggleGenre = (genre) => {
    setGenres((prevGenres) =>
      prevGenres.includes(genre)
        ? prevGenres.filter((g) => g !== genre)
        : [...prevGenres, genre]
    );
  };

  const toggleState = (currentState, setState) => {
    setState(currentState === 1 ? 0 : 1);
  };

  return (
    <div>
      <h2 className="centered-header">Create your Movie and see how much you'll make!</h2>
      <p className="centered-subtext">(Because movies in 2020 haven't had the time to make a lot of money, your revenue may be deceptively small)</p>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Budget:</label>
          <input
            type="number"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            placeholder="Enter budget"
            required
          />
        </div>
        <div>
          <label>Runtime:</label>
          <input
            type="number"
            value={runtime}
            onChange={(e) => setRuntime(e.target.value)}
            placeholder="Enter runtime"
            required
          />
        </div>

        {/* Has Homepage */}
        <div className="label-inline">
          <label>Has Website:</label>
          <button
            type="button"
            className={`small-button ${hasHomepage === 1 ? 'active' : ''}`}
            onClick={() => toggleState(hasHomepage, setHasHomepage)}
          >
            {hasHomepage === 1 ? 'Yes' : 'No'}
          </button>
        </div>

        <div>
          <label>Genres:</label>
          <div className="genres-container">
            {genreOptions.map((genre) => (
              <label key={genre}>
                <input
                  type="checkbox"
                  checked={genres.includes(genre)}
                  onChange={() => toggleGenre(genre)}
                />
                {genre}
              </label>
            ))}
          </div>
        </div>

        <button type="submit">Submit</button>
      </form>

      {results && (
        <div className="results">
          <h3>Results</h3>
          {results.error ? (
            <p className="error">{results.error}</p>
          ) : (
            <>
              <p>XGBoost Revenue Prediction: {results.xgboost_prediction}</p>
              <p>Random Forest Category Prediction: {results.random_forest_prediction} revenue</p>  
            </>
          )}
        </div>
      )}

      <div className="graph-section">
        <h3>Graphs (Budget and Revenue counts vs. these variables)</h3>
        <div>
          {Object.keys(graphMap).map((graphKey) => (
            <button
              key={graphKey}
              onClick={() => setCurrentGraph(graphKey)}
              style={{
                marginRight: '10px',
                backgroundColor: currentGraph === graphKey ? '#ccc' : '#fff',
              }}
            >
              {graphMap[graphKey]}
            </button>
          ))}
        </div>
        <div>
          <img
            src={`http://localhost:5001/static/${currentGraph}.jpg`}
            alt={graphMap[currentGraph]}
          />
        </div>
      </div>
    </div>
  );
};

export default DataAnalysis;
