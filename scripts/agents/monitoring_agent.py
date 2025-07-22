#!/usr/bin/env python3
"""
System Monitoring Agent

This agent handles system health and performance monitoring.
"""

import time
import logging
import psutil
from datetime import datetime
from pathlib import Path

class SystemMonitoringAgent:
    """System health and performance monitoring agent."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/monitoring-agent.log'),
                logging.StreamHandler()
            ]
        )
    
    def check_system_health(self):
        """Check system health metrics."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        self.logger.info(f"CPU Usage: {cpu_percent}%")
        self.logger.info(f"Memory Usage: {memory.percent}%")
        self.logger.info(f"Disk Usage: {disk.percent}%")
        
        # Alert if thresholds exceeded
        if cpu_percent > 80:
            self.logger.warning(f"High CPU usage: {cpu_percent}%")
        if memory.percent > 80:
            self.logger.warning(f"High memory usage: {memory.percent}%")
        if disk.percent > 80:
            self.logger.warning(f"High disk usage: {disk.percent}%")
    
    def run(self):
        """Main agent loop."""
        self.logger.info("Starting System Monitoring Agent")
        
        while True:
            try:
                self.check_system_health()
                time.sleep(300)  # Run every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in monitoring agent: {e}")
                time.sleep(60)  # Wait 1 minute on error

if __name__ == "__main__":
    agent = SystemMonitoringAgent()
    agent.run()
