_LEAVE_BALANCES = {
    "alice": "12 days",
    "bob": "8 days",
    "carol": "15 days",
}


def get_leave_balance(employee_name: str) -> str:
    normalized_name = employee_name.strip().casefold()
    return _LEAVE_BALANCES.get(
        normalized_name,
        f"No demo leave balance found for {employee_name.strip()}.",
    )