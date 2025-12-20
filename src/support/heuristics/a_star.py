from typing import Set
from queue import PriorityQueue
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.contracts.planning_contract import PlanningContract

class CountingIncorrectOverlaps:
    def __init__(
        self,
        planning: PlanningContract,
        initial_block: BlocksWorldState,
    ) -> None:
        self.__planning = planning
        self.__goal_overlaps = self.__extract_overlaps(
            self.__planning.states['goal'])
        self.__priority_queue_cost_based: PriorityQueue[tuple[int, BlocksWorldState]] = PriorityQueue()
        self.__priority_queue_cost_based.put((0, initial_block))

    def is_avaliable(self) -> bool:
        return self.__priority_queue_cost_based.empty() is False

    def pick(self) -> BlocksWorldState:
        return self.__priority_queue_cost_based.get()[1]

    def evaluate_cost(self, state: BlocksWorldState) -> None:
        estimate_cost = state.g + min(self.h1(state), self.h2(state))
        self.push(estimate_cost, state)

    def h1(self, state: BlocksWorldState) -> int:
        current_overlaps = self.__extract_overlaps(state.current)
        return min(len(current_overlaps - self.__goal_overlaps), len(self.__goal_overlaps - current_overlaps))

    def h2(self, state: BlocksWorldState):
        return sum(1 if fact not in state.current else -1 for fact in self.__planning.states['goal'])

    def push(self, estimative: int, state: BlocksWorldState) -> None:
        self.__priority_queue_cost_based.put((estimative, state))

    def __extract_overlaps(self, state: Set[int]) -> Set[str]:
        remap_state = self.__planning.remap(state)
        return set(filter(lambda partition: 'on' in partition or 'ontable' in partition, remap_state))
