"""
Masterplan Tool - Generates Detailed Automation Plans

Creates comprehensive blueprint for implementing the chosen automation
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class MasterplanTool:
    def __init__(self):
        """Initialize the masterplan tool with LLM"""
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
        print("📋 Masterplan Tool initialized")
    
    def generate_masterplan(self, chosen_suggestion: dict, memory_state: dict) -> str:
        """
        Generate a comprehensive automation masterplan
        
        Args:
            chosen_suggestion: The automation the user chose
            memory_state: Full OPT context from discovery
            
        Returns:
            Detailed masterplan as markdown string
        """
        # Extract context
        om = memory_state['operating_model']
        p = memory_state['process']
        t = memory_state['task']
        
        # Build masterplan generation prompt
        prompt = f"""You are an automation architect creating a detailed implementation plan.

BUSINESS CONTEXT:
==================
Business: {om.get('business_type')} ({om.get('business_size')})
Current Tools: {om.get('tools_used')}
Process: {p.get('name')} - {p.get('description')}
Frequency: {p.get('frequency')}
Time Spent: {p.get('time_spent')}

CHOSEN AUTOMATION:
==================
Name: {chosen_suggestion.get('name')}
Description: {chosen_suggestion.get('description')}
Time Saved: {chosen_suggestion.get('time_saved')}
Money Saved: {chosen_suggestion.get('money_saved')}
Complexity: {chosen_suggestion.get('complexity')}
Impact: {chosen_suggestion.get('impact')}

Task Details:
- Inputs: {t.get('inputs')}
- Outputs: {t.get('outputs')}
- Description: {t.get('description')}

YOUR TASK:
Create a comprehensive, actionable masterplan in Markdown format.

REQUIRED SECTIONS:

# 🎯 AUTOMATION MASTERPLAN
## [Automation Name]

### 📊 Executive Summary
[2-3 sentences: what this does, why it matters, value delivered]

### 🔄 Current Workflow (BEFORE Automation)
[Step-by-step breakdown of manual process]
1. [Step 1]
2. [Step 2]
...
⏱️ Time: [total time]
💰 Cost: [labor cost]
😫 Pain Points: [frustrations]

### ✨ Automated Workflow (AFTER Automation)
[Step-by-step breakdown of automated process]
1. [Step 1]
2. [Step 2]
...
⏱️ Time: [reduced time]
💰 Cost: [reduced cost]
🎉 Benefits: [improvements]

### 🛠️ Technical Requirements
**Software:**
- Python 3.9+
- [Required libraries]

**Data/Files:**
- [Input files needed]
- [File formats]

**Credentials/Access:**
- [Any API keys, passwords needed]

**System:**
- [OS requirements]
- [Scheduling tool if needed]

### 📝 Implementation Steps
**Phase 1: Setup (15-30 minutes)**
1. [Setup step 1]
2. [Setup step 2]

**Phase 2: Configuration (30-45 minutes)**
1. [Config step 1]
2. [Config step 2]

**Phase 3: Testing (15-30 minutes)**
1. [Test step 1]
2. [Test step 2]

**Phase 4: Deployment (15 minutes)**
1. [Deploy step 1]
2. [Deploy step 2]

Total Setup Time: [X hours]

### 🎯 Expected Outcomes
**Time Savings:**
- Daily: [X minutes]
- Weekly: [X hours]
- Monthly: [X hours]
- Yearly: [X hours]

**Cost Savings:**
- Monthly: $[X]
- Yearly: $[Y]

**Quality Improvements:**
- [Benefit 1]
- [Benefit 2]

**ROI:**
- Payback Period: [time to break even]
- First Year Savings: $[amount]

### 📈 Success Metrics
How to measure if automation is working:
- [Metric 1]: [Target]
- [Metric 2]: [Target]
- [Metric 3]: [Target]

### ⚠️ Considerations & Risks
**Potential Issues:**
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

**Maintenance:**
- [What needs monitoring]
- [How often to review]

### 🚀 Next Steps
1. [Immediate next action]
2. [Second action]
3. [Third action]

IMPORTANT:
- Be specific and actionable
- Use real numbers and estimates
- Make it beginner-friendly
- Focus on Python-based automation
- Keep technical requirements realistic
- Show clear value proposition

