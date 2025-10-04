import google.generativeai as genai

class GeminiLLMWrapper:
    def __init__(self, api_key=None, temperature=0.7, max_tokens=512, top_p=0.95):
        if api_key:
            genai.configure(api_key=api_key)
        else:
            genai.configure()
        self.model_id = "gemini-2.5-flash"
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.model = genai.GenerativeModel(self.model_id)

    def query(self, prompt):
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
                "top_p": self.top_p
            }
        )
        # Try to extract the text safely
        try:
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                return "No valid response from Gemini. Try refining your prompt."
        except Exception as e:
            return f"Error extracting Gemini response: {e}"
