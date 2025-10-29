# Day 2 Setup Guide - FitBot AI

## Immediate Next Steps

### 1. Install Python Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Day 2 dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `.env` file and add:

```env
# Required - Your OpenAI API key (already in your .env)
OPENAI_API_KEY=sk-proj-your-key-here

# Optional - Get free key at https://openweathermap.org/api
OPENWEATHER_API_KEY=your_key_here

# Optional - Sign up at https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=pk-lf-your-key
LANGFUSE_SECRET_KEY=sk-lf-your-key
```

### 3. Initialize RAG Vector Store

```bash
# Start backend - this will create FAISS index on first run
uvicorn main:app --reload --port 8000
```

Wait for:
```
Creating new FAISS vector store from knowledge base...
Creating embeddings for X document chunks...
Saved vector store to ./data/vectorstore/faiss_index
```

### 4. Install Frontend Dependencies

Open new terminal:

```bash
cd frontend

# Fix npm permissions (if needed on macOS/Linux)
sudo chown -R $(whoami) ~/.npm

# Install dependencies
npm install

# Start frontend
npm run dev
```

### 5. Test the System

**Backend Health Check:**
```bash
curl http://localhost:8000/api/v1/ai/health
```

**Frontend:**
- Open http://localhost:3000
- Navigate to "AI Chat"
- Try: "What's a good workout for weight loss?"

## Common Issues & Solutions

### Issue: npm permission errors

**Solution:**
```bash
sudo chown -R $(whoami) ~/.npm
cd frontend && npm install
```

### Issue: FAISS import errors

**Solution:**
```bash
pip uninstall faiss-cpu
pip install faiss-cpu==1.8.0
```

### Issue: OpenAI API errors

**Solution:**
- Verify OPENAI_API_KEY in .env
- Check API key at https://platform.openai.com/api-keys
- Ensure billing is set up

### Issue: Database connection errors

**Solution:**
```bash
# Restart PostgreSQL container
docker-compose down
docker-compose up -d

# Wait 10 seconds then restart backend
uvicorn main:app --reload --port 8000
```

## Testing Checklist

- [ ] Backend starts without errors
- [ ] http://localhost:8000/docs shows AI endpoints
- [ ] http://localhost:8000/api/v1/ai/health returns healthy
- [ ] http://localhost:8000/api/v1/ai/tools lists 4 tools
- [ ] Frontend builds and starts
- [ ] http://localhost:3000 shows dashboard
- [ ] Chat interface loads
- [ ] Can send message to AI and get response
- [ ] Theme toggle works (dark/light mode)
- [ ] Dashboard shows existing data

## Feature Highlights

### AI Agent Features
- Conversational memory (remembers context)
- 4 custom tools (Calculator, Weather, WebSearch, FitnessTracker)
- RAG-enhanced responses (grounded in fitness knowledge)
- Streaming responses (real-time feedback)

### Frontend Features
- Responsive design (mobile-first)
- Dark/light theme toggle
- Real-time chat interface
- Dashboard with workout stats and goals
- Error handling with toast notifications

### Backend Features
- OpenAI GPT-4o-mini integration
- FAISS vector store for RAG
- Langfuse observability (optional)
- RESTful API with Swagger docs
- Production-ready error handling

## Usage Examples

### Example Chat Queries

1. "What are my workout stats this month?"
2. "Calculate my BMI if I'm 180cm and 75kg"
3. "What's the weather in New York for running?"
4. "Search for the best protein sources for muscle building"
5. "Create a 3-day workout split for beginners"

### API Examples

**Chat:**
```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are good cardio exercises?"}'
```

**Get Agent Info:**
```bash
curl http://localhost:8000/api/v1/ai/agent
```

## Performance Tips

- RAG retrieval adds ~200-500ms latency (worth it for accuracy)
- First chat message may be slower (model initialization)
- Use `use_rag=false` for faster responses when RAG not needed
- Clear memory periodically for long conversations

## Next Steps

1. Add more users and workouts via dashboard
2. Try different chat queries to test AI capabilities
3. Configure Langfuse for observability
4. Get OpenWeatherMap key for weather features
5. Customize fitness knowledge base in `app/rag.py`

## Support

Issues: https://github.com/adarshvuppala-nu/Fitness-Tracker-Service/issues