Generate the complete masterplan now:"""

        try:
            response = self.groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=3000  # Allow longer response for detailed plan
            )
            
            masterplan = response.choices[0].message.content.strip()
            
            print(f"✅ Generated masterplan ({len(masterplan)} chars)")
            return masterplan
            
        except Exception as e:
            print(f"❌ Masterplan generation error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Fallback: Create basic masterplan
            return self._create_fallback_masterplan(chosen_suggestion, t)
    
    def _create_fallback_masterplan(self, suggestion: dict, task: dict) -> str:
        """Create a basic masterplan if LLM fails"""
        return f"""# 🎯 AUTOMATION MASTERPLAN
## {suggestion.get('name', 'Task Automation')}

### 📊 Executive Summary
{suggestion.get('description', 'Automate the specified task')}

Estimated value: {suggestion.get('time_saved', 'significant time')} saved, 
{suggestion.get('money_saved', '$200/month')} in cost savings.

### 🔄 Current Workflow (BEFORE)
1. Manual execution of: {task.get('name', 'task')}
2. Time consuming and repetitive
3. Prone to human error

⏱️ Time: {task.get('time_spent', '30 minutes')}

### ✨ Automated Workflow (AFTER)
1. Script runs automatically
2. Processes {task.get('inputs', 'data')}
3. Generates {task.get('outputs', 'results')}

⏱️ Time: Automated (no manual time needed)

### 🛠️ Technical Requirements
- Python 3.9+
- Required libraries (will be specified in code)
- Access to {task.get('inputs', 'input data')}

### 📝 Implementation Steps
1. Install Python and dependencies
2. Configure automation script
3. Test with sample data
4. Deploy and schedule

### 🎯 Expected Outcomes
- Time Saved: {suggestion.get('time_saved', '30 minutes/day')}
- Cost Saved: {suggestion.get('money_saved', '$200/month')}
- Improved accuracy and consistency

### 🚀 Next Steps
1. Review this plan
2. Proceed to code generation
3. Test the automation
4. Deploy to production
"""
    
    def save_masterplan(self, masterplan: str, filename: str = "masterplan.md") -> str:
        """
        Save masterplan to file
        
        Args:
            masterplan: The generated masterplan
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        import os
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        filepath = os.path.join("output", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(masterplan)
        
        print(f"💾 Masterplan saved to: {filepath}")
        return filepath


# Test the masterplan tool
if __name__ == "__main__":
    from memory.conversation_memory import ConversationMemory
    
    print("="*60)
    print("TESTING MASTERPLAN TOOL")
    print("="*60 + "\n")
    
    # Create sample data
    memory = ConversationMemory()
    
    # Populate with bakery example
    memory.update_operating_model('business_type', 'Bakery')
    memory.update_operating_model('business_size', '2 employees')
    memory.update_operating_model('tools_used', 'Excel, Gmail')
    memory.mark_phase_complete('operating_model')
    
    memory.update_process('name', 'Inventory Management')
    memory.update_process('description', 'Daily inventory counting and tracking')
    memory.update_process('frequency', 'Daily')
    memory.update_process('time_spent', '30-45 minutes')
    memory.mark_phase_complete('process')
    
    memory.update_task('name', 'Email suppliers for low stock')
    memory.update_task('description', 'Check Excel, identify low items, email suppliers')
    memory.update_task('inputs', 'Excel file with inventory counts')
    memory.update_task('outputs', 'Email to supplier with order details')
    memory.mark_phase_complete('task')
    
    # Sample chosen suggestion
    chosen_suggestion = {
        "rank": 1,
        "name": "Automated Low Stock Email Alerts",
        "description": "Automatically monitor inventory levels and send email alerts to suppliers when stock falls below threshold",
        "time_saved": "25 minutes/day",
        "money_saved": "$200/month",
        "complexity": "Easy",
        "impact": "High",
        "value_score": 90,
        "implementation": "Python script with pandas for Excel reading and smtplib for email",
        "why_this_rank": "Direct user request, high impact, low complexity"
    }
    
    # Generate masterplan
    print("📋 Generating comprehensive masterplan...\n")
    masterplan_tool = MasterplanTool()
    masterplan = masterplan_tool.generate_masterplan(chosen_suggestion, memory.get_state())
    
    # Display masterplan
    print("\n" + "="*60)
    print("GENERATED MASTERPLAN")
    print("="*60 + "\n")
    print(masterplan)
    
    # Save to file
    print("\n" + "="*60)
    filepath = masterplan_tool.save_masterplan(masterplan, "bakery_inventory_masterplan.md")
    print(f"✅ Masterplan saved to: {filepath}")