from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import os, stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET")

app = FastAPI(title="Payment Orchestrator (POC)")

class IntentCreate(BaseModel):
    amount: int = Field(..., gt=0, description="Amount in smallest currency unit (e.g., cents)")
    currency: str = "usd"
    connected_account_id: str | None = None
    description: str | None = None

@app.post("/payments/intents")
async def create_intent(payload: IntentCreate):
    try:
        kwargs = {
            "amount": payload.amount,
            "currency": payload.currency,
            "description": payload.description or "POC payment",
            "automatic_payment_methods": {"enabled": True},
        }
        if payload.connected_account_id:
            kwargs["transfer_data"] = {"destination": payload.connected_account_id}
        intent = stripe.PaymentIntent.create(**kwargs)
        return {"client_secret": intent["client_secret"], "id": intent["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature", "")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret) if endpoint_secret else None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")
    # Simplified processing
    return {"received": True}
