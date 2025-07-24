#!/usr/bin/env python3
"""
Dark Web Checker - Email Breach Detection Tool
Author: Matteo Sala (matteo.sala@hackforce.ai)
License: MIT
"""

import os
import sys
import json
import csv
import time
import argparse
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dark_web_checker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DarkWebChecker:
    """Main class for checking email addresses against data breaches."""
    
    def __init__(self, api_key: str, hourly_limit: int = 100, request_delay: float = 1.6):
        """
        Initialize the Dark Web Checker.
        
        Args:
            api_key (str): Have I Been Pwned API key
            hourly_limit (int): Maximum requests per hour (default: 100)
            request_delay (float): Delay between requests in seconds (default: 1.6)
        """
        self.api_key = api_key
        self.base_url = "https://haveibeenpwned.com/api/v3"
        self.hourly_limit = hourly_limit
        self.request_delay = request_delay
        self.request_history = []  # Track request timestamps
        
        self.session = requests.Session()
        self.session.headers.update({
            'hibp-api-key': self.api_key,
            'User-Agent': 'DarkWebChecker/1.0'
        })
        
        logger.info(f"Initialized with hourly limit: {hourly_limit} requests/hour, delay: {request_delay}s")
        
    def display_banner(self):
        """Display the application banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██╗    ██╗███████╗██████╗             ║
║    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██║    ██║██╔════╝██╔══██╗            ║
║    ██║  ██║███████║██████╔╝█████╔╝     ██║ █╗ ██║█████╗  ██████╔╝            ║
║    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║███╗██║██╔══╝  ██╔══██╗            ║
║    ██████╔╝██║  ██║██║  ██║██║  ██╗    ╚███╔███╔╝███████╗██████╔╝            ║
║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝             ║
║                                                                              ║
║                          ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ ║
║                         ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗║
║                         ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝║
║                         ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗║
║                         ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║║
║                          ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝║
║                                                                              ║
║                    Email Breach Detection Tool v1.0.0                       ║
║                    Powered by Have I Been Pwned API                         ║
║                                                                              ║
║                        Author: Matteo Sala                                   ║
║                        Email: matteo.sala@hackforce.ai                      ║
║                                                                              ║
║                              MIT License                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print("🔍 Checking email addresses for data breaches...")
        print("⚠️  Remember: This tool is for legitimate security purposes only!\n")

    def _clean_old_requests(self):
        """Remove request timestamps older than 1 hour."""
        one_hour_ago = datetime.now() - timedelta(hours=1)
        self.request_history = [
            timestamp for timestamp in self.request_history 
            if timestamp > one_hour_ago
        ]

    def _check_rate_limit(self) -> bool:
        """
        Check if we can make another request within the hourly limit.
        
        Returns:
            bool: True if request is allowed, False if rate limit exceeded
        """
        self._clean_old_requests()
        return len(self.request_history) < self.hourly_limit

    def _wait_for_rate_limit(self):
        """Wait until we can make another request within the hourly limit."""
        while not self._check_rate_limit():
            self._clean_old_requests()
            oldest_request = min(self.request_history) if self.request_history else datetime.now()
            wait_until = oldest_request + timedelta(hours=1)
            wait_seconds = (wait_until - datetime.now()).total_seconds()
            
            if wait_seconds > 0:
                logger.warning(f"Hourly rate limit ({self.hourly_limit}) reached. Waiting {wait_seconds:.0f} seconds...")
                print(f"⏳ Rate limit reached. Waiting {wait_seconds:.0f} seconds until next request...")
                time.sleep(min(wait_seconds, 60))  # Wait in chunks of max 60 seconds

    def _record_request(self):
        """Record the timestamp of a request."""
        self.request_history.append(datetime.now())

    def check_email_breach(self, email: str) -> Dict[str, Any]:
        """
        Check if an email address has been involved in data breaches.
        
        Args:
            email (str): Email address to check
            
        Returns:
            Dict[str, Any]: Breach information or error details
        """
        try:
            # Check and wait for rate limit
            self._wait_for_rate_limit()
            
            url = f"{self.base_url}/breachedaccount/{email}"
            params = {'truncateResponse': 'false'}
            
            logger.info(f"Checking email: {email} (Requests this hour: {len(self.request_history)})")
            
            # Record the request
            self._record_request()
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                breaches = response.json()
                logger.info(f"Found {len(breaches)} breaches for {email}")
                return {
                    'email': email,
                    'status': 'found',
                    'breach_count': len(breaches),
                    'breaches': breaches,
                    'checked_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            elif response.status_code == 404:
                logger.info(f"No breaches found for {email}")
                return {
                    'email': email,
                    'status': 'clean',
                    'breach_count': 0,
                    'breaches': [],
                    'checked_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            elif response.status_code == 429:
                logger.warning(f"Rate limit exceeded by API. Waiting...")
                time.sleep(6)  # Wait 6 seconds for API rate limit
                return self.check_email_breach(email)  # Retry
            else:
                error_msg = f"API error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return {
                    'email': email,
                    'status': 'error',
                    'error': error_msg,
                    'checked_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            return {
                'email': email,
                'status': 'error',
                'error': error_msg,
                'checked_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {
                'email': email,
                'status': 'error',
                'error': error_msg,
                'checked_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }

    def load_emails_from_file(self, file_path: str) -> List[str]:
        """
        Load email addresses from various file formats.
        
        Args:
            file_path (str): Path to the input file
            
        Returns:
            List[str]: List of email addresses
        """
        emails = []
        file_extension = Path(file_path).suffix.lower()
        
        try:
            if file_extension == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        emails = [str(item) for item in data if '@' in str(item)]
                    elif isinstance(data, dict):
                        # Try to find email fields in the JSON
                        for key, value in data.items():
                            if isinstance(value, list):
                                emails.extend([str(item) for item in value if '@' in str(item)])
                            elif '@' in str(value):
                                emails.append(str(value))
                                
            elif file_extension == '.csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    csv_reader = csv.reader(f)
                    for row in csv_reader:
                        for cell in row:
                            if '@' in str(cell):
                                emails.append(str(cell).strip())
                                
            else:  # Treat as text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if '@' in line:
                            emails.append(line)
                            
        except Exception as e:
            logger.error(f"Error loading emails from file: {str(e)}")
            raise
            
        # Remove duplicates and validate emails
        unique_emails = list(set(emails))
        valid_emails = [email for email in unique_emails if self.is_valid_email(email)]
        
        logger.info(f"Loaded {len(valid_emails)} valid email addresses from {file_path}")
        return valid_emails

    def is_valid_email(self, email: str) -> bool:
        """
        Basic email validation.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email appears valid
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def save_results(self, results: List[Dict[str, Any]], output_file: str):
        """
        Save results to output file.
        
        Args:
            results (List[Dict[str, Any]]): Results to save
            output_file (str): Output file path
        """
        file_extension = Path(output_file).suffix.lower()
        
        try:
            if file_extension == '.json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                    
            elif file_extension == '.csv':
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    if results:
                        fieldnames = ['email', 'status', 'breach_count', 'checked_at']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for result in results:
                            row = {
                                'email': result['email'],
                                'status': result['status'],
                                'breach_count': result.get('breach_count', 0),
                                'checked_at': result['checked_at']
                            }
                            writer.writerow(row)
                            
            else:  # Text format
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("Dark Web Checker Results\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for result in results:
                        f.write(f"Email: {result['email']}\n")
                        f.write(f"Status: {result['status']}\n")
                        f.write(f"Breach Count: {result.get('breach_count', 0)}\n")
                        f.write(f"Checked At: {result['checked_at']}\n")
                        
                        if result['status'] == 'found' and result.get('breaches'):
                            f.write("Breaches:\n")
                            for breach in result['breaches']:
                                f.write(f"  - {breach.get('Name', 'Unknown')}: {breach.get('BreachDate', 'Unknown date')}\n")
                        elif result['status'] == 'error':
                            f.write(f"Error: {result.get('error', 'Unknown error')}\n")
                            
                        f.write("-" * 30 + "\n\n")
                        
            logger.info(f"Results saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise

def get_api_key() -> str:
    """Get API key from environment variable or user input."""
    api_key = os.getenv('HIBP_API_KEY')
    if not api_key:
        print("🔑 Have I Been Pwned API key required!")
        print("You can get your API key from: https://haveibeenpwned.com/API/Key")
        print("Set it as environment variable: export HIBP_API_KEY='your_key_here'")
        api_key = input("Enter your API key: ").strip()
    return api_key

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Dark Web Checker - Email Breach Detection Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dark_web_checker.py -f emails.txt -o results.json
  python dark_web_checker.py -e user@example.com -o results.csv
  python dark_web_checker.py --file emails.csv --output results.txt --hourly-limit 50
  python dark_web_checker.py -f emails.txt -o results.json --request-delay 2.0
        """
    )
    
    parser.add_argument('-f', '--file', type=str, help='Input file containing email addresses (txt, csv, json)')
    parser.add_argument('-e', '--email', type=str, help='Single email address to check')
    parser.add_argument('-o', '--output', type=str, help='Output file for results (txt, csv, json)')
    parser.add_argument('--api-key', type=str, help='Have I Been Pwned API key')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--hourly-limit', type=int, default=100, 
                       help='Maximum requests per hour (default: 100)')
    parser.add_argument('--request-delay', type=float, default=1.6,
                       help='Delay between requests in seconds (default: 1.6)')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get rate limiting configuration from environment or use defaults
    hourly_limit = int(os.getenv('HIBP_HOURLY_LIMIT', args.hourly_limit))
    request_delay = float(os.getenv('HIBP_REQUEST_DELAY', args.request_delay))
    
    # Initialize checker
    checker = DarkWebChecker("", hourly_limit=hourly_limit, request_delay=request_delay)
    checker.display_banner()
    
    # Display rate limiting info
    print(f"⚙️  Rate limiting: {hourly_limit} requests/hour, {request_delay}s delay between requests\n")
    
    # Get API key
    api_key = args.api_key or get_api_key()
    if not api_key:
        print("❌ API key is required to use this tool.")
        sys.exit(1)
    
    checker.api_key = api_key
    checker.session.headers.update({'hibp-api-key': api_key})
    
    # Get emails to check
    emails = []
    
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        emails = checker.load_emails_from_file(args.file)
    elif args.email:
        if checker.is_valid_email(args.email):
            emails = [args.email]
        else:
            print(f"❌ Invalid email address: {args.email}")
            sys.exit(1)
    else:
        # Interactive mode
        choice = input("Do you want to check a single email address? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            email = input("Enter email address: ").strip()
            if checker.is_valid_email(email):
                emails = [email]
            else:
                print("❌ Invalid email address format.")
                sys.exit(1)
        else:
            file_path = input("Enter path to file containing email addresses: ").strip()
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                sys.exit(1)
            emails = checker.load_emails_from_file(file_path)
    
    if not emails:
        print("❌ No valid email addresses found.")
        sys.exit(1)
    
    # Get output file
    output_file = args.output
    if not output_file:
        output_file = input("Enter output file path (e.g., results.json): ").strip()
        if not output_file:
            output_file = "results.json"
    
    # Check emails
    print(f"\n🔍 Checking {len(emails)} email address(es)...")
    results = []
    
    for i, email in enumerate(emails, 1):
        print(f"[{i}/{len(emails)}] Checking: {email}")
        result = checker.check_email_breach(email)
        results.append(result)
        
        # Apply request delay between emails (except for the last one)
        if i < len(emails):
            time.sleep(checker.request_delay)
    
    # Save results
    checker.save_results(results, output_file)
    
    # Summary
    found_breaches = sum(1 for r in results if r['status'] == 'found')
    clean_emails = sum(1 for r in results if r['status'] == 'clean')
    errors = sum(1 for r in results if r['status'] == 'error')
    
    print(f"\n📊 Summary:")
    print(f"   Total emails checked: {len(emails)}")
    print(f"   🚨 Found in breaches: {found_breaches}")
    print(f"   ✅ Clean: {clean_emails}")
    print(f"   ❌ Errors: {errors}")
    print(f"   📄 Results saved to: {output_file}")
    
    if found_breaches > 0:
        print(f"\n⚠️  {found_breaches} email(s) found in data breaches!")
        print("   Consider changing passwords and enabling 2FA for affected accounts.")

if __name__ == "__main__":
    main()