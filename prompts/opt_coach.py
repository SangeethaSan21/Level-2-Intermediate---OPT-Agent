"""
OPT Coach Prompts - Interview Questions and Guidance

Prompts for conducting the OPT Framework discovery interview
"""

# Welcome message
WELCOME_PROMPT = """
👋 Hello! I'm your AI Automation Assistant!

I help small business owners and solopreneurs automate their repetitive work.

🎯 Here's how I work:
1. I'll ask about your business (OPT Framework)
2. I'll suggest 3 automation opportunities
3. You pick one, and I'll create:
   ✅ A detailed masterplan
   ✅ Working Python code
   ✅ Step-by-step setup guide

This takes about 10-15 minutes of conversation.

Let's start! What kind of business do you run? Tell me about it.
"""

# Operating Model Questions
BUSINESS_TYPE_QUESTION = "Let's start! What kind of business do you run? Tell me about it."

BUSINESS_SIZE_QUESTION = "How many people work in your business? What's the team size?"

TOOLS_USED_QUESTION = "What tools or systems do you currently use to run your business? (e.g., Excel, email, specific software)"

PAIN_POINTS_QUESTION = "What are the biggest time-consuming or frustrating parts of running your business?"

# Process Questions
PROCESS_NAME_QUESTION = "Let's focus on one specific workflow. What's a repetitive process that takes a lot of your time?"

def get_process_description_question(process_name: str) -> str:
    return f"Can you describe the '{process_name}' process in more detail? What are the steps involved?"

def get_frequency_question(process_name: str) -> str:
    return f"How often do you do this '{process_name}' process? (daily, weekly, monthly?)"

def get_time_spent_question(process_name: str) -> str:
    return f"Roughly how much time does '{process_name}' take each time you do it?"

# Task Questions
def get_task_name_question(process_name: str) -> str:
    return f"Within the '{process_name}' process, what's the most specific, repetitive task we could automate?"

def get_task_description_question(task_name: str) -> str:
    return f"Can you describe exactly what happens in '{task_name}'? What are the inputs and outputs?"

def get_inputs_question(task_name: str) -> str:
    return f"What information or data do you need to perform '{task_name}'? (e.g., files, emails, databases)"

def get_outputs_question(task_name: str) -> str:
    return f"What's the result or output of '{task_name}'? (e.g., email sent, file created, data updated)"

# Transition Messages
DISCOVERY_COMPLETE_MESSAGE = """
🎉 Excellent! I have everything I need.

Now let me analyze your business and identify automation opportunities...

⏳ Analyzing processes and generating suggestions...

(This will take about 30 seconds)
"""

# Extraction Prompt Template
def get_extraction_prompt(context: str, user_message: str) -> str:
    return f"""{context}

User's message: "{user_message}"

Extract the requested information and respond with ONLY a JSON object:
{{
  "extracted_value": "the extracted information here",
  "confidence": "high/medium/low"
}}

Be concise and extract only the key information."""

# Context Templates
CONTEXT_TEMPLATES = {
    "business_type": """We're asking about: BUSINESS TYPE
Extract: type of business (e.g., 'bakery', 'consulting firm', 'online store')""",
    
    "business_size": """We're asking about: BUSINESS SIZE
Extract: team size (e.g., '2 employees', 'solo', '10 people')""",
    
    "tools_used": """We're asking about: TOOLS USED
Extract: tools/software (e.g., 'Excel, Gmail', 'Salesforce', 'manual processes')""",
    
    "pain_points": """We're asking about: PAIN POINTS
Extract: frustrations or time-consuming tasks""",
    
    "process_name": """We're asking about: PROCESS NAME
Extract: the name of a repetitive workflow""",
    
    "process_description": """We're asking about: PROCESS DESCRIPTION
Extract: detailed description of the process""",
    
    "frequency": """We're asking about: PROCESS FREQUENCY
Extract: how often (e.g., 'daily', 'weekly', '3 times per week')""",
    
    "time_spent": """We're asking about: TIME SPENT
Extract: duration (e.g., '30 minutes', '2 hours', '15 min')""",
    
    "task_name": """We're asking about: SPECIFIC TASK NAME
Extract: specific automatable task within the process""",
    
    "task_description": """We're asking about: TASK DESCRIPTION
Extract: detailed description of the task""",
    
    "inputs": """We're asking about: TASK INPUTS
Extract: data sources or inputs needed""",
    
    "outputs": """We're asking about: TASK OUTPUTS
Extract: results or outputs produced"""
}