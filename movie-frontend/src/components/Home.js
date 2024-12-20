import React, { useState } from 'react';
import axios from 'axios';
import '../styles.css';

const Home = () => {
  const [query, setQuery] = useState('');
  const [mediaType, setMediaType] = useState('movie');
  const [searchResults, setSearchResults] = useState([]);
  const [searchMessage, setSearchMessage] = useState('');

  const [recommendQuery, setRecommendQuery] = useState('');
  const [recommendMediaType, setRecommendMediaType] = useState('movie');
  const [actorName, setActorName] = useState('');
  const [recommendResults, setRecommendResults] = useState([]);
  const [recommendMessage, setRecommendMessage] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5001/search_media', {
        params: { query, media_type: mediaType },
        withCredentials: true,
      });
      setSearchResults(response.data);
      setSearchMessage('');
    } catch (error) {
      setSearchResults([]);
      setSearchMessage(error.response?.data?.error || 'Search failed');
    }
  };

  const handleAddToFavorites = async (item) => {
    try {
      const response = await axios.post(
        'http://127.0.0.1:5001/add_to_favorites',
        {
          title: item.title,
          media_type: mediaType,
          movie_id: item.id,
        },
        { withCredentials: true }
      );
      setSearchMessage(response.data.message);
    } catch (error) {
      setSearchMessage(error.response?.data?.error || 'Failed to add to favorites');
    }
  };

  const handleRecommendations = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5001/recommendations', {
        params: {
          title: recommendQuery,
          media_type: recommendMediaType,
          actor_name: actorName,
        },
        withCredentials: true,
      });
      setRecommendResults(response.data);
      setRecommendMessage('');
    } catch (error) {
      setRecommendResults([]);
      setRecommendMessage(error.response?.data?.error || 'Recommendations failed');
    }
  };

  return (
    <div className="container">
      <h2>Home</h2>

      <div className="search-section">
        <h3>Search and Add to Favorites</h3>
        <input
          type="text"
          placeholder="Search for a movie or show..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={() => setMediaType('movie')}>Movie</button>
        <button onClick={() => setMediaType('tv')}>Show</button>
        <button onClick={handleSearch}>Search</button>
        <div className="results-container">
          {searchResults.length > 0 ? (
            searchResults.map((item) => (
              <div key={item.id} className="result-item">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                <p>Rating: {item.rating}</p>
                <button onClick={() => handleAddToFavorites(item)}>Add to Favorites</button>
              </div>
            ))
          ) : (
            <p>{searchMessage || 'No results found'}</p>
          )}
        </div>
      </div>

      <div className="recommendations-section" style={{ marginTop: '20px' }}>
        <h3>Get Recommendations</h3>
        <input
          type="text"
          placeholder="Enter a movie or show title..."
          value={recommendQuery}
          onChange={(e) => setRecommendQuery(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter an actor's name (optional)..."
          value={actorName}
          onChange={(e) => setActorName(e.target.value)}
        />
        <button onClick={() => setRecommendMediaType('movie')}>Movie</button>
        <button onClick={() => setRecommendMediaType('tv')}>Show</button>
        <button onClick={handleRecommendations}>Recommend</button>
        <div className="recommendations-container">
          {recommendResults.length > 0 ? (
            recommendResults.map((item) => (
              <div key={item.movie_id} className="recommendation-item" style={{ backgroundColor: item.highlight ? '#ffeb3b' : 'white' }}>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                <p>Rating: {item.rating}</p>
              </div>
            ))
          ) : (
            <p>{recommendMessage || 'No recommendations found'}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
