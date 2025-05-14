from dataclasses import dataclass

@dataclass
class OpenAiMessage:
    """OpenAI API message model.

    Attributes:
        role (str): The role of the message sender (e.g., "system", "user", "assistant").
        content (str): The content of the message.
    """

    role: str
    content: str
    
    def to_dict(self) -> dict:
        """Convert the OpenAiMessage instance to a dictionary."""
        return {
            "role": self.role.lower(),
            "content": self.content,
        }