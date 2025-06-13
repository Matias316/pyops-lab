import pytest
from .uid_analyzer import analyze_uid_traffic

def test_typical_case():
    timestamps = [
                1749836642, 1749836642, 1749836642,
                1749836643, 1749836643,
                1749836644,
                1749836645, 1749836645, 1749836645,
                1749836645
    ]        
    uids = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "a"]
    threshold = 3

    assert analyze_uid_traffic(timestamps,uids,threshold) == (False, 4, True)