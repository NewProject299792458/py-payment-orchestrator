# Payment Orchestrator (FastAPI + Stripe Connect) — POC

**Status:** POC / test mode only. Do not use in production.
- FastAPI service for simple payment intent creation and Stripe webhook handling.
- Supports Stripe **Connect** destination charges / connected accounts (test mode).
- Dockerized; includes pytest smoke tests and `.env.example`.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill STRIPE_SECRET / STRIPE_WEBHOOK_SECRET (test keys)
uvicorn app.main:app --reload
```

### Webhooks (Stripe CLI)
```bash
stripe listen --forward-to localhost:8000/webhooks/stripe
```

### Endpoints
- `POST /payments/intents` → create PaymentIntent (amount/currency, optional connected_account_id)
- `POST /webhooks/stripe` → verify signature & process events

Environment (`.env`):
```
STRIPE_SECRET=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

Docker:
```bash
docker compose up --build
```

Tests:
```bash
pytest -q
```
