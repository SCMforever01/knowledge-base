from django.db import models
import uuid
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} by {self.user.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    event_type = models.CharField(max_length=50)  # e.g., 'agent_message', 'agent_thought'
    created_at = models.DateTimeField(auto_now_add=True)
    message_id = models.UUIDField(default=uuid.uuid4, editable=False)
    task_id = models.UUIDField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    tool = models.CharField(max_length=100, null=True, blank=True)
    tool_labels = models.JSONField(null=True, blank=True)
    tool_input = models.TextField(null=True, blank=True)
    message_files = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Message in {self.conversation.conversation_id}: {self.content[:50]}"

class Metadata(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metadata for {self.conversation.conversation_id}"


def get_conversation_history(user: str, conversation_id: str) -> List[Dict[str, Any]]:
    try:
        user_obj = User.objects.get(username=user)
        conversation = Conversation.objects.get(conversation_id=conversation_id, user=user_obj)
        messages = Message.objects.filter(conversation=conversation).order_by('created_at')
        history = [
            {
                "content": message.content,
                "event_type": message.event_type,
                "created_at": message.created_at,
                "message_id": message.message_id,
                "task_id": message.task_id,
                "position": message.position,
                "tool": message.tool,
                "tool_labels": message.tool_labels,
                "tool_input": message.tool_input,
                "message_files": message.message_files
            }
            for message in messages
        ]
        metadata = Metadata.objects.filter(conversation=conversation).first()
        if metadata:
            history.append({
                "metadata": metadata.metadata,
                "created_at": metadata.created_at
            })
        return history
    except User.DoesNotExist:
        logger.error(f"User {user} does not exist.")
        return []
    except Conversation.DoesNotExist:
        logger.error(f"Conversation {conversation_id} does not exist for user {user}.")
        return []