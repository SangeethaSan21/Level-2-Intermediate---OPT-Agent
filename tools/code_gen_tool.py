"""
Code Generation Tool - Creates Working Python Scripts

Generates beginner-friendly, production-ready Python code from masterplan
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class CodeGenTool:
    def __init__(self):
        """Initialize the code generation tool with LLM"""
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
        print("💻 Code Generation Tool initialized")
    
    def generate_code(self, chosen_suggestion: dict, masterplan: str, task: dict) -> dict:
        """
        Generate complete Python automation script
        
        Args:
            chosen_suggestion: The chosen automation
            masterplan: The generated masterplan
            task: Task details from memory
            
        Returns:
            dict with 'code', 'filename', 'requirements'
        """
        # Build code generation prompt
        prompt = f'''You are an expert Python developer creating automation scripts for non-technical users.

AUTOMATION TASK:
================
Name: {chosen_suggestion.get('name')}
Description: {chosen_suggestion.get('description')}

Task Details:
- Inputs: {task.get('inputs')}
- Outputs: {task.get('outputs')}
- Description: {task.get('description')}

Implementation Approach: {chosen_suggestion.get('implementation')}

MASTERPLAN CONTEXT:
===================
{masterplan[:1500]}...

YOUR TASK:
==========
Generate a COMPLETE, WORKING Python script that automates this task.

REQUIREMENTS:
=============
1. **Beginner-Friendly Code:**
   - Clear variable names (no single letters)
   - Extensive comments explaining each section
   - Simple, readable logic (no complex comprehensions)
   - Print statements showing progress

2. **Production-Ready:**
   - Error handling (try/except blocks)
   - Input validation
   - Clear error messages
   - Graceful failures

3. **Well-Structured:**
   - Configuration via environment variables (.env file)
   - Main logic in functions
   - if __name__ == "__main__" guard
   - Docstrings for functions

4. **Complete Documentation:**
   - File header with description
   - Setup instructions including .env file
   - Usage examples
   - Required file formats
   - Troubleshooting tips

5. **Realistic Implementation:**
   - Use standard libraries when possible
   - Common libraries: pandas, smtplib, os, datetime, python-dotenv
   - No external services requiring paid APIs
   - File-based operations (CSV/Excel/TXT)

6. **SECURITY REQUIREMENTS:**
   - NEVER hardcode passwords, API keys, or email credentials
   - ALWAYS use os.getenv() for sensitive data
   - ALWAYS include load_dotenv() from python-dotenv
   - ALWAYS include validate_configuration() function
   - ALWAYS document required .env variables in comments

CODE STRUCTURE:
===============
```python
"""
[Script Name]
[Brief description]

Author: AI-Automation-Agent
Created: [Date]

WHAT THIS SCRIPT DOES:
- [Key function 1]
- [Key function 2]
- [Key function 3]

SETUP INSTRUCTIONS:
1. Install Python 3.9+
2. Install dependencies: pip install -r requirements.txt
3. Create a .env file with required variables (see CONFIGURATION section)
4. Run: python script_name.py

REQUIREMENTS:
- Python 3.9+
- python-dotenv
- [Library 1]
- [Library 2]

ENVIRONMENT VARIABLES (.env file):
Create a .env file in the same directory with:
VARIABLE_NAME=value
ANOTHER_VARIABLE=value
(See CONFIGURATION section for details)
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
# [Other imports]

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION - Edit .env file, NOT this code!
# ============================================================================
#
# SECURITY: Never hardcode sensitive information like passwords, API keys, or emails!
# Create a .env file in the same directory with these variables:
#
# Example .env file:
# ------------------
# EMAIL_SENDER=your_email@gmail.com
# EMAIL_PASSWORD=your_app_specific_password
# INPUT_FILE=data.xlsx
# THRESHOLD_VALUE=10
#
# The script will load these automatically from the .env file

# Load from environment variables (secure)
# Replace these with actual variable names based on the automation

# For email-based automations:
# EMAIL_SENDER = os.getenv('EMAIL_SENDER')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
# EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
# EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))

# For file-based automations:
# INPUT_FILE_PATH = os.getenv('INPUT_FILE_PATH', 'input.xlsx')
# OUTPUT_FILE_PATH = os.getenv('OUTPUT_FILE_PATH', 'output.xlsx')

