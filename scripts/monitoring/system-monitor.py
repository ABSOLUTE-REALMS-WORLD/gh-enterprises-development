#!/usr/bin/env python3
"""
System Monitor

Real-time system monitoring tool.
"""

import time
import logging
import psutil
import sys
from datetime import datetime
from pathlib import Path

class SystemMonitor:
    """Real-time system monitoring."""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """Set up logging."""
        Path('logs').mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/system-monitor.log'),
                logging.StreamHandler()
            ]
        )
    
    def get_system_info(self):
        """Get current system information."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / (1024**3)
            }
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return None
    
    def monitor_once(self):
        """Run one monitoring cycle."""
        info = self.get_system_info()
        if not info:
            return False
        
        self.logger.info(f"CPU: {info['cpu_percent']:.1f}% | "
                        f"Memory: {info['memory_percent']:.1f}% | "
                        f"Disk: {info['disk_percent']:.1f}%")
        
        # Check for alerts
        alerts = []
        if info['cpu_percent'] > 80:
            alerts.append(f"High CPU usage: {info['cpu_percent']:.1f}%")
        if info['memory_percent'] > 80:
            alerts.append(f"High memory usage: {info['memory_percent']:.1f}%")
        if info['disk_percent'] > 80:
            alerts.append(f"High disk usage: {info['disk_percent']:.1f}%")
        
        for alert in alerts:
            self.logger.warning(f"⚠️ {alert}")
        
        return True
    
    def monitor_continuous(self, interval=60):
        """Run continuous monitoring."""
        self.logger.info(f"Starting continuous monitoring (interval: {interval}s)")
        
        try:
            while True:
                self.monitor_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'continuous':
        monitor = SystemMonitor()
        monitor.monitor_continuous()
    else:
        monitor = SystemMonitor()
        monitor.monitor_once()

if __name__ == "__main__":
    main()
