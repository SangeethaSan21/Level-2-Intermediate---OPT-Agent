"""
Task Analysis Prompts - Automation Suggestion Generation
"""

def get_analysis_prompt(operating_model: dict, process: dict, task: dict) -> str:
    """Generate prompt for analyzing business and suggesting automations"""
    return f"""You are an automation consultant analyzing a business to suggest automations.

BUSINESS CONTEXT:
====================
Operating Model:
- Business Type: {operating_model.get('business_type', 'Unknown')}
- Team Size: {operating_model.get('business_size', 'Unknown')}
- Current Tools: {operating_model.get('tools_used', 'Unknown')}
- Pain Points: {operating_model.get('pain_points', 'Unknown')}

Process Being Analyzed:
- Name: {process.get('name', 'Unknown')}
- Description: {process.get('description', 'Unknown')}
- Frequency: {process.get('frequency', 'Unknown')}
- Time Spent: {process.get('time_spent', 'Unknown')}

Specific Task Mentioned:
- Name: {task.get('name', 'Unknown')}
- Description: {task.get('description', 'Unknown')}
- Inputs: {task.get('inputs', 'Unknown')}
- Outputs: {task.get('outputs', 'Unknown')}

YOUR TASK:
Generate 3 automation suggestions ranked by value (impact vs complexity).

For EACH suggestion, provide:
1. Name (concise, descriptive)
2. Description (2-3 sentences explaining what it does)
3. Time Saved (estimated)
4. Money Saved (estimated)
5. Complexity (Easy/Medium/Hard)
6. Impact (Low/Medium/High)
7. Value Score (0-100)
8. Implementation Summary
9. Why This Rank

RESPOND WITH ONLY VALID JSON.
"""

SUGGESTION_DISPLAY_TEMPLATE = """
🎯 AUTOMATION SUGGESTIONS

Based on your business, here are 3 automation opportunities ranked by value:
"""