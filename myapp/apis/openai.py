from .generic import GenericModelAPI

class OpenAIModelAPI(GenericModelAPI):
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        super().__init__(api_key, base_url, "chat/completions")