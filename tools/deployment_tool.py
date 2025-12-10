"""
Deployment Tool - Creates Setup and Deployment Instructions

Generates beginner-friendly guide for installing and running the automation
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class DeploymentTool:
    def __init__(self):
        """Initialize the deployment tool with LLM"""
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
        print("🚀 Deployment Tool initialized")
    
    def generate_deployment_guide(self, code_data: dict, chosen_suggestion: dict, memory_state: dict) -> str:
        """
        Generate comprehensive deployment instructions
        
        Args:
            code_data: Generated code info (filename, requirements, code)
            chosen_suggestion: The automation details
            memory_state: Business context
            
        Returns:
            Deployment guide as markdown string
        """
        filename = code_data.get('filename', 'automation.py')
        requirements = code_data.get('requirements', [])
        code = code_data.get('code', '')
        
        # Extract configuration from code
        config_vars = self._extract_config_variables(code)
        
        # Build deployment guide prompt
        prompt = f"""You are a technical writer creating deployment instructions for non-technical users.

AUTOMATION DETAILS:
===================
Script Name: {filename}
Automation: {chosen_suggestion.get('name')}
Description: {chosen_suggestion.get('description')}
Complexity: {chosen_suggestion.get('complexity')}

Required Libraries: {', '.join(requirements) if requirements else 'None (uses standard library)'}

Configuration Variables Found:
{chr(10).join(f"- {var}" for var in config_vars) if config_vars else "- None found"}

Business Context:
- Business Type: {memory_state['operating_model'].get('business_type')}
- Current Tools: {memory_state['operating_model'].get('tools_used')}

YOUR TASK:
==========
Create a COMPLETE deployment guide that a non-technical person can follow.

REQUIRED SECTIONS:

# 🚀 DEPLOYMENT GUIDE
## {chosen_suggestion.get('name')}

### 📋 Prerequisites
**Before you start, you'll need:**
- [ ] A computer (Windows, Mac, or Linux)
- [ ] Internet connection
- [ ] 30 minutes of time
- [ ] [Any specific files or accounts needed]

**Estimated Setup Time:** [X minutes]

---

### ✅ Step 1: Install Python (5-10 minutes)

**What is Python?**
[Brief 1-sentence explanation]

**Installation Instructions:**

**For Windows:**
1. Go to python.org/downloads
2. Download Python 3.9 or newer
3. Run the installer
4. ⚠️ IMPORTANT: Check "Add Python to PATH"
5. Click "Install Now"
6. Verify: Open Command Prompt, type `python --version`

**For Mac:**
1. Open Terminal
2. Install Homebrew (if not installed): [command]
3. Run: `brew install python3`
4. Verify: `python3 --version`

**For Linux:**
1. Open Terminal
2. Run: `sudo apt-get update && sudo apt-get install python3`
3. Verify: `python3 --version`

---

### 📦 Step 2: Install Required Libraries ({len(requirements)} libraries)

**What are libraries?**
[Brief 1-sentence explanation]

**Installation Command:**
```bash
pip install {' '.join(requirements) if requirements else '# No libraries needed!'}
```

**Copy the command above and paste it in your terminal/command prompt.**

**Verification:**
```bash
python -c "import {requirements[0] if requirements else 'sys'}; print('✅ Libraries installed!')"
```

If you see "✅ Libraries installed!" - you're good to go!

---

### ⚙️ Step 3: Configure the Script (5-10 minutes)

**What needs configuration?**

Open `{filename}` in a text editor (Notepad, TextEdit, VS Code, etc.)

Find the **CONFIGURATION** section (near the top) and edit these values:

{chr(10).join(f'''
**{var}:**
- Current value: [placeholder]
- What to change it to: [specific instruction]
- Example: [example value]
''' for var in config_vars[:5]) if config_vars else "No configuration needed - script is ready to use!"}

**Important Notes:**
- Keep quotation marks around text values
- Use forward slashes (/) in file paths (even on Windows)
- Don't delete any lines, only change the values

---

### 🧪 Step 4: Test the Automation (5 minutes)

**Before running automatically, let's test it manually:**

1. Open terminal/command prompt
2. Navigate to script folder:
   ```bash
   cd path/to/folder
   ```
3. Run the script:
   ```bash
   python {filename}
   ```

**What to expect:**
- [Expected output 1]
- [Expected output 2]
- ✅ "Automation completed successfully!" message

**If you see errors:** Jump to Troubleshooting section below

---

### ⏰ Step 5: Schedule Automatic Execution (10 minutes)

**Make it run automatically every [frequency]:**

**For Windows (Task Scheduler):**
1. Open Task Scheduler
2. Click "Create Basic Task"
3. Name: "{chosen_suggestion.get('name')}"
4. Trigger: [Daily/Weekly/etc.]
5. Action: Start a Program
6. Program: `python`
7. Arguments: `{filename}`
8. Start in: [folder path]
9. Finish and test

**For Mac (Launchd):**
1. Create file: `~/Library/LaunchAgents/com.automation.plist`
2. [Detailed plist configuration]
3. Load: `launchctl load ~/Library/LaunchAgents/com.automation.plist`

**For Linux (Cron):**
1. Edit crontab: `crontab -e`
2. Add line: `0 8 * * * cd /path/to/script && python {filename}`
3. Save and exit

---

### 🐛 Troubleshooting

**Problem: "python is not recognized"**
- Solution: Python not in PATH. Reinstall and check "Add to PATH"

**Problem: "ModuleNotFoundError"**
- Solution: Library not installed. Run `pip install [library-name]`

**Problem: "FileNotFoundError"**
- Solution: Check file paths in configuration are correct

