"""
OPT Automation Agent - Main Entry Point

Run this to start the agent conversation
"""

from agent.core import OPTAgent


def main():
    """Run the OPT Agent interactively"""
    
    print("\n" + "🎯"*30)
    print("OPT AUTOMATION AGENT")
    print("Find and automate your repetitive work!")
    print("🎯"*30)
    
    # Initialize agent
    agent = OPTAgent()
    
    # Start conversation
    print("\n" + "="*60)
    print("💬 CONVERSATION MODE")
    print("="*60)
    print("Type 'exit' or 'quit' to end the conversation")
    print("="*60 + "\n")
    
    # Send welcome message
    welcome = agent.chat("Hello")
    print(f"🤖 Agent:\n{welcome}\n")
    
    # Conversation loop
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            # Check for exit
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Thanks for using OPT Agent! Goodbye!\n")
                
                # Save session
                agent.save_session()
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Get agent response
            response = agent.chat(user_input)
            print(f"\n🤖 Agent:\n{response}\n")
            
            # Check if done
            if agent.memory.get_state()['phase'] == 'done':
                save_choice = input("\n💾 Save this session? (y/n): ").strip().lower()
                if save_choice == 'y':
                    agent.save_session()
                
                continue_choice = input("\n🔄 Start another automation? (y/n): ").strip().lower()
                if continue_choice == 'y':
                    agent = OPTAgent()  # Fresh start
                    welcome = agent.chat("Hello")
                    print(f"\n🤖 Agent:\n{welcome}\n")
                else:
                    print("\n👋 Thanks for using OPT Agent! Goodbye!\n")
                    break
        
        except KeyboardInterrupt:
            print("\n\n⏸️  Interrupted by user")
            save_choice = input("💾 Save session before exit? (y/n): ").strip().lower()
            if save_choice == 'y':
                agent.save_session()
            print("\n👋 Goodbye!\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Let's try again...\n")


if __name__ == "__main__":
    main()