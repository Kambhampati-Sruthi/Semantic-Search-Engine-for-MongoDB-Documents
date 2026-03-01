import streamlit as st
import requests
import json

# ==============================
# CONFIG
# ==============================
# Replace this with your Render backend URL
BACKEND_URL = "https://semantic-search-engine-backend.onrender.com"

st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="🔍",
    layout="wide"
)

# ==============================
# SESSION STATE
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==============================
# LOGIN PAGE
# ==============================
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    .login-card {
        max-width: 450px;
        margin: 80px auto;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        text-align: center;
        background: linear-gradient(to bottom right, #f0f4ff, #d9e2ff);
    }
    .login-card h2 {
        margin-bottom: 20px;
        color: #333;
    }
    .login-info {
        font-size: 14px;
        margin-top: 10px;
        color: #555;
        background-color: #eef;
        padding: 8px;
        border-radius: 5px;
    }
    </style>
    <div class="login-card">
        <h2>🔐 Welcome to Semantic Search</h2>
        <p>Use the following credentials:</p>
        <div class="login-info">Username: <b>admin</b><br>Password: <b>admin123</b></div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login successful! Please refresh the page if needed.")
        else:
            st.error("Invalid credentials")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==============================
# HEADER
# ==============================
st.markdown("""
<h1 style="text-align:center;">🔍 Semantic Search Engine</h1>
<p style="text-align:center;">AI-powered document search using embeddings</p>
<hr>
""", unsafe_allow_html=True)

# ==============================
# TABS
# ==============================
tab1, tab2, tab3, tab4 = st.tabs(
    ["➕ Add Document", "🔎 Search", "📊 Statistics", "📄 Sample Docs"]
)

# ==============================
# ADD DOCUMENT
# ==============================
with tab1:
    st.subheader("➕ Add Document")
    title = st.text_input("Document Title")
    content = st.text_area("Document Content", height=200)

    if st.button("Add Document"):
        if not title.strip() or not content.strip():
            st.warning("Title and content are required")
        else:
            try:
                r = requests.post(
                    f"{BACKEND_URL}/add-document",
                    json={"title": title.strip(), "content": content.strip()},
                    timeout=15
                )
                if r.status_code == 200:
                    st.success("✅ Document added successfully")
                else:
                    st.error(f"❌ Backend error ({r.status_code})")
                    st.code(r.text)
            except Exception as e:
                st.error(f"⚠️ Backend not reachable: {e}")

# ==============================
# SEARCH
# ==============================
with tab2:
    st.subheader("🔎 Semantic Search")

    query = st.text_input(
        "Search Query",
        placeholder="e.g. Artificial Intelligence"
    )
    top_k = st.slider("Top Results", 1, 10, 5)
    threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.3)

    if st.button("Search"):
        if not query.strip():
            st.warning("Please enter a search query")
            st.stop()

        payload = {"query": json.dumps({
            "query": query.strip(),
            "top_k": int(top_k),
            "threshold": float(threshold)
        })}

        try:
            r = requests.post(f"{BACKEND_URL}/search", json=payload, timeout=15)
            if r.status_code != 200:
                st.error(f"❌ Backend error ({r.status_code})")
                st.code(r.text)
                st.stop()

            results = r.json()
            if not results:
                st.info("No results found")
            else:
                for res in results:
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9;">
                        <h4>{res.get('title','')}</h4>
                        <p>{res.get('content','')}</p>
                        <small>Similarity: {res.get('score',0):.2f}</small>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Backend not reachable: {e}")

# ==============================
# STATISTICS
# ==============================
with tab3:
    st.subheader("📊 Statistics")
    try:
        r = requests.get(f"{BACKEND_URL}/stats", timeout=10)
        if r.status_code == 200:
            st.json(r.json())
        else:
            st.error(f"❌ Backend error ({r.status_code})")
            st.code(r.text)
    except:
        st.error("⚠️ Backend not reachable")

# ==============================
# SAMPLE DOCS
# ==============================
with tab4:
    st.subheader("📄 Sample Documents")
    samples = [
        ("AI Basics", "Artificial intelligence includes machine learning and deep learning"),
        ("Deep Learning", "Deep learning uses neural networks with many layers"),
        ("NLP", "Natural Language Processing helps computers understand text"),
        ("Computer Vision", "Computer vision enables machines to interpret images"),
    ]

    for title, content in samples:
        if st.button(f"Add: {title}", key=title):
            try:
                r = requests.post(f"{BACKEND_URL}/add-document", json={"title": title, "content": content})
                if r.status_code == 200:
                    st.success(f"✅ Added {title}")
                else:
                    st.error("❌ Failed to add document")
            except:
                st.error("⚠️ Backend not reachable")
