from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState


class DLS(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.__limit = 1000000

    def __is_cycle(self, state: BlocksWorldState) -> bool:
        hook = state

        while hook.parent is not None:
            if state == hook.parent:
                return True
            hook = hook.parent
        return False

    def execute(self) -> tuple[list[str] | None, int, int]:
        hook_cost = 0

        while len(self._frontier) and hook_cost < self.__limit:
            state: BlocksWorldState = self._frontier.pop()

            if self.is_goal_state(state):
                return self._planning.solution(state), self._num_generated_nodes, len(self._frontier)

            if hook_cost >= self.__limit:
                return None, self._num_generated_nodes, len(self._frontier)
            elif not self.__is_cycle(state):
                hook_cost += 1

                for successor in state.successors(self._planning.actions):
                    self._frontier.append(successor)
                    self._num_generated_nodes += 1
        return None, self._num_generated_nodes, len(self._frontier)

    def increment_limit(self, new_limit: int) -> None:
        self.__limit += new_limit
