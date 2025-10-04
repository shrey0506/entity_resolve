class InvestmentSuggestionAgent:
    def __init__(self, llm):
        self.llm = llm  # Instance of LLM wrapper

    def generate_investment_advice(self, grounded_context, technical_analysis):
        prompt = f"""
        Based on the following:
        - Macroeconomic context: {grounded_context['macro']}
        - Microeconomic context: {grounded_context['micro']}
        - Technical indicators from recent stock data: {technical_analysis}

        Suggest when and how much to invest. Include risk considerations.

        Respond ONLY with a valid JSON object in the following format (no explanation, no extra text):

        {{
          "recommendation": "Buy/Sell/Hold",
          "amount": "Suggested investment amount in INR",
          "entry_timing": "When to invest",
          "exit_timing" : "When to exit",
          "risk": "Risk assessment"
        }}
        """
        advice = self.llm.query(prompt)
        return advice
