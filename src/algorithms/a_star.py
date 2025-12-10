from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.support.heuristics.a_star import GoalRelativeDistance


class AStar(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.__heuristic = GoalRelativeDistance(planning, self._frontier)

    def execute(self) -> tuple[list[str] | None, int, int]:
        while self.__heuristic.is_avaliable():
            state = self.__heuristic.pick()

            if self.is_goal_state(state):
                return self._planning.solution(state), self._num_generated_nodes, len(self._explored)

            if state.key in self._explored:
                continue
            self._explored.add(state.key)

            for successor in state.successors(self._planning.actions):
                self._num_generated_nodes += 1
                if successor.key not in self._explored:
                    self.__heuristic.evaluate_cost(successor)
        return None, self._num_generated_nodes, len(self._explored)
