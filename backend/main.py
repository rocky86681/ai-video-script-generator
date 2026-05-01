"""
AI Video Script Generator — FastAPI Backend

Main application entry point. Provides REST API endpoints for
generating AI-powered video scripts with scene breakdowns,
voiceover narrations, and production-ready shot lists.

Author: AI Video Script Generator Team
Version: 1.0.0
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from models import ScriptRequest, ScriptResponse
from llm_service import llm_service

# ──────────────────────────────────────────────
# Logging Configuration
# ──────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Application Lifespan
# ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("═" * 60)
    logger.info("🎬  AI Video Script Generator API — Starting Up")
    logger.info(f"   Model: {settings.OPENAI_MODEL}")
    logger.info(f"   API Key: {'✅ Configured' if settings.OPENAI_API_KEY else '❌ NOT SET'}")
    logger.info("═" * 60)
    yield
    logger.info("🎬  AI Video Script Generator API — Shutting Down")


# ──────────────────────────────────────────────
# FastAPI Application
# ──────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware — allows frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# API Routes
# ──────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "AI Video Script Generator API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check with configuration status."""
    return {
        "status": "healthy",
        "model": settings.OPENAI_MODEL,
        "api_key_configured": bool(settings.OPENAI_API_KEY)
    }


@app.post(
    "/generate-script",
    response_model=ScriptResponse,
    tags=["Script Generation"],
    summary="Generate a complete video script",
    description=(
        "Generate a professional video script with title, hook, "
        "full script, scene breakdowns, voiceover narration, "
        "thumbnail suggestions, and a shot list."
    )
)
async def generate_script(request: ScriptRequest):
    """
    Generate a complete AI-powered video script.

    **Input:**
    - `topic` — The main subject of the video
    - `style` — YouTube, Cinematic, or Instagram Reel
    - `duration` — 30 seconds, 1 minute, or 5 minutes

    **Output:**
    A structured JSON response containing the title, hook, complete script,
    scene-by-scene breakdown with camera angles, voiceover narration,
    thumbnail suggestions, alternative titles, and a detailed shot list.
    """
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail=(
                "API key is not configured. Please set OPENAI_API_KEY "
                "or GROQ_API_KEY in your .env file."
            )
        )

    try:
        logger.info(
            f"📝 New script request: "
            f"topic='{request.topic}', "
            f"style={request.style.value}, "
            f"duration={request.duration.value}"
        )

        result = await llm_service.generate_script(
            topic=request.topic,
            style=request.style.value,
            duration=request.duration.value
        )

        logger.info(f"✅ Script generated successfully: '{result.title}'")
        return result

    except ValueError as e:
        logger.error(f"❌ Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Script generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate script: {str(e)}"
        )


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
