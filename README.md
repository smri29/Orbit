# Orbit 🪐
**A RAG-powered internal research assistant for CollabCircle.**

Orbit is a specialized AI chatbot designed to serve as the central knowledge hub for CollabCircle. Powered by Google's Gemini API and LangChain, Orbit ingests internal research papers, policy documents, and meeting minutes to provide accurate, context-aware answers to organization members.

## Features
* **Walled Garden:** Answers questions *only* based on the internal CollabCircle documents you upload.
* **Zero-Cost Embeddings:** Uses a local embedding model (HuggingFace) to process documents without hitting API rate limits.
* **Privacy First:** Uses a local vector database (ChromaDB) to store document knowledge securely.
* **Smart Fallback:** Automatically handles deployment environments (Linux/Cloud) vs. local development (Windows).

## Tech Stack
* **Frontend:** Streamlit
* **LLM:** Google Gemini Flash (via `gemini-flash-latest` for stability)
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2` running locally)
* **Vector Store:** ChromaDB
* **Orchestration:** LangChain

## Setup (Local Development)

### 1. Prerequisites
* Python 3.10+
* A Google Cloud API Key (for Gemini)

### 2. Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/smri29/Orbit.git](https://github.com/smri29/Orbit.git)
    cd Orbit
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration
Create a `.env` file in the root directory and add your Google API key:
```ini
GOOGLE_API_KEY="AIzaSy....."

```

### 4. Run the App

```bash
streamlit run app.py

```

*Note: The first time you run the app, it will download the embedding model (~90MB). This is normal.*

---

5. Reboot the app. Orbit handles the SQLite database requirements automatically via `pysqlite3-binary`.

## License

Internal Tool for CollabCircle.