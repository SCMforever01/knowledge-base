from .generic import GenericModelAPI

class MifyModelAPI(GenericModelAPI):
    def __init__(self, api_key: str, base_url: str = "https://mify-be.pt.xiaomi.com/api/v1"):
        super().__init__(api_key, base_url, "chat-messages")