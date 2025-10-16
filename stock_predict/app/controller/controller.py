from src.orchestrator.orchestrator import StockMarketOrchestrator
from src.llm_model.llm_model import GeminiLLMWrapper
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))
llm_api_key = os.getenv("GEMINI_API_KEY")

def get_investment_advice(stock_symbol: str) -> str:
    orchestrator = StockMarketOrchestrator()
    advice = orchestrator.run(stock_symbol)
    return advice

def chat_with_ai(prompt: str) -> str:
    orchestrator = StockMarketOrchestrator()
    response = orchestrator.chat_with_ai_model(prompt)
    return response

def get_gemini_response(session_id:int, prompt: str) -> str:
    llm_wrapper = GeminiLLMWrapper(api_key=llm_api_key)
    system_prompt = f"You are a helpful assistant. your task is to provide information to the user based on their queries. Also you need to preseve the context based on session id: {session_id}"
    prompt = f"{system_prompt}\nUser: {prompt}\nAssistant:"
    response = llm_wrapper.query(prompt)
    return response

