from collections import deque
from typing import Set
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.contracts.planning_contract import PlanningContract


class GoalRelativeDistance:
    def __init__(self, planning: PlanningContract, data_structure: deque[BlocksWorldState]) -> None:
        self.__planning = planning
        self.__priority_queue_cost_based = self.__prepare_priority_queue(data_structure)

    def is_avaliable(self) -> bool:
        return len(self.__priority_queue_cost_based) != 0

    def pick(self) -> BlocksWorldState:
        return self.__priority_queue_cost_based.popleft()[1]

    def evaluate_cost(self, state: BlocksWorldState) -> None:
        cost = state.g + h0(state, self.__planning.states['goal'])
        self.__push(cost, state)

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


def h0(current_state: BlocksWorldState, goal: Set[int]):
    return sum(1 for fact in goal if fact not in current_state.current)


def h1(current_state: BlocksWorldState, goal: Set[int]) -> int:
    return len(current_state.current & goal)


def h2(current_state: BlocksWorldState, goal: Set[int]) -> int: # GBFS
    score = 0

    for fact in current_state.current:
        if current_state.parent is not None and fact not in current_state.parent.current and fact in goal:
            score += 2
        elif fact in goal:
            score += 1
        elif current_state.parent is not None and fact in current_state.parent.current and fact not in goal:
            score -= 2
        elif fact not in goal:
            score -= 1
    return score
