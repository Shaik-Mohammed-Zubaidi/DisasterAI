import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    try {
      setResult(null);
      const { data } = await axios.get(`http://127.0.0.1:5000?query=${query}`);
      console.log('Data:', data);
      setResult(data.message);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <form onSubmit={handleQuerySubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Enter your query"
          style={{ marginBottom: '10px', padding: '10px', width: '300px' }}
        />
        <button type="submit" style={{ padding: '10px 20px' }}>Submit</button>
      </form>
      {result === null ? (
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <h3>Loading...</h3>
          </div>
        ) : (
          result && (
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
              <h3>Result:</h3>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )
        )
      }
    </div>
  );
}

export default App;