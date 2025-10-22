#!/usr/bin/env python3
"""Quick script to verify transaction and check account history."""

import os
import sys
from dotenv import load_dotenv
from beem import Hive
from beem.account import Account
from beem.blockchain import Blockchain

def main():
    """Main entry point."""
    load_dotenv()

    account_name = os.getenv("HIVE_ACCOUNT")

    # Get transaction ID from command line argument
    if len(sys.argv) < 2:
        print("Usage: python verify_transaction.py <transaction_id>")
        print("\nExample: python verify_transaction.py 497fda7b8dd90882915441404a2c6bdef96f8a72")
        sys.exit(1)

    tx_id = sys.argv[1]

    print(f"Checking account: {account_name}")
    print(f"Looking for transaction: {tx_id}\n")

    # Initialize Hive
    hive = Hive()

    # Check account history for recent custom_json operations
    print("=== Recent account operations ===")
    account = Account(account_name, blockchain_instance=hive)

    try:
        # Get recent account history
        history = list(account.history(only_ops=["custom_json"]))

        if history:
            # Limit to last 10 operations
            recent_ops = history[-10:]
            print(f"Found {len(recent_ops)} recent custom_json operations:\n")
            for op in recent_ops:
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


if __name__ == "__main__":
    main()
