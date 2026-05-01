"""
Prompt Engineering Module for the AI Video Script Generator.

Contains carefully designed prompt templates that instruct the LLM
to produce structured, consistent, and high-quality video scripts.
"""


def build_system_prompt() -> str:
    """
    Build the system-level prompt that defines the AI's role and behavior.
    This establishes the persona and output format expectations.
    """
    return """You are an expert video scriptwriter and content strategist with 15+ years of experience creating scripts for YouTube, Netflix, Instagram, and major production studios.

Your expertise includes:
- Writing compelling hooks that capture attention in the first 5 seconds
- Structuring scripts for maximum viewer retention
- Creating scene-by-scene breakdowns with professional camera directions
- Writing natural, engaging voiceover narrations
- Suggesting thumbnail concepts and title optimization for SEO

IMPORTANT RULES:
1. Always respond with VALID JSON only. No markdown, no extra text.
2. Follow the exact JSON schema provided in the user prompt.
3. Make the script engaging, professional, and tailored to the specified style.
4. Use industry-standard camera terminology (e.g., "Wide Shot", "Close-Up", "Dolly In", "Crane Shot").
5. Match the tone and pacing to the video style (casual for YouTube, dramatic for Cinematic, fast-paced for Instagram Reels).
6. Ensure the script length matches the requested duration:
   - 30 seconds: ~75 words
   - 1 minute: ~150 words
   - 5 minutes: ~750 words"""


def build_user_prompt(topic: str, style: str, duration: str) -> str:
    """
    Build the user-level prompt with specific generation instructions.

    Args:
        topic: The video topic/subject
        style: The video style (YouTube, Cinematic, Instagram Reel)
        duration: The target duration (30 seconds, 1 minute, 5 minutes)

    Returns:
        A fully formatted prompt string with JSON schema instructions.
    """

    # Style-specific guidance
    style_guides = {
        "YouTube": {
            "tone": "conversational, energetic, and relatable",
            "pacing": "moderate with emphasis on retention hooks every 30 seconds",
            "camera_style": "mix of talking head, B-roll, and screen recordings",
            "hook_style": "question-based or bold statement to create curiosity"
        },
        "Cinematic": {
            "tone": "dramatic, polished, and emotionally evocative",
            "pacing": "slow and deliberate with dramatic pauses",
            "camera_style": "cinematic shots including drone, gimbal, slow-motion, and dramatic lighting",
            "hook_style": "visually stunning opening with a powerful voiceover line"
        },
        "Instagram Reel": {
            "tone": "snappy, trendy, and attention-grabbing",
            "pacing": "extremely fast with quick cuts every 2-3 seconds",
            "camera_style": "vertical framing, close-ups, dynamic transitions, text overlays",
            "hook_style": "pattern interrupt or controversial/surprising statement"
        }
    }

    guide = style_guides.get(style, style_guides["YouTube"])

    # Duration-based scene count guidance
    scene_counts = {
        "30 seconds": "3-4 scenes",
        "1 minute": "5-7 scenes",
        "5 minutes": "12-18 scenes"
    }
    scene_count = scene_counts.get(duration, "5-7 scenes")

    # Shot count guidance
    shot_counts = {
        "30 seconds": "4-6 shots",
        "1 minute": "8-12 shots",
        "5 minutes": "20-30 shots"
    }
    shot_count = shot_counts.get(duration, "8-12 shots")

    return f"""Generate a complete, professional video script for the following:

**TOPIC:** {topic}
**STYLE:** {style}
**DURATION:** {duration}

**STYLE GUIDELINES:**
- Tone: {guide['tone']}
- Pacing: {guide['pacing']}
- Camera Style: {guide['camera_style']}
- Hook Style: {guide['hook_style']}

**REQUIREMENTS:**
- Create {scene_count} scenes with detailed camera directions
- Include {shot_count} in the shot list
- Provide 3 thumbnail suggestions with specific design details
- Provide 3 alternative title options optimized for SEO
- The voiceover should be natural and match the style's tone
- The hook must be attention-grabbing and work within the first 5 seconds

**RESPOND WITH THIS EXACT JSON STRUCTURE:**
{{
  "title": "A compelling, SEO-optimized title for the video",
  "hook": "The attention-grabbing opening line or action for the first 5 seconds",
  "script": "The complete video script with natural flow and transitions between scenes",
  "scenes": [
    {{
      "scene": 1,
      "description": "Detailed description of what happens in this scene",
      "camera": "Specific camera angle/movement (e.g., 'Wide Shot - Slow Dolly In')",
      "duration": "Estimated duration (e.g., '5 seconds')",
      "visual_notes": "Additional notes about lighting, graphics, text overlays, etc."
    }}
  ],
  "voiceover": "The complete voiceover narration text, written naturally for speaking aloud",
  "thumbnail_suggestions": [
    {{
      "concept": "Description of the thumbnail concept",
      "text_overlay": "Text to display on the thumbnail",
      "color_scheme": "Color palette suggestion (e.g., 'Bold red and white on dark background')",
      "style_notes": "Additional style details (e.g., 'Use shocked face expression, large bold font')"
    }}
  ],
  "title_alternatives": [
    "Alternative Title Option 1",
    "Alternative Title Option 2",
    "Alternative Title Option 3"
  ],
  "shot_list": [
    {{
      "shot_number": 1,
      "shot_type": "Wide Shot / Close-Up / Medium Shot / etc.",
      "description": "What this shot captures",
      "equipment_notes": "Suggested equipment or technique (e.g., 'Tripod, 50mm lens')"
    }}
  ]
}}

CRITICAL: Return ONLY valid JSON. No markdown formatting, no code blocks, no explanatory text before or after the JSON."""
