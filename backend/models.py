"""
Pydantic models for request/response validation.
Defines the data schema for the AI Video Script Generator API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


# ──────────────────────────────────────────────
# Enums for constrained input values
# ──────────────────────────────────────────────

class VideoStyle(str, Enum):
    """Supported video styles."""
    YOUTUBE = "YouTube"
    CINEMATIC = "Cinematic"
    INSTAGRAM_REEL = "Instagram Reel"


class VideoDuration(str, Enum):
    """Supported video durations."""
    SHORT = "30 seconds"
    MEDIUM = "1 minute"
    LONG = "5 minutes"


# ──────────────────────────────────────────────
# Request Models
# ──────────────────────────────────────────────

class ScriptRequest(BaseModel):
    """Request body for the /generate-script endpoint."""

    topic: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="The main topic or subject of the video.",
        examples=["How to Build a PC on a Budget"]
    )
    style: VideoStyle = Field(
        ...,
        description="The style/format of the video."
    )
    duration: VideoDuration = Field(
        ...,
        description="The target duration of the video."
    )


# ──────────────────────────────────────────────
# Response Models
# ──────────────────────────────────────────────

class SceneBreakdown(BaseModel):
    """A single scene in the video script."""

    scene: int = Field(..., description="Scene number")
    description: str = Field(..., description="What happens in this scene")
    camera: str = Field(..., description="Camera angle or shot type")
    duration: str = Field(..., description="Estimated duration of the scene")
    visual_notes: str = Field(
        default="",
        description="Additional visual/editing notes"
    )


class ShotListItem(BaseModel):
    """A single item in the shot list for video editing."""

    shot_number: int
    shot_type: str  # e.g., "Wide Shot", "Close-Up", "Drone Shot"
    description: str
    equipment_notes: str = ""


class ThumbnailSuggestion(BaseModel):
    """Thumbnail design suggestion."""

    concept: str
    text_overlay: str
    color_scheme: str
    style_notes: str


class ScriptResponse(BaseModel):
    """Full response from the AI script generation."""

    title: str = Field(..., description="Suggested video title")
    hook: str = Field(
        ..., description="Attention-grabbing opening (first 5 seconds)"
    )
    script: str = Field(..., description="Full video script text")
    scenes: List[SceneBreakdown] = Field(
        ..., description="Scene-by-scene breakdown"
    )
    voiceover: str = Field(
        ..., description="Full voiceover narration text"
    )
    thumbnail_suggestions: List[ThumbnailSuggestion] = Field(
        default_factory=list,
        description="Thumbnail design suggestions"
    )
    title_alternatives: List[str] = Field(
        default_factory=list,
        description="Alternative title options"
    )
    shot_list: List[ShotListItem] = Field(
        default_factory=list,
        description="Detailed shot list for video editing"
    )
    estimated_word_count: int = Field(
        default=0,
        description="Estimated total word count of the script"
    )
    target_duration: str = Field(
        default="",
        description="The target duration requested"
    )
