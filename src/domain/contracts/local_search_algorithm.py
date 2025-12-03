from abc import ABC, abstractmethod
from src.domain.contracts.planning_contract import PlanningContract

class LocalSearchAlgorithm(ABC):
    def __init__(self, planning: PlanningContract) -> None:
        self._planning = planning

    @abstractmethod
    def execute(self) -> tuple[list[str] | None, int]:
        ...
