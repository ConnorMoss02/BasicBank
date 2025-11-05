from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field 
from typing import Dict, List
from datetime import datetime

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


# Step 2: Read Endpoints (Balance)

@app.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: str):
    acct = accounts.get(account_id)
    if not acct:
        raise HTTPException(status_code=404, detail="Account not found")
    return acct

class BalanceResponse(BaseModel):
    accountId: str
    balance: float

@app.get("/accounts/{account_id}/balance", response_model=BalanceResponse)
def get_balance(account_id: str):
    acct = accounts.get(account_id)
    if not acct:
        raise HTTPException(status_code=404, detail="Account not found")
    return BalanceResponse(accountId=acct.accountId, balance=acct.balance)

# Step 3: Transfer Between Accounts Enpoints
class TransferRequest(BaseModel):
    fromAccountId: str = Field(..., example="acc1")
    toAccountId: str = Field(..., example="acc2")
    amount: float = Field(..., gt=0, example=50.0)

class TransferRecord(BaseModel):
    transferId: str
    timestamp: datetime
    fromAccountId: str
    toAccountId: str
    amount: float

transfers: List[TransferRecord] = []
next_transfer_id = 1

@app.post("/transfers", response_model=TransferRecord, status_code=201)
def transfer_funds(request: TransferRequest):
    global next_transfer_id

    if request.fromAccountId == request.toAccountId:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")
    
    from_acct = accounts.get(request.fromAccountId)
    to_acct = accounts.get(request.toAccountId)

    if not from_acct or not to_acct:
        raise HTTPException(status_code=404, detail="One or both accounts not found")
    
    if (from_acct.balance < request.amount):
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    from_acct.balance -= request.amount
    to_acct.balance += request.amount

    record = TransferRecord(
        transferId=f"t{next_transfer_id}",
        timestamp=datetime.utcnow(),
        fromAccountId=request.fromAccountId,
        toAccountId=request.toAccountId,
        amount=request.amount
    )

    next_transfer_id += 1
    transfers.append(record)
    return record 