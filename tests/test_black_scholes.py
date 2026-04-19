
import pytest
from src import pricer
from src.pricer.black_scholes import BlackScholesPricer
import numpy as np 


@pytest.fixture
def black_scholes_pricer():
    S = 100  # Stock price
    K = 100  # Strike price
    T = 1    # Time to maturity (in years)
    r = 0.05 # Risk-free interest rate
    sigma = 0.2 # Volatility
    return BlackScholesPricer(S, K, T, sigma, r)

def test_call_black_scholes(black_scholes_pricer: BlackScholesPricer):

    expected_call_price = 10.4506  # Expected call price (pre-calculated)
    call_price = black_scholes_pricer.price_call()
    assert expected_call_price == pytest.approx(call_price, rel=1e-4)

def test_put_black_scholes(black_scholes_pricer: BlackScholesPricer):
    expected_put_price = 5.5735  # Expected put price (pre-calculated)
    put_price = black_scholes_pricer.price_put()
    assert expected_put_price == pytest.approx(put_price, rel=1e-4) 


@pytest.mark.parametrize("S, K, T, sigma, r, parity", [
    (100, 100, 1.0, 0.20, 0.05, 100-100*np.exp(-0.05)),  # ATM
    (100, 110, 1.0, 0.20, 0.05, 100-110*np.exp(-0.05)),  # OTM
    (110, 100, 1.0, 0.20, 0.05, 110-100*np.exp(-0.05)),  # ITM
    (100, 100, 0.5, 0.20, 0.05, 100-100*np.exp(-0.05*0.5)),  # T court
    (100, 100, 1.0, 0.40, 0.05, 100-100*np.exp(-0.05*1.0)),  # haute vol
],ids=[
    "ATM",
    "OTM",
    "ITM",
    "T court",
    "haute vol"
])
def test_call_parity(S, K, T, sigma, r, parity):
    pricer = BlackScholesPricer(S, K, T, sigma, r)
    call_price = pricer.price_call()    
    put_price = pricer.price_put()
    assert call_price - put_price == pytest.approx(parity, rel=1e-4)

def test_zero_volatility_call():
    """Avec sigma=0, call = max(S - K*e^(-rT), 0)"""
    pricer = BlackScholesPricer(100, 90, 1, 0.0001, 0.05)
    import math
    expected = max(100 - 90 * math.exp(-0.05), 0)
    assert pricer.price_call() == pytest.approx(expected, rel=1e-3)

@pytest.mark.parametrize("S, K, T, sigma, r, expected_call", [
    (100, 100, 1.0, 0.20, 0.05, 10.4506),  # ATM
    (100, 110, 1.0, 0.20, 0.05,  6.0402),  # OTM
    (110, 100, 1.0, 0.20, 0.05, 17.4998),  # ITM
    (100, 100, 0.5, 0.20, 0.05,  7.0469),  # T court
    (100, 100, 1.0, 0.40, 0.05, 19.7514),  # haute vol
],ids=[
    "ATM",
    "OTM",
    "ITM",
    "T court",
    "haute vol"
])
def test_call_price_scenarios(S, K, T, sigma, r, expected_call):
    pricer = BlackScholesPricer(S, K, T, sigma, r)
    assert pricer.price_call() == pytest.approx(expected_call, rel=1e-1)
