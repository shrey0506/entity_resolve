from src.orchestrator.orchestrator import StockMarketOrchestrator

def get_investment_advice(stock_symbol: str) -> str:
    orchestrator = StockMarketOrchestrator()
    advice = orchestrator.run(stock_symbol)
    return advice