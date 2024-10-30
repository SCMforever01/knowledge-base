import logging
import re
from typing import Dict, Optional, Any, List, Generator
import requests
import json

from myapp.ResponseHandler import ResponseHandler

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenericModelAPI:
    def __init__(self, api_key: str, base_url: str, endpoint: str):
        self.api_key = api_key
        self.base_url = base_url
        self.endpoint = endpoint

    def send_message(self, query: str, inputs: Dict[str, Any], response_mode: str, user: str,
                     conversation_id: Optional[str] = None, files: Optional[List[Dict[str, Any]]] = None,
                     auto_generate_name: bool = True) -> List[Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "query": query,
            "inputs": inputs,
            "response_mode": response_mode,
            "user": user,
            "conversation_id": conversation_id,
            "files": files,
            "auto_generate_name": auto_generate_name
        }

        logger.info(f"Sending message to {self.base_url}/{self.endpoint} with response mode: {response_mode}")
        logger.info(f"Request data: {data}")

        if response_mode == "streaming":
            return list(self._streaming_send_message(data, headers))
        else:
            return self._blocking_send_message(data, headers)

    def _streaming_send_message(self, data: Dict[str, Any], headers: Dict[str, str]) -> Generator[Dict[str, Any], None, None]:
        response = requests.post(f"{self.base_url}/{self.endpoint}", json=data, headers=headers, stream=True)
        logger.info(f"Received response status code: {response.status_code}")
        if response.status_code == 200:
            pattern = re.compile(r'data: (.+)')
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    match = pattern.match(line)
                    if match:
                        event_data = match.group(1).strip()
                        if event_data:
                            logger.info(f"Raw event data: {event_data}")
                            print(event_data)
                            try:
                                event = json.loads(event_data)
                                logger.info(f"Event received: {event}")
                                yield event
                            except json.JSONDecodeError as e:
                                logger.error(f"Failed to parse JSON: {e}, Event Data: {event_data}")
        else:
            logger.error(f"Error: {response.status_code}, {response.text}")
            raise Exception(f"streaming_send_message_Error: {response.status_code}, {response.text}")

    def _blocking_send_message(self, data: Dict[str, Any], headers: Dict[str, str]) -> List[Dict[str, Any]]:
        response = requests.post(f"{self.base_url}/{self.endpoint}", json=data, headers=headers)
        logger.info(f"Received response status code: {response.status_code}")

        if response.status_code == 200:
            logger.info(f"Raw response text: {response.text}")
            events = ResponseHandler._parse_response(response.text)
            logger.info(f"Parsed events: {events}")
            return events
        else:
            logger.error(f"Error: {response.status_code}, {response.text}")
            raise Exception(f"Error: {response.status_code}, {response.text}")