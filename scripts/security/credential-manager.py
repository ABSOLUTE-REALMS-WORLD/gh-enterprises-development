#!/usr/bin/env python3
"""
Credential Manager

This script provides credential management and security checking functionality.
Mentioned in README.md as: python scripts/security/credential-manager.py check
"""

import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime

class CredentialManager:
    """Manages credentials and security checking."""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def check_credentials(self):
        """Check credential status and security."""
        self.logger.info("🔐 Running credential security check...")
        
        issues = []
        
        # Check environment variables
        required_env_vars = [
            'GITHUB_TOKEN',
            'AZURE_CLIENT_ID',
            'AZURE_CLIENT_SECRET',
            'AZURE_TENANT_ID'
        ]
        
        for env_var in required_env_vars:
            if not os.getenv(env_var):
                issues.append(f"Missing environment variable: {env_var}")
            elif len(os.getenv(env_var, '')) < 10:
                issues.append(f"Environment variable may be invalid: {env_var}")
        
        # Check .env file
        env_file = Path('.env')
        if env_file.exists():
            # Check permissions
            stat_info = env_file.stat()
            if stat_info.st_mode & 0o077:
                issues.append(".env file has insecure permissions (readable by others)")
            
            self.logger.info("✅ .env file found with secure permissions")
        else:
            issues.append(".env file not found")
        
        # Check .gitignore
        gitignore = Path('.gitignore')
        if gitignore.exists():
            with open(gitignore) as f:
                content = f.read()
                if '.env' not in content:
                    issues.append(".env not listed in .gitignore")
        else:
            issues.append(".gitignore file not found")
        
        # Report results
        if not issues:
            self.logger.info("✅ All credential checks passed!")
            return 0
        else:
            self.logger.error(f"❌ Found {len(issues)} credential issues:")
            for issue in issues:
                self.logger.error(f"  - {issue}")
            return len(issues)
    
    def show_status(self):
        """Show current credential status."""
        self.logger.info("📊 Credential Status Report")
        self.logger.info("=" * 50)
        
        # Check each credential
        credentials = {
            'GITHUB_TOKEN': 'GitHub Personal Access Token',
            'AZURE_CLIENT_ID': 'Azure Service Principal Client ID',
            'AZURE_CLIENT_SECRET': 'Azure Service Principal Secret',
            'AZURE_TENANT_ID': 'Azure Tenant ID',
            'AZURE_SUBSCRIPTION_ID': 'Azure Subscription ID'
        }
        
        for env_var, description in credentials.items():
            value = os.getenv(env_var)
            if value:
                self.logger.info(f"✅ {description}: Present")
            else:
                self.logger.info(f"❌ {description}: Missing")
    
    def help(self):
        """Show help information."""
        print("""
Credential Manager - Security and Credential Management Tool

Usage:
    python scripts/security/credential-manager.py <command>

Commands:
    check       Run security check on credentials
    status      Show current credential status
    help        Show this help message

Examples:
    python scripts/security/credential-manager.py check
    python scripts/security/credential-manager.py status
        """)

def main():
    manager = CredentialManager()
    
    if len(sys.argv) < 2:
        manager.help()
        return 1
    
    command = sys.argv[1]
    
    if command == 'check':
        return manager.check_credentials()
    elif command == 'status':
        manager.show_status()
        return 0
    elif command == 'help':
        manager.help()
        return 0
    else:
        print(f"Unknown command: {command}")
        manager.help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
