def format_symbol(token: str, base_currency: str = "usdt") -> str:
    return f"{token.lower()}{base_currency}"
