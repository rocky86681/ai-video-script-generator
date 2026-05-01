"""
LLM Service Module for the AI Video Script Generator.

Handles communication with the OpenAI API (or compatible endpoints)
and parses the structured JSON response from the LLM.
"""

import json
import logging
from openai import AsyncOpenAI
from config import settings
from prompts import build_system_prompt, build_user_prompt
from models import ScriptResponse

logger = logging.getLogger(__name__)


class LLMService:
    """Service class for interacting with OpenAI-compatible LLM APIs."""

    def __init__(self):
        """Initialize the OpenAI async client."""
        if not settings.OPENAI_API_KEY:
            logger.warning(
                "OPENAI_API_KEY is not set. API calls will fail. "
                "Please set it in your .env file."
            )
            
        client_kwargs = {"api_key": settings.OPENAI_API_KEY}
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("gsk_"):
            client_kwargs["base_url"] = "https://api.groq.com/openai/v1"
            
        self.client = AsyncOpenAI(**client_kwargs)
        self.model = settings.OPENAI_MODEL
        
        # Fallback to a Groq model if using a Groq key but left the default GPT model in env
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("gsk_") and self.model.startswith("gpt-"):
            self.model = "llama-3.3-70b-versatile"

    async def generate_script(
        self, topic: str, style: str, duration: str
    ) -> ScriptResponse:
        """
        Generate a complete video script using the LLM.

        Args:
            topic: The video topic/subject
            style: The video style (YouTube, Cinematic, Instagram Reel)
            duration: The target duration (30 seconds, 1 minute, 5 minutes)

        Returns:
            ScriptResponse: Parsed and validated script data

        Raises:
            ValueError: If the LLM response cannot be parsed
            Exception: If the API call fails
        """
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(topic, style, duration)

        logger.info(
            f"Generating script | Topic: '{topic}' | "
            f"Style: {style} | Duration: {duration}"
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=4096,
                response_format={"type": "json_object"}
            )

            raw_content = response.choices[0].message.content
            logger.info(f"Received response ({len(raw_content)} chars)")

            # Parse the JSON response
            script_data = self._parse_response(raw_content)

            # Add metadata
            script_data["target_duration"] = duration
            script_data["estimated_word_count"] = len(
                script_data.get("script", "").split()
            )

            # Validate through Pydantic model
            return ScriptResponse(**script_data)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(
                "The AI generated an invalid response. "
                "Please try again."
            )
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise

    def _parse_response(self, raw_content: str) -> dict:
        """
        Parse the raw LLM response into a Python dictionary.
        Handles edge cases like markdown code blocks in the response.

        Args:
            raw_content: Raw string response from the LLM

        Returns:
            dict: Parsed JSON data
        """
        content = raw_content.strip()

        # Strip markdown code fences if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()
        return json.loads(content)


# Singleton instance
llm_service = LLMService()
