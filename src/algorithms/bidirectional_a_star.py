from collections import deque
from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState


class BiDirectionalAStar(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.initial = self._planning.current_state
        self.goal = BlocksWorldState(self._goal, self.planning.actions, name='leaf')
        self.__frontier_end: deque[BlocksWorldState] = deque([self.goal])
        self.__explored_map_initial: dict[str, BlocksWorldState] = {self.initial.key: self.initial}
        self.__explored_map_end: dict[str, BlocksWorldState] = {self.goal.key: self.goal}
        self.__meeting: BlocksWorldState | None = None

    def execute(self) -> tuple[list[str] | None, int, int]:
        if self.initial == self.goal:
            return None, 0, 0
        while self._frontier and self.__frontier_end:
            self.expand_front_from_initial()
            if meeting := self.is_intersecting():
                return self.build_path(meeting), self.expansions, self.explorations

            self.expand_front_from_goal()
            if meeting := self.is_intersecting():
                return self.build_path(meeting), self.expansions, self.explorations
        return None, self.expansions, self.explorations

    def is_intersecting(self) -> BlocksWorldState | None:
        ...

    def expand_front_from_initial(self) -> None:
        current = queue.popleft()
        self.explorations += 1

        for nxt in current.successors(self.planning.actions):
            self.expansions += 1
            if nxt.key in visited_this:
                continue

            visited_this[nxt.key] = nxt

            if nxt.key in visited_other:
                return nxt

            queue.append(nxt)

        return None

    def expand_front_from_goal(self) -> None:
        current = queue.popleft()
        self.explorations += 1

        for nxt in current.successors(self.planning.actions):
            self.expansions += 1
            if nxt.key in visited_this:
                continue

            visited_this[nxt.key] = nxt

            if nxt.key in visited_other:
                return nxt

            queue.append(nxt)

        return None

    def build_path(self, meet: BlocksWorldState):
        left = deque()
        node = meet
        while node.parent is not None:
            left.insert(0, node.identifier)
            node = node.parent

        right = deque()
        node = self.__explored_map_end[meet.key]
        while node.parent is not None:
            right.append(node.identifier)
            node = node.parent
        return left + right
