# 🚀 DEPLOYMENT GUIDE
## Automated Supplier Emailer

### 📋 Prerequisites
**Before you start, you'll need:**
- [ ] A computer (Windows, Mac, or Linux)
- [ ] Internet connection
- [ ] 30 minutes of time
- [ ] A Gmail account (for automated email sending)
- [ ] The `automated_supplier_emailer.py` script file
- [ ] An Excel file with supplier information

**Estimated Setup Time:** 30 minutes

---

### ✅ Step 1: Install Python (5-10 minutes)

**What is Python?**
Python is a programming language that helps us create automated tasks.

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
2. Install Homebrew (if not installed): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3. Run: `brew install python3`
4. Verify: `python3 --version`

**For Linux:**
1. Open Terminal
2. Run: `sudo apt-get update && sudo apt-get install python3`
3. Verify: `python3 --version`

---

### 📦 Step 2: Install Required Libraries (2 libraries)

**What are libraries?**
Libraries are pre-written code that helps us perform specific tasks.

**Installation Command:**
```bash
pip install python-dotenv pandas
```

**Copy the command above and paste it in your terminal/command prompt.**

**Verification:**
```bash
python -c "import python-dotenv; print('✅ Libraries installed!')"
```

If you see "✅ Libraries installed!" - you're good to go!

---

### ⚙️ Step 3: Configure the Script (5-10 minutes)

**What needs configuration?**

Open `automated_supplier_emailer.py` in a text editor (Notepad, TextEdit, VS Code, etc.)

No configuration needed - script is ready to use!

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
   python automated_supplier_emailer.py
   ```

**What to expect:**
- Emails sent to suppliers with low stock levels
- A success message in the terminal/command prompt
- ✅ "Automation completed successfully!" message

**If you see errors:** Jump to Troubleshooting section below

---

### ⏰ Step 5: Schedule Automatic Execution (10 minutes)

**Make it run automatically every day:**

**For Windows (Task Scheduler):**
1. Open Task Scheduler
2. Click "Create Basic Task"
3. Name: "Automated Supplier Emailer"
4. Trigger: Daily
5. Action: Start a Program
6. Program: `python`
7. Arguments: `automated_supplier_emailer.py`
8. Start in: [folder path]
9. Finish and test

**For Mac (Launchd):**
1. Create file: `~/Library/LaunchAgents/com.automation.plist`
2. Add the following content:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.automation</string>
    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/python</string>
      <string>/path/to/automated_supplier_emailer.py</string>
    </array>
    <key>StartInterval</key>
    <integer>86400</integer>
  </dict>
</plist>
```
3. Load: `launchctl load ~/Library/LaunchAgents/com.automation.plist`

**For Linux (Cron):**
1. Edit crontab: `crontab -e`
2. Add line: `0 8 * * * cd /path/to/script && python automated_supplier_emailer.py`
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

**Problem: "Email not sending"**
- Solution: Check email credentials, internet connection, and email service status

**Problem: "Script not running automatically"**
- Solution: Check scheduled task, cron job, or launchd configuration

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
- pandas documentation: pandas.pydata.org

---

### 🎉 Congratulations!

Your automation is now deployed and running!

**What happens next:**
- The script will check the Excel file for low stock levels every day
- It will send emails to suppliers with low stock levels
- You can monitor the automation by checking the email logs and supplier responses

**Monitoring:**
- Check the email logs regularly
- Verify that emails are being sent to suppliers with low stock levels
- Adjust the script configuration as needed to optimize the automation

Remember, automation is a process, and it may require some fine-tuning to work perfectly. If you have any questions or need further assistance, don't hesitate to reach out. Happy automating! 🚀