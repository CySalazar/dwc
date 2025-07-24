# Dark Web Checker - Technical Documentation

## Architecture Overview

The Dark Web Checker is a Python-based command-line application designed to check email addresses against the Have I Been Pwned (HIBP) database to identify potential data breaches.

### Core Components

#### 1. DarkWebChecker Class
The main class that handles all breach checking operations.

**Key Methods:**
- `__init__(api_key)`: Initializes the checker with HIBP API key
- `display_banner()`: Shows the application banner
- `check_email_breach(email)`: Checks a single email against HIBP API
- `load_emails_from_file(file_path)`: Loads emails from various file formats
- `save_results(results, output_file)`: Saves results in multiple formats
- `is_valid_email(email)`: Validates email format

#### 2. File Format Support

**Input Formats:**
- **Text files (.txt)**: One email per line
- **CSV files (.csv)**: Emails can be in any column
- **JSON files (.json)**: Arrays of emails or objects containing email fields

**Output Formats:**
- **JSON (.json)**: Complete structured data with all breach information
- **CSV (.csv)**: Tabular format with summary information
- **Text (.txt)**: Human-readable report format

#### 3. API Integration

The application integrates with the Have I Been Pwned API v3:
- **Base URL**: `https://haveibeenpwned.com/api/v3`
- **Endpoint**: `/breachedaccount/{email}`
- **Authentication**: API key via `hibp-api-key` header
- **Rate Limiting**: 1 request per 1.5 seconds (automatically handled)

### Data Flow

1. **Input Processing**
   - Command-line arguments parsing
   - File format detection and email extraction
   - Email validation

2. **API Communication**
   - HTTP requests to HIBP API
   - Rate limiting compliance
   - Error handling and retry logic

3. **Result Processing**
   - Data aggregation and formatting
   - Output file generation
   - Summary statistics

### Error Handling

The application implements comprehensive error handling:
- **Network errors**: Connection timeouts, DNS failures
- **API errors**: Rate limiting, authentication failures, service unavailable
- **File errors**: Missing files, permission issues, format errors
- **Data errors**: Invalid email formats, malformed input files

### Security Considerations

- API keys are handled securely (environment variables preferred)
- No sensitive data is logged
- Rate limiting prevents API abuse
- Input validation prevents injection attacks

### Performance Characteristics

- **Memory Usage**: Minimal - processes emails sequentially
- **Network Usage**: Optimized with session reuse and proper headers
- **Rate Limiting**: Compliant with HIBP API limits (1.5s between requests)
- **Scalability**: Suitable for checking thousands of emails (with time consideration)

## API Reference

### Command Line Interface

```bash
python dark_web_checker.py [OPTIONS]
```

**Options:**
- `-f, --file FILE`: Input file containing email addresses
- `-e, --email EMAIL`: Single email address to check
- `-o, --output FILE`: Output file for results
- `--api-key KEY`: Have I Been Pwned API key
- `-v, --verbose`: Enable verbose logging

### Environment Variables

- `HIBP_API_KEY`: Have I Been Pwned API key (recommended method)

### Return Codes

- `0`: Success
- `1`: Error (invalid input, API failure, file not found, etc.)

## Configuration

### Logging Configuration

The application uses Python's logging module with:
- **File logging**: `dark_web_checker.log`
- **Console logging**: Real-time progress updates
- **Log levels**: INFO (default), DEBUG (with --verbose)

### API Configuration

- **Timeout**: 30 seconds per request
- **User Agent**: `DarkWebChecker/1.0`
- **Rate Limiting**: 1.6 seconds between requests (safety margin)

## Dependencies

- **requests**: HTTP library for API communication
- **pathlib**: Modern path handling
- **json**: JSON data processing
- **csv**: CSV file handling
- **argparse**: Command-line argument parsing
- **logging**: Application logging
- **re**: Email validation

## Testing Considerations

### Unit Testing Areas
- Email validation logic
- File format parsing
- API response handling
- Error scenarios

### Integration Testing Areas
- End-to-end workflow
- File I/O operations
- API communication
- Rate limiting behavior

### Performance Testing
- Large file processing
- Network timeout handling
- Memory usage with large datasets

## Deployment

### Requirements
- Python 3.7+
- Internet connection
- Have I Been Pwned API key

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export HIBP_API_KEY="your_api_key_here"
```

## Maintenance

### Log Monitoring
- Monitor `dark_web_checker.log` for errors
- Track API rate limiting issues
- Monitor file processing errors

### Updates
- Keep dependencies updated
- Monitor HIBP API changes
- Update email validation patterns as needed