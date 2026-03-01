const express = require("express");
const axios = require("axios");

const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { query, top_k = 5, threshold = 0.3 } = req.body;

    const response = await axios.post("http://localhost:8000/search", {
      query,
      top_k,
      threshold
    });

    res.json(response.data);
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Semantic search failed" });
  }
});

module.exports = router;