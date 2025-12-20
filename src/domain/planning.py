from typing import Generator, Set
import time
import tracemalloc
import sys
from src.support.factories.algorithm_factory import AlgorithmFactory
from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.strips_notation import StripsNotation


class Planning(PlanningContract):
    def __init__(self, strips: StripsNotation):
        self.__instance = strips.instance_ref
        self.__map = self.__map_clauses(strips)
        self.__inverve_map = {self.__map[key]: key for key in self.__map}
        self.__actions = self.__resolve_actions(strips.actions)

        self.__initial_state = self.__resolve_facts(strips.states['initial'])
        self.__goal_state = self.__infers_goal(strips)

        self.__state_space = BlocksWorldState(
            self.__initial_state, self.__actions)

        self.__planner: LocalSearchAlgorithm | None = None
        self.__show_report = True

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
            'initial': self.__initial_state,
            'goal': self.__goal_state,
        }

    def remap(self, state: Set[int]) -> Set[str]:
        return {self.__inverve_map[fact] for fact in state}

    def successors(self) -> Generator[BlocksWorldState, None, None]:
        return self.__state_space.successors(self.__actions)

    def solution(self, goal_state: BlocksWorldState) -> list[str]:
        solution_path: list[str] = []

        while goal_state.parent is not None:
            solution_path.insert(0, goal_state.identifier)
            goal_state = goal_state.parent
        return solution_path

    def set_algorithm(self, algorithm_key: str) -> None:
        self.__planner = AlgorithmFactory.make(algorithm_key, self)
    
    def off_report(self) -> None:
        self.__show_report = False

    def execute(self) -> None:
        if self.__planner is None:
            raise AssertionError('The algorithm is not set')

        tracemalloc.start()
        start = time.perf_counter()
        result, expansions, explorations = self.__planner.execute()
        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        if self.__show_report is False:
            print(f'Instance: {self.__instance}')
            if result:
                print(
                    f"Solution Found! ({len(result)} step{'s' if len(result) != 1 else ''}) Time: {elapsed:.6f}s")
            else:
                print(f"No solution found. Time: {elapsed:.6f}s")
            return

        self.__report(result, expansions,
                              explorations, elapsed, current, peak)

    def __report(self, result: list[str] | None, expansions: int, explorations: int, elapsed: float, current: int, peak: int) -> None:
        algo_name = type(
            self.__planner).__name__ if self.__planner is not None else None
        sizeof = sys.getsizeof(self.current_state)

        print("=" * 60)
        print("Execution summary".center(60))
        print("=" * 60)
        print(f"Algorithm         : {algo_name}")
        print(f"Instance          : {self.__instance}")
        print(f"Time elapsed      : {elapsed:.6f} s")
        print(f"Expanded nodes    : {expansions}")
        print(f"Explored nodes    : {explorations}")
        print(f"Total memory cost : {(explorations * sizeof / 1024):.2f} KB")
        print(
            f"Memory usage      : current={current / 1024:.2f} KB; peak={peak / 1024:.2f} KB")
        print("-" * 60)

        if result:
            print(
                f"Solution ({len(result)} step{'s' if len(result) != 1 else ''}):")
            for i, step in enumerate(result, start=1):
                print(f"  {i:2d}. {step}")
        else:
            print("No solution found")

        print("=" * 60)

    def __map_clauses(self, strips: StripsNotation) -> dict[str, int]:
        action_hook: dict[str, int] = {}

        for fact in strips.avaliable_facts:
            if fact not in action_hook.keys():
                action_hook[fact] = abs(action_hook.get(f'~{fact}', len(
                    action_hook) + 1)) if fact.startswith('~') is False else -action_hook.get(
                        fact[1:], len(action_hook) + 1)
        return action_hook

    def __resolve_facts(self, target: list[str]) -> Set[int]:
        return {self.__map[fact] for fact in target}

    def __resolve_actions(self, actions: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, Set[int]]]:
        return {
            action_name: {
                'pre': self.__resolve_facts(conditions['pre']),
                'post': self.__resolve_facts(conditions['post']),
            }
            for action_name, conditions in actions.items()
        }

    def __infers_goal(self, strips: StripsNotation) -> Set[int]:
        goal = strips.states['goal']
        goal_facts_disposition = list(
            map(lambda fact: fact.split('_')[0], goal))
        state_builder: Set[str] = set(goal)

        if 'holding' not in goal_facts_disposition:
            state_builder.add('handempty')

        for atom in strips.atoms:
            clear_exists = True
            ontable_exists = True
            rest = strips.atoms.copy()
            rest.remove(atom)

            for other in rest:
                if f'on_{other}_{atom}' in goal:
                    clear_exists = False
                elif f'on_{atom}_{other}' in goal:
                    ontable_exists = False
            if clear_exists:
                state_builder.add(f'clear_{atom}')
            if ontable_exists:
                state_builder.add(f'ontable_{atom}')

        return self.__resolve_facts(list(state_builder))
