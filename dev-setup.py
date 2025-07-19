#!/usr/bin/env python3
"""
Development Setup Script

This script helps with common development tasks in the GH Enterprises development repository.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, Any

class DevelopmentSetup:
    """Development setup and utility functions."""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.logs_dir = self.project_root / "logs"
        
    def check_system_status(self) -> Dict[str, Any]:
        """Check the current system status."""
        print("🔍 Checking system status...")
        
        status = {
            "agents_running": False,
            "logs_available": False,
            "env_file": False,
            "dependencies": False
        }
        
        # Check if agents are running
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            if "agent_manager.py" in result.stdout:
                status["agents_running"] = True
                print("✅ Background agents are running")
            else:
                print("❌ Background agents are not running")
        except Exception as e:
            print(f"❌ Error checking agents: {e}")
        
        # Check logs directory
        if self.logs_dir.exists():
            status["logs_available"] = True
            print("✅ Logs directory exists")
        else:
            print("❌ Logs directory not found")
        
        # Check .env file
        env_file = self.project_root / ".env"
        if env_file.exists():
            status["env_file"] = True
            print("✅ Environment file exists")
        else:
            print("❌ Environment file not found")
        
        # Check dependencies
        try:
            import azure.identity
            import requests
            import psutil
            status["dependencies"] = True
            print("✅ Dependencies are installed")
        except ImportError as e:
            print(f"❌ Missing dependencies: {e}")
        
        return status
    
    def show_logs(self, agent_name: str = "all") -> None:
        """Show logs for specified agent or all agents."""
        print(f"📋 Showing logs for {agent_name}...")
        
        if agent_name == "all":
            log_files = ["monitoring-agent.log", "security-agent.log", "credential-agent.log"]
        else:
            log_files = [f"{agent_name}-agent.log"]
        
        for log_file in log_files:
            log_path = self.logs_dir / log_file
            if log_path.exists():
                print(f"\n--- {log_file} ---")
                with open(log_path, 'r') as f:
                    content = f.read()
                    if content.strip():
                        print(content)
                    else:
                        print("(No logs yet)")
            else:
                print(f"❌ Log file not found: {log_file}")
    
    def run_security_scan(self) -> bool:
        """Run security scan using the credential manager."""
        print("�� Running security scan...")
        
        try:
            # Use the credential manager from the parent directory
            credential_manager = self.project_root.parent / "scripts" / "security" / "credential-manager.py"
            
            if credential_manager.exists():
                result = subprocess.run([
                    sys.executable, str(credential_manager), "check"
                ], capture_output=True, text=True)
                
                print("Security Scan Results:")
                print(result.stdout)
                
                if result.returncode == 0:
                    print("✅ Security scan completed successfully")
                    return True
                else:
                    print("❌ Security scan failed")
                    return False
            else:
                print("❌ Credential manager not found")
                return False
                
        except Exception as e:
            print(f"❌ Error running security scan: {e}")
            return False
    
    def show_help(self) -> None:
        """Show help information."""
        print("""
🔧 Development Setup Help

Available commands:
  status     - Check system status
  logs       - Show agent logs
  security   - Run security scan
  help       - Show this help

Usage:
  python dev-setup.py [command]

Examples:
  python dev-setup.py status
  python dev-setup.py logs monitoring
  python dev-setup.py security
        """)

def main():
    """Main function."""
    setup = DevelopmentSetup()
    
    if len(sys.argv) < 2:
        setup.show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        setup.check_system_status()
    elif command == "logs":
        agent = sys.argv[2] if len(sys.argv) > 2 else "all"
        setup.show_logs(agent)
    elif command == "security":
        setup.run_security_scan()
    elif command == "help":
        setup.show_help()
    else:
        print(f"❌ Unknown command: {command}")
        setup.show_help()

if __name__ == "__main__":
    main()
