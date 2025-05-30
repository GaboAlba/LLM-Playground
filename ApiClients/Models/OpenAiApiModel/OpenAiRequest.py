from .OpenAiMessage import OpenAiMessage
from ApiClients.Models.LLMRequest import LLMRequest
from dataclasses import dataclass, field
from typing import List

@dataclass
class OpenAiRequest(LLMRequest):
    """OpenAI API request model.

    Attributes:
        model (str): The name of the model to use.
        messages (list): A list of messages to send to the model.
        temperature (float): Sampling temperature. Higher values mean more random completions.
        max_tokens (int): The maximum number of tokens to generate in the completion.
        top_p (float): Nucleus sampling parameter. 0.5 means half of all likelihood-weighted options are considered.
        frequency_penalty (float): Penalizes new tokens based on their existing frequency in the text so far.
        presence_penalty (float): Penalizes new tokens based on whether they appear in the text so far.
    """

    model: str
    messages: List[OpenAiMessage] = field(default_factory=list)
    temperature: float = 0.7
    max_completion_tokens: int = 1000
    top_p: float = 1.0
    tools: List = field(default_factory=list)
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0