from task15 import BankCard
import pytest

# task 4
def test_bank_card():
    a = BankCard(100, 2)
    assert a.total_sum == 100
    assert a.balance_limit == 2
    assert a.__str__() == "To learn the balance call balance."
    a(50)
    assert a.total_sum == 50
    assert a.balance() == 50
    assert a.balance_limit == 1
    try:
        a(50)
    except ValueError:
        pass
    assert a.total_sum == 0
    a.put(30)
    assert a.balance() == 30
    try:
        a.balance()
    except ValueError:
        pass

    b = BankCard(50)
    
    for i in range(100):
        assert b.balance() == 50
    
    c = BankCard(300, 2)
    d = a + c
    assert d.total_sum == 330
    assert d.balance_limit == 2
