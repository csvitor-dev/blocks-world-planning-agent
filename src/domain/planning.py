from typing import Generator, Set
import time
import tracemalloc

from src.support.factories.algorithm_factory import AlgorithmFactory
from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.strips_notation import StripsNotation


class Planning(PlanningContract):

    def __init__(self, strips: StripsNotation):
        self.__map = self.__map_clauses(strips)
        self.__actions = self.__resolve_actions(strips.actions)
        states = strips.states
        self.__initial_state = self.__resolve_facts(states['initial'])
        self.__goal_state = self.__resolve_facts(states['goal'])
        self.__state_space = BlocksWorldState(
            self.__initial_state,
            self.__actions
        )

        self.__planner: LocalSearchAlgorithm | None = None

    @property
    def current_state(self) -> BlocksWorldState:
        return self.__state_space

    @property
    def map(self) -> dict[str, int]:
        return self.__map

    @property
    def actions(self) -> dict[str, dict[str, Set[int]]]:
        return self.__actions

    @property
    def states(self) -> dict[str, Set[int]]:
        return {
            "initial": self.__initial_state,
            "goal": self.__goal_state
        }

    def successors(self) -> Generator[BlocksWorldState, None, None]:
        return self.__state_space.successors(self.__actions)

    def solution(self, goal_state: BlocksWorldState) -> list[str]:
        caminho: list[str] = []
        while goal_state.parent is not None:
            caminho.insert(0, goal_state.identifier)
            goal_state = goal_state.parent
        return caminho

    def set_algoritm(self, key: str) -> None:
        self.__planner = AlgorithmFactory.make(key, self)

    def execute(self) -> None:
        if self.__planner is None:
            raise AssertionError("Algorithm not set")

        tracemalloc.start()
        inicio = time.perf_counter()

        resultado, expandidos, explorados = self.__planner.execute()

        tempo = time.perf_counter() - inicio
        atual, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.__mostrar(resultado, expandidos, explorados, tempo, atual, pico)

    def __mostrar(self, result, exp, explor, tempo, atual, pico):
        nome_algo = type(self.__planner).__name__ if self.__planner else None

        print("=" * 60)
        print("Execution summary".center(60))
        print("=" * 60)
        print(f"Algorithm       : {nome_algo}")
        print(f"Time elapsed    : {tempo:.6f} s")
        print(f"Expanded nodes  : {exp}")
        print(f"Explored nodes  : {explor}")
        print(f"Memory usage    : current={atual/1024:.2f} KB; peak={pico/1024:.2f} KB")
        print("-" * 60)

        if result:
            print(f"Solution ({len(result)} steps):")
            for i, step in enumerate(result, 1):
                print(f"{i:2d}. {step}")
        else:
            print("No solution found")

        print("=" * 60)

    def __map_clauses(self, strips: StripsNotation) -> dict[str, int]:
        tabela: dict[str, int] = {}
        contador = 1

        for fact in strips.avaliable_facts:
            if fact not in tabela:
                tabela[fact] = contador
                complemento = "~" + fact
                if complemento not in tabela:
                    tabela[complemento] = -contador
                contador += 1

        return tabela

    def __resolve_facts(self, target: list[str]) -> Set[int]:
        return {self.__map[p] for p in target}

    def __resolve_actions(self, actions: dict[str, dict[str, list[str]]]):
        convertido = {}
        for nome, cond in actions.items():
            convertido[nome] = {
                "pre": self.__resolve_facts(cond["pre"]),
                "post": self.__resolve_facts(cond["post"]),
            }
        return convertido
