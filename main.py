import sys
import os
# Ensure the root folder is in the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import Config
from app.core.rag_pipeline import BibleCopilot

def main():
    # 1. Show Initialization Status
    print("\n" + "="*50)
    print("📖 RAG BIBLE COPILOT INITIALIZING...")
    print("="*50)
    
    # Display active configuration
    mode_display = "☁️ GOOGLE GEMINI (Cloud)" if Config.LLM_TYPE == "gemini" else f"🏠 OLLAMA ({Config.LOCAL_MODEL_NAME})"
    print(f"ACTIVE LLM: {mode_display}")
    print(f"VECTOR DB : {Config.VECTOR_STORE_TYPE.upper()}")
    print("="*50)

    # 2. Initialize the Copilot
    try:
        # Note: We updated LLMService to read Config internally, 
        # so we don't necessarily need to pass the API key here anymore.
        copilot = BibleCopilot(
            api_key=Config.GEMINI_API_KEY, 
            mode=Config.VECTOR_STORE_TYPE
        )
        print("\n✅ System Ready! Ask your question below.")
    except Exception as e:
        print(f"\n❌ Initialization Failed: {e}")
        return

    while True:
        query = input("\n🙏 Question: ")
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("Stopping Copilot. God bless!")
            break
        
        if not query.strip():
            continue

        print("🔍 Searching scriptures and thinking...")
        
        try:
            response = copilot.ask(query)
            
            print("\n" + "-"*30)
            print("✨ ANSWER:")
            print(response['answer'])
            
            print("\n📜 SOURCES:")
            for source in response['sources']:
                print(f"  • {source}")
            print("-" * 30)
            
        except Exception as e:
            # Check for common rate limit errors to give better feedback
            if "429" in str(e):
                print("\n⚠️ Rate Limit Reached! Switch LLM_TYPE to 'local' in your .env to continue for free.")
            else:
                print(f"\n⚠️ Error: {e}")

if __name__ == "__main__":
    main()