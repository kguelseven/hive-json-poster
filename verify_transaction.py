#!/usr/bin/env python3
"""Quick script to verify transaction and check account history."""

import os
from dotenv import load_dotenv
from beem import Hive
from beem.account import Account
from beem.blockchain import Blockchain

load_dotenv()

account_name = os.getenv("HIVE_ACCOUNT")
tx_id = "497fda7b8dd90882915441404a2c6bdef96f8a72"  # Last transaction ID

print(f"Checking account: {account_name}")
print(f"Looking for transaction: {tx_id}\n")

# Initialize Hive
hive = Hive()

# Check account history for recent custom_json operations
print("=== Recent account operations ===")
account = Account(account_name, blockchain_instance=hive)

try:
    # Get recent account history
    history = account.history(limit=10, only_ops=["custom_json"])

    if history:
        print(f"Found {len(list(history))} recent custom_json operations:\n")
        for op in account.history(limit=10, only_ops=["custom_json"]):
            print(f"Block: {op.get('block')}")
            print(f"Timestamp: {op.get('timestamp')}")
            print(f"Transaction ID: {op.get('trx_id')}")
            print(f"Operation: {op}")
            print("-" * 80)
    else:
        print("No recent custom_json operations found")

except Exception as e:
    print(f"Error checking history: {e}")

# Try to get transaction details
print("\n=== Transaction lookup ===")
try:
    blockchain = Blockchain(blockchain_instance=hive)
    tx = blockchain.get_transaction(tx_id)
    if tx:
        print(f"Transaction found!")
        print(f"Details: {tx}")
    else:
        print("Transaction not found in blockchain")
except Exception as e:
    print(f"Error looking up transaction: {e}")
