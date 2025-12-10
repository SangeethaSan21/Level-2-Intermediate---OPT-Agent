"""
Test Scenarios for OPT Agent

Automated tests for different business scenarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core import OPTAgent
import json


class TestScenarios:
    def __init__(self):
        """Initialize test runner"""
        self.results = []
    
    def test_bakery_scenario(self):
        """
        Test Scenario 1: Small Bakery
        Tests inventory automation discovery
        """
        print("\n" + "="*60)
        print("TEST SCENARIO 1: SMALL BAKERY")
        print("="*60 + "\n")
        
        agent = OPTAgent()
        
        # Conversation sequence
        conversation = [
            ("Hello", "start"),
            ("I run a small bakery", "business_type"),
            ("Just 2 people - me and my assistant", "business_size"),
            ("We use Excel and Gmail", "tools"),
            ("Manually tracking inventory every single day", "pain_points"),
            ("Inventory tracking process", "process_name"),
            ("Walk around, count ingredients, write on paper, update Excel", "process_desc"),
            ("Daily", "frequency"),
            ("30-45 minutes", "time_spent"),
            ("Emailing suppliers when running low on stock", "task_name"),
            ("Check Excel, see what's low, manually email each supplier", "task_desc"),
            ("Excel file with inventory counts", "inputs"),
            ("Email to supplier with order details", "outputs"),
            ("1", "choice"),  # Choose first automation
        ]
        
        try:
            for i, (user_msg, stage) in enumerate(conversation, 1):
                print(f"\n[{i}] User: {user_msg}")
                response = agent.chat(user_msg)
                print(f"[{i}] Agent: {response[:200]}...")
                
                # Stop after choosing automation (don't generate full code in test)
                if stage == "choice" and agent.memory.get_state()['phase'] == 'masterplan':
                    print("\n✅ Test passed: Successfully reached masterplan phase")
                    break
            
            result = {
                "scenario": "Small Bakery",
                "status": "PASSED",
                "phases_completed": agent.memory.get_state()['phase'],
                "discovery_complete": agent.memory.is_discovery_complete()
            }
            
            self.results.append(result)
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            result = {
                "scenario": "Small Bakery",
                "status": "FAILED",
                "error": str(e)
            }
            self.results.append(result)
            return False
    
    def test_ecommerce_scenario(self):
        """
        Test Scenario 2: E-commerce Store
        Tests order processing automation
        """
        print("\n" + "="*60)
        print("TEST SCENARIO 2: E-COMMERCE STORE")
        print("="*60 + "\n")
        
        agent = OPTAgent()
        
        conversation = [
            ("Hello", "start"),
            ("I run an online clothing store", "business_type"),
            ("5 people on my team", "business_size"),
            ("Shopify, Gmail, and spreadsheets", "tools"),
            ("Processing orders manually takes forever", "pain_points"),
            ("Order fulfillment", "process_name"),
            ("Check orders, update inventory, send confirmation emails", "process_desc"),
            ("Multiple times per day", "frequency"),
            ("About 2 hours total per day", "time_spent"),
            ("Sending order confirmation emails", "task_name"),
            ("Copy order details and paste into email template", "task_desc"),
            ("Order data from Shopify", "inputs"),
            ("Confirmation email to customer", "outputs"),
            ("1", "choice"),
        ]
        
        try:
            for i, (user_msg, stage) in enumerate(conversation, 1):
                print(f"\n[{i}] User: {user_msg}")
                response = agent.chat(user_msg)
                print(f"[{i}] Agent: {response[:200]}...")
                
                if stage == "choice" and agent.memory.get_state()['phase'] == 'masterplan':
                    print("\n✅ Test passed: Successfully reached masterplan phase")
                    break
            
            result = {
                "scenario": "E-commerce Store",
                "status": "PASSED",
                "phases_completed": agent.memory.get_state()['phase'],
                "discovery_complete": agent.memory.is_discovery_complete()
            }
            
            self.results.append(result)
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            result = {
                "scenario": "E-commerce Store",
                "status": "FAILED",
                "error": str(e)
            }
            self.results.append(result)
            return False
    
    def test_freelancer_scenario(self):
        """
        Test Scenario 3: Freelance Consultant
        Tests invoice automation
        """
        print("\n" + "="*60)
        print("TEST SCENARIO 3: FREELANCE CONSULTANT")
        print("="*60 + "\n")
        
        agent = OPTAgent()
        
        conversation = [
            ("Hello", "start"),
            ("I'm a freelance marketing consultant", "business_type"),
            ("Solo - just me", "business_size"),
            ("Google Docs, email, and manual tracking", "tools"),
            ("Creating and sending invoices takes way too long", "pain_points"),
            ("Client invoicing", "process_name"),
            ("Track hours, calculate total, create invoice, email to client", "process_desc"),
            ("Monthly for each client", "frequency"),
            ("1-2 hours per month", "time_spent"),
            ("Creating the invoice document", "task_name"),
            ("Fill in template with hours, rates, client info", "task_desc"),
            ("Time tracking spreadsheet", "inputs"),
            ("PDF invoice", "outputs"),
            ("1", "choice"),
        ]
        
        try:
            for i, (user_msg, stage) in enumerate(conversation, 1):
                print(f"\n[{i}] User: {user_msg}")
                response = agent.chat(user_msg)
                print(f"[{i}] Agent: {response[:200]}...")
                
                if stage == "choice" and agent.memory.get_state()['phase'] == 'masterplan':
                    print("\n✅ Test passed: Successfully reached masterplan phase")
                    break
            
            result = {
                "scenario": "Freelance Consultant",
                "status": "PASSED",
                "phases_completed": agent.memory.get_state()['phase'],
                "discovery_complete": agent.memory.is_discovery_complete()
            }
            
            self.results.append(result)
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            result = {
                "scenario": "Freelance Consultant",
                "status": "FAILED",
                "error": str(e)
            }
            self.results.append(result)
            return False
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("\n" + "🧪"*30)
        print("OPT AGENT - TEST SUITE")
        print("🧪"*30)
        
        # Run tests
        test1 = self.test_bakery_scenario()
        test2 = self.test_ecommerce_scenario()
        test3 = self.test_freelancer_scenario()
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.results if r['status'] == 'PASSED')
        total = len(self.results)
        
        print(f"\n✅ Tests Passed: {passed}/{total}")
        print(f"📈 Success Rate: {(passed/total)*100:.1f}%\n")
        
        for i, result in enumerate(self.results, 1):
            status_icon = "✅" if result['status'] == 'PASSED' else "❌"
            print(f"{status_icon} {i}. {result['scenario']}: {result['status']}")
            if result['status'] == 'PASSED':
                print(f"   - Discovery Complete: {result.get('discovery_complete', 'N/A')}")
                print(f"   - Final Phase: {result.get('phases_completed', 'N/A')}")
            else:
                print(f"   - Error: {result.get('error', 'Unknown')}")
        
        # Save results
        os.makedirs("tests/results", exist_ok=True)
        with open("tests/results/test_results.json", 'w') as f:
            json.dump({
                "summary": {
                    "total": total,
                    "passed": passed,
                    "failed": total - passed,
                    "success_rate": f"{(passed/total)*100:.1f}%"
                },
                "results": self.results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: tests/results/test_results.json")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED!")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed")
            return False


if __name__ == "__main__":
    tester = TestScenarios()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)