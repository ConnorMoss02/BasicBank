# BasicBank API (FastAPI)

A tiny admin-facing banking API with a barebones web page.

## Endpoints

- POST `/accounts` — create account with initial deposit
- GET `/accounts/{accountId}` — account details
- GET `/accounts/{accountId}/balance` — balance only
- POST `/transfers` — move funds between accounts
- GET `/accounts/{accountId}/transfers` — transfer history

> Storage is **in-memory** for the exercise, so data resets on server reload.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Curl commands for quick test

# create

curl -s -X POST http://127.0.0.1:8000/accounts -H "Content-Type: application/json" -d '{"customerId":"c1","initialDeposit":100}'
curl -s -X POST http://127.0.0.1:8000/accounts -H "Content-Type: application/json" -d '{"customerId":"c2","initialDeposit":50}'

# transfer

curl -s -X POST http://127.0.0.1:8000/transfers -H "Content-Type: application/json" -d '{"fromAccountId":"acc1","toAccountId":"acc2","amount":25}'

# balance + history

curl -s http://127.0.0.1:8000/accounts/acc1/balance
curl -s http://127.0.0.1:8000/accounts/acc1/transfers
