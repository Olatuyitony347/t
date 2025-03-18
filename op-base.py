from web3 import Web3
from eth_account import Account
import time
import sys
import config

# Network details
private_key = config.private_key_metamask.strip() 
rpc_url = 'https://sepolia.optimism.io'  # DO NOT CHANGE
chain_id = 11155420  # DO NOT CHANGE
contract_address = '0xb6Def636914Ae60173d9007E732684a9eEDEF26E'  # DO NOT CHANGE
my_address = config.wallet_address

# Connect to the network
web3 = Web3(Web3.HTTPProvider(rpc_url))
if not web3.is_connected():
    raise Exception("Failed to connect to the network")

# Create an account from the private key
account = Account.from_key(private_key)

# Transaction data for bridge (DO NOT CHANGE)
data = '0x56591d5962617374000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000B04079bCD3187eE95826d14f42C87e027Cb2192C000000000000000000000000000000000000000000000000016326b9978f6ab400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000016345785d8a0000'

# Function to create and send a transaction
def send_bridge_transaction():
    # Get the nonce for the sender's address
    nonce = web3.eth.get_transaction_count(my_address)

    # Estimate gas
    try:
        gas_estimate = web3.eth.estimate_gas({
            'to': contract_address,
            'from': my_address,
            'data': data,
            'value': web3.to_wei(0.1, 'ether')  # Sending 0.1 ETH
        })
        gas_limit = gas_estimate + 20000  # Add a gas buffer
    except Exception as e: 
        print(f"Error estimating gas: {e}")
        return None

    # Create the transaction
    transaction = {
        'nonce': nonce,
        'to': contract_address,
        'value': web3.to_wei(0.1, 'ether'),  # Sending 0.1 ETH
        'gas': gas_limit,  # Use the estimated gas limit
        'gasPrice': web3.eth.gas_price,
        'chainId': chain_id,
        'data': data
    }

    # Sign the transaction with the private key
    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

    # Send the transaction
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)  # Use raw_transaction
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None

# Main function to send multiple transactions
def send_multiple_transactions(num_transactions):
    successful_txs = 0
    try:
        for _ in range(num_transactions):
            tx_hash = send_bridge_transaction()
            if tx_hash:
                successful_txs += 1
                print(f"Tx Hash: {tx_hash} | Total Successful Tx: {successful_txs}")
            time.sleep(config.transaction_delay)  # Delay 30 seconds between transactions
    except KeyboardInterrupt:
        print("\nScript stopped by the user.")
    print(f"Total successful transactions: {successful_txs}")

# Number of transactions to send
try:
    num_transactions = int(input("Enter the number of transactions to send: "))
    send_multiple_transactions(num_transactions)
except ValueError:
    print("Invalid input, please enter a number.")
    sys.exit(1)