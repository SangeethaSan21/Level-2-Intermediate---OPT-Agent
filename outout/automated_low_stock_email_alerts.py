"""
Automated Low Stock Email Alerts
Monitor inventory and email suppliers when stock is low

Author: AI-Automation-Agent
Created: 2024-03-16

WHAT THIS SCRIPT DOES:
- Reads an Excel file with inventory data
- Checks inventory levels and identifies items below threshold
- Sends email alerts to suppliers for low stock items

SETUP INSTRUCTIONS:
1. Install Python 3.9+ and required libraries (pandas, smtplib)
2. Create an Excel file with inventory data (columns: item_name, quantity, supplier_email)
3. Configure the script with your email settings and inventory file path

USAGE:
python automated_low_stock_email_alerts.py

REQUIREMENTS:
- Python 3.9+
- pandas
- smtplib
- openpyxl (for reading Excel files)

TROUBLESHOOTING TIPS:
- Check the Excel file path and format
- Verify email settings and credentials
- Check the threshold value and adjust as needed
"""

import os
import sys
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ============================================================================
# CONFIGURATION - Edit these values for your setup
# ============================================================================
# Inventory file path and name
INVENTORY_FILE_PATH = "inventory.xlsx"

# Email settings
EMAIL_SENDER = "sangeethadayanand621@gmail.com.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_SMTP_SERVER = "smtp.example.com"
EMAIL_SMTP_PORT = 587

# Threshold value for low stock (items with quantity below this value will trigger an alert)
LOW_STOCK_THRESHOLD = 5

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def read_inventory_file(file_path):
    """
    Reads the inventory Excel file and returns a pandas DataFrame
    
    Args:
        file_path (str): Path to the inventory Excel file
    
    Returns:
        pandas.DataFrame: Inventory data
    """
    try:
        # Read the Excel file using pandas
        inventory_data = pd.read_excel(file_path)
        return inventory_data
    
    except Exception as e:
        print(f"❌ Error reading inventory file: {str(e)}")
        sys.exit(1)

def check_low_stock(inventory_data):
    """
    Checks the inventory data and identifies items below the low stock threshold
    
    Args:
        inventory_data (pandas.DataFrame): Inventory data
    
    Returns:
        pandas.DataFrame: Low stock items
    """
    # Filter the inventory data to get items with quantity below the threshold
    low_stock_items = inventory_data[inventory_data["quantity"] < LOW_STOCK_THRESHOLD]
    return low_stock_items

def send_email_alerts(low_stock_items):
    """
    Sends email alerts to suppliers for low stock items
    
    Args:
        low_stock_items (pandas.DataFrame): Low stock items
    """
    # Set up the email server
    server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    
    # Iterate over the low stock items and send an email alert for each item
    for index, row in low_stock_items.iterrows():
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = row["supplier_email"]
        msg["Subject"] = f"Low Stock Alert: {row['item_name']}"
        body = f"Item {row['item_name']} is running low (quantity: {row['quantity']}). Please restock as soon as possible."
        msg.attach(MIMEText(body, "plain"))
        
        # Send the email
        try:
            server.sendmail(EMAIL_SENDER, row["supplier_email"], msg.as_string())
            print(f"✅ Email alert sent to {row['supplier_email']} for item {row['item_name']}")
        
        except Exception as e:
            print(f"❌ Error sending email alert: {str(e)}")
    
    # Close the email server
    server.quit()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting Automated Low Stock Email Alerts...")
    print("="*60)
    
    try:
        # Read the inventory file
        inventory_data = read_inventory_file(INVENTORY_FILE_PATH)
        print(f"✅ Inventory file read successfully: {INVENTORY_FILE_PATH}")
        
        # Check for low stock items
        low_stock_items = check_low_stock(inventory_data)
        print(f"✅ Low stock items identified: {len(low_stock_items)}")
        
        # Send email alerts for low stock items
        send_email_alerts(low_stock_items)
        print(f"✅ Email alerts sent for low stock items")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("   Please check the setup instructions and troubleshooting tips.")
        sys.exit(1)
    
    print("✅ Automation completed successfully!")