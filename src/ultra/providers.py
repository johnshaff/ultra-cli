import openai
from typing import List
from ultra.text_templates import TRANSCRIBE_EXACT, TRANSCRIBE_SPEAKERS, TRANSCRIBE_SPEAKERS_V2

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
        result = openai.models.list()
        models = [m.id for m in result.data if "gpt" in m.id]
        return sorted(models)

    def get_cheapest_model(self) -> str:
        # Hardcode the model for now.
        return "gpt-4o-mini"

    def stream_completion(self, model_name: str, messages: list):
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
        response = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()

    def send_non_streaming_request(self, messages: list) -> str:
        response = openai.chat.completions.create(
            model=self.get_cheapest_model(),
            messages=messages,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()

    def format_transcription(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            file_upload = openai.files.create(file=f, purpose="user_data")
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": file_upload.id}},
                    {"type": "text", "text": TRANSCRIBE_SPEAKERS_V2}
                ]
            }
        ]
        return self.send_non_streaming_request(messages)
        