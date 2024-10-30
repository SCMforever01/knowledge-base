import logging
import re
import json
from typing import List, Dict, Any

from myapp.chat.models import Conversation, User, Metadata, Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class ResponseHandler:
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = events
        logger.info(f"Initialized ResponseHandler with events: {events}")

    @classmethod
    def from_response_text(cls, response_text: str):
        logger.info(f"Raw response text: {response_text}")
        events = cls._parse_response(response_text)
        return cls(events)

    @staticmethod
    def _parse_response(response_text: str) -> List[Dict[str, Any]]:
        events = []
        pattern = re.compile(r'data: (.+)')
        for line in response_text.splitlines():
            match = pattern.match(line)
            if match:
                event_data = match.group(1).strip()
                if event_data:
                    logger.info(f"Parsed event data: {event_data}")
                    try:
                        event = json.loads(event_data)
                        events.append(event)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON: {e}, Event Data: {event_data}")
        return events

    def show_stream(self):
        """流式展示响应数据"""
        for event in self.events:
            if event.get('event') == 'agent_message':
                print(event['answer'], end='', flush=True)
            elif event.get('event') == 'agent_thought':
                print(f"\nThought: {event['thought']}")
            elif event.get('event') == 'message_end':
                print("\nMessage End")
            else:
                print(event)

    def show_non_stream(self):
        """非流式展示响应数据"""
        answer = ""
        thoughts = []
        for event in self.events:
            if event.get('event') == 'agent_message':
                answer += event['answer']
            elif event.get('event') == 'agent_thought':
                thoughts.append(event['thought'])
            elif event.get('event') == 'message_end':
                break
        print(f"Answer: {answer}")
        if thoughts:
            print("Thoughts:")
            for thought in thoughts:
                print(f"  - {thought}")

    def get_answer(self) -> str:
        """获取完整的回答"""
        answer = ""
        for event in self.events:
            if event.get('event') == 'agent_message':
                answer += event['answer']
        return answer

    def get_thoughts(self) -> list:
        """获取所有的思考内容"""
        thoughts = []
        for event in self.events:
            if event.get('event') == 'agent_thought':
                thoughts.append(event['thought'])
        return thoughts

    def get_metadata(self) -> dict:
        """获取消息结束时的元数据"""
        for event in self.events:
            if event.get('event') == 'message_end':
                return event.get('metadata', {})
        return {}

    def save_to_database(self):
        user, created = User.objects.get_or_create(username=self.events[0]['user'],
                                                   defaults={'email': f"{self.events[0]['user']}@example.com"})
        conversation, created = Conversation.objects.get_or_create(conversation_id=self.conversation_id, user=user)

        for event in self.events:
            if event['event'] == 'message_end':
                metadata = Metadata(
                    conversation=conversation,
                    metadata=event.get('metadata', {}),
                )
                metadata.save()
                logger.info(f"Metadata saved: {metadata}")
            else:
                message = Message(
                    conversation=conversation,
                    content=event.get('answer', '') or event.get('thought', ''),
                    event_type=event['event'],
                    message_id=event.get('message_id'),
                    task_id=event.get('task_id'),
                    position=event.get('position'),
                    tool=event.get('tool'),
                    tool_labels=event.get('tool_labels'),
                    tool_input=event.get('tool_input'),
                    message_files=event.get('message_files')
                )
                message.save()
                logger.info(f"Message saved: {message}")