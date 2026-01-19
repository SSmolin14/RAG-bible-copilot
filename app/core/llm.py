import ollama
from google import genai
from app.config import Config

class LLMService:
    def __init__(self, api_key: str = None):
        """
        Initializes the LLM service. 
        Accepts an optional api_key to prevent TypeErrors when called with one.
        """
        self.type = Config.LLM_TYPE
        
        if self.type == "gemini":
            # Use the passed api_key if available, otherwise fall back to Config
            actual_key = api_key if api_key else Config.GEMINI_API_KEY
            
            if not actual_key:
                raise ValueError("GEMINI_API_KEY missing in .env and no key provided.")
            
            self.client = genai.Client(api_key=actual_key)
        
        # Note: Ollama doesn't require a client initialization here 
        # as it uses the local engine directly.

    def generate_answer(self, question: str, context: str):
        prompt = f"Answer based ONLY on the provided Bible context. If the answer isn't there, say you don't know.\n\nContext:\n{context}\n\nQuestion: {question}"

        if self.type == "gemini":
            try:
                response = self.client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                return response.text
            except Exception as e:
                return f"Gemini Error: {str(e)}"
        
        elif self.type == "local":
            try:
                # Using the Ollama library for local inference
                response = ollama.chat(
                    model=Config.LOCAL_MODEL_NAME,
                    messages=[{'role': 'user', 'content': prompt}]
                )
                return response['message']['content']
            except Exception as e:
                return f"Ollama Error: Ensure Ollama is running. {str(e)}"