# For threshold-based automations:
# THRESHOLD_VALUE = int(os.getenv('THRESHOLD_VALUE', '10'))

[Configuration variables using os.getenv() with clear comments]

# ============================================================================
# VALIDATION - Check required variables exist
# ============================================================================

def validate_configuration():
    """
    Validate that all required environment variables are set
    
    Exits with helpful error message if any are missing
    """
    missing = []
    
    # Check each required variable
    # Add checks based on what the automation needs
    # Example:
    # if not EMAIL_SENDER:
    #     missing.append('EMAIL_SENDER')
    # if not EMAIL_PASSWORD:
    #     missing.append('EMAIL_PASSWORD')
    
    if missing:
        print("❌ Configuration Error: Missing required environment variables")
        print("\nMissing variables:")
        for var in missing:
            print(f"   - {{var}}")
        print("\n📝 To fix this:")
        print("   1. Create a file named '.env' in this directory")
        print("   2. Add these lines to the .env file:")
        for var in missing:
            print(f"      {{var}}=your_value_here")
        print("\n   3. Save the file and run the script again")
        print("\n⚠️  Note: Never commit .env file to git! Add it to .gitignore")
        sys.exit(1)

# Run validation immediately
validate_configuration()

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def function_name():
    """
    Clear docstring explaining what this does
    
    Returns:
        Description of return value
    """
    # Implementation with comments
    pass

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting [Automation Name]...")
    print("="*60)
    
    try:
        # Main logic here
        pass
        
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("   [Helpful troubleshooting message]")
        sys.exit(1)
    
    print("\n✅ Automation completed successfully!")
