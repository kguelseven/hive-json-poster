import os
import json
from typing import Any, Dict
from datetime import datetime
from dotenv import load_dotenv
from beem import Hive
from beem.account import Account


def post_custom_json(
    account_name: str,
    posting_key: str,
    json_id: str,
    json_data: Dict[str, Any],
    required_auths: list = None,
    required_posting_auths: list = None,
) -> Dict[str, Any]:
    """
    Post custom JSON to Hive blockchain.

    Args:
        account_name: Hive account name
        posting_key: Hive posting key
        json_id: Custom JSON identifier (e.g., 'my-app')
        json_data: Dictionary containing the JSON data to post
        required_auths: List of accounts that must approve with active key (optional)
        required_posting_auths: List of accounts that must approve with posting key (optional)

    Returns:
        Transaction result dictionary
    """
    # Initialize Hive instance
    hive = Hive(keys=[posting_key])

    # Set required auths - default to account_name for posting auth if not specified
    if required_posting_auths is None:
        required_posting_auths = [account_name]
    if required_auths is None:
        required_auths = []

    # Post custom JSON
    result = hive.custom_json(
        id=json_id,
        json_data=json_data,
        required_auths=required_auths,
        required_posting_auths=required_posting_auths,
    )

    return result


def main() -> None:
    """Main entry point for the CLI application."""
    # Load environment variables
    load_dotenv()

    # Get configuration from environment
    account_name = os.getenv("HIVE_ACCOUNT")
    posting_key = os.getenv("HIVE_POSTING_KEY")
    json_id = os.getenv("HIVE_JSON_ID", "custom-json-app")

    if not account_name or not posting_key:
        print("Error: HIVE_ACCOUNT and HIVE_POSTING_KEY must be set in .env file")
        return

    print(f"Posting custom JSON to Hive blockchain 20 times...")
    print(f"Account: {account_name}")
    print(f"JSON ID: {json_id}\n")

    successful = 0
    failed = 0

    for i in range(1, 21):
        # Example custom JSON data with counter and current timestamp
        json_data = {
            "app": "hive-json-poster",
            "action": "test",
            "message": f"Hello from Python! Post #{i}",
            "timestamp": datetime.now().isoformat(),
            "counter": i
        }

        print(f"[{i}/20] Posting...")

        try:
            result = post_custom_json(
                account_name=account_name,
                posting_key=posting_key,
                json_id=json_id,
                json_data=json_data,
            )

            # Extract transaction ID
            tx_id = result.get('trx_id') or result.get('id') or result.get('txid')

            if tx_id:
                print(f"  ✓ Success! Transaction ID: {tx_id}")
                successful += 1
            else:
                print(f"  ⚠ Posted but no transaction ID returned")
                successful += 1

        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Summary: {successful} successful, {failed} failed out of 20 posts")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
