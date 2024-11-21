import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [query, setQuery] = useState('');
  const [mediaType, setMediaType] = useState('movie'); // Default to 'movie'
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5001/search_media', {
        params: { query, media_type: 'movie' },
        withCredentials: true,
      });
      setResults(response.data);
      setMessage(''); // Clear any previous messages
    } catch (error) {
      setResults([]); // Clear results on error
      setMessage(error.response?.data?.error || 'Search failed');
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
        { withCredentials: true } // Move withCredentials here
      );
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || 'Failed to add to favorites');
    }
  };
  

  return (
    <div>
      <h2>Home</h2>
      <div>
        <input
          type="text"
          placeholder="Search for a movie or show..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={() => setMediaType('movie')}>Movie</button>
        <button onClick={() => setMediaType('tv')}>Show</button>
        <button onClick={handleSearch}>Search</button>
      </div>
      <div>
        {results.length > 0 ? (
          results.map((item) => (
            <div key={item.id}>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              <p>Rating: {item.rating}</p>
              <button onClick={() => handleAddToFavorites(item)}>
                Add to Favorites
              </button>
            </div>
          ))
        ) : (
          <p>{message || 'No results found'}</p>
        )}
      </div>
    </div>
  );
};

export default Home;
