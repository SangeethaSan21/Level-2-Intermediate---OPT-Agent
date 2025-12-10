"""
OPT Agent Core - Main Conversation Orchestrator

Manages the entire automation discovery and generation workflow
"""

import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.conversation_memory import ConversationMemory
from tools.discovery_tool import DiscoveryTool
from tools.analysis_tool import AnalysisTool
from tools.masterplan_tool import MasterplanTool
from tools.code_gen_tool import CodeGenTool
from tools.deployment_tool import DeploymentTool


class OPTAgent:
    def __init__(self):
        """Initialize the OPT Agent with all tools"""
        print("\n" + "="*60)
        print("🤖 INITIALIZING OPT AUTOMATION AGENT")
        print("="*60 + "\n")
        
        # Initialize memory
        self.memory = ConversationMemory()
        
        # Initialize all tools
        self.discovery = DiscoveryTool()
        self.analysis = AnalysisTool()
        self.masterplan = MasterplanTool()
        self.codegen = CodeGenTool()
        self.deployment = DeploymentTool()
        
        # Track current phase
        self.current_phase = 'discovery'
        
        print("\n✅ Agent ready! Let's find automation opportunities!\n")
    
    def chat(self, user_message: str) -> str:
        """
        Main conversation handler
        
        Args:
            user_message: What the user said
            
        Returns:
            Agent's response
        """
        # Add user message to memory
        self.memory.add_message('user', user_message)
        
        # Get current state
        state = self.memory.get_state()
        current_phase = state['phase']
        
        print(f"\n{'─'*60}")
        print(f"📍 Phase: {current_phase.upper()}")
        print(f"{'─'*60}\n")
        
        # Route to appropriate handler based on phase
        if current_phase == 'discovery':
            response = self._handle_discovery(user_message)
        
        elif current_phase == 'analysis':
            response = self._handle_analysis(user_message)
        
        elif current_phase == 'masterplan':
            response = self._handle_masterplan()
        
        elif current_phase == 'code':
            response = self._handle_code_generation()
        
        elif current_phase == 'deployment':
            response = self._handle_deployment()
        
        elif current_phase == 'done':
            response = self._handle_done()
        
        else:
            response = "🤔 Hmm, I seem to be in an unknown state. Let's start over!"
            self.memory.transition_phase('discovery')
        
        # Add agent response to memory
        self.memory.add_message('agent', response)
        
        return response
    
    def _handle_discovery(self, user_message: str) -> str:
        """
        Handle discovery phase - collect OPT information
        """
        state = self.memory.get_state()
        
        # If this is the first message, start with welcome
        if len(state['messages']) <= 2:
            return self._welcome_message()
        
        # Extract information from user's response
        extraction = self.discovery.extract_information(user_message, state)
        self.discovery.update_memory_with_extraction(extraction, self.memory)
        
        # Check if discovery is complete
        if self.discovery.is_complete(state):
            print("\n" + "="*60)
            print("✅ DISCOVERY COMPLETE!")
            print("="*60)
            print(self.memory.get_summary())
            print("="*60 + "\n")
            
            # Transition to analysis
            self.memory.transition_phase('analysis')
            
            return self._start_analysis()
        
        # Ask next question
        next_question = self.discovery.get_next_question(state)
        return next_question
    
    def _handle_analysis(self, user_message: str) -> str:
        """
        Handle analysis phase - suggest automations
        """
        state = self.memory.get_state()
        
        # If we haven't generated suggestions yet, generate them
        if not state.get('suggestions'):
            print("🔬 Analyzing your business and generating suggestions...\n")
            suggestions = self.analysis.analyze_and_suggest(state)
            state['suggestions'] = suggestions
            
            # Display suggestions
            display = self.analysis.display_suggestions(suggestions)
            return display
        
        # User is choosing a suggestion
        suggestions = state['suggestions']
        chosen = self.analysis.get_chosen_suggestion(suggestions, user_message)
        state['chosen_task'] = chosen
        
        print(f"\n✅ User chose: {chosen.get('name')}\n")
        
        # Transition to masterplan
        self.memory.transition_phase('masterplan')
        
        return "Perfect choice! 🎯 Let me create a comprehensive masterplan for you...\n\n⏳ Generating detailed automation plan..."
    
    def _handle_masterplan(self) -> str:
        """
        Handle masterplan phase - generate detailed plan
        """
        state = self.memory.get_state()
        chosen_task = state.get('chosen_task')
        
        if not chosen_task:
            return "❌ Error: No task selected. Please choose a task first."
        
        # Generate masterplan
        print("📋 Generating masterplan...\n")
        masterplan = self.masterplan.generate_masterplan(chosen_task, state)
        state['masterplan'] = masterplan
        
        # Save masterplan
        self.masterplan.save_masterplan(masterplan)
        
        # Transition to code generation
        self.memory.transition_phase('code')
        
        response = f"""
✅ Masterplan Complete!

{masterplan}

{'='*60}

Great! Now let me write the Python code for you...

⏳ Generating automation script...
"""
        return response
    
    def _handle_code_generation(self) -> str:
        """
        Handle code generation phase - write Python script
        """
        state = self.memory.get_state()
        chosen_task = state.get('chosen_task')
        masterplan = state.get('masterplan')
        task = state['task']
        
        # Generate code
        print("💻 Generating Python code...\n")
        code_data = self.codegen.generate_code(chosen_task, masterplan, task)
        state['code'] = code_data
        
        # Save code
        self.codegen.save_code(code_data)
        
        # Transition to deployment
        self.memory.transition_phase('deployment')
        
        # Show code preview
        code_lines = code_data['code'].splitlines()
        preview = '\n'.join(code_lines[:30])
        
        response = f"""
✅ Code Generated!

📁 Filename: {code_data['filename']}
📦 Requirements: {', '.join(code_data['requirements']) if code_data['requirements'] else 'None (uses standard library)'}
📊 Lines of Code: {len(code_lines)}

Code Preview (first 30 lines):
{'─'*60}
{preview}
{'─'*60}

... ({len(code_lines) - 30} more lines)

💾 Full code saved to: output/{code_data['filename']}

{'='*60}

Perfect! Now let me create the deployment guide...

⏳ Generating setup instructions...
"""
        return response
    
    def _handle_deployment(self) -> str:
        """
        Handle deployment phase - create setup guide
        """
        state = self.memory.get_state()
        chosen_task = state.get('chosen_task')
        code_data = state.get('code')
        
        # Generate deployment guide
        print("🚀 Generating deployment guide...\n")
        guide = self.deployment.generate_deployment_guide(code_data, chosen_task, state)
        state['deployment_guide'] = guide
        
        # Save guide
        self.deployment.save_deployment_guide(guide)
        
        # Transition to done
        self.memory.transition_phase('done')
        
        response = f"""
✅ Deployment Guide Complete!

{guide}

{'='*60}

🎉 CONGRATULATIONS! Your automation is ready!

📦 DELIVERABLES:
   ✅ Masterplan: output/masterplan.md
   ✅ Python Code: output/{code_data['filename']}
   ✅ Requirements: output/requirements.txt
   ✅ Setup Guide: output/DEPLOYMENT.md

🚀 NEXT STEPS:
   1. Open the deployment guide
   2. Follow the step-by-step instructions
   3. Test your automation
   4. Schedule it to run automatically

💰 EXPECTED VALUE:
   - Time Saved: {chosen_task.get('time_saved', 'Significant')}
   - Money Saved: {chosen_task.get('money_saved', 'Considerable')}
   - Impact: {chosen_task.get('impact', 'High')} 🔥

Need help with anything else? Just ask!
"""
        return response
    
    def _handle_done(self) -> str:
        """
        Handle done phase - conversation complete
        """
        return """
✅ Your automation project is complete!

All files are in the output/ folder. 

Would you like to:
1. Create another automation?
2. Get help with deployment?
3. Exit?

(Or just say what you need!)
"""
    
    def _welcome_message(self) -> str:
        """Initial welcome message"""
        return """
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
    
    def _start_analysis(self) -> str:
        """Transition message from discovery to analysis"""
        return """
