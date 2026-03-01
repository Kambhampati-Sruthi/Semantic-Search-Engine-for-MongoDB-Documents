export async function searchQuery(query) {
  const res = await fetch("http://localhost:5000/api/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  return res.json();
}