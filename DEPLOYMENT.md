# AutoJobScout Deployment Guide

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Easiest - Free Tier Available)

**Pros:**
- Free tier available
- Easy deployment from GitHub
- No infrastructure management

**Cons:**
- Limited resources (1GB RAM on free tier)
- Cannot run local Ollama models (you'll need to use cloud LLM APIs)

**Steps:**

1. **Prepare for Cloud Deployment**
   
   Replace Ollama with OpenAI or Anthropic API:
   
   ```bash
   pip install openai anthropic langchain-openai
   ```
   
   Update your agent files to use cloud LLMs instead of Ollama.

2. **Push to GitHub**
   
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin your-repo-url
   git push -u origin main
   ```

3. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Add environment variables in settings
   - Deploy!

4. **Add `.streamlit/config.toml`**
   
   ```toml
   [server]
   headless = true
   port = 8501
   enableCORS = false
   enableXsrfProtection = true
   
   [theme]
   primaryColor = "#667eea"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   textColor = "#262730"
   font = "sans serif"
   ```

---

### Option 2: Docker + AWS/GCP/Azure (Recommended for Production)

**Pros:**
- Full control
- Can run Ollama locally in container
- Scalable

**Cons:**
- Requires server management
- Costs money

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p storage logs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./storage:/app/storage
      - ./logs:/app/logs
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - ENVIRONMENT=production
    depends_on:
      - ollama
    restart: unless-stopped
  
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

**Deploy to AWS EC2:**

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ec2-user@your-ip

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and run
git clone your-repo
cd your-repo
docker-compose up -d
```

---

### Option 3: Railway.app (Easy + Affordable)

**Pros:**
- Easy deployment
- Free tier ($5 credit/month)
- Supports Docker

**Steps:**

1. Create `railway.toml`:
   ```toml
   [build]
   builder = "DOCKERFILE"
   
   [deploy]
   startCommand = "streamlit run app.py"
   restartPolicyType = "ON_FAILURE"
   ```

2. Push to GitHub

3. Deploy on Railway:
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Add environment variables
   - Deploy!

---

### Option 4: Hugging Face Spaces (Free)

**Pros:**
- Free hosting
- Great for ML apps
- Built-in gradio/streamlit support

**Steps:**

1. Create account on [huggingface.co](https://huggingface.co)

2. Create new Space (select Streamlit)

3. Add `README.md` header:
   ```yaml
   ---
   title: AutoJobScout
   emoji: 🧭
   colorFrom: purple
   colorTo: blue
   sdk: streamlit
   sdk_version: 1.37.1
   app_file: app.py
   pinned: false
   ---
   ```

4. Push code to the Space

---

## 🔧 Pre-Deployment Checklist

- [ ] Add `.gitignore`:
  ```
  __pycache__/
  *.py[cod]
  .env
  .venv/
  venv/
  storage/*.faiss
  storage/*.npy
  logs/
  .DS_Store
  ```

- [ ] Create `requirements.txt` with pinned versions
- [ ] Add error handling and logging
- [ ] Set up environment variables
- [ ] Test locally with production settings
- [ ] Add health check endpoint
- [ ] Configure CORS if needed
- [ ] Add rate limiting for API calls
- [ ] Set up monitoring/alerts

---

## 📊 Cost Estimates

| Platform | Free Tier | Paid (Small) | Notes |
|----------|-----------|--------------|-------|
| Streamlit Cloud | Yes (limited) | $0/mo | Must use cloud LLMs |
| Railway | $5 credit/mo | ~$20/mo | Good for prototypes |
| AWS EC2 t3.medium | No | ~$30/mo | Full control |
| Hugging Face | Yes | Free-$9/mo | Limited compute |
| Render | Yes | $7/mo | Docker support |

---

## 🔐 Security Best Practices

1. **Never commit secrets** - use environment variables
2. **Add rate limiting** to prevent abuse
3. **Sanitize user inputs** (resume text)
4. **Use HTTPS** in production
5. **Implement authentication** if needed
6. **Regular security updates** for dependencies
7. **Monitor logs** for suspicious activity

---

## 📈 Monitoring & Maintenance

**Recommended tools:**
- **Sentry** - Error tracking
- **Datadog/New Relic** - Performance monitoring
- **Uptime Robot** - Uptime monitoring
- **Google Analytics** - Usage analytics

**Setup logging:**
```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

---

## 🚨 Troubleshooting

### Issue: Out of Memory
**Solution:** Reduce batch sizes, use smaller embedding model, or upgrade instance

### Issue: Slow job fetching
**Solution:** Implement caching, reduce sources, or parallelize requests

### Issue: LLM timeouts
**Solution:** Increase timeout, use streaming, or switch to faster model

---

## 📞 Support

For issues, check:
1. Application logs in `logs/` directory
2. Streamlit community forum
3. GitHub issues