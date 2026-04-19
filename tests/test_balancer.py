from src.pricer.balancer import get_etf_price, portfolio_value, needs_rebalancing
from unittest.mock import patch

@patch('src.pricer.balancer.get_etf_price')
def test_portfolio_value(mock_get_price):
    mock_get_price.side_effect = lambda ticker: {"IWDA": 100, "EUNL": 200}[ticker]
    holdings = {"IWDA": 10, "EUNL": 5}
    assert portfolio_value(holdings) == 10*100 + 5*200

@patch('src.pricer.balancer.requests.get')
def test_get_etf_price(mock_get):
    mock_get.return_value.json.return_value = {"price": 100}
    assert get_etf_price("IWDA") == 100
    
@patch('src.pricer.balancer.get_etf_price')
def test_needs_rebalancing(mock_get_price):
    mock_get_price.side_effect = lambda ticker: {"IWDA": 100, "EUNL": 200}[ticker]
    holdings = {"IWDA": 10, "EUNL": 5}
    assert needs_rebalancing("IWDA", target_weight=0.6, tolerance=0.05) == True
    assert needs_rebalancing("IWDA", target_weight=0.5, tolerance=0.05) == False