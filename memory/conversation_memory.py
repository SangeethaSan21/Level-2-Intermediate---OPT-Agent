"""
Conversation Memory - Tracks the state of the OPT discovery process

This is simpler than Level 1's vector memory - just tracks conversation state
"""

class ConversationMemory:
    def __init__(self):
        """
        Initialize conversation state
        
        State tracks:
        - Current phase (discovery, analysis, masterplan, code, deployment)
        - Information collected (operating model, process, task)
        - Conversation history (all messages)
        """
        self.state = {
            # What phase are we in?
            'phase': 'discovery',  # discovery → analysis → masterplan → code → deployment
            
            # Operating Model (O)
            'operating_model': {
                'business_type': None,      # e.g., "bakery"
                'business_size': None,      # e.g., "2 employees"
                'tools_used': None,         # e.g., "Excel, email"
                'pain_points': None,        # e.g., "manual inventory"
                'completed': False
            },
            
            # Process (P)
            'process': {
                'name': None,               # e.g., "inventory management"
                'description': None,        # e.g., "daily counting of ingredients"
                'frequency': None,          # e.g., "daily"
                'time_spent': None,         # e.g., "30 minutes"
                'completed': False
            },
            
            # Task (T)
            'task': {
                'name': None,               # e.g., "email suppliers when low stock"
                'description': None,        # detailed description
                'inputs': None,             # e.g., "inventory CSV"
                'outputs': None,            # e.g., "email to supplier"
                'completed': False
            },
            
            # Analysis results
            'suggestions': [],              # List of automation suggestions
            'chosen_task': None,            # Which suggestion user chose
            
            # Generated outputs
            'masterplan': None,             # The automation plan
            'code': None,                   # Generated Python code
            'deployment_guide': None,       # How to deploy
            
            # Conversation history
            'messages': []                  # All user/agent messages
        }
    
    def add_message(self, role: str, content: str):
        """
        Add a message to conversation history
        
        Args:
            role: 'user' or 'agent'
            content: The message text
        """
        self.state['messages'].append({
            'role': role,
            'content': content
        })
    
    def update_operating_model(self, key: str, value: str):
        """Update a field in operating model"""
        self.state['operating_model'][key] = value
        print(f"✅ Updated Operating Model: {key} = {value}")
    
    def update_process(self, key: str, value: str):
        """Update a field in process"""
        self.state['process'][key] = value
        print(f"✅ Updated Process: {key} = {value}")
    
    def update_task(self, key: str, value: str):
        """Update a field in task"""
        self.state['task'][key] = value
        print(f"✅ Updated Task: {key} = {value}")
    
    def mark_phase_complete(self, phase: str):
        """Mark a discovery phase as complete"""
        if phase == 'operating_model':
            self.state['operating_model']['completed'] = True
        elif phase == 'process':
            self.state['process']['completed'] = True
        elif phase == 'task':
            self.state['task']['completed'] = True
        print(f"✅ Phase '{phase}' completed!")
    
    def transition_phase(self, new_phase: str):
        """
        Move to next phase
        
        Args:
            new_phase: One of: analysis, masterplan, code, deployment, done
        """
        old_phase = self.state['phase']
        self.state['phase'] = new_phase
        print(f"🔄 Phase transition: {old_phase} → {new_phase}")
    
    def is_discovery_complete(self) -> bool:
        """Check if all OPT discovery is complete"""
        return (
            self.state['operating_model']['completed'] and
            self.state['process']['completed'] and
            self.state['task']['completed']
        )
    
    def get_phase(self) -> str:
        """Get current phase"""
        return self.state['phase']
    
    def get_summary(self) -> str:
        """
        Get a summary of everything collected
        
        Returns:
            Human-readable summary
        """
        summary = "📋 DISCOVERY SUMMARY:\n\n"
        
        # Operating Model
        summary += "🏢 OPERATING MODEL:\n"
        om = self.state['operating_model']
        if om['business_type']:
            summary += f"  - Business: {om['business_type']}\n"
        if om['business_size']:
            summary += f"  - Size: {om['business_size']}\n"
        if om['tools_used']:
            summary += f"  - Tools: {om['tools_used']}\n"
        if om['pain_points']:
            summary += f"  - Pain Points: {om['pain_points']}\n"
        
        # Process
        summary += "\n⚙️ PROCESS:\n"
        p = self.state['process']
        if p['name']:
            summary += f"  - Name: {p['name']}\n"
        if p['description']:
            summary += f"  - Description: {p['description']}\n"
        if p['frequency']:
            summary += f"  - Frequency: {p['frequency']}\n"
        if p['time_spent']:
            summary += f"  - Time Spent: {p['time_spent']}\n"
        
        # Task
        summary += "\n✅ TASK:\n"
        t = self.state['task']
        if t['name']:
            summary += f"  - Name: {t['name']}\n"
        if t['description']:
            summary += f"  - Description: {t['description']}\n"
        if t['inputs']:
            summary += f"  - Inputs: {t['inputs']}\n"
        if t['outputs']:
            summary += f"  - Outputs: {t['outputs']}\n"
        
        return summary
    
    def get_state(self) -> dict:
        """Get the entire state (for debugging or saving)"""
        return self.state


# Test the memory
if __name__ == "__main__":
    print("Testing Conversation Memory...\n")
    
    memory = ConversationMemory()
    
    # Simulate discovery
    print("=== Operating Model ===")
    memory.add_message('user', 'I run a small bakery')
    memory.update_operating_model('business_type', 'Bakery')
    memory.update_operating_model('business_size', '2 employees')
    memory.update_operating_model('tools_used', 'Excel, Email')
    memory.mark_phase_complete('operating_model')
    
    print("\n=== Process ===")
    memory.add_message('user', 'I spend time tracking inventory daily')
    memory.update_process('name', 'Inventory Tracking')
    memory.update_process('frequency', 'Daily')
    memory.update_process('time_spent', '30 minutes')
    memory.mark_phase_complete('process')
    
    print("\n=== Task ===")
    memory.add_message('user', 'Email suppliers when stock is low')
    memory.update_task('name', 'Low Stock Email Alerts')
    memory.update_task('description', 'Check inventory and email suppliers')
    memory.mark_phase_complete('task')
    
    print("\n" + "="*60)
    print(memory.get_summary())
    print("="*60)
    
    print(f"\nDiscovery complete: {memory.is_discovery_complete()}")
    print(f"Current phase: {memory.get_phase()}")