🎉 Excellent! I have everything I need.

Now let me analyze your business and identify automation opportunities...

⏳ Analyzing processes and generating suggestions...

(This will take about 30 seconds)
"""
    
    def save_session(self, filename: str = "session.json") -> str:
        """
        Save the entire conversation session
        
        Args:
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        import json
        
        os.makedirs("output", exist_ok=True)
        filepath = os.path.join("output", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.memory.get_state(), f, indent=2)
        
        print(f"💾 Session saved to: {filepath}")
        return filepath


# Test the agent
if __name__ == "__main__":
    print("\n" + "🎯"*30)
    print("TESTING OPT AGENT")
    print("🎯"*30 + "\n")
    
    agent = OPTAgent()
    
    # Simulate a conversation
    test_conversation = [
        "Hi!",
        "I run a small bakery",
        "Just 2 people - me and my assistant",
        "We use Excel and Gmail mostly",
        "The biggest pain is tracking inventory every single day",
        "The inventory tracking process",
        "I walk around, count everything, write it on paper, then update Excel",
        "Every single day",
        "Takes about 30-45 minutes",
        "Emailing suppliers when we're running low on items",
        "I check the Excel, see what's low, then email each supplier manually",
        "The Excel file with current stock levels",
        "An email to the supplier with what we need",
        "1",  # Choose first suggestion
    ]
    
    print("🤖 Starting conversation simulation...\n")
    
    for i, user_msg in enumerate(test_conversation, 1):
        print(f"\n{'='*60}")
        print(f"MESSAGE {i}")
        print(f"{'='*60}")
        print(f"👤 User: {user_msg}")
        print()
        
        response = agent.chat(user_msg)
        print(f"🤖 Agent: {response[:500]}...")  # Show first 500 chars
        
        if len(response) > 500:
            print(f"\n... (response continues, {len(response)} total chars)")
        
        # Stop after masterplan to avoid long output
        if agent.memory.get_state()['phase'] == 'done':
            break
        
        input("\n⏸️  Press Enter for next message...")
    
    # Save session
    print("\n" + "="*60)
    agent.save_session("bakery_automation_session.json")
    print("✅ Test complete!")