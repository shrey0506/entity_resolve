import os
from dotenv import load_dotenv
from src.agents.macro_micro_agent import MacroMicroAgent
from src.agents.stock_data_agent import StockDataAgent
from src.agents.technical_analysis_agent import TechnicalAnalysisAgent
from src.agents.investment_suggestion_agent import InvestmentSuggestionAgent
from src.llm_model.llm_model import GeminiLLMWrapper

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))
llm_api_key = os.getenv("GEMINI_API_KEY")

class StockMarketOrchestrator:
    def __init__(self):
        llm_wrapper = GeminiLLMWrapper(llm_api_key)
        self.macro_micro_agent = MacroMicroAgent(llm_wrapper)
        self.stock_data_agent = StockDataAgent()
        self.technical_analysis_agent = TechnicalAnalysisAgent()
        self.investment_suggestion_agent = InvestmentSuggestionAgent(llm_wrapper)

    def run(self, stock_symbol):
        grounded_context = self.macro_micro_agent.get_grounded_economic_context(stock_symbol)
        stock_data = self.stock_data_agent.fetch_stock_data(stock_symbol)
        tech_indicators = self.technical_analysis_agent.compute_technical_indicators(stock_data["historical_data"])
        advice = self.investment_suggestion_agent.generate_investment_advice(grounded_context, tech_indicators.tail(30).to_dict())
        return advice

