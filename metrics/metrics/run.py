from percentiles_calculator import compute_p95

if __name__ == '__main__':
    latencies = list(map(float, input().split()))
    print(compute_p95(latencies))