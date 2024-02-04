import base58
import click
import json
import requests

from blockchain.handler import create_mint, mint_tokens

from flask import Blueprint

from solders.keypair import Keypair

from solders.rpc.requests import GetBalance, RequestAirdrop
from solders.rpc.config import RpcContextConfig, RpcRequestAirdropConfig
from solders.pubkey import Pubkey
from solders.commitment_config import CommitmentLevel


make_request = lambda body: requests.post("https://api.devnet.solana.com/", json=json.loads(body)).json()

command_blueprint = Blueprint('ngnc_commands', __name__, cli_group='helpers')


@command_blueprint.cli.command('generate_keypair')
def generate_keypair():
    account = Keypair()
    secret = account.secret()
    pubkey = account.pubkey()
    encoded_str = str(base58.b58encode(secret))[2:-1]

    print("Private Key:", encoded_str)
    print("Public Key:", pubkey)


    # to convert to bytes
    # -> base58.b58decode(encoded_str)


@command_blueprint.cli.command('airdrop')
@click.argument('pubkey')
def request_airdrop(pubkey: str):
    config = RpcRequestAirdropConfig(commitment=CommitmentLevel.Confirmed)
    body =  RequestAirdrop(Pubkey.from_string(pubkey), 1000000000, config).to_json()
    signature = make_request(body)["result"]
    print (f"1 SOL requested for {pubkey}")
    print (f"https://solscan.io/tx/{signature}?cluster=devnet")
    return signature


@command_blueprint.cli.command('balance')
@click.argument('pubkey')
def get_balance(pubkey: str):
    config = RpcContextConfig(min_context_slot=1)
    body = GetBalance(Pubkey.from_string(pubkey), config).to_json()
    response = make_request(body)
    value = response["result"]["value"]
    print(f"{pubkey} has a balance of {value/1e9} SOL")
    return value


@command_blueprint.cli.command('create_token')
def create_token():
    create_mint()


@command_blueprint.cli.command('airdrop_ngnc')
@click.argument('pubkey')
@click.argument('amount', type=int)
def airdrop_token(pubkey, amount):
    signature = mint_tokens(pubkey, amount)
    print (f"{amount/1e9} NGNC sent to {pubkey}")
    print (f"https://solscan.io/tx/{signature}?cluster=devnet")