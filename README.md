# RPC Performance Testing Suite

A comprehensive Python toolkit for testing and benchmarking proxy servers and RPC endpoints. This suite provides quantitative analysis of network latency and reliability for Solana and Ethereum blockchain infrastructure.

## Overview

This toolkit enables systematic evaluation of proxy server performance and RPC endpoint reliability through automated testing protocols. It is designed for high-frequency trading systems, DeFi applications, and blockchain analytics platforms requiring optimal network performance.

## Architecture

### Solana RPC Proxy Tester
Tests multiple proxy servers against Solana RPC endpoints to identify optimal routing configurations for blockchain data access.

### Ethereum RPC Endpoint Tester (Updated)
Added comprehensive Ethereum RPC endpoint testing functionality with support for multiple concurrent tests and statistical analysis of response times.

## Features

**Performance Metrics**: Precise response time measurement in milliseconds with statistical aggregation
**Response Validation**: Verification of RPC response integrity and data validity
**Comprehensive Error Analysis**: Detailed logging of connection failures, timeouts, and protocol errors
**Optimal Configuration Identification**: Automated ranking of endpoints by performance criteria
**Fault Tolerance**: Robust error handling for network instabilities and service interruptions
**Interactive Command Line Interface**: Streamlined workflow for operational deployment

## Installation

### Prerequisites
- Python 3.7 or higher
- Standard library modules (urllib, json, statistics)

### Setup

1. **Repository Access**:
   ```bash
   git clone [repository-url]
   cd rpcTester
   ```

2. **Dependency Management**:
   ```bash
   # Virtual environment setup (recommended)
   python3 -m venv rpc_testing_env
   source rpc_testing_env/bin/activate

   # For Solana proxy testing only
   pip install requests
   ```

   **macOS Homebrew Compatibility**:
   ```bash
   # Handle externally-managed-environment restrictions
   python3 -m venv rpc_testing_env
   source rpc_testing_env/bin/activate
   pip install requests
   ```

## Usage

### Ethereum RPC Endpoint Testing

#### Interactive Mode (Default)
```bash
python3 rpctestereth.py
```

The system will prompt for:
- RPC endpoints (one per line, empty line to finish)
- Number of test iterations per endpoint

#### Command Line Mode
```bash
python3 rpctestereth.py <endpoint1> <endpoint2> ... -n <test_count>
```

#### Example Usage
```bash
# Test multiple endpoints with 10 iterations each
python3 rpctestereth.py https://mainnet.gateway.tenderly.co/api-key https://eth.llamarpc.com -n 10

# Force interactive mode
python3 rpctestereth.py -i
```

### Solana Proxy Testing

1. **Initialize Testing Session**:
   ```bash
   python3 rpctester.py
   ```

2. **Configuration Parameters**:
   - RPC URL endpoint
   - Target Solana address for testing
   - Proxy configuration strings
   - Execute testing protocol

### Configuration Specifications

#### Ethereum RPC Testing
- **Test Method**: eth_blockNumber JSON-RPC call
- **Timeout**: 10 seconds per request
- **Statistical Analysis**: Mean response time calculation
- **Result Ranking**: Ascending order by latency

#### Proxy Format Specification
```
ip:port:username:password
```

Example:
```
192.168.1.100:8080:credentials:authentication
```

## Technical Implementation

### Ethereum RPC Testing Protocol

1. **Request Formation**: JSON-RPC 2.0 eth_blockNumber method call
2. **Concurrent Testing**: Sequential execution across multiple endpoints
3. **Latency Measurement**: High-precision timing using system clock
4. **Statistical Aggregation**: Mean calculation across test iterations
5. **Performance Ranking**: Sorting by average response time

### Solana Proxy Testing Protocol

1. **RPC Method**: getAccountInfo request to specified address
2. **Proxy Evaluation**: Individual testing of each proxy configuration
3. **Performance Measurement**: Millisecond-precision response timing
4. **Data Validation**: JSON-RPC response structure verification
5. **Result Analysis**: Performance-based ranking with error categorization

### Sample Response Structure

Ethereum eth_blockNumber response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x1b4"
}
```

Solana getAccountInfo response:
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

## Performance Analysis Output

```
Testing 3 RPC endpoint(s) with 5 tests each...

Testing RPC: https://mainnet.gateway.tenderly.co/api-key
Test 1/5: 243.78ms
Test 2/5: 156.42ms
Test 3/5: 189.33ms
Test 4/5: 201.55ms
Test 5/5: 167.89ms
Average ping: 191.79ms

================================================================================
RESULTS (ranked by speed):
================================================================================
1. https://mainnet.gateway.tenderly.co/api-key - 191.79ms
2. https://eth.llamarpc.com - 365.16ms
3. https://failed-endpoint.com - FAILED
```

## Application Domains

**High-Frequency Trading**: Latency optimization for time-sensitive trading algorithms
**DeFi Protocol Integration**: Reliable blockchain state access for smart contract interactions
**Portfolio Management Systems**: Real-time balance and position tracking
**Blockchain Analytics**: Optimized data collection for analytical workloads
**Infrastructure Monitoring**: Performance benchmarking of RPC provider services

## Configuration Parameters

### Timeout Configuration
Default timeout: 10 seconds per request
```python
timeout_duration = 10  # Configurable in source code
```

### Custom RPC Method Testing
Modify payload structure for alternative RPC methods:
```python
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "custom_method",
    "params": ["parameter_list"]
}
```

## Troubleshooting

### Dependency Issues

**requests module not found**:
```bash
pip install requests
```

**macOS externally-managed-environment**:
```bash
python3 -m venv rpc_testing_env
source rpc_testing_env/bin/activate
pip install requests
```

### Network Connectivity

**Connection timeouts**: Verify proxy validity and network connectivity
**Authentication failures**: Confirm proxy credentials and endpoint access permissions
**Rate limiting**: Implement request throttling for provider-imposed limits

### Data Validation Errors

**Invalid RPC responses**: Verify endpoint URL and API key configuration
**Malformed addresses**: Confirm blockchain address format compliance
**Protocol mismatches**: Ensure RPC method compatibility with endpoint

## Error Classification

- **Invalid proxy format**: Non-compliant proxy string structure
- **Connection timeout**: Network latency exceeds threshold parameters
- **HTTP 4xx/5xx**: Authentication or server-side processing failures
- **JSON-RPC errors**: Protocol-level response errors

## License

This project operates under the MIT License framework.

## Development

Contributions are evaluated based on technical merit and performance impact. Submit issues and pull requests through the standard repository workflow.

## Technical Support

For implementation issues or performance optimization inquiries, reference the troubleshooting documentation or submit detailed issue reports with system configuration and error logs.