# RPC Proxy Tester

A Python tool for testing multiple proxy servers against Solana RPC endpoints to find the fastest and most reliable connection.

## Overview

This tool helps you identify the best proxy server for your Solana RPC calls by testing multiple proxies simultaneously and ranking them by response time. It's particularly useful for trading bots, DeFi applications, or any service that requires fast and reliable blockchain data access.

## Features

- 🚀 **Performance Testing**: Measures response times for each proxy in milliseconds
- 🔍 **Response Validation**: Verifies that RPC responses are valid Solana data
- 📊 **Detailed Results**: Shows successful vs failed proxies with error details
- 🏆 **Best Proxy Identification**: Automatically identifies the fastest working proxy
- 🛡️ **Error Handling**: Comprehensive error handling for timeouts and connection issues
- 💬 **Interactive CLI**: User-friendly command-line interface

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the script**:
   ```bash
   # Save the rpctester.py file to your desired directory
   ```

2. **Install dependencies**:
   ```bash
   # Create virtual environment (recommended)
   python3 -m venv rpc_tester_env
   source rpc_tester_env/bin/activate
   
   # Install required packages
   pip install requests
   ```

   **Alternative for macOS with Homebrew**:
   ```bash
   # If you get "externally-managed-environment" error
   python3 -m venv rpc_tester_env
   source rpc_tester_env/bin/activate
   pip install requests
   ```

## Usage

### Basic Usage

1. **Run the script**:
   ```bash
   python3 rpctester.py
   ```

2. **Follow the interactive prompts**:
   - Enter your RPC URL
   - Enter the Solana address to test
   - Enter proxy strings (one per line)
   - Press Enter twice to start testing

### Example Input

```
🔧 RPC Proxy Tester
==================================================
Enter RPC URL: https://mainnet.helius-rpc.com/?api-key=your-api-key
Enter Solana address to test: 86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY

Enter proxy strings (format: ip:port:username:password)
Enter one proxy per line. Press Enter twice when done:
82.23.238.143:5479:pkqlkuvb:alin4kij1661
166.0.2.122:8083:pkqlkuvb:alin4kij1661
82.24.251.87:7934:pkqlkuvb:alin4kij1661
148.135.189.31:8017:pkqlkuvb:alin4kij1661

```

### Proxy Format

Proxies should be provided in the format:
```
ip:port:username:password
```

Example:
```
192.168.1.100:8080:myuser:mypass
```

## How It Works

1. **RPC Call**: The tool makes a `getAccountInfo` request to the specified Solana address
2. **Proxy Testing**: Each proxy is tested individually with the same RPC call
3. **Performance Measurement**: Response times are measured in milliseconds
4. **Validation**: Responses are validated to ensure they're proper Solana RPC responses
5. **Ranking**: Results are sorted by response time (fastest first)

### Sample RPC Response

A successful response looks like:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "context": {
      "slot": 352811946,
      "apiVersion": "2.2.7"
    },
    "value": {
      "lamports": 4881739942,
      "data": "",
      "owner": "11111111111111111111111111111111",
      "executable": false,
      "rentEpoch": 18446744073709552000,
      "space": 0
    }
  }
}
```

## Sample Output

```
Testing 4 proxies...
--------------------------------------------------------------------------------
Testing proxy 1/4: 82.23.238.143:5479
  ✓ Success - Response time: 145.23ms
Testing proxy 2/4: 166.0.2.122:8083
  ✓ Success - Response time: 89.45ms
Testing proxy 3/4: 82.24.251.87:7934
  ✗ Failed - Error: Connection timeout
Testing proxy 4/4: 148.135.189.31:8017
  ✓ Success - Response time: 203.67ms

================================================================================
RESULTS SUMMARY
================================================================================

🎉 SUCCESSFUL PROXIES (3):
------------------------------------------------------------
1. 166.0.2.122:8083
   Response time: 89.45ms
   ⭐ FASTEST PROXY

2. 82.23.238.143:5479
   Response time: 145.23ms

3. 148.135.189.31:8017
   Response time: 203.67ms

❌ FAILED PROXIES (1):
------------------------------------------------------------
• 82.24.251.87:7934
  Error: Connection timeout

================================================================================
🏆 BEST PROXY
================================================================================
IP:Port: 166.0.2.122:8083
Full proxy string: 166.0.2.122:8083:pkqlkuvb:alin4kij1661
Response time: 89.45ms
================================================================================
```

## Use Cases

- **Trading Bots**: Find the fastest proxy for high-frequency trading
- **DeFi Applications**: Ensure reliable blockchain data access
- **Portfolio Trackers**: Optimize response times for real-time balance updates
- **NFT Tools**: Speed up metadata and ownership queries
- **Blockchain Analytics**: Improve data collection performance

## Configuration

### Timeout Settings
The default timeout is 10 seconds per proxy. You can modify this in the code:
```python
def test_rpc_call(self, rpc_url: str, solana_address: str, proxy_config: Optional[Dict] = None, timeout: int = 10):
```

### Custom RPC Methods
While the tool uses `getAccountInfo` by default, you can modify the payload to test other RPC methods:
```python
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getAccountInfo",  # Change this method
    "params": [
        solana_address,
        {
            "encoding": "base58"
        }
    ]
}
```

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'requests'"**
   ```bash
   pip install requests
   ```

2. **"externally-managed-environment" error on macOS**
   ```bash
   python3 -m venv rpc_tester_env
   source rpc_tester_env/bin/activate
   pip install requests
   ```

3. **Connection timeouts**
   - Check if your proxies are valid and working
   - Verify your internet connection
   - Try increasing the timeout value

4. **Invalid RPC responses**
   - Verify your RPC URL and API key
   - Check if the Solana address is valid
   - Ensure the RPC endpoint supports the method being called

### Error Messages

- **"Invalid proxy format"**: Make sure your proxy follows the `ip:port:username:password` format
- **"Connection timeout"**: The proxy didn't respond within the timeout period
- **"HTTP 4xx/5xx errors"**: Authentication or server issues with the proxy or RPC endpoint

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## Support

If you encounter any issues or have questions, please check the troubleshooting section or create an issue in the project repository.