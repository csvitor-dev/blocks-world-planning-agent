from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from collections import deque
from src.domain.blocks_world_state import BlocksWorldState


class BFS(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.__explored = set()
        self.__frontier = deque()
        self.__goal = set(planning.states.get('goal'))
        self.__frontier.append(self._planning.current_state)
        self.__num_generated_nodes = 0

    def execute(self) -> list[str] | None:
        while len(self.__frontier):
            state: BlocksWorldState = self.__frontier.popleft()
            
            if state.key in self.__explored:
                continue
            self.__explored.add(state.key)            

            if self.__goal.issubset(set(state.current)):
                return self._planning.solution(state), self.__num_generated_nodes

            for successor in state.successors(self._planning.actions):
                self.__num_generated_nodes += 1
                if successor.key not in self.__explored:
                    self.__frontier.append(successor)
                    
        return None, self.__num_generated_nodes
