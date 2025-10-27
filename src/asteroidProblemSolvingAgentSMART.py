from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram

class AsteroidProblemSolvingAgentSMART(SimpleProblemSolvingAgentProgram):
    def __init__(self, initial_state=None, environment=None, goal=None, program=None):
        super().__init__(initial_state)
        self.environment = environment
        self.goal = goal
        self.program = program  # This is your search function (UCS/IDS)
        self.plan = []
        self.performance = (environment.rows * environment.cols) // 2
        self.alive = True

        # ✅ New tracking attributes
        self.last_result = None
        self.path_cost = None

    def update_state(self, state, percept):
        # Just mirror percept as state
        return percept

    def formulate_goal(self, state):
        return self.goal

    def formulate_problem(self, state, goal):
        from src.asteroid_problem import AsteroidMazeProblem
        print(f"🧠 Formulating problem from {state} to {goal}")
        return AsteroidMazeProblem(self.environment, state, goal)

    def search(self, problem):
        # Uses the search algorithm passed in
        return self.program(problem)

    def __call__(self, percept, curGoal=None):
        self.state = self.update_state(self.state, percept)

        if not self.plan:
            print(f"\n🧩 AsteroidProblemSolvingAgentSMART: planning from {self.state} to {self.goal}")
            problem = self.formulate_problem(self.state, self.goal)
            result = self.search(problem)
            self.last_result = result

            if result is None:
                print("❌ No plan found.")
                return None

            # ✅ Extract full path and cost
            if hasattr(result, "path"):
                self.plan = result.path()
                self.path_cost = getattr(result, "path_cost", getattr(result, "g", len(self.plan) - 1))
            else:
                self.plan = result
                self.path_cost = len(self.plan) - 1

            print(f"🧭 Found plan: {self.plan}")
            print(f"✅ Plan length: {len(self.plan)} | Cost: {self.path_cost}")

        if self.plan:
            next_action = self.plan.pop(0)
            print(f"➡️ Executing action: {next_action}")
            return next_action

        print("✅ Goal reached — no more actions.")
        return None
