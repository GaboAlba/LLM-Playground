import os
import openai
from google import genai

class LLMClient:
  allowed_models = []
  def _init_(self, api_key : str, model : str):
    self.api_key = api_key
    self.model = model
    if self.model not in self.allowed_models:
      raise ValueError(f"Model {self.model} is not allowed. Allowed models are: {self.allowedModels}")
    
  def generate_response(self, prompt: str) -> str:
    """
    Generate a response from the LLM using the provided prompt.
    This method should be overridden by subclasses.
    """
    raise NotImplementedError("Subclasses must implement this method.")
  
  def convert_prompt_to_object(self, prompt:str) -> dict:
    """
    Convert the prompt to a dictionary object.
    This method should be overridden by subclasses.
    """
    raise NotImplementedError("Subclasses must implement this method.")