from ApiClients.Models.OpenAiApiModel.OpenAiMessage import OpenAiMessage
from ApiClients.Models.LLMRequest import LLMRequest
from dataclasses import dataclass, field
from typing import List

@dataclass
class GoogleAiRequest(LLMRequest):
    """OpenAI API request model.

    Attributes:
        model (str): The name of the model to use.
        system_message (str): The system message to set the context for the model.
        content_message (str): The content message to send to the model.
        temperature (float): Sampling temperature. Higher values mean more random completions.
        max_output_tokens (int): The maximum number of tokens to generate in the completion.
        top_k (int): The number of highest probability tokens to consider for sampling.
        top_p (float): Nucleus sampling parameter. 1.0 means half of all likelihood-weighted options are considered.
        tools (List): A list of tools that the model can use.
        frequency_penalty (float): Penalizes new tokens based on their existing frequency in the text so far.
        presence_penalty (float): Penalizes new tokens based on whether they appear in the text so far.
    """

    model: str
    system_message: str
    content_message: str
    # messages: List[OpenAiMessage] = field(default_factory=list)
    temperature: float = 0.7
    max_output_tokens: int = 1000
    top_k: int = 3
    top_p: float = 1.0
    tools: List = field(default_factory=list)
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0