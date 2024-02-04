import os
from paystackapi.paystack import Paystack

paystack = Paystack(secret_key=os.environ["PAYSTACK_SECRET_KEY"])


def generate_payment_slug(address):
    res = paystack.page.create(
        name=f"NGNC Payment {address}",
        description=f"This is the on-ramp service to mint NGNC to {address}",
        metadata = {
            "address": address
        }
    )
    return res

