from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract


class DLS(LocalSearchAlgorithm):
    def __init__(self, planning: PlanningContract) -> None:
        super().__init__(planning)

    def execute(self) -> None:
        print("Executing DLS Algorithm")
        print(self._planning.current_state)
