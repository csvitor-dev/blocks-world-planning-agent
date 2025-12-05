from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.algorithms.depth_limitted_search import DLS


class IDS(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)
        self.__dls_instance = DLS(planning)
        self.__num_generated = 0

    def execute(self) -> tuple[list[str] | None, int, int]:
        while True:
            solution_path, N, explored_nodes = self.__dls_instance.execute()
            self.__dls_instance.set_limit(1, to_increment=True)
            self.__num_generated += N

            if solution_path is not None:
                return solution_path, self.__num_generated, explored_nodes
        
        
