import React, { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [threshold, setThreshold] = useState(0.3);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const search = async () => {
    if (!query.trim()) {
      setError("Please enter a search query");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: query,
          top_k: topK,
          threshold: threshold
        })
      });

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError("Failed to fetch search results");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h2>🔍 Semantic Search Engine</h2>
      <p>AI-powered semantic document search</p>

      {/* Search Input */}
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter search query"
        style={{ width: "350px", padding: "8px" }}
      />

      <button
        onClick={search}
        style={{ marginLeft: "10px", padding: "8px 15px" }}
      >
        Search
      </button>

      {/* Controls */}
      <div style={{ marginTop: "15px" }}>
        <label>
          Top Results:
          <input
            type="number"
            value={topK}
            min="1"
            max="10"
            onChange={(e) => setTopK(Number(e.target.value))}
            style={{ marginLeft: "8px", width: "60px" }}
          />
        </label>

        <label style={{ marginLeft: "20px" }}>
          Similarity Threshold:
          <input
            type="number"
            step="0.1"
            min="0"
            max="1"
            value={threshold}
            onChange={(e) => setThreshold(Number(e.target.value))}
            style={{ marginLeft: "8px", width: "60px" }}
          />
        </label>
      </div>

      {/* Status */}
      {loading && <p>🔄 Searching...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Results */}
      <ul style={{ marginTop: "25px" }}>
        {results.length === 0 && !loading && <p>No results found</p>}

        {results.map((item, index) => (
          <li key={index} style={{ marginBottom: "15px" }}>
            <strong>{item.title}</strong>
            <br />
            <small>
              Similarity Score: <b>{item.score.toFixed(2)}</b>
            </small>
            <p>{item.content}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;