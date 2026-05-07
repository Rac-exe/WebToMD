"""Concrete AI provider implementations.

Each provider is only imported if its SDK is installed.
Missing SDK -> ImportError caught gracefully by the caller.
"""

from __future__ import annotations

import os

from webtomd.ai.base import AIProvider


class AnthropicProvider(AIProvider):
    name = "Anthropic"
    default_model = "claude-sonnet-4-5"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        import anthropic

        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = client.messages.create(
            model=self.default_model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text


class OpenAIProvider(AIProvider):
    name = "OpenAI"
    default_model = "gpt-4o-mini"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        import openai

        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        resp = client.chat.completions.create(
            model=self.default_model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content or ""


class GeminiProvider(AIProvider):
    name = "Google Gemini"
    default_model = "gemini-2.0-flash"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        import google.generativeai as genai

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel(self.default_model)
        resp = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens),
        )
        return resp.text


class GroqProvider(AIProvider):
    name = "Groq"
    default_model = "llama-3.3-70b-versatile"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        from groq import Groq

        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        resp = client.chat.completions.create(
            model=self.default_model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content or ""


class OllamaProvider(AIProvider):
    name = "Ollama"
    default_model = "llama3.2"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        import httpx

        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        resp = httpx.post(
            f"{host}/api/generate",
            json={"model": self.default_model, "prompt": prompt, "stream": False},
            timeout=120.0,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
