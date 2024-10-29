from .generic import GenericModelAPI

class AnthropicModelAPI(GenericModelAPI):
    def __init__(self, api_key: str, base_url: str = "https://api.anthropic.com/v1"):
        super().__init__(api_key, base_url, "complete")