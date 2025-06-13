import math

def compute_p95(latencies: list[float]):
    """
    Compute the 95th percentile of a list of latencies in milliseconds.

    The 95th percentile (P95) is commonly used in defining request latency SLOs.
    It represents the maximum latency under which 95% of requests should be served.
    Requests exceeding this value are considered out of SLO.
    """

    if len(latencies) < 1:
        raise ValueError("Unable to compute p95: Empty list")
    
    sorted_latencies = sorted(latencies) # Sorting list ASC

    initial_index = math.ceil(0.95 * len(sorted_latencies)) -1 # Calculate position 95th position in the list

    # Consider edge cases
    index = max(0, min(initial_index, len(sorted_latencies) - 1))
    
    return sorted_latencies[index]
