# 🤖 Emzyking AI – Code-Only Chatbot API

Emzyking AI is a **Large Language Model (LLM)-powered backend service** purpose-built for **code generation and programming**. It handles chat session management, multi-turn conversations, agent routing, prompt scoring, and feedback collection. Built with FastAPI, PostgreSQL, and deployed on Railway.

## 🌐 Live URLs

- **Base URL**: [https://emzykingai-production.up.railway.app](https://emzykingai-production.up.railway.app)
- **Swagger Docs**: [https://emzykingai-production.up.railway.app/docs](https://emzykingai-production.up.railway.app/docs)

---

## ⚙️ Features

- ✅ LLM-Powered Code-Only Responses
- ✅ Dynamic Agent Routing Based on Prompt
- ✅ ML-Based Prompt Scoring and Intent Matching
- ✅ New Chat Session Creation
- ✅ Multi-Turn Chat Support
- ✅ One-Off Code Generation
- ✅ Retrieve Chat History by Chat ID
- ✅ Retrieve All Chat Sessions
- ✅ User Feedback Collection on Responses
- ✅ PostgreSQL Integration via SQLAlchemy
- ✅ CORS Enabled for Frontend Integration
- ✅ Scalable Deployment on Railway

---

## 📂 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/new-chat` | Start a new chat session |
| `POST` | `/continue-chat` | Continue an existing chat session |
| `POST` | `/generate-code` | One-off code generation |
| `POST` | `/feedback` | Submit feedback on an assistant's message |
| `GET` | `/chat-history/{chat_id}` | Retrieve chat history for a specific session |
| `GET` | `/all-chat-history` | Retrieve all chat sessions |

---

## 🧠 Routing and Scoring Flow

- Every user prompt is routed by the `RouterAgent`, which evaluates all specialized agents using an **ML scoring function** from `ranking_model.py`.
- `score_prompt()` uses a lightweight classifier to assign confidence scores to each agent based on prompt fit.
- The best-matching agent is selected and its `handle()` function is invoked.
- Feedback on the response can later be submitted via `/feedback` to influence retraining.

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.10+
- **Database**: PostgreSQL (via SQLAlchemy)
- **Deployment**: Railway (Nixpacks)
- **LLM Provider**: Google Gemini (OpenAI as fallback)
- **Others**: Uvicorn, Pydantic, psycopg2, Alembic, Scikit-learn

---

## 🚀 Deployment Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Emzykings/emzyking_ai.git
cd emzyking_ai
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key
DATABASE_URL=your_postgres_connection_string
```

### 5. Run the Server Locally

```bash
uvicorn backend.main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the API.

---

## 🚀 Production Deployment (Railway)

**Start Command:**

```bash
uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}
```

**Environment Variables:**

* `GEMINI_API_KEY`
* `DATABASE_URL`

---

## 🗂️ Project Structure

```
emzyking_ai/
├── backend/
│   ├── main.py               # API endpoints and routing
│   ├── llm_handler.py        # LLM integration and code filtering
│   ├── router_agent.py       # Selects best agent using scoring
│   ├── scorer.py             # Ranks agents using prompt scoring
│   ├── ranking_model.py      # ML model for agent relevance scoring
│   ├── feedback_handler.py   # Collects user feedback on agent responses
│   ├── schemas.py            # Pydantic request models
│   ├── agent_registry.py     # Registry for all available agents
│   ├── utils.py              # Shared utilities (e.g., response formatters)
│   ├── context/
│   │   └── context_builder.py   # Builds contextual memory per chat
│   ├── agents/
│   │   ├── base_agent.py     # Base class for all specialized agents
│   │   ├── code_generator.py
│   │   ├── code_explainer.py
│   │   ├── bug_fixer.py
│   │   ├── memory_agent.py
│   │   └── router_agent.py
│   └── database/
│       ├── db_connection.py  # Database session management
│       ├── db_models.py      # SQLAlchemy ORM models
│       ├── create_tables.py  # DB table creation script
│       └── __init__.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── alembic.ini
└── migrations/
```

---

## 📬 Postman API Collection

**Collection Name**: `Emzyking AI API`

### Collection-Level Variable:

```text
base_url = https://emzykingai-production.up.railway.app
```

### Requests to Add:

| Name               | Method | URL                                     | Body                            |
| ------------------ | ------ | --------------------------------------- | ------------------------------- |
| Home               | GET    | `{{base_url}}/`                         | None                            |
| New Chat           | POST   | `{{base_url}}/new-chat`                 | None                            |
| Continue Chat      | POST   | `{{base_url}}/continue-chat`            | `{"chat_id": "", "prompt": ""}` |
| Generate Code      | POST   | `{{base_url}}/generate-code`            | `{"prompt": ""}`                |
| Submit Feedback    | POST   | `{{base_url}}/feedback`                 | `{"message_id": 1, "is_approved": true, "user_comment": "Great answer!"}` |
| Chat History by ID | GET    | `{{base_url}}/chat-history/{{chat_id}}` | None                            |
| All Chat History   | GET    | `{{base_url}}/all-chat-history`         | None                            |

> You can export the collection as `.json` to share with your team.

---

## 🔌 API Wrappers

### JavaScript (Axios)

```js
import axios from 'axios';

const API_BASE = 'https://emzykingai-production.up.railway.app';

export const createNewChat = async () => {
  const res = await axios.post(`${API_BASE}/new-chat`);
  return res.data.chat_id;
};

export const continueChat = async (chatId, prompt) => {
  const res = await axios.post(`${API_BASE}/continue-chat`, { chat_id: chatId, prompt });
  return res.data.response;
};

export const generateCode = async (prompt) => {
  const res = await axios.post(`${API_BASE}/generate-code`, { prompt });
  return res.data.code;
};

export const getChatHistory = async (chatId) => {
  const res = await axios.get(`${API_BASE}/chat-history/${chatId}`);
  return res.data.history;
};

export const getAllChats = async () => {
  const res = await axios.get(`${API_BASE}/all-chat-history`);
  return res.data.all_chats;
};

export const submitFeedback = async (messageId, isApproved, comment) => {
  const res = await axios.post(`${API_BASE}/feedback`, {
    message_id: messageId,
    is_approved: isApproved,
    user_comment: comment,
  });
  return res.data;
};
```

### Python (Requests)

```python
import requests

API_BASE = "https://emzykingai-production.up.railway.app"

def create_new_chat():
    res = requests.post(f"{API_BASE}/new-chat")
    return res.json()['chat_id']

def continue_chat(chat_id, prompt):
    res = requests.post(f"{API_BASE}/continue-chat", json={"chat_id": chat_id, "prompt": prompt})
    return res.json()['response']

def generate_code(prompt):
    res = requests.post(f"{API_BASE}/generate-code", json={"prompt": prompt})
    return res.json()['code']

def get_chat_history(chat_id):
    res = requests.get(f"{API_BASE}/chat-history/{chat_id}")
    return res.json()['history']

def get_all_chats():
    res = requests.get(f"{API_BASE}/all-chat-history")
    return res.json()['all_chats']

def submit_feedback(message_id, is_approved, comment):
    res = requests.post(f"{API_BASE}/feedback", json={
        "message_id": message_id,
        "is_approved": is_approved,
        "user_comment": comment
    })
    return res.json()
```

---

## 🧠 Frontend Integration Guide

### Session Flow

1. **Start a chat:**
   `createNewChat()` → store `chat_id` in state

2. **Send message in session:**
   `continueChat(chat_id, user_input)`

3. **Get chat history:**
   Call `getChatHistory(chat_id)` on component mount

4. **One-off code generation:**
   Use `generateCode(prompt)` for instant output

5. **Submit feedback:**
   After rendering assistant response, allow user to approve/disapprove it → call `submitFeedback()`

### Notes

* All requests use `application/json`
* No authentication required (public for now)
* CORS is fully enabled

---

## 🔮 Future Enhancements

* 🔐 JWT-based API Authentication
* 📊 Rate Limiting & Usage Analytics
* 🌍 Multi-Region Deployments
* 🐳 Docker Support
* 🔁 WebSocket Support for Real-time Messaging
* 🤖 Continuous Feedback-Informed Agent Retraining

---

## 👤 Author

**Emzyking AI Team**  
*Backend Engineer: Emzyking*