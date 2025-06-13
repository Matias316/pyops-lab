from collections import Counter, defaultdict

def analyze_uid_traffic(timestamps: list[int], uids: list[str], threshold: int) -> tuple[bool, int, bool]:
    """  
    Args:
        timestamps: List of UNIX timestamps in seconds when UIDs were generated.
        uids: List of corresponding UIDs.
        threshold: Maximum allowed UIDs per second.
    Returns:
        A tuple:
          (has_duplicates: bool, max_rate: int, rate_exceeded: bool)
    Example:
        Inputs:
            timestamps = [
                1749836642, 1749836642, 1749836642,
                1749836643, 1749836643,
                1749836644,
                1749836645, 1749836645, 1749836645, 
                1749836645
            ]        
            uids = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "a"]
            threshold = 3
        
        Output:
            (False, 4, True)
    """
    if len(timestamps) != len(uids):
        raise ValueError("Timestamps and UIDs list must match length")
    
    if len(timestamps) < 0 or len(timestamps) != len(uids):
        raise ValueError("Timestamps and UIDs list must match length and include at least 1 element")

    # Counter returns a dictionary with unique values and ocurrences   
    # E.g. {'1749836642': 2, '1749836643': 1 }     
    timestamps_counts = Counter(timestamps) 
    
    max_rate = max(timestamps_counts.values())
    rate_exceeded = max_rate > threshold

    uids_by_timestamp = defaultdict(set)
    # Dictionary usign ts as key and a set (unique values) of uids
    # E.g. {'1749836642': ['a'], '1749836643': ['a,b'] } 
    for ts, uid in zip(timestamps, uids):
        uids_by_timestamp[ts].add(uid)

    # If the set of unique values for a specific timestamp is less than count of timestamp
    # then there were collisions, i.e., same uid for a same timestamp
    collisions = any(len(uid_set) < timestamps_counts[ts]
        for ts, uid_set in uids_by_timestamp.items()
    )

    return collisions, max_rate, rate_exceeded