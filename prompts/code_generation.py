"""
Code Generation Prompts - Python Script Creation
"""

CODE_GENERATION_SYSTEM_PROMPT = "You are an expert Python developer creating automation scripts for non-technical users."

def get_code_generation_prompt(automation: dict, masterplan: str, task: dict) -> str:
    """Generate prompt for creating Python automation code"""
    return f"""You are an expert Python developer creating automation scripts for non-technical users.

AUTOMATION TASK:
================
Name: {automation.get('name')}
Description: {automation.get('description')}

Task Details:
- Inputs: {task.get('inputs')}
- Outputs: {task.get('outputs')}
- Description: {task.get('description')}

Implementation Approach: {automation.get('implementation')}

MASTERPLAN CONTEXT:
===================
{masterplan[:1500]}...

YOUR TASK:
Generate a COMPLETE, WORKING Python script that automates this task.

REQUIREMENTS:
- Beginner-friendly code with clear comments
- Production-ready with error handling
- Well-structured with configuration section
- Complete documentation in docstring
- Use standard libraries when possible

RESPOND WITH ONLY THE PYTHON CODE.
"""

DEPLOYMENT_GUIDE_TEMPLATE = """
# 🚀 DEPLOYMENT GUIDE
## {automation_name}

Step-by-step instructions for setting up and running your automation.
"""