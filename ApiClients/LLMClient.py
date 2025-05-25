import os
import openai
from google import genai
from .Models.LLMRequest import LLMRequest

class LLMClient:
  allowed_models = []
  name = ""
  model = ""
  NOT_IMPLEMENTED_ERROR = "Subclasses must implement this method."
  def _init_(self, api_key : str = "test"):
    self.api_key = api_key
  
  def generate_response(self, request:LLMRequest) -> str:
    """
    Generate a response from the LLM using the provided prompt.
    This method should be overridden by subclasses.
    """
    raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR)
  
  def convert_prompt_to_object(self, prompt:str):
    """
    Convert the prompt to a dictionary object.
    This method should be overridden by subclasses.
    """
    raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR)
  
  def build_request(self, model:str, messages:list, temperature:float, max_tokens:int, top_k:int, top_p:float, frequency_penalty:float, presence_penalty:float) -> LLMRequest:
    """
    Build the request object for the LLM.
    This method should be overridden by subclasses.
    """
    raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR)