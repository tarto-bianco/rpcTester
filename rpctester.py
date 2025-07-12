#!/usr/bin/env python3
"""
RPC Proxy Tester
Tests multiple proxies against a Solana RPC endpoint to find the fastest one.
"""

import requests
import time
import json
import sys
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse

class RPCTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def parse_proxy(self, proxy_string: str) -> Dict[str, str]:
        """
        Parse proxy string format: ip:port:username:password
        Returns dict with proxy configuration for requests
        """
        parts = proxy_string.strip().split(':')
        if len(parts) != 4:
            raise ValueError(f"Invalid proxy format. Expected ip:port:username:password, got: {proxy_string}")
        
        ip, port, username, password = parts
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
        
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def test_rpc_call(self, rpc_url: str, solana_address: str, proxy_config: Optional[Dict] = None, timeout: int = 10) -> Tuple[bool, float, Optional[Dict]]:
        """
        Test a single RPC call through a proxy
        Returns (success, response_time, response_data)
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [
                solana_address,
                {
                    "encoding": "base58"
                }
            ]
        }
        
        try:
            start_time = time.time()
            
            if proxy_config:
                response = self.session.post(
                    rpc_url,
                    json=payload,
                    proxies=proxy_config,
                    timeout=timeout
                )
            else:
                response = self.session.post(
                    rpc_url,
                    json=payload,
                    timeout=timeout
                )
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Check if it's a valid Solana RPC response
                if 'jsonrpc' in response_data and 'result' in response_data:
                    return True, response_time, response_data
                else:
                    return False, response_time, response_data
            else:
                return False, response_time, {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except requests.exceptions.RequestException as e:
            return False, float('inf'), {"error": str(e)}
        except json.JSONDecodeError as e:
            return False, float('inf'), {"error": f"Invalid JSON response: {str(e)}"}
        except Exception as e:
            return False, float('inf'), {"error": f"Unexpected error: {str(e)}"}
    
    def test_proxies(self, rpc_url: str, solana_address: str, proxy_strings: List[str]) -> List[Dict]:
        """
        Test all proxies and return results sorted by response time
        """
        results = []
        
        print(f"\nTesting {len(proxy_strings)} proxies...")
        print("-" * 80)
        
        for i, proxy_string in enumerate(proxy_strings, 1):
            print(f"Testing proxy {i}/{len(proxy_strings)}: {proxy_string.split(':')[0]}:{proxy_string.split(':')[1]}")
            
            try:
                proxy_config = self.parse_proxy(proxy_string)
                success, response_time, response_data = self.test_rpc_call(
                    rpc_url, solana_address, proxy_config
                )
                
                result = {
                    'proxy': proxy_string,
                    'proxy_ip': proxy_string.split(':')[0],
                    'proxy_port': proxy_string.split(':')[1],
                    'success': success,
                    'response_time_ms': response_time,
                    'response_data': response_data
                }
                
                if success:
                    print(f"  ✓ Success - Response time: {response_time:.2f}ms")
                else:
                    print(f"  ✗ Failed - Error: {response_data.get('error', 'Unknown error')}")
                
                results.append(result)
                
            except Exception as e:
                print(f"  ✗ Failed - Error parsing proxy: {str(e)}")
                results.append({
                    'proxy': proxy_string,
                    'proxy_ip': proxy_string.split(':')[0] if ':' in proxy_string else proxy_string,
                    'proxy_port': proxy_string.split(':')[1] if len(proxy_string.split(':')) > 1 else 'N/A',
                    'success': False,
                    'response_time_ms': float('inf'),
                    'response_data': {'error': str(e)}
                })
        
        # Sort by response time (successful ones first, then by response time)
        results.sort(key=lambda x: (not x['success'], x['response_time_ms']))
        
        return results
    
    def display_results(self, results: List[Dict]):
        """
        Display test results in a formatted table
        """
        print("\n" + "="*80)
        print("RESULTS SUMMARY")
        print("="*80)
        
        successful_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]
        
        if successful_results:
            print(f"\n🎉 SUCCESSFUL PROXIES ({len(successful_results)}):")
            print("-" * 60)
            for i, result in enumerate(successful_results, 1):
                print(f"{i}. {result['proxy_ip']}:{result['proxy_port']}")
                print(f"   Response time: {result['response_time_ms']:.2f}ms")
                if i == 1:
                    print("   ⭐ FASTEST PROXY")
                print()
        
        if failed_results:
            print(f"\n❌ FAILED PROXIES ({len(failed_results)}):")
            print("-" * 60)
            for result in failed_results:
                print(f"• {result['proxy_ip']}:{result['proxy_port']}")
                error_msg = result['response_data'].get('error', 'Unknown error')
                print(f"  Error: {error_msg}")
                print()
        
        if successful_results:
            best_proxy = successful_results[0]
            print("="*80)
            print("🏆 BEST PROXY")
            print("="*80)
            print(f"IP:Port: {best_proxy['proxy_ip']}:{best_proxy['proxy_port']}")
            print(f"Full proxy string: {best_proxy['proxy']}")
            print(f"Response time: {best_proxy['response_time_ms']:.2f}ms")
            print("="*80)
        else:
            print("❌ No working proxies found!")

def get_user_input():
    """
    Get user input for RPC URL, proxies, and Solana address
    """
    print("🔧 RPC Proxy Tester")
    print("="*50)
    
    # Get RPC URL
    rpc_url = input("Enter RPC URL: ").strip()
    if not rpc_url:
        print("Error: RPC URL cannot be empty!")
        sys.exit(1)
    
    # Get Solana address
    solana_address = input("Enter Solana address to test: ").strip()
    if not solana_address:
        print("Error: Solana address cannot be empty!")
        sys.exit(1)
    
    # Get proxies
    print("\nEnter proxy strings (format: ip:port:username:password)")
    print("Enter one proxy per line. Press Enter twice when done:")
    
    proxy_strings = []
    while True:
        proxy = input().strip()
        if not proxy:
            break
        proxy_strings.append(proxy)
    
    if not proxy_strings:
        print("Error: At least one proxy must be provided!")
        sys.exit(1)
    
    return rpc_url, solana_address, proxy_strings

def main():
    """
    Main function to run the RPC tester
    """
    try:
        # Get user input
        rpc_url, solana_address, proxy_strings = get_user_input()
        
        # Initialize tester
        tester = RPCTester()
        
        # Test proxies
        results = tester.test_proxies(rpc_url, solana_address, proxy_strings)
        
        # Display results
        tester.display_results(results)
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()