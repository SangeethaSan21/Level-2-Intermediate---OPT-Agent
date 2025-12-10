"""
Discovery Tool - Conducts OPT Framework Interview

This tool asks questions to understand:
- O: Operating Model (the business)
- P: Process (the workflow)
- T: Task (the specific automation target)
"""

import os
import json
import sys

# FIX: Add parent directory to path FIRST
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# NOW import local modules
from groq import Groq
from dotenv import load_dotenv
from memory.conversation_memory import ConversationMemory  # ← Now Python can find it!

load_dotenv()


class DiscoveryTool:
    def __init__(self):
        """Initialize the discovery tool with LLM"""
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
        print("🔍 Discovery Tool initialized")
    
    def get_next_question(self, memory_state: dict) -> str:
        """
        Determine what to ask next based on what we know
        
        Args:
            memory_state: Current conversation state from memory
            
        Returns:
            Next question to ask
        """
        # Check Operating Model
        om = memory_state['operating_model']
        if not om.get('business_type'):
            return "Let's start! What kind of business do you run? Tell me about it."
        
        if not om.get('business_size'):
            return "How many people work in your business? What's the team size?"
        
        if not om.get('tools_used'):
            return "What tools or systems do you currently use to run your business? (e.g., Excel, email, specific software)"
        
        if not om.get('pain_points'):
            return "What are the biggest time-consuming or frustrating parts of running your business?"
        
        # Check Process
        p = memory_state['process']
        if not p.get('name'):
            return "Let's focus on one specific workflow. What's a repetitive process that takes a lot of your time?"
        
        if not p.get('description'):
            return f"Can you describe the '{p['name']}' process in more detail? What are the steps involved?"
        
        if not p.get('frequency'):
            return f"How often do you do this '{p['name']}' process? (daily, weekly, monthly?)"
        
        if not p.get('time_spent'):
            return f"Roughly how much time does '{p['name']}' take each time you do it?"
        
        # Check Task
        t = memory_state['task']
        if not t.get('name'):
            return f"Within the '{p['name']}' process, what's the most specific, repetitive task we could automate?"
        
        if not t.get('description'):
            return f"Can you describe exactly what happens in '{t['name']}'? What are the inputs and outputs?"
        
        if not t.get('inputs'):
            return f"What information or data do you need to perform '{t['name']}'? (e.g., files, emails, databases)"
        
        if not t.get('outputs'):
            return f"What's the result or output of '{t['name']}'? (e.g., email sent, file created, data updated)"
        
        # All info collected!
        return None
    
    def extract_information(self, user_message: str, memory_state: dict) -> dict:
        """
        Use LLM to extract structured information from user's response
        
        Args:
            user_message: What the user said
            memory_state: Current state to understand context
            
        Returns:
            dict with extracted info: {'field': 'value', ...}
        """
        # Determine what we're trying to extract
        om = memory_state['operating_model']
        p = memory_state['process']
        t = memory_state['task']
        
        # Build context for LLM
        context = "Extract information from the user's message.\n\n"
        
        if not om.get('business_type'):
            context += "We're asking about: BUSINESS TYPE\n"
            context += "Extract: type of business (e.g., 'bakery', 'consulting firm', 'online store')\n"
        elif not om.get('business_size'):
            context += "We're asking about: BUSINESS SIZE\n"
            context += "Extract: team size (e.g., '2 employees', 'solo', '10 people')\n"
        elif not om.get('tools_used'):
            context += "We're asking about: TOOLS USED\n"
            context += "Extract: tools/software (e.g., 'Excel, Gmail', 'Salesforce', 'manual processes')\n"
        elif not om.get('pain_points'):
            context += "We're asking about: PAIN POINTS\n"
            context += "Extract: frustrations or time-consuming tasks\n"
        elif not p.get('name'):
            context += "We're asking about: PROCESS NAME\n"
            context += "Extract: the name of a repetitive workflow\n"
        elif not p.get('description'):
            context += "We're asking about: PROCESS DESCRIPTION\n"
            context += "Extract: detailed description of the process\n"
        elif not p.get('frequency'):
            context += "We're asking about: PROCESS FREQUENCY\n"
            context += "Extract: how often (e.g., 'daily', 'weekly', '3 times per week')\n"
        elif not p.get('time_spent'):
            context += "We're asking about: TIME SPENT\n"
            context += "Extract: duration (e.g., '30 minutes', '2 hours', '15 min')\n"
        elif not t.get('name'):
            context += "We're asking about: SPECIFIC TASK NAME\n"
            context += "Extract: specific automatable task within the process\n"
        elif not t.get('description'):
            context += "We're asking about: TASK DESCRIPTION\n"
            context += "Extract: detailed description of the task\n"
        elif not t.get('inputs'):
            context += "We're asking about: TASK INPUTS\n"
            context += "Extract: data sources or inputs needed\n"
        elif not t.get('outputs'):
            context += "We're asking about: TASK OUTPUTS\n"
            context += "Extract: results or outputs produced\n"
        
        prompt = f"""{context}

User's message: "{user_message}"

Extract the requested information and respond with ONLY a JSON object:
{{
  "extracted_value": "the extracted information here",
  "confidence": "high/medium/low"
}}

Be concise and extract only the key information."""

        try:
            response = self.groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.3
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            result = json.loads(response_text.strip())
            return result
            
        except Exception as e:
            print(f"⚠️ Extraction error: {str(e)}")
            # Fallback: just return the user's message
            return {
                "extracted_value": user_message,
                "confidence": "low"
            }
    
    def update_memory_with_extraction(self, extraction: dict, memory):
        """
        Update memory with extracted information
        
        Args:
            extraction: Result from extract_information()
            memory: ConversationMemory instance
        """
        value = extraction.get('extracted_value', '')
        state = memory.get_state()
        
        om = state['operating_model']
        p = state['process']
        t = state['task']
        
        # Figure out what field to update
        if not om.get('business_type'):
            memory.update_operating_model('business_type', value)
        elif not om.get('business_size'):
            memory.update_operating_model('business_size', value)
        elif not om.get('tools_used'):
            memory.update_operating_model('tools_used', value)
        elif not om.get('pain_points'):
            memory.update_operating_model('pain_points', value)
            memory.mark_phase_complete('operating_model')
            print("✅ Operating Model Complete!\n")
        elif not p.get('name'):
            memory.update_process('name', value)
        elif not p.get('description'):
            memory.update_process('description', value)
        elif not p.get('frequency'):
            memory.update_process('frequency', value)
        elif not p.get('time_spent'):
            memory.update_process('time_spent', value)
            memory.mark_phase_complete('process')
            print("✅ Process Complete!\n")
        elif not t.get('name'):
            memory.update_task('name', value)
        elif not t.get('description'):
            memory.update_task('description', value)
        elif not t.get('inputs'):
            memory.update_task('inputs', value)
        elif not t.get('outputs'):
            memory.update_task('outputs', value)
            memory.mark_phase_complete('task')
            print("✅ Task Complete! Discovery phase done!\n")
  

    def is_complete(self, memory_state: dict) -> bool:
        """
        Check if discovery is complete - STRICTER VERSION
        
        Returns:
            True only if ALL OPT fields are filled AND marked complete
        """
        om = memory_state['operating_model']
        p = memory_state['process']
        t = memory_state['task']
        
        # Check Operating Model - ALL fields required
        om_complete = (
            om.get('business_type') and 
            om.get('business_size') and 
            om.get('tools_used') and 
            om.get('pain_points') and
            om.get('completed', False)
        )
        
        # Check Process - ALL fields required
        p_complete = (
            p.get('name') and 
            p.get('description') and 
            p.get('frequency') and 
            p.get('time_spent') and
            p.get('completed', False)
        )
        
        # Check Task - ALL fields required
        t_complete = (
            t.get('name') and 
            t.get('description') and 
            t.get('inputs') and 
            t.get('outputs') and
            t.get('completed', False)
        )
        
        # Log completion status for debugging
        if not om_complete:
            print(f"⚠️ Operating Model incomplete: {[k for k, v in om.items() if not v and k != 'completed']}")
        if not p_complete:
            print(f"⚠️ Process incomplete: {[k for k, v in p.items() if not v and k != 'completed']}")
        if not t_complete:
            print(f"⚠️ Task incomplete: {[k for k, v in t.items() if not v and k != 'completed']}")
        
        return om_complete and p_complete and t_complete

