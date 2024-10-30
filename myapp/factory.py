import logging
from typing import Dict, Any

from myapp.apis.mify import MifyModelAPI
from myapp.apis.openai import OpenAIModelAPI
from myapp.apis.anthropic import AnthropicModelAPI


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelAPIFactory:
    @staticmethod
    def create_model_api(api_type: str, config: Dict[str, Any]) -> OpenAIModelAPI | AnthropicModelAPI | MifyModelAPI:
        if api_type == "openai":
            logger.info(f"Creating OpenAIModelAPI with API key: {config['api_key']} and base URL: {config['base_url']}")
            return OpenAIModelAPI(api_key=config["api_key"], base_url=config["base_url"])
        elif api_type == "anthropic":
            logger.info(f"Creating AnthropicModelAPI with API key: {config['api_key']} and base URL: {config['base_url']}")
            return AnthropicModelAPI(api_key=config["api_key"], base_url=config["base_url"])
        elif api_type == "mify":
            logger.info(f"Creating MifyModelAPI with API key: {config['api_key']} and base URL: {config['base_url']}")
            return MifyModelAPI(api_key=config["api_key"], base_url=config["base_url"])
        else:
            raise ValueError(f"Unsupported API type: {api_type}")