from collections import deque
from typing import Set
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.contracts.planning_contract import PlanningContract

class CountingIncorrectOverlaps:
    def __init__(
        self,
        planning: PlanningContract,
        data_structure: deque[BlocksWorldState],
    ) -> None:
        self.__planning = planning
        self.__goal_overlaps = self.__extract_overlaps(
            self.__planning.states['goal'])
        self.__priority_queue_cost_based = self.__prepare_priority_queue(
            data_structure)

    def is_avaliable(self) -> bool:
        return len(self.__priority_queue_cost_based) != 0

    def pick(self) -> BlocksWorldState:
        return self.__priority_queue_cost_based.popleft()[1]

    def evaluate_cost(self, state: BlocksWorldState) -> None:
        cost = state.g + min(self.h1(state), self.h2(state))
        self.__push(cost, state)

    def h1(self, state: BlocksWorldState) -> int:
        current_overlaps = self.__extract_overlaps(state.current)
        return len(current_overlaps - self.__goal_overlaps)

    def h2(self, state: BlocksWorldState):
        return sum(1 if fact not in state.current else -1 for fact in self.__planning.states['goal'])

    def __push(self, cost: int, state: BlocksWorldState) -> None:
        for index in range(len(self.__priority_queue_cost_based)):
            if cost < self.__priority_queue_cost_based[index][0]:
                self.__priority_queue_cost_based.insert(index, (cost, state))
                return
        self.__priority_queue_cost_based.append((cost, state))

    def __prepare_priority_queue(self, data_structure: deque[BlocksWorldState]) -> deque[tuple[int, BlocksWorldState]]:
        new_structure: deque[tuple[int, BlocksWorldState]] = deque()
        new_structure.append((0, data_structure[0]))
        return new_structure

    def __extract_overlaps(self, state: Set[int]) -> Set[str]:
        remap_state = self.__planning.remap(state)
        return set(filter(lambda partition: 'on' in partition or 'ontable' in partition, remap_state))
