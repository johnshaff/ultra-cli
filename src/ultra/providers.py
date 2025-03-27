import openai
from typing import List

class BaseProvider:
    def list_models(self) -> List[str]:
        """Return a list of available model names."""
        raise NotImplementedError()

    def get_cheapest_model(self) -> str:
        """Return the cheapest model name to use for compaction."""
        raise NotImplementedError()

    def stream_completion(self, model_name: str, messages: list):
        """Stream tokens from the provider. Must yield partial text."""
        raise NotImplementedError()

    def get_completion(self, model_name: str, prompt: str) -> str:
        """Get a single completion from the provider. (Used for summary, etc.)"""
        raise NotImplementedError()

    def short_name(self) -> str:
        """Identifier for the provider, e.g. 'openai'."""
        raise NotImplementedError()

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def short_name(self) -> str:
        return "openai"

    def list_models(self) -> List[str]:
        # For large org accounts, listing all can be lengthy.
        # As an example, we fetch them and filter by ones we want to show:
        result = openai.models.list()
        models = [m.id for m in result.data if "gpt" in m.id]
        return sorted(models)

    def get_cheapest_model(self) -> str:
        """
        Hardcode or implement logic to pick a cheap model like "gpt-3.5-turbo".
        """
        return "gpt-4o-mini"

    def stream_completion(self, model_name: str, messages: list):
        """
        messages: A list of dicts: [{"role": "user"/"assistant"/"system", "content": "text"}]
        Yields tokens as they come in.
        """
        response = openai.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is not None:
                yield content

    def get_completion(self, model_name: str, prompt: str) -> str:
        """Non-streaming single response (helpful for summary, system tasks, etc.)."""
        response = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()