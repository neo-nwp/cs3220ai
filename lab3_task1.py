from src.fwgcproblemClass import FWGCProblem
from src.fwgcproblemsolvingagent import FWGCProblemSolvingAgent
from src.PS_agentPrograms import BestFirstSearchAgentProgram

def main():
    """
    Sets up and solves the Farmer, Wolf, Goat, and Cabbage problem.
    """
    print("--- Solving the Farmer, Wolf, Goat, and Cabbage Problem ---")
    
    # 1. Define the problem by creating an instance of the problem class.
    fwgc_problem = FWGCProblem()

    # 2. Define the search algorithm to be used.
    # BestFirstSearchAgentProgram with a uniform cost acts like Breadth-First Search.
    search_program = BestFirstSearchAgentProgram()

    # 3. Create the problem-solving agent.
    agent = FWGCProblemSolvingAgent(
        initial_state=fwgc_problem.initial,
        goal=fwgc_problem.goal,
        program=search_program
    )
    
    # 4. The agent uses its search program to find a solution.
    # The 'program' returns the goal node when it finds a solution.
    goal_node = agent.search(fwgc_problem)
    
    # 5. Print the solution path.
    if goal_node:
        print("\n✅ Solution Found!")
        solution_path = goal_node.path()
        
        # Get the set of all items for displaying the East bank correctly
        all_items = fwgc_problem.all_items
        
        print("\n--- Step-by-Step Solution ---")
        for i, node in enumerate(solution_path):
            west_bank = sorted(list(node.state))
            east_bank = sorted(list(all_items - node.state))
            
            if node.action:
                action_str = " then ".join(sorted(list(node.action))) + " cross"
                print(f"Step {i}: {action_str.ljust(25)} -> West Bank: {west_bank}, East Bank: {east_bank}")
            else:
                # Initial state
                print(f"Step {i}: {'Initial State'.ljust(25)} -> West Bank: {west_bank}, East Bank: {east_bank}")
        
        action_sequence = goal_node.solution()
        print("\nSequence of Actions ( crossings ):")
        print(action_sequence)
        
    else:
        print("\n❌ No solution found.")

if __name__ == "__main__":
    main()