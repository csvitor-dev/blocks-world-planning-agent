from collections import deque
from typing import Set
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.contracts.planning_contract import PlanningContract


class GoalRelativeDistance:
    def __init__(self, planning: PlanningContract, data_structure: deque[BlocksWorldState]) -> None:
        self.__planning = planning
        self.__priority_queue = self.__prepare_priority_queue(data_structure)

    def is_avaliable(self) -> bool:
        return len(self.__priority_queue) != 0

    def pick(self) -> BlocksWorldState:
        return self.__priority_queue.popleft()[1]

    def evaluate_cost(self, state: BlocksWorldState) -> None:
        priority1 = state.g + h0(state, self.__planning.states['goal'])
        self.__push(priority1, state)

    def __push(self, priority: int, state: BlocksWorldState) -> None:
        if not self.is_avaliable():
            self.__priority_queue.append((priority, state))
            return

        for index in range(len(self.__priority_queue)):
            if priority >= self.__priority_queue[index][0]:
                self.__priority_queue.insert(index, (priority, state))
                return

    def __prepare_priority_queue(self, data_structure: deque[BlocksWorldState]) -> deque[tuple[int, BlocksWorldState]]:
        if len(data_structure) > 1:
            raise ValueError('Data structure invalid set')
        new_structure: deque[tuple[int, BlocksWorldState]] = deque()
        new_structure.append((0, data_structure[0]))
        return new_structure


def h0(current: BlocksWorldState, goal: Set[int]):
    return sum(1 for fact in goal if fact not in current.current)


def h1(current_state: BlocksWorldState, goal: Set[int]) -> int:
    return len(current_state.current & goal)


def h3(current_state: BlocksWorldState, goal: Set[int]) -> int:
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
