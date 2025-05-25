import json
from google import genai
from ApiClients.LLMClient import LLMClient
from .Models.LLMRequest import LLMRequest
from .Utils import Utils
from .Models.OpenAiApiModel.OpenAiMessage import OpenAiMessage
from .Models.GoogleAiApiModel.GoogleAiRequest import GoogleAiRequest
from google import genai
from google.genai import types

class GoogleAiClient(LLMClient):
  def __init__(self, api_key : str = "test"):
    super()._init_(api_key)
    self.name = "GoogleAI"
    self.client = genai.Client(api_key=self.api_key)
    try:
      models = self.client.models.list()
      self.allowed_models = []
      for model in models.page:
        self.allowed_models.append(model.name)
    except Exception as e:
      print(f"Error fetching models: {e}")
      self.allowed_models = []

  def generate_response(self, request:GoogleAiRequest) -> str:
    try:
      response = self.client.models.generate_content(
        model=request.model,
        contents= request.content_message,
        config= types.GenerateContentConfig(
          system_instruction= request.system_message,
          temperature= request.temperature,
          max_output_tokens= request.max_output_tokens,
          top_k= request.top_k,
          top_p= request.top_p,
          frequency_penalty= request.frequency_penalty,
          presence_penalty= request.presence_penalty
        )
      )

      if (len(response.candidates) > 0):
        return response.text
      else:
        return "No candidates returned from Google AI API"

    except Exception as e:
      print(f"Call to Google AI API failed: {e}")
      return ""
  
  def convert_prompt_to_object(self, prompt:str):
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
  
  def build_request(self, model:str, messages:list[OpenAiMessage], temperature:float, max_tokens:int, top_k:int, top_p:float, frequency_penalty:float, presence_penalty:float) -> LLMRequest:
    """
    Build the GoogleAiRequest object.
    """
    system_message = ""
    content_message = ""
    for msg in messages:
      # Only one system message is allowed.
      if msg.role == "system":
        system_message = msg.content
      else:
        content_message += msg.role + ":" + msg.content
    
    return GoogleAiRequest(
      model=model,
      system_message=system_message,
      content_message=content_message,
      temperature=temperature,
      max_output_tokens=max_tokens,
      top_k=top_k,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty
    )
