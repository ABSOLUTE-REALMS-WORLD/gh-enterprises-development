#!/usr/bin/env python3
"""
Agent Starter Script

This script starts all background agents.
Mentioned in README.md as: python scripts/agents/start-agents.py
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.agents.agent_manager import AgentManager

def main():
    """Main function to start all agents."""
    print("🚀 Starting GH Enterprises Background Agents")
    print("=" * 50)
    
    try:
        manager = AgentManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n🛑 Agent startup interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting agents: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
