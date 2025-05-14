from ApiClients.LLMClient import LLMClient
from google import genai

class GoogleAiClient(LLMClient):
  def __init__(self, api_key : str):
    super()._init_(api_key)
    self.name = "GoogleAI"
    self.client = genai.Client(api_key=self.api_key)
    models = self.client.models.list()
    self.allowed_models = []
    for model in models.page:
      self.allowed_models.append(model.name)
