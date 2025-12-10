"""
Automated Supplier Emailer
Checks the Excel file for low stock levels and automatically sends emails to suppliers.

Author: AI-Automation-Agent
Created: 2024-09-16

WHAT THIS SCRIPT DOES:
- Reads the Excel file for inventory levels
- Checks for low stock levels based on a threshold value
- Sends automated emails to suppliers for low stock levels

SETUP INSTRUCTIONS:
1. Install Python 3.9+
2. Install dependencies: pip install -r requirements.txt
3. Create a .env file with required variables (see CONFIGURATION section)
4. Run: python automated_supplier_emailer.py

REQUIREMENTS:
- Python 3.9+
- python-dotenv
- pandas
- smtplib

ENVIRONMENT VARIABLES (.env file):
Create a .env file in the same directory with:
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
INPUT_FILE=data.xlsx
THRESHOLD_VALUE=10
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SUPPLIER_EMAILS=supplier1@example.com,supplier2@example.com
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SUPPLIER_EMAILS=supplier1@example.com,supplier2@example.com
#
# The script will load these automatically from the .env file

# Load from environment variables (secure)
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
INPUT_FILE_PATH = os.getenv('INPUT_FILE', 'data.xlsx')
THRESHOLD_VALUE = int(os.getenv('THRESHOLD_VALUE', '10'))
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SUPPLIER_EMAILS = os.getenv('SUPPLIER_EMAILS', 'supplier1@example.com,supplier2@example.com').split(',')

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
    if not EMAIL_SENDER:
        missing.append('EMAIL_SENDER')
    if not EMAIL_PASSWORD:
        missing.append('EMAIL_PASSWORD')
    if not INPUT_FILE_PATH:
        missing.append('INPUT_FILE')
    if not THRESHOLD_VALUE:
        missing.append('THRESHOLD_VALUE')
    if not SMTP_SERVER:
        missing.append('SMTP_SERVER')
    if not SMTP_PORT:
        missing.append('SMTP_PORT')
    if not SUPPLIER_EMAILS:
        missing.append('SUPPLIER_EMAILS')
    
    if missing:
        print(" Configuration Error: Missing required environment variables")
        print("Missing variables:")
        for var in missing:
            print(f"   - {var}")
        print(" To fix this:")
        print("   1. Create a file named '.env' in this directory")
        print("   2. Add these lines to the .env file:")
        for var in missing:
            print(f"      {var}=your_value_here")
        print("   3. Save the file and run the script again")
        print(" Note: Never commit .env file to git! Add it to .gitignore")
        sys.exit(1)

# Run validation immediately
validate_configuration()

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def read_excel_file(file_path):
    """
    Reads the Excel file for inventory levels
    
    Args:
        file_path (str): Path to the Excel file
    
    Returns:
        pandas.DataFrame: Inventory levels
    """
    try:
        # Read the Excel file
        inventory_levels = pd.read_excel(file_path)
        return inventory_levels
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        sys.exit(1)

def check_low_stock_levels(inventory_levels, threshold_value):
    """
    Checks for low stock levels based on a threshold value
    
    Args:
        inventory_levels (pandas.DataFrame): Inventory levels
        threshold_value (int): Threshold value
    
    Returns:
        list: List of low stock levels
    """
    low_stock_levels = []
    for index, row in inventory_levels.iterrows():
        if row['Quantity'] < threshold_value:
            low_stock_levels.append(row)
    return low_stock_levels

def send_email(subject, message, from_addr, to_addr, password, smtp_server, smtp_port):
    """
    Sends an email using the specified parameters
    
    Args:
        subject (str): Email subject
        message (str): Email message
        from_addr (str): From email address
        to_addr (str): To email address
        password (str): Password for the from email address
        smtp_server (str): SMTP server
        smtp_port (int): SMTP port
    """
    try:
        # Create a message
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        
        # Set up the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_addr, password)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print(" Starting Automated Supplier Emailer...")
    print("="*60)
    
    try:
        # Read the Excel file
        inventory_levels = read_excel_file(INPUT_FILE_PATH)
        print("Inventory levels read successfully.")
        
        # Check for low stock levels
        low_stock_levels = check_low_stock_levels(inventory_levels, THRESHOLD_VALUE)
        print(f"Found {len(low_stock_levels)} low stock levels.")
        
        # Send emails to suppliers
        for supplier_email in SUPPLIER_EMAILS:
            subject = "Low Stock Levels"
            message = "Please replenish the following items: \n"
            for low_stock_level in low_stock_levels:
                message += f"{low_stock_level['Item']}: {low_stock_level['Quantity']}\n"
            send_email(subject, message, EMAIL_SENDER, supplier_email, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT)
            print(f"Email sent to {supplier_email} successfully.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please check the error message and try again.")
        sys.exit(1)
    
    print("Automated Supplier Emailer completed successfully!")