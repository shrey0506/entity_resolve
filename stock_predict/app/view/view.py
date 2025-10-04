from fastapi import APIRouter

from app.controller.controller import get_investment_advice

router = APIRouter()

@router.post("/hello")
async def say_hello():
    return {"message": "Hello from the view endpoint!"}

@router.post("/advice")
async def investment_advice_endpoint(stock_symbol: str):
    advice = get_investment_advice(stock_symbol)
    return {"advice": advice}