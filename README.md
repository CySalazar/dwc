# 🔍 Dark Web Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Have I Been Pwned](https://img.shields.io/badge/API-Have%20I%20Been%20Pwned-red.svg)](https://haveibeenpwned.com/)

A powerful command-line tool to check if email addresses have been compromised in data breaches using the Have I Been Pwned database.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██╗    ██╗███████╗██████╗             ║
║    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██║    ██║██╔════╝██╔══██╗            ║
║    ██║  ██║███████║██████╔╝█████╔╝     ██║ █╗ ██║█████╗  ██████╔╝            ║
║    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║███╗██║██╔══╝  ██╔══██╗            ║
║    ██████╔╝██║  ██║██║  ██║██║  ██╗    ╚███╔███╔╝███████╗██████╔╝            ║
║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝             ║
║                                                                              ║
║                     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗   ║
║                    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗  ║
║                    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝  ║
║                    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗  ║
║                    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║  ║
║                     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ║
║                                                                              ║
║                          Email Breach Detection Tool                         ║
║                         Using Have I Been Pwned API                         ║
║                                                                              ║
║                        Author: Matteo Sala                                   ║
║                        Email: matteo.sala@hackforce.ai                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 🌟 Features

- ✅ **Multiple Input Formats**: Support for TXT, CSV, and JSON files
- ✅ **Comprehensive Reports**: Detailed breach information with multiple output formats
- ✅ **Rate Limiting**: Automatic handling of API rate limits
- ✅ **Interactive Mode**: User-friendly prompts for easy operation
- ✅ **Batch Processing**: Check thousands of emails efficiently
- ✅ **Detailed Logging**: Comprehensive logging for debugging and monitoring
- ✅ **Security Focused**: Secure API key handling and data processing

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/DarkWebChecker.git
cd DarkWebChecker

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Key

Visit [Have I Been Pwned API](https://haveibeenpwned.com/API/Key) to obtain your API key.

### 3. Configure API Key

Choose one of these methods:

#### Method 1: .env File (Recommended)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
HIBP_API_KEY=your_actual_api_key_here
```

#### Method 2: Environment Variable
```bash
# Linux/macOS
export HIBP_API_KEY="your_api_key_here"

# Windows
set HIBP_API_KEY=your_api_key_here
```

#### Method 3: Command Line Parameter
```bash
python dark_web_checker.py --api-key your_api_key_here -e email@example.com -o results.json
```

### 4. Run the Tool

```bash
# Check a single email
python dark_web_checker.py -e user@example.com -o results.json

# Check multiple emails from file
python dark_web_checker.py -f emails.txt -o results.csv

# Interactive mode
python dark_web_checker.py
```

## 📖 Usage Examples

### Single Email Check
```bash
python dark_web_checker.py -e john.doe@company.com -o john_results.json
```

### Batch Email Check
```bash
python dark_web_checker.py -f employee_emails.txt -o company_breach_report.csv
```

### With Custom API Key
```bash
python dark_web_checker.py -f emails.csv -o results.txt --api-key YOUR_API_KEY
```

### Verbose Mode
```bash
python dark_web_checker.py -f emails.json -o results.json -v
```

## 📁 Input File Formats

### Text Files (.txt)
```
user1@example.com
user2@company.org
admin@website.net
```

### CSV Files (.csv)
```csv
Name,Email,Department
John Doe,john@company.com,IT
Jane Smith,jane@company.com,HR
```

### JSON Files (.json)
```json
[
  "user1@example.com",
  "user2@example.com",
  "user3@example.com"
]
```

## 📊 Output Formats

- **JSON**: Complete structured data with all breach details
- **CSV**: Tabular format perfect for spreadsheet analysis
- **TXT**: Human-readable reports for easy review

## 🛡️ Philosophy

Dark Web Checker was created with the following principles in mind:

### Security First
- **Legitimate Use Only**: Designed for checking your own email addresses or those you have explicit permission to check
- **Privacy Focused**: No data storage, direct API communication only
- **Secure by Design**: Proper API key handling and secure data transmission

### User Experience
- **Simple Interface**: Easy-to-use command-line interface with helpful prompts
- **Multiple Formats**: Support for various input and output formats
- **Comprehensive Documentation**: Detailed guides for all user levels

### Reliability
- **Error Handling**: Robust error handling for network issues, API problems, and file errors
- **Rate Limiting**: Automatic compliance with API rate limits
- **Logging**: Comprehensive logging for troubleshooting and monitoring

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **Bug Reports**: Found a bug? Please open an issue with detailed information
2. **Feature Requests**: Have an idea for improvement? We'd love to hear it
3. **Code Contributions**: Submit pull requests for bug fixes or new features
4. **Documentation**: Help improve our documentation
5. **Testing**: Help test the tool with different scenarios

### Development Setup

```bash
# Fork the repository
git clone https://github.com/yourusername/DarkWebChecker.git
cd DarkWebChecker

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest tests/
```

### Contribution Guidelines

1. **Code Style**: Follow PEP 8 guidelines
2. **Testing**: Add tests for new features
3. **Documentation**: Update documentation for changes
4. **Commit Messages**: Use clear, descriptive commit messages
5. **Pull Requests**: Provide detailed descriptions of changes

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a positive environment

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[User Manual](docs/user_manual.md)**: Complete guide for end users
- **[Technical Documentation](docs/technical_documentation.md)**: Architecture and implementation details
- **[API Reference](docs/api_reference.md)**: Detailed API documentation

## ⚖️ Legal and Ethical Use

### Intended Use
This tool is designed for:
- ✅ Checking your own email addresses
- ✅ Security audits with proper authorization
- ✅ Educational purposes
- ✅ Legitimate security research

### Prohibited Use
Do NOT use this tool for:
- ❌ Checking emails without permission
- ❌ Harassment or stalking
- ❌ Illegal activities
- ❌ Violating privacy rights

### Disclaimer
- This tool relies on the Have I Been Pwned database
- Results may not include all breaches or the most recent ones
- Users are responsible for complying with applicable laws and regulations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Troy Hunt** and the [Have I Been Pwned](https://haveibeenpwned.com/) team for providing the invaluable breach database
- **Python Community** for the excellent libraries that make this tool possible
- **Contributors** who help improve this tool

## 📞 Support

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Open an issue on GitHub
- **API Support**: Visit [Have I Been Pwned Support](https://haveibeenpwned.com/API/v3)

## 🔄 Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Support for TXT, CSV, and JSON input formats
- Multiple output formats (JSON, CSV, TXT)
- Automatic rate limiting
- Comprehensive error handling
- Interactive mode
- Detailed logging

---

**⚠️ Remember: Use this tool responsibly and only for legitimate security purposes!**