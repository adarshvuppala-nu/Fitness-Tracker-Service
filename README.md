# Fitness Tracker API

Production-ready full-stack fitness tracking application with AI-powered coaching, built with FastAPI, React, LangChain, and OpenAI.

 Features

# Core Backend
- REST API with FastAPI for Users, Workouts, Goals, and Progress Metrics
- PostgreSQL database with Alembic migrations
- UUID-based primary keys and comprehensive validation
- Full CRUD operations with filtering and pagination
- Automatic API documentation (Swagger UI)

# AI Integration
- AI Chat Assistant: Conversational fitness coach powered by GPT-4o-mini
- Custom Tools: Calculator, Weather, Web Search, Fitness Data Query
- RAG Pipeline: FAISS vector store with fitness knowledge base
- Langfuse Integration: LLM observability and tracing
- React Frontend: Responsive dashboard and real-time chat interface
- Dark/Light Theme: Persistent theme switching with TailwindCSS

 Tech Stack

**Backend:**
- FastAPI 0.115.0
- PostgreSQL 16
- SQLAlchemy 2.0.35
- LangChain 0.3.0
- OpenAI GPT-4o-mini
- FAISS (vector store)
- Langfuse (observability)

**Frontend:**
- React 19
- Vite 7
- TailwindCSS 3.4
- React Router 6
- Axios
- Lucide Icons

 Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key
- (Optional) OpenWeatherMap API Key
- (Optional) Langfuse Account

 Quick Start

# 1. Clone Repository

```bash
git clone https://github.com/adarshvuppala-nu/Fitness-Tracker-Service.git
cd Fitness-Tracker-Service
```

# 2. Backend Setup

```bash
# Start PostgreSQL
docker-compose up -d

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn main:app --reload --port 8000
```

Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs

# 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend App: http://localhost:3000

 Environment Variables

Create `.env` in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5433/fitness_tracker
DATABASE_HOST=localhost
DATABASE_PORT=5433
DATABASE_NAME=fitness_tracker
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=Fitness Tracker API
VERSION=1.0.0

# OpenAI
OPENAI_API_KEY=sk-proj-...

# OpenWeatherMap (Optional)
OPENWEATHER_API_KEY=your_key_here

# Langfuse (Optional - for LLM observability)
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

 API Endpoints

# Core CRUD
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{id}` - Get user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

Similar patterns for:
- `/api/v1/workout-sessions`
- `/api/v1/fitness-goals`
- `/api/v1/progress-metrics`

# AI Assistant
- `POST /api/v1/ai/chat` - Chat with AI agent
- `GET /api/v1/ai/agent` - Agent info
- `GET /api/v1/ai/tools` - Available tools
- `GET /api/v1/ai/health` - Service health
- `POST /api/v1/ai/clear-memory` - Clear chat history

 Usage Examples

# Chat with AI

```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a weight loss plan for me",
    "use_memory": true,
    "use_rag": true
  }'
```

# Create Workout

```bash
curl -X POST http://localhost:8000/api/v1/workout-sessions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "uuid-here",
    "type": "running",
    "duration": 30,
    "calories_burned": 300,
    "date": "2024-10-28"
  }'
```

 Development

# Run Tests

```bash
# Backend tests
pytest tests/ -v

# Frontend tests (if configured)
cd frontend && npm test
```

# Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

 Project Structure

```
fitness-tracker-api/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── docker-compose.yml      # PostgreSQL container
├── alembic/                # Database migrations
├── app/
│   ├── core/               # Config & database
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── crud/               # CRUD operations
│   ├── api/v1/             # API endpoints
│   ├── tools.py            # LangChain custom tools
│   ├── rag.py              # RAG pipeline & FAISS
│   └── agent.py            # AI agent with memory
├── tests/                  # Pytest test suite
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── hooks/          # Custom hooks
    │   ├── contexts/       # React context
    │   └── services/       # API client
    ├── package.json
    └── vite.config.js
```

 Deployment

# Backend

```bash
# Build production
pip install -r requirements.txt

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

# Frontend

```bash
cd frontend
npm run build
# Deploy dist/ folder to hosting (Vercel, Netlify, etc.)
```

 AI Agent Capabilities

1. Query Fitness Data: Retrieve workouts, goals, and progress metrics
2. Calculate Metrics: BMI, TDEE, macro splits, calorie needs
3. Check Weather: For outdoor workout planning
4. Search Web: Latest fitness research and equipment info
5. Provide Coaching: Evidence-based fitness and nutrition advice
6. Context Aware: RAG-augmented responses with fitness knowledge base

 Observability

If Langfuse is configured, all LLM interactions are traced:

- Prompt/completion pairs
- Tool usage
- RAG retrievals
- Response times
- Token usage

View traces at: https://cloud.langfuse.com

 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

 License

MIT License

 Support

Issues: https://github.com/adarshvuppala-nu/Fitness-Tracker-Service/issues
