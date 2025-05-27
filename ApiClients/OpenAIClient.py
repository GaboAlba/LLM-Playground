import openai
import json
from .Utils import Utils
from ApiClients.LLMClient import LLMClient
from .Models.OpenAiApiModel.OpenAiMessage import OpenAiMessage
from .Models.OpenAiApiModel.OpenAiRequest import OpenAiRequest

class OpenAIClient(LLMClient):  
  def __init__(self, api_key : str = "test"):
    super()._init_(api_key)
    self.name = "OpenAI"
    self.client = openai.OpenAI(api_key= self.api_key)
    try:
      models = self.client.models.list()
      self.allowed_models = []
      for model in models.data:
        self.allowed_models.append(model.id)
    except Exception as e:
      print(f"Error fetching models: {e}")
      self.allowed_models = []

  def generate_response(self, request: OpenAiRequest) -> str:
    try:
      messages = []
      for msg in request.messages:
        messages.append(msg.to_dict())
      response = self.client.responses.create(
        model=request.model,
        input= messages,
        temperature = request.temperature,
        max_output_tokens = request.max_completion_tokens,
        top_p = request.top_p
      )

      return response.output[0].content[0].text
    except Exception as e:
      print(f"Call to OpenAI API failed: {e}")
      return ""
    
  def convert_prompt_to_object(self, prompt:str) -> list[dict]:
    """
    Convert the prompt to a list of OpenAiMessage objects.
    """
    print("Hit the child class")
    try:
      # Split the prompt into sections based on the role tags
      messages = Utils.convert_prompt_to_json(prompt)
      openai_messages = [OpenAiMessage(role=message['role'], content=message['content']) for message in messages]
      return openai_messages
    except json.JSONDecodeError as e:
      print(f"Failed to decode JSON: {e}")
      return []
    
  def build_request(self, model:str, messages:list[OpenAiMessage], temperature:float, max_tokens:int, top_k:int, top_p:float, frequency_penalty:float, presence_penalty:float) -> OpenAiRequest:
    """
    Build the OpenAiRequest object.
    """
    return OpenAiRequest(
      model=model,
      messages=messages,
      temperature=temperature,
      max_completion_tokens=max_tokens,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty
    )