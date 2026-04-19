import requests

def get_etf_price(ticker: str) -> float:
    """Appelle une API externe pour récupérer le prix d'un ETF."""
    response = requests.get(f"https://api.market.com/price/{ticker}")
    return response.json()["price"]

def portfolio_value(holdings: dict[str, float]) -> float:
    """holdings = {"IWDA": 10, "EUNL": 5} — ticker: nombre de parts"""
    return sum(get_etf_price(ticker) * qty for ticker, qty in holdings.items())

holdings = {"IWDA": 10, "EUNL": 5}  # Exemples de holdings
def needs_rebalancing(ticker: str, target_weight: float, tolerance: float = 0.05) -> bool:
    """Retourne True si le poids actuel dévie de plus de tolerance."""
    current_price = get_etf_price(ticker)
    portfolio_total = portfolio_value(holdings)
    current_weight = current_price / portfolio_total
    return abs(current_weight - target_weight) > tolerance