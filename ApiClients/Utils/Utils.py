# The format that we will use for the prompt is: 
# {{role system}}
# System prompt
# {{role/}}
# {{role user}}
# User prompt
# {{role/}}
# {{role assistant}}
# Assistant prompt}}
# {{role/}}
# This needs to converted to a list of json objects to be passed into the different LLMs such as OpenAI and GenAi from Google.

import re

def convert_prompt_to_json(prompt: str) -> list[dict]:
    try:
      pattern = re.compile(r"\{\{role (\w+)\}\}(.*?)\{\{role/\}\}", re.DOTALL)
      matches = pattern.findall(prompt)

      messages = []
      for role, content in matches:
          clean_content = content.strip()
          messages.append({"role": role.strip().lower(), "content": clean_content})
      
      return messages
    except Exception as e:
        print(f"Failed to convert prompt to JSON: {e}")
        print(f"Prompt: {prompt}")
        print("The correct format is: {{role system}} System prompt {{role/}} {{role user}} User prompt {{role/}} {{role assistant}} Assistant prompt {{role/}}")
        return []