```

CRITICAL SECURITY REQUIREMENTS:
- NEVER use hardcoded credentials (EMAIL_PASSWORD, API_KEYS, etc.)
- ALWAYS use os.getenv() for sensitive data
- ALWAYS include validate_configuration() function
- ALWAYS add python-dotenv to imports and requirements
- ALWAYS include clear .env file example in comments
- For Gmail: Instruct users to use App Passwords, not regular passwords

Generate the complete Python script now:'''

        try:
            response = self.groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.5,  # Lower temp for more reliable code
                max_tokens=3000
            )
            
            code = response.choices[0].message.content.strip()
            
            # Extract code from markdown if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            # Generate filename
            filename = self._generate_filename(chosen_suggestion.get('name'))
            
            # Extract requirements
            requirements = self._extract_requirements(code)
            
            print(f"✅ Generated code ({len(code)} chars, {len(code.splitlines())} lines)")
            
            return {
                'code': code,
                'filename': filename,
                'requirements': requirements
            }
            
        except Exception as e:
            print(f"❌ Code generation error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Fallback: Create basic template
            return self._create_fallback_code(chosen_suggestion, task)
    
    def _generate_filename(self, automation_name: str) -> str:
        """Generate a Python filename from automation name"""
        # Convert to snake_case
        filename = automation_name.lower()
        filename = filename.replace(' ', '_')
        filename = ''.join(c for c in filename if c.isalnum() or c == '_')
        return f"{filename}.py"
    
    def _extract_requirements(self, code: str) -> list:
        """Extract required libraries from import statements"""
        requirements = []
        
        # Common library mappings
        lib_mapping = {
            'pandas': 'pandas',
            'openpyxl': 'openpyxl',
            'xlrd': 'xlrd',
            'requests': 'requests',
            'flask': 'flask',
            'numpy': 'numpy',
            'bs4': 'beautifulsoup4',
            'cv2': 'opencv-python',
            'dotenv': 'python-dotenv',  # Added for environment variables
        }
        
        for line in code.splitlines():
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                for lib, pip_name in lib_mapping.items():
                    if lib in line:
                        if pip_name not in requirements:
                            requirements.append(pip_name)
        
        # ALWAYS include python-dotenv if we're using environment variables
        if 'load_dotenv' in code and 'python-dotenv' not in requirements:
            requirements.append('python-dotenv')
        
        return requirements
    
    def _create_fallback_code(self, suggestion: dict, task: dict) -> dict:
        """Create a basic code template if LLM fails"""
        code = f'''"""
{suggestion.get('name', 'Automation Script')}

This script automates: {task.get('name', 'the specified task')}

SETUP:
1. Install Python 3.9+
2. Install requirements: pip install -r requirements.txt
3. Create a .env file with required variables
4. Run: python automation_script.py

ENVIRONMENT VARIABLES (.env file):
INPUT_FILE=input.txt
OUTPUT_FILE=output.txt
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION - Uses .env file
# ============================================================================
INPUT_FILE = os.getenv('INPUT_FILE', 'input.txt')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'output.txt')

# ============================================================================
# VALIDATION
# ============================================================================

def validate_configuration():
    """Validate required configuration"""
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: Input file not found: {{INPUT_FILE}}")
        print("   Please check your .env file")
        sys.exit(1)

validate_configuration()

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Main automation logic
    """
    print("🚀 Starting automation...")
    print(f"📄 Input: {{INPUT_FILE}}")
    
    try:
        # TODO: Add automation logic here
        print("⚙️  Processing...")
        
        # Example: Read input
        with open(INPUT_FILE, 'r') as f:
            data = f.read()
        
        # Example: Process data
        result = data  # Replace with actual processing
        
        # Example: Write output
        with open(OUTPUT_FILE, 'w') as f:
            f.write(result)
        
        print(f"✅ Complete! Output saved to {{OUTPUT_FILE}}")
        
    except FileNotFoundError:
        print(f"❌ Error: {{INPUT_FILE}} not found")
        print("   Please check the file path in your .env file")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        return {
            'code': code,
            'filename': 'automation_script.py',
            'requirements': ['python-dotenv']  # Always include dotenv
        }
    
    def save_code(self, code_data: dict) -> tuple:
        """
        Save generated code and requirements to files
        
        Args:
            code_data: dict from generate_code()
            
        Returns:
            tuple of (code_path, requirements_path)
        """
        import os
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        # Save Python script
        code_path = os.path.join("output", code_data['filename'])
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(code_data['code'])
        print(f"💾 Code saved to: {code_path}")
        
        # Save requirements.txt
        if code_data['requirements']:
            req_path = os.path.join("output", "requirements.txt")
            with open(req_path, 'w', encoding='utf-8') as f:
                for req in code_data['requirements']:
                    f.write(f"{req}\n")
            print(f"💾 Requirements saved to: {req_path}")
            return (code_path, req_path)
        
        return (code_path, None)


# Test the code generation tool
if __name__ == "__main__":
    print("="*60)
    print("TESTING CODE GENERATION TOOL")
    print("="*60 + "\n")
    
    # Sample data
    chosen_suggestion = {
        "name": "Automated Low Stock Email Alerts",
        "description": "Monitor inventory and email suppliers when stock is low",
        "implementation": "Python with pandas for Excel reading, smtplib for email"
    }
    
    task = {
        "name": "Email suppliers for low stock",
        "description": "Check Excel file, identify items below threshold, send email alerts",
        "inputs": "Excel file with inventory (columns: item_name, quantity, supplier_email)",
        "outputs": "Email alerts to suppliers"
    }
    
    masterplan = """
    # Automation Masterplan
    This automation reads an Excel file daily, checks inventory levels,
    and sends email alerts to suppliers when items fall below threshold.
    Technical: Python 3.9+, pandas, smtplib
    """
    
    # Generate code
    print("💻 Generating Python code...\n")
    codegen = CodeGenTool()
    code_data = codegen.generate_code(chosen_suggestion, masterplan, task)
    
    # Display code preview
    print("\n" + "="*60)
    print("GENERATED CODE PREVIEW")
    print("="*60 + "\n")
    lines = code_data['code'].splitlines()
    for i, line in enumerate(lines[:50], 1):  # Show first 50 lines
        print(f"{i:3d} | {line}")
    
    if len(lines) > 50:
        print(f"\n... ({len(lines) - 50} more lines) ...")
    
    print(f"\n📊 Code Stats:")
    print(f"   - Lines: {len(lines)}")
    print(f"   - Characters: {len(code_data['code'])}")
    print(f"   - Filename: {code_data['filename']}")
    print(f"   - Requirements: {', '.join(code_data['requirements']) if code_data['requirements'] else 'None'}")
    
    # Save to file
    print("\n" + "="*60)
    paths = codegen.save_code(code_data)
    print(f"✅ Files saved:")
    print(f"   - {paths[0]}")
    if paths[1]:
        print(f"   - {paths[1]}")