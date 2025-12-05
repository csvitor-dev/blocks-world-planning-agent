from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState
from typing import Set
from collections import deque


class DLS(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.__limit = 1000000
        self.__num_generated = 0
        self.__frontier: deque[BlocksWorldState] = deque()
        self.__frontier.append(self._planning.current_state)
        self.__goal: Set[int] = set(planning.states['goal'])

    def __is_cycle(self, state: BlocksWorldState) -> bool:
        hook = state

        while hook.parent is not None:
            if state == hook.parent:
                return True
            hook = hook.parent
        return False

    def execute(self) -> tuple[list[str] | None, int, int]:
        hook_cost = 0

        while len(self.__frontier) and hook_cost < self.__limit:
            state: BlocksWorldState = self.__frontier.pop()

            if self.__goal.issubset(set(state.current)):
                return self._planning.solution(state), self.__num_generated, len(self.__frontier)

            if hook_cost >= self.__limit:
                return None, self.__num_generated, len(self.__frontier)
            elif not self.__is_cycle(state):
                hook_cost += 1

                for successor in state.successors(self._planning.actions):
                    self.__frontier.append(successor)
                    self.__num_generated += 1

        return None, self.__num_generated, len(self.__frontier)

    def set_limit(self, new_limit: int, to_increment: bool = False) -> None:
        self.__limit = new_limit if to_increment is False else self.__limit + new_limit
