#!/usr/bin/env python3
import argparse
import time
import urllib.request
import urllib.parse
import json
import statistics
from typing import Tuple

def test_rpc_endpoint(rpc_url: str, num_tests: int = 10) -> Tuple[str, float]:
    """
    Test an RPC endpoint with eth_blockNumber calls and return average ping time.

    Args:
        rpc_url: The RPC endpoint URL
        num_tests: Number of tests to run (default 10)

    Returns:
        Tuple of (rpc_url, average_ping_ms)
    """
    ping_times = []

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }

    for i in range(num_tests):
        try:
            start_time = time.time()

            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(rpc_url, data=data, headers={'Content-Type': 'application/json'})

            with urllib.request.urlopen(req, timeout=10) as response:
                response_data = response.read()
                end_time = time.time()

                if response.status == 200:
                    ping_time_ms = (end_time - start_time) * 1000
                    ping_times.append(ping_time_ms)
                    print(f"Test {i+1}/{num_tests} for {rpc_url}: {ping_time_ms:.2f}ms")
                else:
                    print(f"Test {i+1}/{num_tests} for {rpc_url}: Failed (HTTP {response.status})")

        except Exception as e:
            print(f"Test {i+1}/{num_tests} for {rpc_url}: Failed ({str(e)})")

    if ping_times:
        avg_ping = statistics.mean(ping_times)
        return rpc_url, avg_ping
    else:
        return rpc_url, float('inf')

def interactive_mode():
    """Interactive mode for inputting RPCs and test count."""
    print("=== RPC Tester - Interactive Mode ===")
    print("Enter RPC endpoints one per line (press Enter on empty line to finish):")

    rpcs = []
    while True:
        rpc = input(f"RPC {len(rpcs) + 1}: ").strip()
        if not rpc:
            break
        rpcs.append(rpc)

    if not rpcs:
        print("No RPCs entered. Exiting.")
        return

    while True:
        try:
            num_tests = int(input(f"\nHow many tests per RPC? (default: 10): ") or "10")
            if num_tests > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    return rpcs, num_tests

def run_tests(rpcs, num_tests):
    """Run tests on the provided RPCs."""
    print(f"\nTesting {len(rpcs)} RPC endpoint(s) with {num_tests} tests each...\n")

    results = []

    for rpc_url in rpcs:
        print(f"Testing RPC: {rpc_url}")
        rpc_url, avg_ping = test_rpc_endpoint(rpc_url, num_tests)
        results.append((rpc_url, avg_ping))
        if avg_ping == float('inf'):
            print(f"Average ping: FAILED\n")
        else:
            print(f"Average ping: {avg_ping:.2f}ms\n")

    # Sort by average ping time (fastest first)
    results.sort(key=lambda x: x[1])

    print("=" * 80)
    print("RESULTS (ranked by speed):")
    print("=" * 80)

    for i, (rpc_url, avg_ping) in enumerate(results, 1):
        if avg_ping == float('inf'):
            print(f"{i}. {rpc_url} - FAILED")
        else:
            print(f"{i}. {rpc_url} - {avg_ping:.2f}ms")

def main():
    parser = argparse.ArgumentParser(description='Test Ethereum RPC endpoints and rank by speed')
    parser.add_argument('rpcs', nargs='*', help='RPC endpoint URLs to test (optional)')
    parser.add_argument('-n', '--num-tests', type=int, default=10,
                       help='Number of tests per RPC (default: 10)')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')

    args = parser.parse_args()

    # If no RPCs provided or interactive mode requested, use interactive mode
    if not args.rpcs or args.interactive:
        result = interactive_mode()
        if result:
            rpcs, num_tests = result
            run_tests(rpcs, num_tests)
    else:
        run_tests(args.rpcs, args.num_tests)

if __name__ == "__main__":
    main()