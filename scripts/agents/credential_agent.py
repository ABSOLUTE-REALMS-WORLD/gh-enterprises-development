#!/usr/bin/env python3
"""
Credential Management Agent

This agent handles automated credential rotation and management.
"""

import time
import logging
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

class CredentialManagementAgent:
    """Automated credential management agent."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.credential_status = {}
        self.load_credential_config()
    
    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/credential-agent.log'),
                logging.StreamHandler()
            ]
        )
    
    def load_credential_config(self):
        """Load credential configuration."""
        try:
            config_path = Path('config/config.json')
            if config_path.exists():
                with open(config_path) as f:
                    config = json.load(f)
                    self.rotation_interval = config.get('security', {}).get('scan_interval', 3600)
            else:
                self.rotation_interval = 3600
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            self.rotation_interval = 3600
    
    def check_environment_credentials(self):
        """Check environment credential status."""
        credentials_to_check = [
            'GITHUB_TOKEN',
            'AZURE_CLIENT_ID',
            'AZURE_CLIENT_SECRET',
            'AZURE_TENANT_ID',
            'AZURE_SUBSCRIPTION_ID'
        ]
        
        issues = []
        for cred_name in credentials_to_check:
            value = os.getenv(cred_name)
            if not value:
                issues.append(f"Missing credential: {cred_name}")
                self.credential_status[cred_name] = {
                    'status': 'missing',
                    'last_checked': datetime.now().isoformat()
                }
            else:
                # Check if credential looks valid (basic validation)
                if len(value) < 10:
                    issues.append(f"Credential may be invalid: {cred_name}")
                    self.credential_status[cred_name] = {
                        'status': 'invalid',
                        'last_checked': datetime.now().isoformat()
                    }
                else:
                    self.credential_status[cred_name] = {
                        'status': 'valid',
                        'last_checked': datetime.now().isoformat()
                    }
        
        return issues
    
    def check_dot_env_file(self):
        """Check .env file security and presence."""
        env_path = Path('.env')
        issues = []
        
        if not env_path.exists():
            issues.append(".env file not found")
            return issues
        
        # Check file permissions
        stat_info = env_path.stat()
        if stat_info.st_mode & 0o077:  # Others or group have access
            issues.append(".env file has insecure permissions")
        
        # Check if .env is in .gitignore
        gitignore_path = Path('.gitignore')
        if gitignore_path.exists():
            with open(gitignore_path) as f:
                if '.env' not in f.read():
                    issues.append(".env file not in .gitignore")
        else:
            issues.append(".gitignore file missing")
        
        return issues
    
    def run_credential_check(self):
        """Run comprehensive credential check."""
        self.logger.info("Starting credential check...")
        
        # Run individual checks
        env_issues = self.check_environment_credentials()
        file_issues = self.check_dot_env_file()
        
        all_issues = env_issues + file_issues
        
        if not all_issues:
            self.logger.info("✅ Credential check completed - All credentials OK")
        else:
            self.logger.warning(f"⚠️ Credential check completed - Found {len(all_issues)} issues:")
            for issue in all_issues:
                self.logger.warning(f"  - {issue}")
        
        # Save status
        status_file = Path('logs/credential-status.json')
        try:
            with open(status_file, 'w') as f:
                json.dump({
                    'last_check': datetime.now().isoformat(),
                    'credential_status': self.credential_status,
                    'issues': all_issues
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving status: {e}")
        
        return len(all_issues)

    def run(self):
        """Main agent loop."""
        self.logger.info("Starting Credential Management Agent")
        
        while True:
            try:
                self.run_credential_check()
                time.sleep(3600)  # Run every hour
                
            except Exception as e:
                self.logger.error(f"Error in credential agent: {e}")
                time.sleep(300)  # Wait 5 minutes on error

if __name__ == "__main__":
    agent = CredentialManagementAgent()
    agent.run()
