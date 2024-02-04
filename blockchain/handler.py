import base58
import os

from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address
from spl.token.client import Token

from solana.rpc.commitment import Confirmed
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair



private_key = os.environ["SOLANA_PRIVATE_KEY"]

client = Client(endpoint="https://rpc.ironforge.network/devnet?apiKey=01HNTJGVRRFEM0GM52QNV3B991", commitment=Confirmed)
owner = Keypair.from_seed(base58.b58decode(private_key)[0:32])

def get_or_create_ata(token: Token, address: Pubkey, mint: Pubkey):
    # TODO: check if ata initialized then create instead
    try:
        ata = token.create_associated_token_account(owner=address)
    except Exception:
        ata = get_associated_token_address(owner=address, mint=mint)
    return ata
    

def mint_tokens(address: str, amount: int):
    """amount in kobo"""
    NGN_TOKEN = "NGNTfR7uP1z678g1PMdad4ds4r5jYFbKQe1KortAKg4"
    token = Token(
        conn=client,
        pubkey=Pubkey.from_string(NGN_TOKEN),
        payer=owner,
        program_id=TOKEN_PROGRAM_ID,
    )
    ata = get_or_create_ata(token, Pubkey.from_string(address), Pubkey.from_string(NGN_TOKEN))
    tx = token.mint_to_checked(
        dest=ata,
        mint_authority=owner,
        amount=amount*10000000,  # amount in kobo and token has 9 decimals
        decimals=9
    )
    signature = tx.value
    return signature


def create_mint():
    # creating token with 2 decimals here
    token = Token.create_mint(
        conn=client,
        payer=owner,
        mint_authority=owner.pubkey(),
        decimals=2,
        program_id=TOKEN_PROGRAM_ID,
    )
    print(f" New token deployed to {token.pubkey}")