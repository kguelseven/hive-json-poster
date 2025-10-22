#!/usr/bin/env python3
"""
Script to retrieve Hive account details including RC and Hive Power.
"""
import os
from dotenv import load_dotenv
from beem import Hive
from beem.account import Account
from beem.rc import RC


def get_account_details(account_name: str) -> dict:
    """
    Retrieve detailed account information including RC and Hive Power.

    Args:
        account_name: Hive account name

    Returns:
        Dictionary with account details
    """
    # Initialize Hive instance
    hive = Hive()

    # Get account object
    account = Account(account_name, blockchain_instance=hive)

    # Get raw account data
    account_data = account.json()

    # Get balances using the proper API
    balances = account.get_balances()

    # Helper to safely get balance amount
    def get_balance_value(balance_dict, symbol):
        """Extract float value from Amount object or return 0.0"""
        try:
            amount_obj = balance_dict.get(symbol)
            if amount_obj:
                return float(amount_obj)
            return 0.0
        except:
            return 0.0

    # Get basic account info
    profile = {
        "username": account.name,
        "reputation": account.rep,
        "created": str(account_data.get("created", "N/A")),

        # Balances (using get_balances() method)
        "hive_balance": get_balance_value(balances["available"], "HIVE"),
        "hbd_balance": get_balance_value(balances["available"], "HBD"),
        "savings_hive": get_balance_value(balances["savings"], "HIVE"),
        "savings_hbd": get_balance_value(balances["savings"], "HBD"),

        # Power & Vesting (using get_steem_power for Hive power)
        "hive_power": float(account.get_steem_power(onlyOwnSP=True)),
        "effective_hive_power": float(account.get_steem_power(onlyOwnSP=False)),
        "delegated_hive_power": 0.0,  # Placeholder - requires additional API calls
        "received_hive_power": 0.0,  # Placeholder - requires additional API calls

        # Voting & Rewards
        "voting_power": account.get_voting_power(),
        "voting_value_hbd": 0.0,  # Placeholder - requires price feed data
        "pending_rewards_hive": get_balance_value(balances["rewards"], "HIVE"),
        "pending_rewards_hbd": get_balance_value(balances["rewards"], "HBD"),
        "pending_rewards_vests": get_balance_value(balances["rewards"], "VESTS"),
    }

    # Get RC (Resource Credits) information using get_rc_manabar()
    try:
        rc_manabar = account.get_rc_manabar()
        max_rc = rc_manabar["max_mana"]
        current_rc = rc_manabar["current_mana"]
        rc_percent = (current_rc / max_rc * 100) if max_rc > 0 else 0

        profile["resource_credits"] = {
            "current_rc": int(current_rc),
            "max_rc": int(max_rc),
            "rc_percentage": round(rc_percent, 2),
            "current_rc_formatted": f"{current_rc:,.0f}",
            "max_rc_formatted": f"{max_rc:,.0f}",
        }
    except Exception as e:
        profile["resource_credits"] = {"error": str(e)}

    # Get post/comment counts
    try:
        follow_count = account.get_follow_count()
        follower_count = follow_count.get("follower_count", 0) if isinstance(follow_count, dict) else 0
        following_count = follow_count.get("following_count", 0) if isinstance(follow_count, dict) else 0
    except:
        follower_count = 0
        following_count = 0

    profile["stats"] = {
        "post_count": account_data.get("post_count", 0),
        "comment_count": account_data.get("comment_count", 0),
        "followers": follower_count,
        "following": following_count,
    }

    return profile


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Get account name from environment or prompt
    account_name = os.getenv("HIVE_ACCOUNT")

    if not account_name:
        account_name = input("Enter Hive username: ").strip()

    if not account_name:
        print("Error: Account name is required")
        return

    print(f"\nFetching profile details for @{account_name}...\n")

    try:
        profile = get_account_details(account_name)

        # Display results
        print("=" * 60)
        print(f"PROFILE: @{profile['username']}")
        print("=" * 60)

        print(f"\nReputation: {profile['reputation']}")
        print(f"Account Created: {profile['created']}")

        print("\n--- BALANCES ---")
        print(f"HIVE Balance: {profile['hive_balance']:.3f} HIVE")
        print(f"HBD Balance: {profile['hbd_balance']:.3f} HBD")
        print(f"Savings HIVE: {profile['savings_hive']:.3f} HIVE")
        print(f"Savings HBD: {profile['savings_hbd']:.3f} HBD")

        print("\n--- HIVE POWER ---")
        print(f"Own Hive Power: {profile['hive_power']:.3f} HP")
        print(f"Delegated Out: {profile['delegated_hive_power']:.3f} HP")
        print(f"Delegated In: {profile['received_hive_power']:.3f} HP")
        print(f"Effective HP: {profile['effective_hive_power']:.3f} HP")

        print("\n--- VOTING & REWARDS ---")
        print(f"Voting Power: {profile['voting_power']:.2f}%")
        print(f"Vote Value: ${profile['voting_value_hbd']:.4f} HBD")
        print(f"Pending HIVE: {profile['pending_rewards_hive']:.3f} HIVE")
        print(f"Pending HBD: {profile['pending_rewards_hbd']:.3f} HBD")
        print(f"Pending VESTS: {profile['pending_rewards_vests']:.6f} VESTS")

        print("\n--- RESOURCE CREDITS ---")
        if "error" not in profile["resource_credits"]:
            rc = profile["resource_credits"]
            print(f"Current RC: {rc['current_rc_formatted']} ({rc['rc_percentage']}%)")
            print(f"Max RC: {rc['max_rc_formatted']}")
        else:
            print(f"RC Error: {profile['resource_credits']['error']}")

        print("\n--- ACTIVITY STATS ---")
        print(f"Posts: {profile['stats']['post_count']}")
        print(f"Comments: {profile['stats']['comment_count']}")
        print(f"Followers: {profile['stats']['followers']}")
        print(f"Following: {profile['stats']['following']}")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"Error fetching profile: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
