# 🧭 AutoJobScout

**AI-powered job discovery using LLM planners, LangGraph orchestration, and multi-source job ingestion.**

[![Streamlit App](https://autojobscout.streamlit.app/)]

---

## 🌟 Features

- 🤖 **Agentic AI Pipeline**: Uses LangGraph to orchestrate multiple AI agents
- 🔍 **Multi-Source Ingestion**: Aggregates jobs from RemoteOK, Remotive, WeWorkRemotely, and NewGrad-Jobs
- 🧠 **Semantic Matching**: Uses sentence transformers and embeddings for intelligent job-resume matching
- 💡 **AI Explanations**: LLM-powered explanations for why jobs match your profile
- 📊 **Skill Gap Analysis**: Identifies missing skills and suggests resume improvements
- ✅ **Self-Critique**: Built-in hallucination detection to ensure accuracy
- 🎯 **Intelligent Planning**: AI planner decides optimal search strategy based on your intent

---

## 🚀 Live Demo

Try it now: **[autojobscout.streamlit.app](https://autojobscout.streamlit.app)**

---

## 📸 Screenshots

![AutoJobScout Interface](https://via.placeholder.com/800x400?text=AutoJobScout+Dashboard)

---

## 🏗️ Architecture

```
User Input (Resume + Intent)
         ↓
    Planner Agent
         ↓
    Job Ingestion (Multi-source)
         ↓
    Job Enrichment (Full descriptions)
         ↓
    Matching Agent (Semantic search)
         ↓
    Gap Analysis Agent
         ↓
    Explainer Agent
         ↓
    Critic Agent (Self-check)
         ↓
    Results Display
```

### Agent Pipeline

1. **Planner Agent**: Determines which job sources to query, how many results to fetch, and whether to run gap analysis
2. **Ingest Node**: Fetches jobs from multiple sources in parallel
3. **Enrich Node**: Optionally fetches full job descriptions for better matching
4. **Match Agent**: Uses embeddings and cosine similarity to rank jobs against your resume
5. **Gap Agent**: Analyzes skill gaps for top matches
6. **Explainer Agent**: Generates natural language explanations for matches
7. **Critic Agent**: Checks explanations for hallucinations and unsupported claims

---

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.11+**
- **Streamlit** - Web interface
- **LangGraph** - Agent orchestration
- **LangChain** - LLM framework
- **Groq API** - Fast cloud LLM inference

### ML/AI
- **Sentence Transformers** - Embeddings (all-MiniLM-L6-v2)
- **scikit-learn** - Cosine similarity search
- **Pydantic** - Data validation and schemas

### Data Sources
- RemoteOK API
- Remotive API
- WeWorkRemotely RSS
- NewGrad-Jobs web scraping

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/abdullahshamail/jobscout.git
   cd jobscout
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

---

## 🔑 Environment Variables

Create a `.env` file with:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
USE_CLOUD_LLM=true
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.0
DEFAULT_JOB_LIMIT=100
DEFAULT_TOP_K=10
ENVIRONMENT=development
```

---

## 📖 Usage

### Web Interface

1. **Paste your resume** in the text area
2. **Enter your job search intent** (e.g., "machine learning engineer roles")
3. **Configure advanced settings** (optional):
   - Number of results
   - Job sources to search
   - Enable/disable full job descriptions
   - Enable/disable skill gap analysis
4. **Click "Find Matching Jobs"**
5. **Review results** with match scores, explanations, and skill gaps

### Command Line

```bash
python main.py path/to/resume.txt --intent "data science roles"
```

---

## 🏗️ Project Structure

```
jobscout/
├── agents/                 # Agent implementations
│   ├── critic.py          # Hallucination detection
│   ├── explainer.py       # Match explanations
│   ├── gap_agent.py       # Skill gap analysis
│   ├── graph.py           # LangGraph workflow
│   ├── match_agent.py     # Semantic matching
│   ├── planner_agent.py   # Strategy planning
│   ├── state.py           # Shared state schema
│   └── tools.py           # Job ingestion utilities
├── jobs/                  # Job source integrations
│   ├── remoteok.py        # RemoteOK API
│   ├── remotive.py        # Remotive API
│   ├── weworkremotely.py  # WeWorkRemotely RSS
│   └── newgrad_jobs.py    # NewGrad scraper
├── rag/                   # Retrieval & embeddings
│   ├── embeddings.py      # Sentence transformers
│   ├── index.py           # Vector search index
│   └── schemas.py         # Data models
├── storage/               # Persistent storage
│   └── paths.py           # File paths config
├── utils/                 # Utilities
│   ├── llm.py            # LLM API wrapper
│   ├── logger.py         # Logging setup
│   └── text.py           # Text processing
├── app.py                # Streamlit web app
├── main.py               # CLI interface
├── config.py             # Configuration
├── requirements.txt      # Dependencies
└── README.md            # This file
```

---

## 🔧 Configuration

### Job Sources

Configure which job boards to search in `config.py` or via the web interface:
- **RemoteOK**: Remote tech jobs
- **Remotive**: Remote work opportunities
- **WeWorkRemotely**: Remote jobs across industries
- **NewGradJobs**: Entry-level positions

### LLM Models

Supports any Groq-compatible model:
- `llama-3.1-70b-versatile` (default, best quality)
- `llama-3.1-8b-instant` (faster, good quality)
- `mixtral-8x7b-32768` (alternative)

### Embedding Models

Default: `sentence-transformers/all-MiniLM-L6-v2`
- Fast and accurate
- 384-dimensional embeddings
- Can be changed in `config.py`

---

## 🚢 Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app from your repository
4. Add secrets in app settings:
   ```toml
   GROQ_API_KEY = "your_key_here"
   USE_CLOUD_LLM = "true"
   LLM_MODEL = "llama-3.1-70b-versatile"
   ENVIRONMENT = "production"
   ```
5. Deploy!

### Docker

```bash
docker build -t autojobscout .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key autojobscout
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for more deployment options.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .
isort .

# Lint
flake8 .
```

---

## 🙏 Acknowledgments

- Built by [Abdullah Shamail](https://linkedin.com/in/abdullahshamail)
- PhD Candidate, Iowa State University
- Research areas: ML/AI, spatio-temporal analysis, scientific computing

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🐛 Known Issues

- Job source APIs may rate-limit during high usage
- Full job description fetching can be slow for large result sets
- Some job postings may have incomplete descriptions

---

## 🗺️ Roadmap

- [ ] Add more job sources (LinkedIn, Indeed, etc.)
- [ ] Implement job alerts and notifications
- [ ] Add resume optimization suggestions
- [ ] Support for cover letter generation
- [ ] Multi-language support
- [ ] Interview preparation tips based on job requirements
- [ ] Salary insights and negotiation tips
- [ ] Company culture analysis

---

## 📞 Contact

**Abdullah Shamail**
- 💼 LinkedIn: [abdullahshamail](https://linkedin.com/in/abdullahshamail)
- 🐙 GitHub: [abdullahshamail](https://github.com/abdullahshamail)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ using AI and lots of coffee ☕**