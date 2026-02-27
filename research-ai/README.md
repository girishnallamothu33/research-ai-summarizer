# Research Paper Summarization for Multi-Disciplinary Knowledge Discovery

This is a complete AI SaaS application that extracts information from research papers (PDF or text), generates multidisciplinary summaries using OpenAI, and visualizes conceptual groupings using sentence embeddings and Plotly.

## Project Structure
```
research-ai/
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entrypoint
│   │   ├── config.py           # Configuration & App settings
│   │   ├── database.py         # SQLAlchemy Setup
│   │   ├── models.py           # DB Models
│   │   ├── schemas.py          # Pydantic Schemas
│   │   ├── api/
│   │   │   └── endpoints.py    # Route Controllers
│   │   └── services/
│   │       ├── ai_service.py   # OpenAI integration
│   │       ├── clustering_service.py # Sentence Transformers clustering 
│   │       └── pdf_service.py  # PyPDF text extraction
│   └── run.py                  # Uvicorn runner script
├── frontend/
│   └── app.py                  # Streamlit frontend
├── .env                        # Environment variables (OpenAI API key)
└── requirements.txt            # Python dependencies
```

## Features
* **PDF Upload:** Automatically extracts text via PyPDF2.
* **Smart Summaries:** Uses OpenAI API to analyze custom scientific contexts (like AI, Physics, Medical, etc).
* **AI Topics Clustering:** Uses Sentence Transformers and scikit-learn (KMeans) to map sentences in 2D space. Contains a visually stunning interactive Plotly chart.
* **Modern SaaS UI:** Uses dark mode UI, streamlit tabs, sidebars, toast notifications, loading spinners, and glassmorphism CSS.
* **Robust Backend:** Built on FastAPI, fully type-hinted with Pydantic, uses SQLAlchemy ORM + SQLite/PostgreSQL, Dependency injection for sessions.

## Setup Instructions

### 1. Install Dependencies
Make sure you are running Python 3.10+.
```bash
pip install -r requirements.txt
```
*(If you have issues installing some ML libraries depending on your OS, you may need a C++ compiler or related tools. Downloading specific pre-compiled wheels for sentence-transformers or PyTorch might be required.)*

### 2. Configure Environment
1. Open the `.env` file in the project root.
2. Replace `your_openai_api_key_here` with a real OpenAI key. Otherwise, the API uses fallback MOCK data.
3. If you want to use PostgreSQL, modify `DATABASE_URL` line (e.g., `postgresql://user:pass@localhost/db`). Currently defaults to SQLite for ease of setup.

### 3. Run the Backend
In your terminal, navigate to the `backend` folder and run:
```bash
cd backend
python run.py
```
This starts the backend at `http://localhost:8000`. Test it via the Swagger UI available at `http://localhost:8000/docs`.

### 4. Run the Frontend
In **another** terminal window, navigate to the `frontend` folder and run:
```bash
cd frontend
streamlit run app.py
```
Access the application on `http://localhost:8501`. 

## Sample API Responses

**POST /api/v1/summarize**
```json
{
  "short_summary": "This paper proposes...",
  "detailed_summary": "An in-depth explanation covering methodology...",
  "keywords": ["Transformers", "Medical AI", "Diagnosis"],
  "key_insights": [
    "Improved accuracy by 15%",
    "Cross-domain applications identified"
  ],
  "discipline_interpretation": "From a Medical perspective, this enhances diagnostics speed."
}
```

**POST /api/v1/cluster**
```json
{
  "clusters": [
    {
      "text": "The patient showed positive signs...",
      "cluster": 0,
      "x": -0.12,
      "y": 0.45
    },
    ...
  ]
}
```
