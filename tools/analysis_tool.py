"""
Analysis Tool - Suggests Automation Opportunities

Takes OPT discovery data and generates 3 ranked automation suggestions
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class AnalysisTool:
    def __init__(self):
        """Initialize the analysis tool with LLM"""
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
        print("🔬 Analysis Tool initialized")
    
    def analyze_and_suggest(self, memory_state: dict) -> list:
        """
        Analyze the business and suggest 3 automation opportunities
        
        Args:
            memory_state: Complete OPT data from discovery
            
        Returns:
            List of 3 automation suggestions with scoring
        """
        # Extract OPT data
        om = memory_state['operating_model']
        p = memory_state['process']
        t = memory_state['task']
        
        # Build analysis prompt
        prompt = f"""You are an automation consultant analyzing a business to suggest automations.

BUSINESS CONTEXT:
====================
Operating Model:
- Business Type: {om.get('business_type', 'Unknown')}
- Team Size: {om.get('business_size', 'Unknown')}
- Current Tools: {om.get('tools_used', 'Unknown')}
- Pain Points: {om.get('pain_points', 'Unknown')}

Process Being Analyzed:
- Name: {p.get('name', 'Unknown')}
- Description: {p.get('description', 'Unknown')}
- Frequency: {p.get('frequency', 'Unknown')}
- Time Spent: {p.get('time_spent', 'Unknown')}

Specific Task Mentioned:
- Name: {t.get('name', 'Unknown')}
- Description: {t.get('description', 'Unknown')}
- Inputs: {t.get('inputs', 'Unknown')}
- Outputs: {t.get('outputs', 'Unknown')}

YOUR TASK:
Generate 3 automation suggestions ranked by value (impact vs complexity).

For EACH suggestion, provide:
1. Name (concise, descriptive)
2. Description (2-3 sentences explaining what it does)
3. Time Saved (estimated, e.g., "25 minutes/day" or "2 hours/week")
4. Complexity (Easy/Medium/Hard)
5. Impact (Low/Medium/High - based on time saved + pain reduction)
6. Implementation Summary (1 sentence on how it would work technically)

RESPOND WITH ONLY VALID JSON:
{{
  "suggestions": [
    {{
      "rank": 1,
      "name": "Automation Name",
      "description": "What it does and why it helps",
      "time_saved": "X minutes/day",
      "money_saved": "$X/month (estimated)",
      "complexity": "Easy/Medium/Hard",
      "impact": "Low/Medium/High",
      "value_score": 85,
      "implementation": "Brief technical approach",
      "why_this_rank": "Why this is ranked #1"
    }},
    {{
      "rank": 2,
      ...
    }},
    {{
      "rank": 3,
      ...
    }}
  ]
}}

