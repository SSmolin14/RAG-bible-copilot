from .retriever import BibleRetriever 
from .llm import LLMService

class BibleCopilot:
    def __init__(self, api_key: str, mode="chroma"):
        self.retriever = BibleRetriever(mode=mode)
        self.llm = LLMService(api_key=api_key)

    def ask(self, question: str):
        # 1. Retrieve
        results = self.retriever.search(question, k=4)
        
        # 2. Format Context
        context_text = "\n".join([f"[{r['citation']}]: {r['text']}" for r in results])
        
        # 3. Generate
        answer = self.llm.generate_answer(question, context_text)
        
        return {
            "answer": answer,
            "sources": [r['citation'] for r in results]
        }