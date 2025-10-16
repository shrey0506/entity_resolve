from fastapi import APIRouter

from app.controller.controller import get_investment_advice, get_gemini_response

router = APIRouter()

@router.post("/hello")
async def say_hello():
    return {"message": "Hello from the view endpoint!"}

@router.post("/advice")
async def investment_advice_endpoint(stock_symbol: str):
    advice = get_investment_advice(stock_symbol)
    return {"advice": advice}

@router.post("/chat")
async def chat_endpoint(session_id:int, prompt: str):
    response = get_gemini_response(session_id, prompt)
    return {"response": response}