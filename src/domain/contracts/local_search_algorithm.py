from abc import ABC, abstractmethod
from collections import deque
from typing import Set
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState


class LocalSearchAlgorithm(ABC):
    def __init__(self, planning: PlanningContract) -> None:
        self._planning = planning
        self._explored: Set[str] = set()
        self._frontier: deque[BlocksWorldState] = deque()
        self._goal: Set[int] = set(planning.states['goal'])
        self._frontier.append(self._planning.current_state)
        self._num_generated_nodes = 0

    @abstractmethod
    def execute(self) -> tuple[list[str] | None, int, int]: ...

    def is_goal_state(self, state: BlocksWorldState) -> bool:
        return state.current == self._goal
