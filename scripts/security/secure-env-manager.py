#!/usr/bin/env python3
"""
Secure Environment Manager

This script manages secure environment loading.
Mentioned in README.md as: python scripts/security/secure-env-manager.py
"""

import os
import sys
import logging
from pathlib import Path

class SecureEnvManager:
    """Manages secure environment variable loading."""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def load_env_file(self, env_file='.env'):
        """Load environment variables from file."""
        env_path = Path(env_file)
        
        if not env_path.exists():
            self.logger.error(f"❌ Environment file {env_file} not found")
            return False
        
        # Check file permissions
        stat_info = env_path.stat()
        if stat_info.st_mode & 0o077:
            self.logger.warning(f"⚠️ {env_file} has insecure permissions")
        
        loaded_vars = 0
        try:
            with open(env_path) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value format
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        # Set environment variable
                        os.environ[key] = value
                        loaded_vars += 1
                        self.logger.info(f"✅ Loaded: {key}")
                    else:
                        self.logger.warning(f"⚠️ Invalid format on line {line_num}: {line}")
            
            self.logger.info(f"✅ Successfully loaded {loaded_vars} environment variables")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error loading {env_file}: {e}")
            return False
    
    def validate_environment(self):
        """Validate that required environment variables are set."""
        required_vars = [
            'GITHUB_TOKEN',
            'AZURE_CLIENT_ID', 
            'AZURE_CLIENT_SECRET',
            'AZURE_TENANT_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.logger.error(f"❌ Missing required environment variables: {missing_vars}")
            return False
        
        self.logger.info("✅ All required environment variables are set")
        return True
    
    def run(self):
        """Main execution method."""
        self.logger.info("🔐 Starting Secure Environment Manager")
        
        # Load .env file
        if not self.load_env_file():
            return 1
        
        # Validate environment
        if not self.validate_environment():
            return 1
        
        self.logger.info("✅ Environment successfully loaded and validated")
        return 0

def main():
    manager = SecureEnvManager()
    return manager.run()

if __name__ == "__main__":
    sys.exit(main())