**Problem: "Permission Denied"**
- Solution: Run with administrator/sudo privileges

**Problem: "SMTP Authentication Failed"**
- Solution: Use app-specific password, enable "Less Secure Apps"

[Add 3-5 more common issues based on the automation type]

---

### ✅ Success Checklist

After deployment, you should have:
- [ ] Python installed and working
- [ ] Libraries installed successfully
- [ ] Script configured with your values
- [ ] Manual test completed successfully
- [ ] Automation scheduled (if applicable)
- [ ] First automated run verified

---

### 📞 Getting Help

**If you're stuck:**
1. Check the error message carefully
2. Review the Troubleshooting section
3. Google the specific error message
4. Check script comments for hints

**Common resources:**
- Python documentation: docs.python.org
- Stack Overflow: stackoverflow.com
- [Specific library documentation]

---

### 🎉 Congratulations!

Your automation is now deployed and running!

**What happens next:**
- [What the automation will do]
- [When it will run]
- [Where to find outputs]

**Monitoring:**
- Check [log file/output] regularly
- Verify [expected results] are happening
- Adjust thresholds/settings as needed

IMPORTANT:
- Write in simple, clear language (8th-grade level)
- Use emojis for visual clarity
- Provide OS-specific instructions
- Include copy-paste commands
- Anticipate common errors
- Be encouraging and supportive

Generate the complete deployment guide now:"""

        try:
            response = self.groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=3000
            )
            
            guide = response.choices[0].message.content.strip()
            
            print(f"✅ Generated deployment guide ({len(guide)} chars)")
            return guide
            
        except Exception as e:
            print(f"❌ Deployment guide generation error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Fallback: Create basic guide
            return self._create_fallback_guide(filename, requirements, chosen_suggestion)
    
    def _extract_config_variables(self, code: str) -> list:
        """Extract configuration variable names from code"""
        config_vars = []
        in_config = False
        
        for line in code.splitlines():
            # Detect configuration section
            if 'CONFIGURATION' in line.upper() and '#' in line:
                in_config = True
                continue
            
            # Exit configuration section
            if in_config and ('def ' in line or 'class ' in line or '# =====' in line):
                break
            
            # Extract variable assignments
            if in_config and '=' in line and not line.strip().startswith('#'):
                var_name = line.split('=')[0].strip()
                if var_name.isupper():  # Configuration constants are usually UPPERCASE
                    config_vars.append(var_name)
        
        return config_vars
    
    def _create_fallback_guide(self, filename: str, requirements: list, suggestion: dict) -> str:
        """Create a basic deployment guide if LLM fails"""
        return f"""# 🚀 DEPLOYMENT GUIDE
## {suggestion.get('name', 'Automation')}

### 📋 Prerequisites
- Python 3.9 or higher
- Text editor
- 30 minutes setup time

### ✅ Step 1: Install Python
Visit python.org/downloads and install Python 3.9+

### 📦 Step 2: Install Libraries
```bash
pip install {' '.join(requirements) if requirements else '# No additional libraries needed'}
```

### ⚙️ Step 3: Configure Script
1. Open `{filename}` in a text editor
2. Find the CONFIGURATION section
3. Edit the values for your setup
4. Save the file

### 🧪 Step 4: Test
```bash
python {filename}
```

### ⏰ Step 5: Schedule (Optional)
Set up Task Scheduler (Windows) or cron (Mac/Linux) to run automatically.

### 🐛 Troubleshooting
- Check Python is installed: `python --version`
- Check libraries installed: `pip list`
- Read error messages carefully

### 🎉 You're Done!
Your automation is ready to use.
"""
    
    def save_deployment_guide(self, guide: str, filename: str = "DEPLOYMENT.md") -> str:
        """
        Save deployment guide to file
        
        Args:
            guide: The generated guide
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        import os
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        filepath = os.path.join("output", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"💾 Deployment guide saved to: {filepath}")
        return filepath


# Test the deployment tool
if __name__ == "__main__":
    from memory.conversation_memory import ConversationMemory
    
    print("="*60)
    print("TESTING DEPLOYMENT TOOL")
    print("="*60 + "\n")
    
    # Sample data
    code_data = {
        'filename': 'automated_low_stock_email_alerts.py',
        'requirements': ['pandas', 'openpyxl'],
        'code': '''
# CONFIGURATION
INVENTORY_FILE = "inventory.xlsx"
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-password"
LOW_STOCK_THRESHOLD = 10
'''
    }
    
    chosen_suggestion = {
        'name': 'Automated Low Stock Email Alerts',
        'description': 'Monitor inventory and email suppliers when stock is low',
        'complexity': 'Easy'
    }
    
    memory = ConversationMemory()
    memory.update_operating_model('business_type', 'Bakery')
    memory.update_operating_model('tools_used', 'Excel, Gmail')
    
    # Generate deployment guide
    print("🚀 Generating deployment guide...\n")
    deployment = DeploymentTool()
    guide = deployment.generate_deployment_guide(code_data, chosen_suggestion, memory.get_state())
    
    # Display guide preview
    print("\n" + "="*60)
    print("DEPLOYMENT GUIDE PREVIEW")
    print("="*60 + "\n")
    lines = guide.splitlines()
    for line in lines[:80]:  # Show first 80 lines
        print(line)
    
    if len(lines) > 80:
        print(f"\n... ({len(lines) - 80} more lines) ...")
    
    # Save to file
    print("\n" + "="*60)
    filepath = deployment.save_deployment_guide(guide)
    print(f"✅ Deployment guide saved to: {filepath}")