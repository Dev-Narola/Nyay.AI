def get_duration_days(billing_cycle: str) -> int:
    match billing_cycle.lower():
        case "daily":
            return 1
        case "weekly":
            return 7
        case "monthly":
            return 30
        case "quarterly":
            return 90
        case "semiannually":
            return 182
        case "yearly":
            return 365
        case _:
            return 30
