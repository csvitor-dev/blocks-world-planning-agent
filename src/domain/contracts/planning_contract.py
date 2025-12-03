from typing import Protocol, Generator
from src.domain.blocks_world_state import BlocksWorldState

class PlanningContract(Protocol):
    @property
    def current_state(self) -> BlocksWorldState: ...

    @property
    def actions(self) -> dict[str, dict[str, list[int]]]: ...

    def successors(self) -> Generator[BlocksWorldState, None, None]: ...