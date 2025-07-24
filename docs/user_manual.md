# Dark Web Checker - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Usage Examples](#usage-examples)
5. [Input File Formats](#input-file-formats)
6. [Output Formats](#output-formats)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

## Introduction

Dark Web Checker is a powerful command-line tool that helps you determine if email addresses have been compromised in data breaches. It uses the Have I Been Pwned database, which contains billions of compromised accounts from thousands of data breaches.

### What it does:
- ✅ Checks email addresses against known data breaches
- ✅ Supports multiple input formats (TXT, CSV, JSON)
- ✅ Generates detailed reports in various formats
- ✅ Handles rate limiting automatically
- ✅ Provides comprehensive logging

### What it doesn't do:
- ❌ Access the dark web directly
- ❌ Perform illegal activities
- ❌ Store or transmit your data to third parties
- ❌ Guarantee 100% accuracy (depends on HIBP database)

## Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection
- Have I Been Pwned API key

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get API Key
1. Visit [Have I Been Pwned API](https://haveibeenpwned.com/API/Key)
2. Purchase an API key (required for automated access)
3. Save your API key securely

### Step 3: Set Environment Variable (Recommended)
```bash
# Linux/macOS
export HIBP_API_KEY="your_api_key_here"

# Windows
set HIBP_API_KEY=your_api_key_here
```

## Getting Started

### Quick Start - Single Email
```bash
python dark_web_checker.py -e user@example.com -o results.json
```

### Quick Start - Multiple Emails from File
```bash
python dark_web_checker.py -f emails.txt -o results.json
```

### Interactive Mode
If you run the script without parameters, it will guide you through the process:
```bash
python dark_web_checker.py
```

## Usage Examples

### Example 1: Check Single Email
```bash
python dark_web_checker.py -e john.doe@company.com -o john_results.json
```

### Example 2: Check Emails from Text File
```bash
python dark_web_checker.py -f employee_emails.txt -o company_breach_report.csv
```

### Example 3: Check with Custom API Key
```bash
python dark_web_checker.py -f emails.csv -o results.txt --api-key YOUR_API_KEY
```

### Example 4: Verbose Mode for Debugging
```bash
python dark_web_checker.py -f emails.json -o results.json -v
```

## Input File Formats

### Text Files (.txt)
One email address per line:
```
user1@example.com
user2@company.org
admin@website.net
```

### CSV Files (.csv)
Emails can be in any column. The tool automatically detects email addresses:
```csv
Name,Email,Department
John Doe,john@company.com,IT
Jane Smith,jane@company.com,HR
Bob Wilson,bob@company.com,Finance
```

### JSON Files (.json)
Multiple formats supported:

**Array format:**
```json
[
  "user1@example.com",
  "user2@example.com",
  "user3@example.com"
]
```

**Object format:**
```json
{
  "employees": [
    "john@company.com",
    "jane@company.com"
  ],
  "admin": "admin@company.com"
}
```

## Output Formats

### JSON Format (.json)
Complete structured data with all breach information:
```json
[
  {
    "email": "user@example.com",
    "status": "found",
    "breach_count": 2,
    "breaches": [
      {
        "Name": "Adobe",
        "Title": "Adobe",
        "BreachDate": "2013-10-04",
        "PwnCount": 152445165,
        "Description": "In October 2013, 153 million Adobe accounts were breached...",
        "DataClasses": ["Email addresses", "Passwords", "Usernames"]
      }
    ],
    "checked_at": "2024-01-15 10:30:45"
  }
]
```

### CSV Format (.csv)
Tabular summary format:
```csv
email,status,breach_count,checked_at
user@example.com,found,2,2024-01-15 10:30:45
clean@example.com,clean,0,2024-01-15 10:30:47
```

### Text Format (.txt)
Human-readable report:
```
Dark Web Checker Results
==================================================

Email: user@example.com
Status: found
Breach Count: 2
Checked At: 2024-01-15 10:30:45
Breaches:
  - Adobe: 2013-10-04
  - LinkedIn: 2012-05-05
------------------------------
```

## Troubleshooting

### Common Issues

#### "API key is required"
**Solution:** Set your API key as an environment variable or use the `--api-key` parameter.

#### "Rate limit exceeded"
**Solution:** The tool automatically handles rate limiting. If you see this message, wait a moment and try again.

#### "File not found"
**Solution:** Check the file path and ensure the file exists. Use absolute paths if needed.

#### "No valid email addresses found"
**Solution:** Verify your input file contains properly formatted email addresses.

#### "Network error"
**Solution:** Check your internet connection and firewall settings.

### Debug Mode
Use the `-v` flag for detailed logging:
```bash
python dark_web_checker.py -f emails.txt -o results.json -v
```

### Log Files
Check `dark_web_checker.log` for detailed error information.

## FAQ

### Q: Is this tool legal to use?
**A:** Yes, when used for legitimate security purposes like checking your own email addresses or those you have permission to check.

### Q: How accurate is the data?
**A:** The tool uses the Have I Been Pwned database, which is highly accurate but may not include all breaches or the most recent ones.

### Q: Can I check passwords?
**A:** No, this tool only checks email addresses. Never share passwords with any online service.

### Q: How much does it cost?
**A:** The tool is free, but you need to purchase a Have I Been Pwned API key for automated access.

### Q: How fast is it?
**A:** Due to API rate limiting, it checks approximately 40 emails per minute.

### Q: Can I check the same email multiple times?
**A:** Yes, but be mindful of rate limits. The breach status may change over time as new breaches are discovered.

### Q: What should I do if my email is found in breaches?
**A:** 
1. Change passwords for affected accounts
2. Enable two-factor authentication
3. Monitor accounts for suspicious activity
4. Consider using a password manager

### Q: Does this tool store my data?
**A:** No, the tool only processes data locally and communicates directly with the Have I Been Pwned API.

### Q: Can I use this for commercial purposes?
**A:** Yes, the tool is released under the MIT license, but check the Have I Been Pwned API terms for commercial usage.

## Support

For technical issues:
1. Check the log file: `dark_web_checker.log`
2. Run with verbose mode: `-v`
3. Review this documentation
4. Check the GitHub issues page

For API-related issues:
- Visit [Have I Been Pwned Support](https://haveibeenpwned.com/API/v3)

## Security Best Practices

1. **Protect your API key**: Never share or commit it to version control
2. **Use environment variables**: Store the API key as an environment variable
3. **Limit access**: Only check emails you own or have permission to check
4. **Secure output files**: Protect result files as they contain sensitive information
5. **Regular updates**: Keep the tool and dependencies updated