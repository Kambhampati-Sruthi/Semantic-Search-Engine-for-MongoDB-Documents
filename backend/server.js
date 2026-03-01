const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Health check
app.get("/", (req, res) => {
  res.send("Node backend is running");
});

// Add document
app.post("/add-document", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:8000/add-document",
      req.body
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Failed to add document" });
  }
});

// Semantic search
app.post("/search", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:8000/search",
      {
        query: req.body.query,
        top_k: req.body.top_k || 5,
        threshold: req.body.threshold || 0.3
      }
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Search failed" });
  }
});

app.listen(5000, () => {
  console.log("Backend running on port 5000");
});