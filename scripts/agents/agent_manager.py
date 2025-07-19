#!/usr/bin/env python3
"""
Agent Manager

This script manages all background agents.
"""

import subprocess
import time
import signal
import sys
from pathlib import Path

class AgentManager:
    """Manages background agents."""
    
    def __init__(self):
        self.processes = {}
        self.agents = [
            "scripts/agents/credential_agent.py",
            "scripts/agents/security_agent.py", 
            "scripts/agents/monitoring_agent.py"
        ]
    
    def start_agents(self):
        """Start all background agents."""
        print("🚀 Starting background agents...")
        
        for agent in self.agents:
            try:
                print(f"Starting {agent}...")
                process = subprocess.Popen([sys.executable, agent])
                self.processes[agent] = process
                print(f"✅ {agent} started (PID: {process.pid})")
            except Exception as e:
                print(f"❌ Failed to start {agent}: {e}")
    
    def stop_agents(self):
        """Stop all background agents."""
        print("🛑 Stopping background agents...")
        
        for agent, process in self.processes.items():
            try:
                print(f"Stopping {agent}...")
                process.terminate()
                process.wait(timeout=10)
                print(f"✅ {agent} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️ Force killing {agent}")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping {agent}: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\n🛑 Received shutdown signal...")
        self.stop_agents()
        sys.exit(0)
    
    def run(self):
        """Main manager loop."""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            self.start_agents()
            
            print("✅ All agents started successfully!")
            print("Press Ctrl+C to stop all agents")
            
            # Keep running
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received...")
            self.stop_agents()

if __name__ == "__main__":
    manager = AgentManager()
    manager.run()
