from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.support.heuristics.a_star import CountingIncorrectOverlaps


class AStar(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.__heuristic = CountingIncorrectOverlaps(planning, self._frontier[0])
        self.__g_score: dict[str, int] = {}

    def execute(self) -> tuple[list[str] | None, int, int]:
        while self.__heuristic.is_avaliable():
            state = self.__heuristic.pick()

            if state.key in self._explored:
                continue

            if self.is_goal_state(state):
                return self._planning.solution(state), self._num_generated_nodes, len(self._explored)
            self._explored.add(state.key)
            self.__g_score[state.key] = state.g

            for successor in state.successors(self._planning.actions):
                self._num_generated_nodes += 1

                if (
                    successor.key in self.__g_score and
                    successor.g >= self.__g_score[successor.key]
                ):
                    continue
                self.__heuristic.evaluate_cost(successor)
        return None, self._num_generated_nodes, len(self._explored)
