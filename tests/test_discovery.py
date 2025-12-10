"""
Test Discovery Tool
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.discovery_tool import DiscoveryTool
from memory.conversation_memory import ConversationMemory


def test_question_generation():
    """Test that discovery tool generates appropriate questions"""
    print("\n" + "="*60)
    print("TEST: Question Generation")
    print("="*60 + "\n")
    
    memory = ConversationMemory()
    discovery = DiscoveryTool()
    
    # Test first question
    question = discovery.get_next_question(memory.get_state())
    assert question is not None
    assert "business" in question.lower()
    print(f"✅ First question generated: {question[:50]}...")
    
    # Update memory and test next question
    memory.update_operating_model('business_type', 'Bakery')
    question = discovery.get_next_question(memory.get_state())
    assert question is not None
    assert "people" in question.lower() or "team" in question.lower()
    print(f"✅ Second question generated: {question[:50]}...")
    
    print("\n✅ Question generation test PASSED\n")
    return True


def test_information_extraction():
    """Test that discovery tool extracts information correctly"""
    print("\n" + "="*60)
    print("TEST: Information Extraction")
    print("="*60 + "\n")
    
    memory = ConversationMemory()
    discovery = DiscoveryTool()
    
    # Test extraction
    user_msg = "I run a small bakery with 2 employees"
    extraction = discovery.extract_information(user_msg, memory.get_state())
    
    assert 'extracted_value' in extraction
    assert 'confidence' in extraction
    print(f"✅ Extracted: {extraction['extracted_value']}")
    print(f"✅ Confidence: {extraction['confidence']}")
    
    print("\n✅ Information extraction test PASSED\n")
    return True


def test_completion_check():
    """Test that discovery knows when it's complete"""
    print("\n" + "="*60)
    print("TEST: Completion Check")
    print("="*60 + "\n")
    
    memory = ConversationMemory()
    discovery = DiscoveryTool()
    
    # Should not be complete initially
    assert not discovery.is_complete(memory.get_state())
    print("✅ Initial state: Not complete (correct)")
    
    # Mark all phases complete
    memory.mark_phase_complete('operating_model')
    memory.mark_phase_complete('process')
    memory.mark_phase_complete('task')
    
    # Should be complete now
    assert discovery.is_complete(memory.get_state())
    print("✅ After marking complete: Complete (correct)")
    
    print("\n✅ Completion check test PASSED\n")
    return True


if __name__ == "__main__":
    print("\n🧪 RUNNING DISCOVERY TOOL TESTS\n")
    
    try:
        test_question_generation()
        test_information_extraction()
        test_completion_check()
        
        print("="*60)
        print("🎉 ALL DISCOVERY TESTS PASSED!")
        print("="*60 + "\n")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)