# Test the discovery tool
if __name__ == "__main__":
    
    
    print("="*60)
    print("TESTING DISCOVERY TOOL")
    print("="*60 + "\n")
    
    # Initialize
    memory = ConversationMemory()
    discovery = DiscoveryTool()
    
    # Simulate conversation
    test_responses = [
        "I run a small bakery shop",
        "Just me and one assistant, so 2 people total",
        "We use Excel for tracking and Gmail for communication",
        "The biggest pain is manually tracking inventory every single day",
        "The inventory tracking process - checking what we have",
        "I walk around, count ingredients, write on paper, then update Excel",
        "Every single day, takes forever",
        "About 30-45 minutes each time",
        "The most annoying part is emailing suppliers when we're running low",
        "I check the Excel sheet, see what's low, then manually email each supplier",
        "The Excel file with current inventory counts",
        "An email sent to the supplier with the order"
    ]
    
    print("🤖 Starting OPT Interview...\n")
    
    for i, user_response in enumerate(test_responses, 1):
        # Get next question
        question = discovery.get_next_question(memory.get_state())
        
        if question is None:
            print("\n✅ Discovery Complete!")
            break
        
        print(f"\n{'='*60}")
        print(f"Question {i}:")
        print(f"Agent: {question}")
        print(f"User: {user_response}")
        
        # Extract info
        extraction = discovery.extract_information(user_response, memory.get_state())
        print(f"Extracted: {extraction['extracted_value']} (confidence: {extraction['confidence']})")
        
        # Update memory
        discovery.update_memory_with_extraction(extraction, memory)
    
    # Show final summary
    print("\n" + "="*60)
    print("FINAL DISCOVERY SUMMARY")
    print("="*60)
    print(memory.get_summary())
    
    print(f"\nDiscovery Complete: {discovery.is_complete(memory.get_state())}")