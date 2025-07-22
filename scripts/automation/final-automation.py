#!/usr/bin/env python3
"""
Final Automation Script

This script runs automated tasks and processes.
Mentioned in README.md as: python scripts/automation/final-automation.py
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime

class AutomationRunner:
    """Runs automated tasks and processes."""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """Set up logging configuration."""
        # Ensure logs directory exists
        Path('logs').mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/automation.log'),
                logging.StreamHandler()
            ]
        )
    
    def run_security_scan(self):
        """Run security scanning."""
        self.logger.info("🔍 Running security scan...")
        
        try:
            # Run credential manager check
            result = subprocess.run([
                sys.executable, 'scripts/security/credential-manager.py', 'check'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("✅ Security scan completed successfully")
            else:
                self.logger.warning(f"⚠️ Security scan found issues: {result.stdout}")
            
            return result.returncode == 0
            
        except Exception as e:
            self.logger.error(f"❌ Error running security scan: {e}")
            return False
    
    def check_system_health(self):
        """Check system health and resources."""
        self.logger.info("💊 Checking system health...")
        
        try:
            import psutil
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.logger.info(f"CPU Usage: {cpu_percent}%")
            self.logger.info(f"Memory Usage: {memory.percent}%")
            self.logger.info(f"Disk Usage: {disk.percent}%")
            
            # Check thresholds
            issues = []
            if cpu_percent > 80:
                issues.append(f"High CPU usage: {cpu_percent}%")
            if memory.percent > 80:
                issues.append(f"High memory usage: {memory.percent}%")
            if disk.percent > 80:
                issues.append(f"High disk usage: {disk.percent}%")
            
            if issues:
                self.logger.warning(f"⚠️ System health issues: {issues}")
                return False
            else:
                self.logger.info("✅ System health is good")
                return True
                
        except ImportError:
            self.logger.warning("⚠️ psutil not available, skipping system health check")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error checking system health: {e}")
            return False
    
    def cleanup_logs(self):
        """Clean up old log files."""
        self.logger.info("🧹 Cleaning up old logs...")
        
        logs_dir = Path('logs')
        if not logs_dir.exists():
            return True
        
        try:
            # Find log files older than 30 days
            cutoff_time = time.time() - (30 * 24 * 60 * 60)  # 30 days
            cleaned_files = 0
            
            for log_file in logs_dir.glob('*.log'):
                if log_file.stat().st_mtime < cutoff_time:
                    # Create backup before deletion
                    backup_name = f"{log_file.stem}.old.log"
                    backup_path = logs_dir / backup_name
                    log_file.rename(backup_path)
                    cleaned_files += 1
            
            if cleaned_files > 0:
                self.logger.info(f"✅ Cleaned up {cleaned_files} old log files")
            else:
                self.logger.info("✅ No old log files to clean up")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error cleaning up logs: {e}")
            return False
    
    def run_automation(self):
        """Run all automation tasks."""
        self.logger.info("🤖 Starting Final Automation")
        self.logger.info("=" * 50)
        
        tasks = [
            ("Security Scan", self.run_security_scan),
            ("System Health Check", self.check_system_health),
            ("Log Cleanup", self.cleanup_logs)
        ]
        
        results = {}
        for task_name, task_func in tasks:
            self.logger.info(f"Running {task_name}...")
            try:
                result = task_func()
                results[task_name] = result
                if result:
                    self.logger.info(f"✅ {task_name} completed successfully")
                else:
                    self.logger.warning(f"⚠️ {task_name} completed with warnings")
            except Exception as e:
                self.logger.error(f"❌ {task_name} failed: {e}")
                results[task_name] = False
        
        # Summary
        self.logger.info("=" * 50)
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)
        
        self.logger.info(f"Automation Summary: {success_count}/{total_count} tasks successful")
        
        for task_name, result in results.items():
            status = "✅" if result else "❌"
            self.logger.info(f"{status} {task_name}")
        
        return success_count == total_count

def main():
    runner = AutomationRunner()
    success = runner.run_automation()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
