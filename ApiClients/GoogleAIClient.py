import LLMClient
from google import genai

class GoogleAiClient(LLMClient):
  def _init_(self, api_key : str, model : str):
    self.allowed_models = self.client.models.list()
    super()._init_(api_key, model)
    self.client = genai.Client(api_key=self.api_key, model=self.model)