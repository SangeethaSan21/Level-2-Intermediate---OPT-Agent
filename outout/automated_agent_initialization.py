"""
Automated Agent Initialization
Initializes the OPTAgent object, saving time by automating the process and reducing the chance of human error.

Author: AI-Automation-Agent
Created: 2023-12-01

WHAT THIS SCRIPT DOES:
- Imports the OPTAgent from agent.core
- Initializes the OPTAgent object
- Prints a line of 60 equals signs as output

SETUP INSTRUCTIONS:
1. Install Python 3.9+
2. Install the agent.core library
3. Save this script as a Python file (e.g., automated_agent_initialization.py)

USAGE:
python automated_agent_initialization.py

REQUIREMENTS:
- Python 3.9+
- agent.core library
"""

import os
import sys
from datetime import datetime
try:
    from agent.core import OPTAgent
except ImportError:
    print("❌ Error: agent.core library not found. Please install the library and try again.")
    sys.exit(1)

# ============================================================================
# CONFIGURATION - Edit these values for your setup
# ============================================================================
# No configuration needed for this script

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================
def initialize_opt_agent():
    """
    Initializes the OPTAgent object.
    
    Returns:
        OPTAgent: The initialized OPTAgent object
    """
    try:
        # Initialize the OPTAgent object
        opt_agent = OPTAgent()
        return opt_agent
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("   Please check the agent.core library installation and try again.")
        sys.exit(1)

def print_output():
    """
    Prints a line of 60 equals signs as output.
    """
    print("="*60)

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("🚀 Starting Automated Agent Initialization...")
    
    try:
        # Initialize the OPTAgent object
        opt_agent = initialize_opt_agent()
        print("✅ OPTAgent object initialized successfully!")
        
        # Print the output
        print_output()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("   Please check the script and try again.")
        sys.exit(1)
    
    print("✅ Automation completed successfully!")