from collections import deque
from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState
from src.algorithms.a_star import AStar


class BiDirectionalAStar(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.initial = planning.current_state
        self.goal = BlocksWorldState(self._goal, planning.actions, name='leaf')
        self.from_initial = AStar(planning)
        other_planning = planning.copy()
        other_planning.set_initial(self.goal.current)
        other_planning.set_goal(self.initial.current)
        self.from_goal = AStar(other_planning)
        self.__explored_map_end: dict[str, BlocksWorldState] = {self.goal.key: self.goal}

    def execute(self) -> tuple[list[str] | None, int, int]:
        exploreds = 0

        if self.initial == self.goal:
            return None, 0, 0
        while self.from_initial.is_avaliable() and self.from_goal.is_avaliable():
            solution, meeting, self._num_generated_nodes, exploreds = self.from_initial.step()
            
            if solution is not None:
                return solution, self._num_generated_nodes, exploreds
            if meeting := self.is_intersecting():
                return self.build_path(meeting), self._num_generated_nodes, exploreds
            solution, meeting, self._num_generated_nodes, exploreds = self.from_goal.step()
            
            if solution is not None:
                return solution, self._num_generated_nodes, exploreds
            if meeting := self.is_intersecting():
                return self.build_path(meeting), self._num_generated_nodes, exploreds
        return None, self._num_generated_nodes, exploreds

    def is_intersecting(self) -> BlocksWorldState | None:
        ...

    def build_path(self, meet: BlocksWorldState) -> list[str]:
        left: deque[str] = deque()
        node = meet
        while node.parent is not None:
            left.insert(0, node.identifier)
            node = node.parent

        right: deque[str] = deque()
        node = self.__explored_map_end[meet.key]
        while node.parent is not None:
            right.append(node.identifier)
            node = node.parent
        return list(left + right)
