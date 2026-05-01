# 🎬 AI Video Script Generator

A full-stack generative AI application that transforms any topic into a **production-ready video script** — complete with scene breakdowns, camera directions, voiceover narration, thumbnail suggestions, and shot lists.

**Built with:** FastAPI · React · OpenAI GPT / Groq · Vite

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Setup & Installation](#-setup--installation)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **AI Script Generation** | Generate complete video scripts using OpenAI GPT |
| **Multiple Video Styles** | YouTube, Cinematic, and Instagram Reel formats |
| **Flexible Duration** | 30 seconds, 1 minute, or 5-minute scripts |
| **Scene Breakdowns** | Detailed scene-by-scene analysis with camera directions |
| **Voiceover Narration** | Ready-to-read voiceover text matched to video style |
| **Shot List** | Professional shot list with equipment notes |
| **Thumbnail Suggestions** | AI-generated thumbnail concepts with color schemes |
| **Title Optimization** | SEO-optimized title with 3 alternatives |
| **Premium UI** | Dark glassmorphism theme with smooth animations |
| **Responsive Design** | Works seamlessly on desktop, tablet, and mobile |

---

## 🛠 Tech Stack

### Backend
- **FastAPI** — High-performance async Python web framework
- **Pydantic v2** — Data validation and serialization
- **OpenAI Python SDK** — GPT & Groq API integration (via OpenAI compatibility)
- **Uvicorn** — ASGI server
- **python-dotenv** — Environment variable management

### Frontend
- **React 19** — Component-based UI library
- **Vite 6** — Next-generation frontend build tool
- **Lucide React** — Beautiful, consistent icon library
- **Vanilla CSS** — Custom design system with CSS variables

---

## 🏗 Project Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                │
│                                                          │
│   ┌─────────┐  ┌───────────┐  ┌──────────────────────┐  │
│   │ Header  │  │ InputForm │  │ ScriptOutput (6 tabs)│  │
│   └─────────┘  └─────┬─────┘  └──────────┬───────────┘  │
│                      │                    │              │
│                      │   POST /generate   │              │
│                      ▼                    │              │
├──────────────────────────────────────────────────────────┤
│                    BACKEND (FastAPI)                      │
│                                                          │
│   ┌─────────┐  ┌────────────┐  ┌──────────────────────┐ │
│   │ main.py │→ │ llm_service│→ │ OpenAI GPT API       │ │
│   │ (API)   │  │ (Service)  │  │ (External)           │ │
│   └─────────┘  └────────────┘  └──────────────────────┘ │
│        ↑              ↑                                  │
│   ┌─────────┐  ┌────────────┐                           │
│   │models.py│  │ prompts.py │                           │
│   │(Schema) │  │ (Prompts)  │                           │
│   └─────────┘  └────────────┘                           │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup & Installation

### Prerequisites
- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **OpenAI API Key** — [Get one](https://platform.openai.com/api-keys)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-video-script-generator
```

### 2. Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure your API key
# Edit .env and replace with your actual OpenAI or Groq API key
# GROQ_API_KEY=gsk_...
# or
# OPENAI_API_KEY=sk-...
```

> ⚠️ **Important:** Open `backend/.env` and set your **OPENAI_API_KEY** or **GROQ_API_KEY** before running the backend. The app automatically detects Groq keys (starting with `gsk_`) and switches to high-performance models like Llama-3.3.

### 3. Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install
```

---

## ▶️ Running the Application

### Start the Backend (Terminal 1)
```bash
cd backend
python main.py
```
The API will start at **http://localhost:8000**

### Start the Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
The UI will open at **http://localhost:5173**

### Verify Everything Works
1. Open **http://localhost:5173** in your browser
2. Enter a video topic (e.g., "How to Build a PC on a Budget")
3. Select a video style and duration
4. Click **Generate Script**
5. View the result across 6 organized tabs

---

## 📡 API Documentation

Once the backend is running, interactive API docs are available at:

| URL | Description |
|-----|-------------|
| `http://localhost:8000/docs` | **Swagger UI** — Interactive API testing |
| `http://localhost:8000/redoc` | **ReDoc** — Clean API documentation |
| `http://localhost:8000/health` | Health check endpoint |

### POST `/generate-script`

**Request Body:**
```json
{
  "topic": "How to Build a PC on a Budget",
  "style": "YouTube",
  "duration": "5 minutes"
}
```

**Response:** A structured JSON with `title`, `hook`, `script`, `scenes[]`, `voiceover`, `thumbnail_suggestions[]`, `title_alternatives[]`, `shot_list[]`, `estimated_word_count`, and `target_duration`.

---

## 📁 Project Structure

```
ai-video-script-generator/
├── backend/
│   ├── main.py              # FastAPI application & routes
│   ├── models.py            # Pydantic request/response schemas
│   ├── llm_service.py       # OpenAI API integration service
│   ├── prompts.py           # Prompt engineering templates
│   ├── config.py            # Environment config & settings
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # API key configuration (not committed)
│   └── .env.example         # Environment variable template
│
├── frontend/
│   ├── index.html           # HTML entry point with SEO meta tags
│   ├── package.json         # Node.js dependencies & scripts
│   ├── vite.config.js       # Vite build configuration
│   └── src/
│       ├── main.jsx          # React entry point
│       ├── App.jsx           # Main application component
│       ├── App.css           # App-level layout styles
│       ├── index.css         # Global design system (945 lines)
│       └── components/
│           ├── Header.jsx       # App header with gradient title
│           ├── InputForm.jsx    # Topic, style, duration form
│           ├── LoadingState.jsx # Animated loading with progress steps
│           ├── ErrorState.jsx   # Error display with retry
│           ├── ScriptOutput.jsx # 6-tab output display
│           └── Footer.jsx      # App footer with credits
│
└── README.md                # Project documentation (this file)
```

---

## 🎨 Design Highlights

- **Dark Theme** with glassmorphism cards and backdrop blur effects
- **Gradient Accents** — Purple-to-cyan gradient system
- **Smooth Animations** — Fade-in, stagger, pulse, and shake animations
- **Custom Scrollbar** — Themed scrollbar matching the accent palette
- **Responsive Layout** — Mobile-first design with CSS Grid/Flexbox
- **Inter + JetBrains Mono** — Professional typography via Google Fonts

---

## 📄 License

This project is created for educational purposes as part of a college final-year project.

---

*Built with ❤️ using FastAPI, React, and OpenAI GPT*
