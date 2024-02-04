from functools import wraps
from serializers import WalletSchema
from payments import generate_payment_slug
from flask_apispec import marshal_with
from utils import Resource
import models
from flask import abort, request, redirect
from blockchain.handler import mint_tokens
from solders.pubkey import Pubkey

def allow_only_example(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check conditions here
        return func(*args, **kwargs)
    return wrapper
    
class Wallet(Resource):
    @marshal_with(WalletSchema())
    def get(self, address):
        try:
            if not Pubkey.from_string(address).is_on_curve():
                abort(400, 'address is noy user owned')
        except:
                abort(400, 'invalid solana address')
        # check if wallet exists and create if not
        wallet = models.Wallet.query.filter_by(address=address).first()
        if wallet is None:
            response = generate_payment_slug(address)["data"]
            wallet = models.Wallet(address=address, payment_page_slug=response["slug"], payment_page_id=response["id"])
            models.db.session.add(wallet)
            models.db.session.commit()
        return wallet


class RedirectSwagger(Resource):
    def get(self):
        return redirect('/swagger-ui')

class Webhook(Resource):
    def post(self):
        body = request.get_json()
        if body["event"] == "charge.success":
            amount = body["data"]["amount"]
            referrer: str = body['data']['metadata']['referrer']
            slug = referrer.split("/")[-1]

            # get wallet from slug
            wallet = models.Wallet.query.filter_by(payment_page_slug=slug).first()

            if wallet is not None:
                # mint tokens
                mint_tokens(wallet.address, amount)
        return {"success": True}