Guidelines:
- Rank #1 should be the mentioned task (highest priority for user)
- Rank #2 and #3 should be related opportunities in the same process
- Easy + High Impact = highest value_score
- Be realistic about time/money savings
- Focus on Python-automatable tasks (not requiring complex infrastructure)
"""

        try:
            response = self.groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            result = json.loads(response_text.strip())
            suggestions = result.get('suggestions', [])
            
            print(f"✅ Generated {len(suggestions)} automation suggestions")
            return suggestions
            
        except Exception as e:
            print(f"❌ Analysis error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Fallback: Create basic suggestion from task data
            return [{
                "rank": 1,
                "name": t.get('name', 'Task Automation'),
                "description": f"Automate: {t.get('description', 'the described task')}",
                "time_saved": p.get('time_spent', '30 minutes/day'),
                "money_saved": "$200/month (estimated)",
                "complexity": "Medium",
                "impact": "High",
                "value_score": 75,
                "implementation": "Python script with automation logic",
                "why_this_rank": "User's primary request"
            }]
    
    def display_suggestions(self, suggestions: list) -> str:
        """
        Format suggestions for display to user
        
        Args:
            suggestions: List from analyze_and_suggest()
            
        Returns:
            Formatted string for display
        """
        output = "\n" + "="*60 + "\n"
        output += "🎯 AUTOMATION SUGGESTIONS\n"
        output += "="*60 + "\n\n"
        
        for suggestion in suggestions:
            rank = suggestion.get('rank', '?')
            name = suggestion.get('name', 'Unknown')
            description = suggestion.get('description', '')
            time_saved = suggestion.get('time_saved', 'Unknown')
            money_saved = suggestion.get('money_saved', 'Unknown')
            complexity = suggestion.get('complexity', 'Unknown')
            impact = suggestion.get('impact', 'Unknown')
            value_score = suggestion.get('value_score', 0)
            
            # Emoji for rank
            rank_emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            
            # Impact indicator
            impact_indicator = "🔥🔥🔥" if impact == "High" else "🔥🔥" if impact == "Medium" else "🔥"
            
            output += f"{rank_emoji} SUGGESTION #{rank}: {name}\n"
            output += f"{'─'*60}\n"
            output += f"📝 {description}\n\n"
            output += f"⏱️  Time Saved: {time_saved}\n"
            output += f"💰 Money Saved: {money_saved}\n"
            output += f"🔧 Complexity: {complexity}\n"
            output += f"📊 Impact: {impact} {impact_indicator}\n"
            output += f"⭐ Value Score: {value_score}/100\n"
            output += f"\n💡 Implementation: {suggestion.get('implementation', 'N/A')}\n"
            output += f"\n✨ Why This Rank: {suggestion.get('why_this_rank', 'N/A')}\n"
            output += "\n" + "="*60 + "\n\n"
        
        output += "Which automation would you like me to build for you?\n"
        output += "(Reply with 1, 2, or 3)\n"
        
        return output
    
    def get_chosen_suggestion(self, suggestions: list, choice: str) -> dict:
        """
        Get the suggestion the user chose
        
        Args:
            suggestions: List of suggestions
            choice: User's choice ("1", "2", or "3")
            
        Returns:
            The chosen suggestion dict
        """
        try:
            choice_num = int(choice.strip())
            if 1 <= choice_num <= len(suggestions):
                chosen = suggestions[choice_num - 1]
                print(f"✅ User chose: {chosen.get('name')}")
                return chosen
            else:
                print(f"⚠️ Invalid choice: {choice}")
                return suggestions[0]  # Default to first
        except:
            print(f"⚠️ Could not parse choice: {choice}")
            return suggestions[0]  # Default to first


# Test the analysis tool
if __name__ == "__main__":
    from memory.conversation_memory import ConversationMemory
    
    print("="*60)
    print("TESTING ANALYSIS TOOL")
    print("="*60 + "\n")
    
    # Create sample discovery data
    memory = ConversationMemory()
    
    # Populate with bakery example
    memory.update_operating_model('business_type', 'Bakery')
    memory.update_operating_model('business_size', '2 employees')
    memory.update_operating_model('tools_used', 'Excel, Gmail')
    memory.update_operating_model('pain_points', 'Manual inventory tracking daily')
    memory.mark_phase_complete('operating_model')
    
    memory.update_process('name', 'Inventory Management')
    memory.update_process('description', 'Walk around, count ingredients, write on paper, update Excel')
    memory.update_process('frequency', 'Daily')
    memory.update_process('time_spent', '30-45 minutes')
    memory.mark_phase_complete('process')
    
    memory.update_task('name', 'Email suppliers for low stock')
    memory.update_task('description', 'Check Excel, identify low items, manually email each supplier')
    memory.update_task('inputs', 'Excel file with inventory counts')
    memory.update_task('outputs', 'Email to supplier with order details')
    memory.mark_phase_complete('task')
    
    # Run analysis
    print("🔬 Analyzing business and generating suggestions...\n")
    analysis = AnalysisTool()
    suggestions = analysis.analyze_and_suggest(memory.get_state())
    
    # Display suggestions
    print(analysis.display_suggestions(suggestions))
    
    # Test choosing a suggestion
    print("\n" + "="*60)
    print("TESTING CHOICE SELECTION")
    print("="*60)
    chosen = analysis.get_chosen_suggestion(suggestions, "1")
    print(f"\nChosen automation: {chosen.get('name')}")
    print(f"Description: {chosen.get('description')}")