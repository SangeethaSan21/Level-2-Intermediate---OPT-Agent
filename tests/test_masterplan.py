"""
Test Masterplan Tool
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.masterplan_tool import MasterplanTool
from memory.conversation_memory import ConversationMemory


def test_masterplan_generation():
    """Test that masterplan tool generates a plan"""
    print("\n" + "="*60)
    print("TEST: Masterplan Generation")
    print("="*60 + "\n")
    
    memory = ConversationMemory()
    memory.update_operating_model('business_type', 'Bakery')
    memory.update_process('name', 'Inventory')
    memory.update_task('name', 'Email alerts')
    
    masterplan_tool = MasterplanTool()
    
    suggestion = {
        'name': 'Test Automation',
        'description': 'Test automation description',
        'time_saved': '30 min/day',
        'complexity': 'Easy'
    }
    
    try:
        masterplan = masterplan_tool.generate_masterplan(suggestion, memory.get_state())
        
        assert masterplan is not None
        assert len(masterplan) > 100
        assert 'Automation' in masterplan or 'MASTERPLAN' in masterplan
        
        print(f"✅ Masterplan generated ({len(masterplan)} characters)")
        print(f"✅ Contains expected sections")
        
        print("\n✅ Masterplan generation test PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ Masterplan generation failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🧪 RUNNING MASTERPLAN TOOL TESTS\n")
    
    if test_masterplan_generation():
        print("="*60)
        print("🎉 MASTERPLAN TESTS PASSED!")
        print("="*60 + "\n")
    else:
        print("❌ TESTS FAILED\n")
        sys.exit(1)