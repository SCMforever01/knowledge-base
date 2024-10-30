from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class BaseModelAPI(ABC):
    @abstractmethod
    def send_message(self, query: str, inputs: Dict[str, Any], response_mode: str, user: str,
                     conversation_id: Optional[str] = None, files: Optional[List[Dict[str, Any]]] = None,
                     auto_generate_name: bool = True) -> Dict[str, Any]:
        pass