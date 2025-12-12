from src.algorithms.a_star import AStar
from src.algorithms.breadth_first_search import BFS
from src.algorithms.depth_limitted_search import DLS
from src.algorithms.iterative_deepening_search import IDS
from src.algorithms.bidirectional import Bidirectional
from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract




class AlgorithmFactory:
    __MAP: dict[str, type[LocalSearchAlgorithm]] = {
        'A*': AStar,
        'BFS': BFS,
        'DLS': DLS,
        'IDS': IDS,
        "bidirectional": Bidirectional,

    }

    @classmethod
    def make(cls, key: str, planning: PlanningContract) -> LocalSearchAlgorithm:
        if key not in cls.__MAP:
            raise ValueError(f'Algorithm "{key}" is not supported')
        return cls.__MAP[key](planning)