import openai
import json
from ApiClients.LLMClient import LLMClient

class OpenAIClient(LLMClient):  
  def __init__(self, api_key : str):
    super()._init_(api_key)
    self.name = "OpenAI"
    self.client = openai.OpenAI(api_key= self.api_key)
    models = self.client.models.list()
    self.allowed_models = []
    for model in models.data:
      self.allowed_models.append(model.id)