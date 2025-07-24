# API Reference - Dark Web Checker

## Overview

This document provides detailed information about the Dark Web Checker's integration with the Have I Been Pwned API and internal API structure.

## Have I Been Pwned API Integration

### Base Configuration
- **API Version**: v3
- **Base URL**: `https://haveibeenpwned.com/api/v3`
- **Authentication**: API Key via header
- **Rate Limit**: 1 request per 1.5 seconds

### Authentication

#### Header Format
```
hibp-api-key: YOUR_API_KEY_HERE
User-Agent: DarkWebChecker/1.0
```

#### API Key Sources (Priority Order)
1. Command line parameter: `--api-key`
2. Environment variable: `HIBP_API_KEY`
3. Interactive prompt

### Endpoints Used

#### GET /breachedaccount/{account}
Retrieves breach information for a specific email address.

**Parameters:**
- `account` (path): Email address to check (URL encoded)
- `truncateResponse` (query): Set to `false` for complete breach data
- `domain` (query, optional): Filter by specific domain
- `includeUnverified` (query, optional): Include unverified breaches

**Request Example:**
```http
GET https://haveibeenpwned.com/api/v3/breachedaccount/user@example.com?truncateResponse=false
hibp-api-key: YOUR_API_KEY
User-Agent: DarkWebChecker/1.0
```

**Response Codes:**
- `200`: Breaches found
- `404`: No breaches found (clean)
- `400`: Bad request (invalid email)
- `401`: Unauthorized (invalid API key)
- `403`: Forbidden (no API key)
- `429`: Rate limit exceeded
- `503`: Service unavailable

**Response Format (200):**
```json
[
  {
    "Name": "Adobe",
    "Title": "Adobe",
    "Domain": "adobe.com",
    "BreachDate": "2013-10-04",
    "AddedDate": "2013-12-04T00:00:00Z",
    "ModifiedDate": "2022-05-15T23:52:49Z",
    "PwnCount": 152445165,
    "Description": "Detailed breach description...",
    "LogoPath": "Adobe.png",
    "DataClasses": [
      "Email addresses",
      "Password hints",
      "Passwords",
      "Usernames"
    ],
    "IsVerified": true,
    "IsFabricated": false,
    "IsSensitive": false,
    "IsRetired": false,
    "IsSpamList": false,
    "IsMalware": false,
    "IsStealerLog": false,
    "IsSubscriptionFree": false
  }
]
```

## Internal API Reference

### DarkWebChecker Class

#### Constructor
```python
DarkWebChecker(api_key: str)
```
Initializes the checker with the provided API key.

**Parameters:**
- `api_key` (str): Have I Been Pwned API key

#### Methods

##### check_email_breach(email: str) -> Dict[str, Any]
Checks a single email address for breaches.

**Parameters:**
- `email` (str): Email address to check

**Returns:**
```python
{
    'email': str,           # Email address checked
    'status': str,          # 'found', 'clean', or 'error'
    'breach_count': int,    # Number of breaches (if found)
    'breaches': List[Dict], # Breach details (if found)
    'checked_at': str,      # Timestamp of check
    'error': str            # Error message (if error)
}
```

**Status Values:**
- `found`: Email found in one or more breaches
- `clean`: Email not found in any breaches
- `error`: Error occurred during check

##### load_emails_from_file(file_path: str) -> List[str]
Loads email addresses from various file formats.

**Parameters:**
- `file_path` (str): Path to input file

**Supported Formats:**
- `.txt`: One email per line
- `.csv`: Emails detected in any column
- `.json`: Arrays or objects containing emails

**Returns:**
- `List[str]`: List of valid email addresses

##### save_results(results: List[Dict[str, Any]], output_file: str)
Saves results to output file in various formats.

**Parameters:**
- `results` (List[Dict]): Results from email checks
- `output_file` (str): Output file path

**Supported Output Formats:**
- `.json`: Complete structured data
- `.csv`: Tabular summary
- `.txt`: Human-readable report

##### is_valid_email(email: str) -> bool
Validates email address format.

**Parameters:**
- `email` (str): Email address to validate

**Returns:**
- `bool`: True if email format is valid

**Validation Pattern:**
```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

##### display_banner()
Displays the application banner with ASCII art.

## Error Handling

### API Errors

#### Rate Limiting (429)
```python
# Automatic retry with exponential backoff
if response.status_code == 429:
    time.sleep(6)  # Wait 6 seconds
    return self.check_email_breach(email)  # Retry
```

#### Authentication Errors (401, 403)
```python
{
    'email': email,
    'status': 'error',
    'error': 'Authentication failed - check API key',
    'checked_at': timestamp
}
```

#### Network Errors
```python
{
    'email': email,
    'status': 'error',
    'error': 'Network error: Connection timeout',
    'checked_at': timestamp
}
```

### File Handling Errors

#### File Not Found
```python
raise FileNotFoundError(f"Input file not found: {file_path}")
```

#### Invalid Format
```python
raise ValueError(f"Unsupported file format: {file_extension}")
```

#### Permission Errors
```python
raise PermissionError(f"Cannot write to output file: {output_file}")
```

## Rate Limiting Implementation

### Strategy
- **Delay**: 1.6 seconds between requests (safety margin)
- **Retry Logic**: Automatic retry on 429 responses
- **Backoff**: 6-second wait on rate limit hit

### Implementation
```python
# Rate limiting between requests
if i < len(emails):
    time.sleep(1.6)

# Rate limit handling
if response.status_code == 429:
    logger.warning("Rate limit exceeded. Waiting...")
    time.sleep(6)
    return self.check_email_breach(email)  # Retry
```

## Configuration Options

### Environment Variables
```bash
HIBP_API_KEY=your_api_key_here
```

### Command Line Arguments
```bash
--api-key YOUR_KEY    # API key override
--verbose            # Enable debug logging
--file FILE          # Input file path
--email EMAIL        # Single email check
--output FILE        # Output file path
```

### Logging Configuration
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dark_web_checker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

## Performance Considerations

### Memory Usage
- **Sequential Processing**: Emails processed one at a time
- **Minimal Memory Footprint**: No large data structures held in memory
- **Streaming**: Large files processed line by line

### Network Optimization
- **Session Reuse**: Single HTTP session for all requests
- **Connection Pooling**: Automatic connection reuse
- **Timeout Handling**: 30-second timeout per request

### Scalability Limits
- **Rate Limiting**: ~40 emails per minute maximum
- **API Quotas**: Subject to HIBP API limits
- **File Size**: No theoretical limit (memory efficient)

## Security Considerations

### API Key Protection
- Environment variables preferred
- No logging of API keys
- Secure transmission (HTTPS only)

### Data Privacy
- No data stored permanently
- Direct API communication only
- Local processing only

### Input Validation
- Email format validation
- File path sanitization
- Parameter validation

## Testing

### Unit Test Coverage
```python
# Test email validation
assert checker.is_valid_email("user@example.com") == True
assert checker.is_valid_email("invalid-email") == False

# Test file loading
emails = checker.load_emails_from_file("test_emails.txt")
assert len(emails) > 0

# Test result formatting
result = checker.check_email_breach("test@example.com")
assert "email" in result
assert "status" in result
```

### Integration Testing
```bash
# Test with real API (requires valid key)
python -m pytest tests/integration_tests.py

# Test file processing
python -m pytest tests/file_tests.py

# Test error handling
python -m pytest tests/error_tests.py
```