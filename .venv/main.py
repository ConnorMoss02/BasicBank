from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field 
from typing import Dict

app = FastAPI()

class Account(BaseModel):
    accountId: str
    customerId: str
    balance: float

class CreateAccountRequest(BaseModel):
    customerId: str = Field(..., example="custBryce")
    initialDeposit: float = Field(..., ge=0, example=100.0)

accounts: Dict[str, Account] = {}
next_id = 1

@app.post("/accounts", response_model=Account, status_code=201)
def create_account(request: CreateAccountRequest):
    global next_id
    account_id = f"acc{next_id}"
    next_id += 1
    new_account = Account(
        accountId=account_id,
        customerId=request.customerId,
        balance=request.initialDeposit
    )
    accounts[account_id] = new_account
    return new_account

