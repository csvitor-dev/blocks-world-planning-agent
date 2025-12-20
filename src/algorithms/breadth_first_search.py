from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState


class BFS(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)

    def execute(self) -> tuple[list[str] | None, int, int]:
        while self._frontier:
            state: BlocksWorldState = self._frontier.popleft()

            if state.key in self._explored:
                continue

            if self.is_goal_state(state):
                return self._planning.solution(state), self._num_generated_nodes, len(self._explored)
            self._explored.add(state.key)

            for successor in state.successors(self._planning.actions):
                self._num_generated_nodes += 1
                if successor.key not in self._explored:
                    self._frontier.append(successor)
        return None, self._num_generated_nodes, len(self._explored)
