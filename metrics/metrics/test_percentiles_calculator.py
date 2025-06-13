import pytest
from .percentiles_calculator import compute_p95

def test_typical_case():
    assert compute_p95([10.2, 20.5, 30.7, 40.3, 50.7]) == 50.7

def test_large_list():
    data = list(range(1, 101))  # 1 to 100
    assert compute_p95(data) == 95.0

def test_single_item():
    assert compute_p95([42]) == 42.0

def test_empty_list():
    with pytest.raises(ValueError) as valueErrorException:
        compute_p95([])
    assert str(valueErrorException.value) == "Unable to compute p95: Empty list"