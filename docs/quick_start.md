# Quick Start Guide - Dark Web Checker

## 🚀 Get Started in 5 Minutes

### Step 1: Setup
```bash
# Clone and enter directory
git clone https://github.com/yourusername/DarkWebChecker.git
cd DarkWebChecker

# Run setup script (Linux/macOS)
./setup.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Get API Key
1. Visit [Have I Been Pwned API](https://haveibeenpwned.com/API/Key)
2. Purchase an API key (required for automated access)
3. Configure your API key using one of these methods:

#### Method 1: .env File (Recommended)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
HIBP_API_KEY=your_actual_api_key_here

# Rate limiting configuration (optional)
HIBP_HOURLY_LIMIT=100        # Maximum 100 requests per hour
HIBP_REQUEST_DELAY=1.6       # 1.6 seconds pause between requests
```

#### Method 2: Environment Variable
```bash
export HIBP_API_KEY="your_actual_api_key_here"
export HIBP_HOURLY_LIMIT=100
export HIBP_REQUEST_DELAY=1.6
```

#### Method 3: Command Line Parameter
```bash
python dark_web_checker.py --api-key your_api_key_here --hourly-limit 50 --request-delay 2.0 -e email@example.com -o results.json
```

### Step 3: Rate Limiting Configuration (Optional)

The application includes a rate limiting system to respect Have I Been Pwned API limits:

**Configurable parameters:**
- **HIBP_HOURLY_LIMIT**: Maximum requests per hour (default: 100)
- **HIBP_REQUEST_DELAY**: Delay between requests in seconds (default: 1.6)

**Configuration via .env:**
```bash
HIBP_HOURLY_LIMIT=50         # Reduce to 50 requests per hour
HIBP_REQUEST_DELAY=2.0       # Increase delay to 2 seconds
```

**Configuration via command line:**
```bash
python dark_web_checker.py --hourly-limit 50 --request-delay 2.0 -f emails.txt -o results.json
```

**Notes:**
- Hourly rate limiting tracks requests made in the last hour
- If you reach the hourly limit, the application will wait automatically
- Higher delay reduces load on HIBP servers but slows execution

### Step 4: Run Your First Check
```bash
# Check a single email
python dark_web_checker.py -e your.email@example.com -o results.json

# Check multiple emails from file
python dark_web_checker.py -f examples/sample_emails.txt -o results.csv
```

## 📝 Common Use Cases

### Personal Email Check
```bash
python dark_web_checker.py -e personal@gmail.com -o my_results.json
```

### Company Email Audit
```bash
python dark_web_checker.py -f company_emails.csv -o security_audit.json
```

### Batch Processing with Logging
```bash
python dark_web_checker.py -f large_email_list.txt -o detailed_report.json -v
```

## 📊 Understanding Results

### Clean Email (No Breaches)
```json
{
  "email": "safe@example.com",
  "status": "clean",
  "breach_count": 0,
  "breaches": [],
  "checked_at": "2024-01-15 10:30:45"
}
```

### Compromised Email (Found in Breaches)
```json
{
  "email": "compromised@example.com",
  "status": "found",
  "breach_count": 2,
  "breaches": [
    {
      "Name": "Adobe",
      "BreachDate": "2013-10-04",
      "PwnCount": 152445165,
      "DataClasses": ["Email addresses", "Passwords"]
    }
  ],
  "checked_at": "2024-01-15 10:30:45"
}
```

## 🛠️ Troubleshooting

### "API key is required"
Set your API key: `export HIBP_API_KEY="your_key"`

### "Rate limit exceeded"
The tool handles this automatically. Just wait a moment.

### "Module not found"
Install dependencies: `pip install -r requirements.txt`

### "Permission denied"
Make script executable: `chmod +x dark_web_checker.py`

## 📚 Next Steps

- Read the [User Manual](user_manual.md) for detailed usage
- Check [Technical Documentation](technical_documentation.md) for advanced features
- Review [API Reference](api_reference.md) for integration details

## 🔒 Security Reminder

✅ **DO**: Check your own emails or those you have permission to check
❌ **DON'T**: Check emails without proper authorization

---

**Need help?** Check the full documentation in the `docs/` directory!