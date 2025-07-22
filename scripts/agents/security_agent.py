#!/usr/bin/env python3
"""
Security Monitoring Agent

This agent handles continuous security monitoring and alerting.
"""

import time
import logging
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

class SecurityMonitoringAgent:
    """Continuous security monitoring agent."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/security-agent.log'),
                logging.StreamHandler()
            ]
        )
    
    def check_file_permissions(self):
        """Check for insecure file permissions."""
        insecure_files = []
        
        # Check for world-writable files
        for root, dirs, files in os.walk('.'):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    stat_info = os.stat(file_path)
                    if stat_info.st_mode & 0o002:  # World writable
                        insecure_files.append(file_path)
                except (OSError, FileNotFoundError):
                    continue
        
        if insecure_files:
            self.logger.warning(f"Found {len(insecure_files)} world-writable files: {insecure_files[:5]}")
        
        return len(insecure_files)
    
    def check_secrets_exposure(self):
        """Check for potential secrets in code."""
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']'
        ]
        
        exposed_secrets = 0
        try:
            for pattern in patterns:
                result = subprocess.run(['grep', '-r', '-i', pattern, '.'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    # Filter out comments and test files
                    actual_secrets = [line for line in lines if not line.strip().startswith('#') 
                                    and 'test' not in line.lower()]
                    exposed_secrets += len(actual_secrets)
        except Exception as e:
            self.logger.error(f"Error checking secrets: {e}")
        
        if exposed_secrets > 0:
            self.logger.warning(f"Found {exposed_secrets} potential secret exposures")
        
        return exposed_secrets
    
    def run_security_scan(self):
        """Run comprehensive security scan."""
        self.logger.info("Starting security scan...")
        
        # Run individual checks
        perm_issues = self.check_file_permissions()
        secret_issues = self.check_secrets_exposure()
        
        total_issues = perm_issues + secret_issues
        
        scan_result = {
            'timestamp': datetime.now().isoformat(),
            'permission_issues': perm_issues,
            'secret_issues': secret_issues,
            'total_issues': total_issues
        }
        
        if total_issues == 0:
            self.logger.info("✅ Security scan completed - No issues found")
        else:
            self.logger.warning(f"⚠️ Security scan completed - Found {total_issues} issues")
        
        return scan_result

    def run(self):
        """Main agent loop."""
        self.logger.info("Starting Security Monitoring Agent")
        
        while True:
            try:
                self.run_security_scan()
                time.sleep(1800)  # Run every 30 minutes
                
            except Exception as e:
                self.logger.error(f"Error in security agent: {e}")
                time.sleep(300)  # Wait 5 minutes on error

if __name__ == "__main__":
    agent = SecurityMonitoringAgent()
    agent.run()
